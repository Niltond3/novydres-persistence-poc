"""Byte-verified ChatGPT Web adapter for the ONE Mapwork pipeline.

A host connector retrieves source/assets; this code has no network, git CLI,
subprocess, OAuth or image-generation implementation. The canonical pipeline
is still scripts/pipeline.py: run_web invokes its main() in-process.
"""
from __future__ import annotations

import ast
import contextlib
import importlib
import hashlib
import io
import os
import tempfile
import importlib.util
import json
import re
import sys
from pathlib import Path
from zipfile import ZipFile, BadZipFile

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
FILE_MANIFEST_SCHEMA = "NOVYDRES_MAPWORK_WEB_FILES"


class WebBridgeError(ValueError):
    pass


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def checked_relative(value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise WebBridgeError("invalid relative file identity")
    p = Path(value)
    if p.is_absolute() or ".." in p.parts or any(s in ("", ".") for s in p.parts):
        raise WebBridgeError("path escapes verified source namespace")
    return p


def verify_files(manifest, *, root, expected_commit=None):
    """Validate real bytes, Git blob identities and provider readback declarations.

    The Git ref itself must be supplied after a real connector read and compared
    to GitHub outside this Python process. A JSON claim alone cannot prove a
    remote HTTP operation or agent visual inspection.
    """
    root = Path(root).resolve()
    if not isinstance(manifest, dict) or manifest.get("schema") != FILE_MANIFEST_SCHEMA:
        raise WebBridgeError("file transport manifest missing/invalid")
    commit = manifest.get("source_commit")
    if not isinstance(commit, str) or not SHA40.fullmatch(commit):
        raise WebBridgeError("unbound GitHub source commit")
    if expected_commit is not None and commit != expected_commit:
        raise WebBridgeError("manifest does not match GitHub connector readback")
    records = manifest.get("files")
    if not isinstance(records, list) or not records:
        raise WebBridgeError("no materialized source files")
    verified, seen = [], set()
    for item in records:
        if not isinstance(item, dict):
            raise WebBridgeError("non-object file record")
        rel = checked_relative(item.get("path"))
        if str(rel) in seen:
            raise WebBridgeError("duplicate file identity: " + str(rel))
        seen.add(str(rel))
        path = (root / rel).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise WebBridgeError("missing or escaping materialized file: " + str(rel))
        raw = path.read_bytes()
        if not SHA64.fullmatch(str(item.get("sha256", ""))) or sha256(raw) != item["sha256"]:
            raise WebBridgeError("file SHA-256 mismatch: " + str(rel))
        if item.get("size_bytes") != len(raw):
            raise WebBridgeError("file length mismatch: " + str(rel))
        provider = item.get("provider")
        if provider == "github":
            if not SHA40.fullmatch(str(item.get("blob_sha", ""))) or git_blob_sha(raw) != item["blob_sha"]:
                raise WebBridgeError("GitHub Git blob mismatch: " + str(rel))
        elif provider == "drive":
            if not isinstance(item.get("drive_file_id"), str) or not item["drive_file_id"]:
                raise WebBridgeError("Drive source ID missing: " + str(rel))
        else:
            raise WebBridgeError("file provider unsupported: " + str(rel))
        verified.append({"path":str(rel),"sha256":sha256(raw),"provider":provider})
    local_modules = {p.relative_to(root).as_posix() for p in
                     (root / "scripts").rglob("*.py") if p.is_file()}
    unverified = local_modules - seen
    if unverified:
        raise WebBridgeError("unverified executable modules: " + ", ".join(sorted(unverified)))
    return {"status":"PASS","source_commit":commit,"files":verified,
            "file_count":len(verified)}


def extract_verified_zip(archive, dest, *, max_bytes=200_000_000, manifest=None, source_commit=None):
    """Safe no-network ZIP extraction; file integrity checked by verify_files afterwards."""
    dest = Path(dest).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    try:
        with ZipFile(archive) as z:
            total = 0
            members = set()
            for member in z.infolist():
                rel = checked_relative(member.filename.rstrip("/"))
                if str(rel) in members:
                    raise WebBridgeError("duplicate ZIP member")
                members.add(str(rel))
                total += member.file_size
                if total > max_bytes or member.file_size > max_bytes:
                    raise WebBridgeError("oversized ZIP rejected")
                target = (dest / rel).resolve()
                if not target.is_relative_to(dest):
                    raise WebBridgeError("ZIP path escape")
                if member.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    if (member.external_attr >> 16) & 0o170000 == 0o120000:
                        raise WebBridgeError("ZIP symlink rejected")
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(z.read(member))
    except (BadZipFile, OSError) as exc:
        raise WebBridgeError("source/archive bytes not readable") from exc
    if manifest is None or source_commit is None:
        raise WebBridgeError("Drive ZIP requires complete verified file manifest and commit")
    if manifest is not None:
        verified = verify_files(manifest, root=dest, expected_commit=source_commit)
        expected = {r["path"] for r in verified["files"]}
        actual = {p.relative_to(dest).as_posix() for p in dest.rglob("*") if p.is_file()}
        if actual != expected:
            raise WebBridgeError("Drive ZIP inventory differs from verified manifest")
    return dest


def _verify_import_graph(module_dir, listed):
    """Every materialized local import target must be part of the verified set."""
    names = {p.stem for p in module_dir.glob("*.py")}
    for p in module_dir.rglob("*.py"):
        rel = "scripts/" + p.relative_to(module_dir).as_posix()
        if rel not in listed:
            raise WebBridgeError("unverified Python import target: " + rel)
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
        except (SyntaxError, UnicodeError) as exc:
            raise WebBridgeError("invalid executable module: " + rel) from exc
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                dependencies = [n.name.split(".")[0] for n in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                dependencies = [node.module.split(".")[0]]
            else:
                continue
            for name in dependencies:
                if name in names and "scripts/" + name + ".py" not in listed:
                    raise WebBridgeError("unverified transitive import: " + name)


def materialize_host_exchange(*, operation, pending_sync, provider_results,
                              github_commits, arg_updates, output_path):
    """Translate actual Web connector receipts/GET files into pipeline exchange.

    This is a pure adapter, not an executor or a second state controller.
    The ChatGPT Web host invokes connected tools and supplies their original
    response metadata plus separately materialized GET bytes. No Python
    callback can call a Web connector. The canonical run_host_exchange validates
    CAS ancestry, artifact uniqueness and the full journal hash chain.

    A provider result has: provider, kind (optional), path, readback_path,
    upload (provider result), readback (provider GET result), and, for GitHub,
    repo_path. Hashes and remote IDs are derived here; never accepted from
    caller-supplied artifact hashes.
    """
    if not isinstance(operation, dict) or not isinstance(operation.get("operation_id"), str):
        raise WebBridgeError("host operation identity missing")
    if operation.get("status") != "PENDING" or not isinstance(operation.get("action"), str):
        raise WebBridgeError("host exchange requires original pending operation")
    if (not isinstance(pending_sync, dict) or
            not isinstance(provider_results, list) or not provider_results or
            not isinstance(github_commits, list) or
            not isinstance(arg_updates, dict)):
        raise WebBridgeError("complete independent host handoff inputs required")
    records = []
    seen = set()
    for item in provider_results:
        if not isinstance(item, dict):
            raise WebBridgeError("invalid provider result")
        provider = item.get("provider")
        local = item.get("path")
        remote = item.get("readback_path")
        upload = item.get("upload")
        get = item.get("readback")
        if (provider not in ("github", "drive") or
                not isinstance(local, str) or not isinstance(remote, str) or
                not isinstance(upload, dict) or not isinstance(get, dict) or
                not Path(local).is_file() or not Path(remote).is_file() or
                Path(local).resolve() == Path(remote).resolve()):
            raise WebBridgeError("provider operation needs separate local and GET files")
        data = Path(local).read_bytes()
        recovered = Path(remote).read_bytes()
        if data != recovered:
            raise WebBridgeError("provider GET bytes differ from upload source")
        kind = item.get("kind")
        if kind is not None and kind not in ("image", "visual-review", "research",
                                             "topology", "intent", "capability",
                                             "other"):
            raise WebBridgeError("unknown host artifact kind")
        record = {"provider":provider,"path":local,"readback_path":remote,
                  "sha256":sha256(data)}
        if kind:
            record["kind"] = kind
        if provider == "drive":
            uploaded_id = upload.get("id")
            downloaded_id = get.get("id")
            if (upload.get("success") is not True or
                    not isinstance(uploaded_id, str) or not uploaded_id or
                    downloaded_id != uploaded_id):
                raise WebBridgeError("Drive upload/GET provider IDs differ")
            record["remote_id"] = uploaded_id
            if kind == "image":
                from PIL import Image
                with Image.open(local) as img:
                    if img.format != "PNG":
                        raise WebBridgeError("native host image must be a PNG")
                    img.verify()
        else:
            blob = git_blob_sha(data)
            repo_path = item.get("repo_path")
            upload_blob = upload.get("sha") or upload.get("content_sha")
            # create_file returns only commit_sha; it is valid exclusively
            # when a separately read back commit/tree binds this path/blob.
            upload_commit = upload.get("commit_sha")
            matching_commits = [c for c in github_commits if
                isinstance(c, dict) and
                isinstance(c.get("files"), dict) and
                c["files"].get(repo_path) == blob and
                c.get("commit_sha") == upload_commit]
            if (get.get("sha") != blob or
                    not isinstance(repo_path, str) or
                    not repo_path or repo_path.startswith("/") or
                    ".." in Path(repo_path).parts or
                    (upload_blob != blob and not (
                        isinstance(upload_commit, str) and
                        SHA40.fullmatch(upload_commit) and matching_commits))):
                raise WebBridgeError("GitHub blob/readback or tree path inconsistent")
            record.update(blob_sha=blob,remote_id=blob,repo_path=repo_path)
        identity = (record["provider"],record["remote_id"])
        if identity in seen:
            raise WebBridgeError("duplicate host provider artifact")
        seen.add(identity)
        records.append(record)
    result = {"operation_id":operation["operation_id"],
              "artifacts":records,"github_commits":github_commits,
              "arg_updates":arg_updates}
    exchange = {"kind":"COMPLETE_OPERATION",
                "operation_id":operation["operation_id"],
                "pending_sync":pending_sync,"result":result}
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    # Do not import orchestration before run_web verifies its Git blob:
    # importing it from this transport helper would trip the source guard
    # (or, worse, allow stale Python modules to affect the canonical run).
    fd, name = tempfile.mkstemp(prefix="." + output.name + ".", dir=output.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as writer:
            json.dump(exchange, writer, ensure_ascii=False, sort_keys=True, indent=2)
            writer.write("\\n")
            writer.flush()
            os.fsync(writer.fileno())
        os.replace(name, output)
        dfd = os.open(output.parent, os.O_RDONLY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    return {"kind":exchange["kind"],"operation_id":exchange["operation_id"],
            "path":str(output),"sha256":sha256(output.read_bytes()),
            "artifacts":len(records)}


def run_web(*, argv, file_manifest, root, source_commit, remote_blobs,
            action_executor=None, remote_readback=None, journal_sync=None):
    """Run exact canonical pipeline.main WITHOUT invoking a terminal or clone.

    Caller must read real files using connectors and check their GitHub/Drive
    readbacks before calling; this adapter cannot authenticate those requests.
    Autonomous callbacks must execute actual host actions, fetch provider bytes
    independently, and perform lease-protected journal commits/readbacks.
    """
    verification = verify_files(file_manifest, root=root, expected_commit=source_commit)
    listed = {r["path"] for r in verification["files"]}
    # This is an independent readback of the exact GitHub tree for the commit,
    # supplied by the host connector. Python never calls GitHub directly.
    if not isinstance(remote_blobs, dict) or not remote_blobs:
        raise WebBridgeError("authenticated remote Git tree blob map required")
    required = {"docs/infra-acceptance.md", "scripts/pipeline.py",
                "scripts/web_bridge.py", "config.json", "scope-index.json",
                "VISUAL_REVIEW_PROTOCOL.md", "PIPELINE.md"}
    if not required.issubset(listed):
        raise WebBridgeError("canonical pipeline or binding Markdown not verified")
    for r in verification["files"]:
        rel = r["path"]
        if (rel in required or
                rel.startswith("scripts/") and rel.endswith(".py")) and r["provider"] != "github":
            raise WebBridgeError("canonical source authority must originate in GitHub: " + rel)
    # Verify every declared GitHub-controlled input, not only Python modules:
    # JSON authority and operational checkpoints may otherwise be silently
    # substituted while the executable modules remain intact.
    source = {r["path"] for r in verification["files"] if r["provider"] == "github"}
    for rel in source:
        content = (Path(root) / rel).read_bytes()
        if remote_blobs.get(rel) != git_blob_sha(content):
            raise WebBridgeError("verified source differs from remote Git commit blob: " + rel)
    module_dir = (Path(root) / "scripts").resolve()
    _verify_import_graph(module_dir, listed)
    hashes = {r["path"]:r["sha256"] for r in verification["files"]}
    names = {p.stem for p in module_dir.glob("*.py")}
    # A module imported before this verification is untrusted even when it
    # points into the current checkout, unless a previous invocation stamped
    # the exact source SHA-256 after verified execution.
    for name, loaded in tuple(sys.modules.items()):
        if name not in names or name == "web_bridge":
            # The adapter is the bootstrap module; its on-disk bytes are
            # verified above but it is not imported by canonical pipeline.
            continue
        rel = "scripts/" + name + ".py"
        origin = getattr(loaded, "__file__", None)
        if (not origin or Path(origin).resolve() != module_dir / (name + ".py") or
                getattr(loaded, "_mapwork_verified_sha256", None) != hashes.get(rel)):
            raise WebBridgeError("stale/unverified cached Python module: " + name)
    # Do not trust an old timestamp-based bytecode cache.
    for cached in module_dir.rglob("__pycache__/*.pyc"):
        cached.unlink()
    importlib.invalidate_caches()
    original_path = list(sys.path)
    old_bytecode = sys.dont_write_bytecode
    sys.path.insert(0, str(module_dir))
    sys.dont_write_bytecode = True
    # The model-facing exchange has no Python connector callbacks. Bind its
    # source pin to the same Git commit whose blobs were independently checked.
    args_list = list(argv)
    if "--autonomous-journal" in args_list:
        if "--source-commit" in args_list:
            pos = args_list.index("--source-commit")
            if pos+1 >= len(args_list) or args_list[pos+1] != source_commit:
                raise WebBridgeError("host source commit differs from verified tree")
        else:
            args_list += ["--source-commit", source_commit]
    output, errors = io.StringIO(), io.StringIO()
    try:
        spec = importlib.util.spec_from_file_location("pipeline", module_dir / "pipeline.py")
        pipeline = importlib.util.module_from_spec(spec)
        sys.modules["pipeline"] = pipeline
        spec.loader.exec_module(pipeline)
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            exit_code = pipeline.main(["run", *args_list],
                                      action_executor=action_executor,
                                      remote_readback=remote_readback,
                                      journal_sync=journal_sync)
        for name in names:
            loaded = sys.modules.get(name)
            if loaded is not None and getattr(loaded, "__file__", None):
                rel = "scripts/" + name + ".py"
                if Path(loaded.__file__).resolve() != module_dir / (name + ".py"):
                    raise WebBridgeError("runtime imported foreign module: " + name)
                loaded._mapwork_verified_sha256 = hashes[rel]
    finally:
        sys.path[:] = original_path
        sys.dont_write_bytecode = old_bytecode
    raw = output.getvalue().strip() or errors.getvalue().strip()
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise WebBridgeError("canonical pipeline did not return a machine JSON verdict") from exc
    status = result.get("status")
    if status not in ("BLOCKED", "FAIL", "CHECKPOINT", "READY_FOR_OWNER_REVIEW"):
        raise WebBridgeError("unrecognized pipeline status")
    if status == "CHECKPOINT" and result.get("result",{}).get("blockers"):
        raise WebBridgeError("checkpoint concealed blockers")
    return {"status":status,"exit_code":exit_code,"transport":verification,
            "pipeline":result,"authorizes_canon":False}

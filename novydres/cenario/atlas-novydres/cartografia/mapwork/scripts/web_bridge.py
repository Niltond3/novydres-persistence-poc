"""Byte-verified ChatGPT Web adapter for the ONE Mapwork pipeline.

A host connector retrieves source/assets; this code has no network, git CLI,
subprocess, OAuth or image-generation implementation. The canonical pipeline
is still scripts/pipeline.py: run_web invokes its main() in-process.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import importlib.util
import json
import re
import sys
from pathlib import Path
from zipfile import ZipFile, BadZipFile

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
FILE_MANIFEST_SCHEMA = "NOVYDRES_MAPWORK_WEB_FILES_1"


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
    return {"status":"PASS","source_commit":commit,"files":verified,
            "file_count":len(verified)}


def extract_verified_zip(archive, dest, *, max_bytes=200_000_000):
    """Safe no-network ZIP extraction; file integrity checked by verify_files afterwards."""
    dest = Path(dest).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    try:
        with ZipFile(archive) as z:
            total = 0
            for member in z.infolist():
                rel = checked_relative(member.filename.rstrip("/"))
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
    return dest


def run_web(*, argv, file_manifest, root, source_commit):
    """Run exact canonical pipeline.main WITHOUT invoking a terminal or clone.

    Caller must read real files using connectors and check their GitHub/Drive
    readbacks before calling; this adapter cannot authenticate those requests.
    """
    verification = verify_files(file_manifest, root=root, expected_commit=source_commit)
    required = {"scripts/pipeline.py", "scripts/mapwork.py", "scripts/flow.py",
                "scripts/contracts.py", "scripts/acceptance.py",
                "docs/infra-acceptance.md", "scripts/web_bridge.py"}
    listed = {r["path"] for r in verification["files"]}
    if not required.issubset(listed):
        raise WebBridgeError("verified canonical pipeline or Markdown contract absent")
    module_dir = (Path(root) / "scripts").resolve()
    for name in ("pipeline", "mapwork", "flow", "contracts", "acceptance"):
        loaded = sys.modules.get(name)
        if loaded is not None and not Path(loaded.__file__).resolve().is_relative_to(module_dir):
            raise WebBridgeError("stale Python module from another source checkout: " + name)
    if str(module_dir) not in sys.path:
        sys.path.insert(0, str(module_dir))
    spec = importlib.util.spec_from_file_location("pipeline", module_dir / "pipeline.py")
    pipeline = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pipeline)  # exact, byte-verified canonical source
    output, errors = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
        exit_code = pipeline.main(["run", *list(argv)])
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

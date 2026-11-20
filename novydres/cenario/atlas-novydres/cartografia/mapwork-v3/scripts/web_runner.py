#!/usr/bin/env python3
"""Fail-closed, read-only GitHub Actions runner for browser agents.

This service emits a verified planning checkpoint, NEVER an image approval.
A request is committed to the candidate branch and bound to its own commit
parent, content SHA and relevant spatial inputs. Pushes inspect every commit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import mapwork as core
import pipeline

ROOT=Path(__file__).resolve().parents[1]
PATH_PREFIX="novydres/cenario/atlas-novydres/cartografia/mapwork-v3/"
REQUEST_SCHEMA="NOVYDRES_MAPWORK_V32_WEB_REQUEST_1"
OUTPUT_SCHEMA="NOVYDRES_MAPWORK_V32_WEB_RESULT_1"
SHA40=re.compile(r"^[0-9a-f]{40}$")
SHA64=re.compile(r"^[0-9a-f]{64}$")


def checked_path(value, *, prefix=None):
    p=Path(value)
    if p.is_absolute() or ".." in p.parts or not p.parts:
        raise core.Invalid("request path must be relative and remain inside Mapwork")
    if prefix is not None and (p.parts[0]!=prefix or p.suffix!=".json" or len(p.parts)!=2):
        raise core.Invalid("request must reside under "+prefix+"/*.json")
    resolved=(ROOT/p).resolve()
    if not resolved.is_relative_to(ROOT.resolve()):
        raise core.Invalid("request path escaped Mapwork")
    return resolved


def _git(*parts):
    return subprocess.check_output(["git",*parts],cwd=ROOT,text=True).strip()


def parent_commit():
    return _git("rev-parse","HEAD^")


def verify_remote_branch():
    """Reject a stale Actions checkout even if its parent SHA happens to match."""
    if os.environ.get("GITHUB_ACTIONS")!="true":
        return
    sha=os.environ.get("GITHUB_SHA","")
    branch=os.environ.get("GITHUB_REF_NAME","")
    ref=os.environ.get("GITHUB_REF","")
    if not SHA40.fullmatch(sha) or not branch.startswith("mapwork-v3/") or ref!="refs/heads/"+branch:
        raise core.Invalid("runner requires a candidate-branch event with an exact SHA")
    if _git("rev-parse","HEAD")!=sha:
        raise core.Invalid("runner checkout differs from the triggering SHA")
    remote=_git("ls-remote","origin","refs/heads/"+branch).splitlines()
    if len(remote)!=1 or remote[0].split()[0]!=sha:
        raise core.Invalid("remote branch SHA changed: obsolete runner request")


def _request_changes_in_commit(commit):
    paths=_git("diff-tree","--no-commit-id","--name-only","-r",commit).splitlines()
    return [p for p in paths if p.startswith(PATH_PREFIX+"web-requests/")
            and p.endswith(".json") and
            len(Path(p[len(PATH_PREFIX):]).parts)==2]


def discover_request_metadata():
    """Inspect the complete ordered push commit interval, never only final diff."""
    head=_git("rev-parse","HEAD")
    if head!=os.environ.get("GITHUB_SHA"):
        raise core.Invalid("runner checkout differs from the triggering SHA")
    before=os.environ.get("GITHUB_EVENT_BEFORE","")
    if before=="0"*40:
        raise core.Invalid("new branch push has no verifiable prior range; use dispatch")
    if before:
        if not SHA40.fullmatch(before):
            raise core.Invalid("push before SHA is malformed")
        try:
            ancestor=_git("merge-base",before,head)
        except subprocess.CalledProcessError as exc:
            raise core.Invalid("push ancestor unavailable; full history required") from exc
        if ancestor!=before:
            raise core.Invalid("push is not a fast-forward; cannot safely skip request commits")
        commits=_git("rev-list","--reverse",f"{before}..{head}").splitlines()
        if not commits and before!=head:
            raise core.Invalid("push commit interval could not be reconstructed")
    else:
        # Single-head fallback only for explicit standalone tests and diagnostics.
        commits=[head]
    changes=[(commit,path) for commit in commits
             for path in _request_changes_in_commit(commit)]
    if len(changes)>1:
        raise core.Invalid("multiple distinct or repeated web requests in push: split into one request per run")
    if not changes:
        return None
    commit,path=changes[0]
    return {"request_path":path[len(PATH_PREFIX):],
            "request_commit_sha":commit,
            "git_path":path}


def discover_request_from_push():
    metadata=discover_request_metadata()
    return metadata["request_path"] if metadata else None


def _request_commit_identity(path,selected=None):
    """For dispatch, recover the last modifying commit of the exact request blob."""
    git_path=PATH_PREFIX+str(path.relative_to(ROOT))
    head=_git("rev-parse","HEAD")
    commit=selected["request_commit_sha"] if selected else _git(
        "log","-1","--format=%H","HEAD","--",git_path)
    if not SHA40.fullmatch(commit):
        raise core.Invalid("versioned request has no verified commit identity")
    try:
        _git("merge-base","--is-ancestor",commit,head)
    except subprocess.CalledProcessError as exc:
        raise core.Invalid("request commit is not an ancestor of checked-out HEAD") from exc
    raw=subprocess.check_output(["git","show",f"{commit}:{git_path}"],cwd=ROOT)
    if raw!=path.read_bytes():
        raise core.Invalid("versioned request bytes changed since its selected commit")
    parent=_git("rev-parse",commit+"^")
    return {"request_commit_sha":commit,
            "request_sha256":hashlib.sha256(raw).hexdigest(),
            "request_parent_sha":parent}


def _input_fingerprints(result,design_root=None):
    """Hash all inputs that a checkpoint depends on, including design unit trees."""
    fingerprints={
        "zone_sha256":result["inputs"]["zone_sha256"],
        "spatial_sha256":result["inputs"]["spatial_sha256"],
        "config_sha256":core.sha(core.CONFIG),
        "world_state_sha256":core.sha(core.STATE),
        "runner_sha256":core.sha(Path(__file__)),
        "pipeline_sha256":core.sha(Path(pipeline.__file__))
    }
    if design_root:
        directory=checked_path(design_root)
        if directory.exists():
            if not directory.is_dir():
                raise core.Invalid("design root must be a directory")
            paths=sorted(directory.rglob("*.json"))
            fingerprints["design_files"]={
                str(p.relative_to(ROOT)):core.sha(p) for p in paths
                if p.is_file() and p.resolve().is_relative_to(ROOT.resolve())}
        else:
            fingerprints["design_files"]=None
    else:
        fingerprints["design_files"]=None
    return fingerprints


def _check_resume(payload,checkpoint,source_fingerprints):
    resume=payload.get("resume")
    if resume is None:
        return None
    if not isinstance(resume,dict):
        raise core.Invalid("resume must identify a versioned remote checkpoint")
    path=checked_path(resume.get("checkpoint_path",""),prefix="web-checkpoints")
    expected=resume.get("checkpoint_sha256")
    if not SHA64.fullmatch(expected or "") or not path.is_file() or core.sha(path)!=expected:
        raise core.Invalid("resume checkpoint missing or tampered")
    old=core.load(path)
    if old.get("schema")!=OUTPUT_SCHEMA or old.get("checkpoint",{}).get("district")!=checkpoint["district"]:
        raise core.Invalid("resume checkpoint identity or district differs")
    if old.get("input_fingerprints")!=source_fingerprints:
        raise core.Invalid("resume checkpoint inputs changed; create a new planning request")
    previous=old["checkpoint"]
    if (previous["phase"]!=checkpoint["phase"] or
        previous["next_action"]!=checkpoint["next_action"]):
        raise core.Invalid("resume phase changed under identical inputs; manual reconciliation required")
    return {"checkpoint_sha256":expected,
            "request_id":old.get("request_id"),
            "source_head_sha":old.get("source_head_sha")}


def run_request(*,district=None,request=None,out):
    root=Path(out)
    root.mkdir(parents=True,exist_ok=True)
    if not (os.environ.get("GITHUB_EVENT_NAME")=="pull_request" and
            request is None and district):
        verify_remote_branch()
    selected=None
    if not request and not district and os.environ.get("GITHUB_EVENT_NAME")=="push":
        selected=discover_request_metadata()
        if selected:
            request=selected["request_path"]
        else:
            district="kingswell"  # Workflow-only push, safe diagnostic
    payload=None
    identity=None
    if request:
        source=checked_path(request,prefix="web-requests")
        payload=core.load(source)
        if payload.get("schema")!=REQUEST_SCHEMA:
            raise core.Invalid("invalid web request schema")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}",payload.get("request_id","")):
            raise core.Invalid("invalid request ID")
        if not SHA40.fullmatch(payload.get("expected_parent_sha","")):
            raise core.Invalid("request must bind to a full expected parent SHA")
        if os.environ.get("GITHUB_ACTIONS")=="true":
            identity=_request_commit_identity(source,selected)
            expected_parent=identity["request_parent_sha"]
        else:
            # Local test/bootstrap mode; remote Actions always verifies the exact
            # committed request and parent rather than trusting HEAD^.
            expected_parent=parent_commit() if os.environ.get("GITHUB_SHA") else payload["expected_parent_sha"]
            identity={"request_commit_sha":None,
                      "request_sha256":core.sha(source),
                      "request_parent_sha":expected_parent}
        if expected_parent!=payload["expected_parent_sha"]:
            raise core.Invalid("stale or non-CAS web request: parent commit differs")
        district=payload.get("district")
        zone=str(checked_path(payload["zone_path"])) if payload.get("zone_path") else None
        spatial=str(checked_path(payload["spatial_path"])) if payload.get("spatial_path") else None
        design_root=payload.get("design_root")
        design_unit=payload.get("design_unit")
    else:
        zone=spatial=design_root=design_unit=None
    if bool(district)==bool(zone):
        raise core.Invalid("web runner needs exactly one district or zone source")
    if design_root is not None:
        design_root=str(checked_path(design_root))
    if design_unit and not re.fullmatch(r"WU-[0-9]{5}-[0-9]{4}-[0-9]{4}",design_unit):
        raise core.Invalid("unsafe design unit identity")
    args=argparse.Namespace(district=district,zone=zone,spatial=spatial,
                            reference=None,assets=None,before=None,execute=False,
                            design_root=design_root,design_unit=design_unit,out=str(root))
    result=pipeline.run(args)
    fingerprints=_input_fingerprints(result,payload.get("design_root") if payload else None)
    resumed=_check_resume(payload,result,fingerprints) if payload else None
    ref=os.environ.get("GITHUB_SHA") or None
    info={
        "schema":OUTPUT_SCHEMA,
        "request_id":payload["request_id"] if payload else None,
        "request_commit_sha":identity["request_commit_sha"] if identity else None,
        "request_sha256":identity["request_sha256"] if identity else None,
        "source_head_sha":ref,
        "requested_parent_sha":payload.get("expected_parent_sha") if payload else None,
        "runner":"GITHUB_ACTIONS_READ_ONLY",
        "media_access":"NOT_PROVISIONED",
        "phase":result["phase"],
        "next_action":result["next_action"],
        "execution":"BLOCKED_OR_AWAITING_EXTERNAL_ACTION",
        "input_fingerprints":fingerprints,
        "resumed_from":resumed,
        "checkpoint":result
    }
    saved=root/"checkpoint.json"
    core.save(saved,info)
    digest=core.sha(saved)
    core.save(root/"readback.json",{
        "checkpoint_sha256":digest,
        "source_head_sha":ref,
        "request_id":info["request_id"],
        "request_commit_sha":info["request_commit_sha"],
        "request_sha256":info["request_sha256"],
        "input_fingerprints":fingerprints,
        "resumed_from":resumed,
        "checkpoint_name":"checkpoint.json"
    })
    print(json.dumps({
        "status":"PASS_DIAGNOSTIC_NOT_IMAGE_AUTHORIZATION",
        "request_id":info["request_id"],
        "request_commit_sha":info["request_commit_sha"],
        "request_sha256":info["request_sha256"],
        "source_head_sha":ref,
        "requested_parent_sha":info["requested_parent_sha"],
        "phase":result["phase"],"next_action":result["next_action"],
        "blockers":result["blockers"],"inputs":result["inputs"],
        "input_fingerprints":fingerprints,"resumed_from":resumed,
        "checkpoint_sha256":digest
    },ensure_ascii=False))
    return info


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--request",default=None)
    p.add_argument("--district",default=None)
    p.add_argument("--out",required=True)
    args=p.parse_args(argv)
    try:
        run_request(district=args.district,request=args.request,out=args.out)
        return 0
    except (core.Invalid,ValueError,KeyError,TypeError,OSError,subprocess.CalledProcessError) as e:
        print(json.dumps({"status":"FAIL","error":str(e)},ensure_ascii=False),file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())

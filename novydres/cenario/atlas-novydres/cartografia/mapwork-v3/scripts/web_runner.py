#!/usr/bin/env python3
"""GitHub Actions bridge for browser-only agents; executes read-only planning in hosted runner.

Agents submit one versioned request through GitHub using compare-and-swap on the
candidate branch, then read the job artifact. Private reference/media are NEVER
sent to public Actions; media-bound operations remain blocked until a trusted
media-enabled executor is explicitly connected.
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
REQUEST_SCHEMA="NOVYDRES_MAPWORK_V32_WEB_REQUEST_1"
OUTPUT_SCHEMA="NOVYDRES_MAPWORK_V32_WEB_RESULT_1"


def checked_path(value, *, prefix=None):
    p=Path(value)
    if p.is_absolute() or ".." in p.parts or not p.parts:
        raise core.Invalid("request path must be relative and remain inside Mapwork")
    if prefix is not None and (p.parts[0]!=prefix or p.suffix!=".json"):
        raise core.Invalid("request must reside under "+prefix+"/*.json")
    resolved=(ROOT/p).resolve()
    if not resolved.is_relative_to(ROOT.resolve()):
        raise core.Invalid("request path escaped Mapwork")
    return resolved


def parent_commit():
    return subprocess.check_output(["git","rev-parse","HEAD^"],cwd=ROOT,text=True).strip()


def discover_request_from_push():
    """Use the checked-out commit, not incomplete push event payload file lists."""
    prefix="novydres/cenario/atlas-novydres/cartografia/mapwork-v3/web-requests/"
    checked_out=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    if checked_out!=os.environ.get("GITHUB_SHA"):
        raise core.Invalid("runner checkout differs from the triggering SHA")
    changed_paths=subprocess.check_output(
        ["git","diff-tree","--no-commit-id","--name-only","-r","HEAD"],
        cwd=ROOT,text=True).splitlines()
    changed={p[len(prefix):] for p in changed_paths
             if p.startswith(prefix) and p.endswith(".json")}
    if len(changed)>1:
        raise core.Invalid("web runner requires at most one committed request per push")
    return "web-requests/"+next(iter(changed)) if changed else None


def run_request(*, district=None, request=None, out):
    root=Path(out)
    root.mkdir(parents=True,exist_ok=True)
    if not request and not district and os.environ.get("GITHUB_EVENT_NAME")=="push":
        request=discover_request_from_push()
        if request is None:
            district="kingswell"  # workflow-only push: safe diagnostic, no art
    payload=None
    if request:
        source=checked_path(request,prefix="web-requests")
        payload=core.load(source)
        if payload.get("schema")!=REQUEST_SCHEMA:
            raise core.Invalid("invalid web request schema")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}",payload.get("request_id","")):
            raise core.Invalid("invalid request ID")
        if not re.fullmatch(r"[0-9a-f]{40}",payload.get("expected_parent_sha","")):
            raise core.Invalid("request must bind to a full expected parent SHA")
        if os.environ.get("GITHUB_SHA") and parent_commit()!=payload["expected_parent_sha"]:
            raise core.Invalid("stale or non-CAS web request: parent commit differs")
        district=payload.get("district")
        zone=str(checked_path(payload["zone_path"])) if payload.get("zone_path") else None
        spatial=str(checked_path(payload["spatial_path"])) if payload.get("spatial_path") else None
        design_root=str(checked_path(payload["design_root"])) if payload.get("design_root") else None
        design_unit=payload.get("design_unit")
    else:
        zone=spatial=design_root=design_unit=None
    if bool(district)==bool(zone):
        raise core.Invalid("web runner needs exactly one district or zone source")
    # No raw Google Drive bytes or local client filesystem are assumed.
    args=argparse.Namespace(district=district,zone=zone,spatial=spatial,
                            reference=None,assets=None,before=None,execute=False,
                            design_root=design_root,design_unit=design_unit,out=str(root))
    result=pipeline.run(args)
    ref=os.environ.get("GITHUB_SHA") or None
    info={"schema":OUTPUT_SCHEMA,"request_id":payload["request_id"] if payload else None,
          "source_head_sha":ref,"requested_parent_sha":payload.get("expected_parent_sha") if payload else None,
          "runner":"GITHUB_ACTIONS_READ_ONLY","media_access":"NOT_PROVISIONED",
          "phase":result["phase"],"next_action":result["next_action"],
          "execution":"BLOCKED_OR_AWAITING_EXTERNAL_ACTION",
          "checkpoint":result}
    saved=root/"checkpoint.json"
    core.save(saved,info)
    digest=hashlib.sha256(saved.read_bytes()).hexdigest()
    core.save(root/"readback.json",{"checkpoint_sha256":digest,"source_head_sha":ref,
                                  "checkpoint_name":"checkpoint.json"})
    print(json.dumps({"status":"PASS_DIAGNOSTIC_NOT_IMAGE_AUTHORIZATION",
                      "phase":result["phase"],"next_action":result["next_action"],
                      "checkpoint_sha256":digest},ensure_ascii=False))
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
    except (core.Invalid,ValueError,KeyError,OSError,subprocess.CalledProcessError) as e:
        print(json.dumps({"status":"FAIL","error":str(e)},ensure_ascii=False),file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())

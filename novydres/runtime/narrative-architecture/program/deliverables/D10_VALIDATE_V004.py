#!/usr/bin/env python3
"""D10 V004 verifies phase test evidence by executing the pinned runner."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

BASE = Path(__file__).resolve().parent
V2_PATH = BASE / "D10_VALIDATE_V002.py"
spec = importlib.util.spec_from_file_location("d10_v2_v004", V2_PATH)
v2 = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(v2)

DELIVERABLES = v2.DELIVERABLES
BRANCH = v2.BRANCH
GATE_OK = v2.GATE_OK
ENVELOPE_SCHEMA = "D10_PHASE_ENVELOPE_SCHEMA_V004.json"
CATALOG_SCHEMA = "D10_PHASE_TEST_CATALOG_SCHEMA_V004.json"
REPORT_SCHEMA = "D10_PHASE_TEST_REPORT_SCHEMA_V004.json"
CATALOG_FILE = "D10_PHASE_BINDING_TESTS_V004.json"


def _blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def _deliverable_ref(root: Path, head: str, ref: dict[str, Any], label: str) -> tuple[bytes | None, list[str]]:
    path = ref.get("path") if isinstance(ref, dict) else None
    if not isinstance(path, str) or not path.startswith(DELIVERABLES + "/") or ".." in Path(path).parts:
        return None, [f"{label} must reference a tracked file inside deliverables"]
    try:
        raw = v2.git_regular_blob(root, head, path)
    except (ValueError, subprocess.CalledProcessError, OSError) as exc:
        return None, [f"{label} has an invalid Git entry or cannot be read: {exc}"]
    if _blob_sha(raw) != ref.get("blob_sha"):
        return None, [f"{label} blob is not verified at pinned HEAD"]
    return raw, []


def _extract_pinned_deliverables(root: Path, head: str, destination: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "archive", "--format=tar", head, DELIVERABLES],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=60,
    )
    if result.returncode:
        return [f"cannot archive pinned phase runner source: {result.stderr.decode(errors='replace')[:500]}"]
    base = destination.resolve()
    try:
        with tarfile.open(fileobj=io.BytesIO(result.stdout), mode="r:") as archive:
            for member in archive.getmembers():
                parts = PurePosixPath(member.name).parts
                deliverable_parts = PurePosixPath(DELIVERABLES).parts
                if not parts or ".." in parts:
                    return ["pinned deliverables archive contains an unsafe path"]
                target = destination.joinpath(*parts)
                if member.isdir() and parts == deliverable_parts[:len(parts)]:
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                if parts[:len(deliverable_parts)] != deliverable_parts:
                    return ["pinned deliverables archive contains an unsafe path"]
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                if not member.isfile():
                    continue
                resolved_parent = target.parent.resolve()
                if resolved_parent != base and base not in resolved_parent.parents:
                    return ["pinned runner path escapes its temporary directory"]
                target.parent.mkdir(parents=True, exist_ok=True)
                stream = archive.extractfile(member)
                if stream is None:
                    return ["pinned runner source cannot be extracted"]
                target.write_bytes(stream.read())
    except (OSError, tarfile.TarError) as exc:
        return [f"pinned deliverables archive is invalid: {exc}"]
    return []


def _pinned_schema(root: Path, head: str, filename: str) -> tuple[dict[str, Any] | None, list[str]]:
    path = f"{DELIVERABLES}/{filename}"
    try:
        raw = v2.git_regular_blob(root, head, path)
        value = json.loads(raw)
    except (ValueError, subprocess.CalledProcessError, OSError, json.JSONDecodeError) as exc:
        return None, [f"schema {filename} is not a regular JSON blob at pinned HEAD: {exc}"]
    if not isinstance(value, dict):
        return None, [f"schema {filename} at pinned HEAD is not an object"]
    return value, []


def _execute_pinned_runner(root: Path, head: str, runner_path: str) -> tuple[dict[str, Any] | None, list[str]]:
    runner_raw, errors = _deliverable_ref(root, head, {"path": runner_path, "blob_sha": _tree_blob(root, head, runner_path)}, "phase test runner")
    if runner_raw is None:
        return None, errors
    try:
        with tempfile.TemporaryDirectory(prefix="novydres-pinned-phase-runner-") as temp:
            temp_root = Path(temp)
            deliverables = temp_root / DELIVERABLES
            archive_errors = _extract_pinned_deliverables(root, head, temp_root)
            if archive_errors:
                return None, archive_errors
            runner = temp_root / runner_path
            report_path = temp_root / "executed-report.json"
            env = {"PATH": os.environ.get("PATH", ""), "PYTHONIOENCODING": "utf-8"}
            try:
                run = subprocess.run(
                    [sys.executable, str(runner), "--self-test", "--report-out", str(report_path)],
                    cwd=deliverables, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    check=False, timeout=120,
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                return None, [f"pinned phase test runner could not complete: {exc}"]
            if run.returncode != 0:
                return None, [f"pinned phase test runner exited {run.returncode}: {run.stderr.decode(errors='replace')[:500]}"]
            if not report_path.is_file():
                return None, ["pinned phase test runner did not produce --report-out"]
            generated = json.loads(report_path.read_bytes())
            if not isinstance(generated, dict):
                return None, ["pinned phase test runner output is not a JSON object"]
            return generated, []
    except json.JSONDecodeError:
        return None, ["pinned phase test runner output is not valid JSON"]


def _tree_blob(root: Path, head: str, path: str) -> str:
    return v2.tree_blob(root, head, path)


def verify_test_report(
    root: Path,
    head: str,
    phase: str,
    catalog_ref: dict[str, Any],
    report_ref: dict[str, Any],
) -> list[str]:
    catalog_raw, errors = _deliverable_ref(root, head, catalog_ref, "phase test catalog")
    report_raw, report_errors = _deliverable_ref(root, head, report_ref, "phase test report")
    errors.extend(report_errors)
    if catalog_raw is None or report_raw is None:
        return errors
    catalog_schema, schema_errors = _pinned_schema(root, head, CATALOG_SCHEMA)
    errors.extend(schema_errors)
    report_schema, schema_errors = _pinned_schema(root, head, REPORT_SCHEMA)
    errors.extend(schema_errors)
    if catalog_schema is None or report_schema is None:
        return errors
    try:
        catalog, report = json.loads(catalog_raw), json.loads(report_raw)
    except json.JSONDecodeError:
        return errors + ["phase catalog or test report is not valid JSON"]
    from jsonschema import Draft202012Validator
    errors.extend(f"phase catalog schema: {item.message}" for item in Draft202012Validator(catalog_schema).iter_errors(catalog))
    errors.extend(f"phase test report schema: {item.message}" for item in Draft202012Validator(report_schema).iter_errors(report))
    if errors:
        return errors
    if catalog.get("phase") != phase:
        errors.append("test catalog does not identify this exact phase")
    cases = catalog.get("test_cases")
    if not isinstance(cases, list) or not cases:
        return errors + ["phase test catalog must contain a non-empty ordered test_cases list"]
    ids = [case.get("id") if isinstance(case, dict) else None for case in cases]
    if any(not isinstance(item, str) or not item for item in ids) or len(set(ids)) != len(ids):
        errors.append("phase test catalog IDs must be unique non-empty strings")
    runner_path = catalog.get("test_runner")
    report_runner = report.get("runner_ref", {})
    if not isinstance(runner_path, str) or not runner_path.startswith(DELIVERABLES + "/") or ".." in Path(runner_path).parts:
        errors.append("phase catalog must name a tracked runner inside deliverables")
    elif report_runner.get("path") != runner_path:
        errors.append("test report runner path differs from its pinned phase catalog")
    if report.get("phase") != phase or report.get("status") != "PASS":
        errors.append("test report is not a passing report for this exact phase")
    if report.get("catalog_ref") != catalog_ref:
        errors.append("test report is not bound to the exact catalog ref in the phase envelope")
    if [case.get("id") if isinstance(case, dict) else None for case in report.get("tests", [])] != ids:
        errors.append("test report IDs or order do not exactly match the phase catalog")
    if any(not isinstance(case, dict) or case.get("result") != "PASS" for case in report.get("tests", [])):
        errors.append("every phase catalog case must have an individual PASS result")
    if report.get("catalog_matches_runner") is not True or report.get("execution_mode") != "EXECUTED":
        errors.append("test report does not record an executed runner aligned to its exact catalog")
    if report.get("passed") != len(ids) or report.get("total") != len(ids):
        errors.append("test report totals do not match the phase-specific catalog")
    if errors:
        return errors
    generated, run_errors = _execute_pinned_runner(root, head, runner_path)
    errors.extend(run_errors)
    if generated is not None and generated != report:
        errors.append("pinned phase runner output differs from the declared test report")
    return errors


def validate_phase_envelope_v4(
    envelope: dict[str, Any], root: Path, source_head: str, expected_input_head: str, expected_master_head: str
) -> list[str]:
    schema, errors = _pinned_schema(root, source_head, ENVELOPE_SCHEMA)
    if schema is None:
        return errors
    from jsonschema import Draft202012Validator
    errors.extend(item.message for item in Draft202012Validator(schema).iter_errors(envelope))
    phase = envelope.get("phase")
    errors.extend(verify_test_report(root, source_head, phase, envelope.get("test_catalog_ref", {}), envelope.get("validation_report_ref", {})))

    previous_base = v2.BASE
    previous_verifier = v2.verify_test_report
    previous_handoff = v2.HANDOFFS.get("D10")
    try:
        with tempfile.TemporaryDirectory(prefix="novydres-v004-schema-") as temp:
            archive_errors = _extract_pinned_deliverables(root, source_head, Path(temp))
            if archive_errors:
                return errors + archive_errors
            v2.BASE = Path(temp) / DELIVERABLES
            v2.verify_test_report = lambda r, h, p, report: verify_test_report(
                r, h, p, envelope.get("test_catalog_ref", {}), report
            )
            v2.HANDOFFS["D10"] = f"{DELIVERABLES}/HANDOFF_D10_V004.json"
            compatible = {key: value for key, value in envelope.items() if key != "test_catalog_ref"}
            errors.extend(v2.validate_phase_envelope_v2(compatible, root, source_head, expected_input_head, expected_master_head))
    finally:
        v2.BASE = previous_base
        v2.verify_test_report = previous_verifier
        if previous_handoff is None:
            v2.HANDOFFS.pop("D10", None)
        else:
            v2.HANDOFFS["D10"] = previous_handoff
    return errors


def _fixture_commit(root: Path, message: str) -> str:
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", message], check=True)
    return v2.run(root, "rev-parse", "HEAD")


def _fixture_runner(phase: str, catalog_name: str, runner_path: str) -> str:
    values = {"phase": phase, "catalog": catalog_name, "runner": runner_path}
    constants = "\n".join(f"{key.upper()}={json.dumps(value)}" for key, value in values.items())
    return f'''#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path
{constants}
BASE = Path(__file__).resolve().parent
def blob(raw):
    return hashlib.sha1(f"blob {{len(raw)}}\\0".encode() + raw).hexdigest()
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--report-out", required=True)
    args = parser.parse_args()
    catalog_path = BASE / CATALOG
    catalog_raw = catalog_path.read_bytes()
    catalog = json.loads(catalog_raw)
    ids = [case["id"] for case in catalog["test_cases"]]
    assert catalog["phase"] == PHASE and ids and len(set(ids)) == len(ids)
    report = {{"phase": PHASE, "status": "PASS", "catalog_ref": {{"path": "{DELIVERABLES}/" + CATALOG, "blob_sha": blob(catalog_raw)}},
              "runner_ref": {{"path": RUNNER, "blob_sha": blob(Path(__file__).read_bytes())}},
              "execution_mode": "EXECUTED", "passed": len(ids), "total": len(ids),
              "catalog_matches_runner": True,
              "tests": [{{"id": ident, "result": "PASS", "detail": None}} for ident in ids]}}
    Path(args.report_out).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
if __name__ == "__main__":
    main()
'''


def self_test(report_path: Path | None = None) -> int:
    names = [
        "D10 report matches output from the pinned runner execution",
        "D11 report matches output from the pinned runner execution",
        "D12 report matches output from the pinned runner execution",
        "a declared PASS report differing from runner output is rejected",
        "a different existing runner is rejected for catalog mismatch",
        "envelope schema is loaded from pinned HEAD despite local drift",
        "symlink phase catalog is rejected",
    ]
    results = {name: "FAIL" for name in names}
    details: dict[str, str | None] = {name: "not executed" for name in names}
    def record(name: str, fn: Any) -> None:
        try:
            fn()
            results[name], details[name] = "PASS", None
        except Exception as exc:
            details[name] = f"{type(exc).__name__}: {exc}"

    with tempfile.TemporaryDirectory(prefix="novydres-d10-v4-") as temp:
        root = Path(temp) / "repo"
        root.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "master", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "D10 V004 Fixture"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "fixture@example.invalid"], check=True)
        dest = root / DELIVERABLES
        dest.mkdir(parents=True)
        for name in (ENVELOPE_SCHEMA, CATALOG_SCHEMA, REPORT_SCHEMA):
            (dest / name).write_bytes((BASE / name).read_bytes())
        fixtures = {}
        for phase, ident in (("D10", "D10-X1"), ("D11", "D11-X1"), ("D12", "D12-X1")):
            cat_name = f"{phase}_CATALOG.json"
            runner_rel = f"{DELIVERABLES}/{phase}_RUNNER.py"
            runner_path = dest / f"{phase}_RUNNER.py"
            runner_path.write_text(_fixture_runner(phase, cat_name, runner_rel), encoding="utf-8")
            catalog = {"document_id":f"{phase}_CATALOG", "version":"V004", "phase":phase,
                       "test_runner":runner_rel, "test_cases":[{"id":ident,"category":"fixture",
                       "description":"Runner verifies phase binding and unique catalog IDs.","expected":"PASS"}]}
            (dest / cat_name).write_text(json.dumps(catalog, sort_keys=True) + "\n", encoding="utf-8")
            fixtures[phase] = (cat_name, runner_rel, ident)
        alternate = dest / "D11_ALTERNATE_RUNNER.py"
        alternate.write_text(_fixture_runner("D11", "D11_CATALOG.json", f"{DELIVERABLES}/D11_ALTERNATE_RUNNER.py"), encoding="utf-8")
        head = _fixture_commit(root, "pin schemas catalogs and phase runners")
        refs = {}
        for phase, (cat_name, runner_rel, _ident) in fixtures.items():
            catalog_path = dest / cat_name
            catalog_ref = {"path":f"{DELIVERABLES}/{cat_name}", "blob_sha":_blob_sha(catalog_path.read_bytes())}
            generated, errors = _execute_pinned_runner(root, head, runner_rel)
            if errors or generated is None:
                raise AssertionError(errors)
            phase_report_path = dest / f"{phase}_REPORT.json"
            phase_report_path.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            refs[phase] = (catalog_ref, {"path":f"{DELIVERABLES}/{phase}_REPORT.json","blob_sha":_blob_sha(phase_report_path.read_bytes())})
        head = _fixture_commit(root, "pin executed phase reports")

        for phase in ("D10", "D11", "D12"):
            cat_ref, report_ref = refs[phase]
            record(names[("D10","D11","D12").index(phase)], lambda p=phase,c=cat_ref,r=report_ref: _expect_no_errors(verify_test_report(root, head, p, c, r)))

        def declared_pass_rejected() -> None:
            report_path = dest / "D11_REPORT.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["tests"][0]["detail"] = "declared without executing the pinned runner"
            report_path.write_text(json.dumps(report) + "\n", encoding="utf-8")
            bad_head = _fixture_commit(root, "manual report mutation")
            bad_ref = {"path":refs["D11"][1]["path"],"blob_sha":_blob_sha(report_path.read_bytes())}
            _expect_errors(verify_test_report(root, bad_head, "D11", refs["D11"][0], bad_ref), "differs from the declared")

        record(names[3], declared_pass_rejected)

        def existing_runner_mismatch_rejected() -> None:
            report_path = dest / "D11_REPORT.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["runner_ref"] = {"path":f"{DELIVERABLES}/D11_ALTERNATE_RUNNER.py",
                                    "blob_sha":_blob_sha(alternate.read_bytes())}
            report_path.write_text(json.dumps(report) + "\n", encoding="utf-8")
            bad_head = _fixture_commit(root, "valid alternate runner path mismatch")
            bad_ref = {"path":refs["D11"][1]["path"],"blob_sha":_blob_sha(report_path.read_bytes())}
            _expect_errors(verify_test_report(root, bad_head, "D11", refs["D11"][0], bad_ref), "differs from its pinned phase catalog")

        record(names[4], existing_runner_mismatch_rejected)

        def pinned_schema_ignores_worktree_drift() -> None:
            schema_path = dest / ENVELOPE_SCHEMA
            pinned = json.loads(schema_path.read_bytes())
            schema_path.write_text('{"type":"null"}', encoding="utf-8")
            loaded, errors = _pinned_schema(root, head, ENVELOPE_SCHEMA)
            if errors or loaded != pinned:
                raise AssertionError(f"schema not resolved from Git HEAD: {errors}")

        record(names[5], pinned_schema_ignores_worktree_drift)

        def symlink_catalog_rejected() -> None:
            symlink = dest / "SYMLINK_CATALOG.json"
            symlink.symlink_to("D11_CATALOG.json")
            symlink_head = _fixture_commit(root, "symlink catalog")
            ref = {"path":f"{DELIVERABLES}/SYMLINK_CATALOG.json","blob_sha":_tree_blob(root,symlink_head,f"{DELIVERABLES}/SYMLINK_CATALOG.json")}
            _expect_errors(verify_test_report(root, symlink_head, "D11", ref, refs["D11"][1]), "regular tracked file")

        record(names[6], symlink_catalog_rejected)

    catalog_file = BASE / CATALOG_FILE
    try:
        catalog = json.loads(catalog_file.read_text(encoding="utf-8"))
        aligned = [case["id"] for case in catalog["test_cases"]] == names
    except (OSError, KeyError, json.JSONDecodeError):
        aligned = False
    for name in names:
        print(f"{name}: {results[name]}" + (f" ({details[name]})" if details[name] else ""))
    passed = sum(value == "PASS" for value in results.values())
    print(f"RESULT {passed}/{len(names)}; gate={'PASS_WITH_UNKNOWN' if passed == len(names) and aligned else 'FAIL'}")
    if report_path:
        catalog_raw = catalog_file.read_bytes() if catalog_file.exists() else b""
        runner_raw = Path(__file__).read_bytes()
        report = {"phase":"D10","status":"PASS" if passed == len(names) and aligned else "FAIL",
                  "catalog_ref":{"path":f"{DELIVERABLES}/{CATALOG_FILE}","blob_sha":_blob_sha(catalog_raw)},
                  "runner_ref":{"path":f"{DELIVERABLES}/D10_VALIDATE_V004.py","blob_sha":_blob_sha(runner_raw)},
                  "execution_mode":"EXECUTED","passed":passed,"total":len(names),
                  "catalog_matches_runner":aligned,
                  "tests":[{"id":name,"result":results[name],"detail":details[name]} for name in names]}
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if passed == len(names) and aligned else 1


def _expect_no_errors(errors: list[str]) -> None:
    if errors:
        raise AssertionError(errors)


def _expect_errors(errors: list[str], fragment: str) -> None:
    if not any(fragment in error for error in errors):
        raise AssertionError(f"expected error containing {fragment!r}; got {errors}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--expected-source-head")
    parser.add_argument("--expected-input-head")
    parser.add_argument("--expected-master-head")
    parser.add_argument("--bundle", type=Path)
    parser.add_argument("--publication-record", type=Path)
    parser.add_argument("--envelope", type=Path)
    parser.add_argument("--report-out", type=Path)
    args = parser.parse_args()
    if args.self_test:
        return self_test(args.report_out)
    if not args.repo_root or not args.expected_source_head or not args.expected_master_head:
        parser.error("verified repository root, source HEAD, and master HEAD are required")
    if args.publication_record:
        errors = v2.verify_publication(json.loads(args.publication_record.read_text()), args.repo_root,
            args.expected_input_head or args.expected_source_head, args.expected_master_head)
    elif args.envelope:
        errors = validate_phase_envelope_v4(json.loads(args.envelope.read_text()), args.repo_root,
            args.expected_source_head, args.expected_input_head or args.expected_source_head, args.expected_master_head)
    elif args.bundle:
        errors = v2.validate_bundle_v2(json.loads(args.bundle.read_text()), args.repo_root,
            args.expected_source_head, args.expected_master_head)
    else:
        parser.error("choose --bundle, --envelope, or --publication-record")
    print(json.dumps({"status":"FAIL" if errors else "PASS_WITH_UNKNOWN","errors":errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

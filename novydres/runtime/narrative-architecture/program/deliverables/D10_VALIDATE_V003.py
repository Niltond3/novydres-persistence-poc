#!/usr/bin/env python3
"""D10 V003 phase-bound validation evidence verifier; documentary only."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

BASE = Path(__file__).resolve().parent
V2_PATH = BASE / "D10_VALIDATE_V002.py"
spec = importlib.util.spec_from_file_location("d10_v2", V2_PATH)
v2 = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(v2)

DELIVERABLES = v2.DELIVERABLES
BRANCH = v2.BRANCH
GATE_OK = v2.GATE_OK


def _deliverable_ref(root: Path, head: str, ref: dict[str, Any], label: str) -> tuple[bytes | None, list[str]]:
    path = ref.get("path") if isinstance(ref, dict) else None
    if not isinstance(path, str) or not path.startswith(DELIVERABLES + "/") or ".." in Path(path).parts:
        return None, [f"{label} must reference a tracked file inside deliverables"]
    try:
        raw = v2.git_regular_blob(root, head, path)
    except (ValueError, subprocess.CalledProcessError, OSError) as exc:
        return None, [f"{label} has an invalid Git entry or cannot be read: {exc}"]
    if v2.blob_sha(raw) != ref.get("blob_sha"):
        return None, [f"{label} blob is not verified at pinned HEAD"]
    return raw, []


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
    try:
        catalog = json.loads(catalog_raw)
        report = json.loads(report_raw)
    except json.JSONDecodeError:
        return errors + ["phase catalog or test report is not valid JSON"]

    try:
        from jsonschema import Draft202012Validator
        for schema_name, value, label in (
            ("D10_PHASE_TEST_CATALOG_SCHEMA_V003.json", catalog, "phase catalog"),
            ("D10_PHASE_TEST_REPORT_SCHEMA_V003.json", report, "phase test report"),
        ):
            schema_path = f"{DELIVERABLES}/{schema_name}"
            schema = json.loads(v2.git_regular_blob(root, head, schema_path))
            errors.extend(f"{label} schema: {item.message}" for item in Draft202012Validator(schema).iter_errors(value))
    except (ValueError, subprocess.CalledProcessError, OSError, json.JSONDecodeError) as exc:
        return errors + [f"phase catalog/report schema cannot be verified at pinned HEAD: {exc}"]

    if catalog.get("phase") != phase:
        errors.append("test catalog does not identify this exact phase")
    cases = catalog.get("test_cases")
    if not isinstance(cases, list) or not cases:
        return errors + ["phase test catalog must contain a non-empty ordered test_cases list"]
    ids = [case.get("id") if isinstance(case, dict) else None for case in cases]
    if any(not isinstance(item, str) or not item for item in ids) or len(set(ids)) != len(ids):
        errors.append("phase test catalog IDs must be unique non-empty strings")
    runner_path = catalog.get("test_runner")
    if not isinstance(runner_path, str) or not runner_path.startswith(DELIVERABLES + "/") or ".." in Path(runner_path).parts:
        errors.append("phase catalog must name a tracked runner inside deliverables")
    else:
        runner_ref = report.get("runner_ref", {})
        if runner_ref.get("path") != runner_path:
            errors.append("test report runner path differs from its pinned phase catalog")
        runner_raw, runner_errors = _deliverable_ref(root, head, runner_ref, "phase test runner")
        errors.extend(runner_errors)
        if runner_raw is None:
            errors.append("phase test runner is not pinned as a regular Git blob")

    if report.get("phase") != phase or report.get("status") != "PASS":
        errors.append("test report is not a passing report for this exact phase")
    if report.get("catalog_ref") != catalog_ref:
        errors.append("test report is not bound to the exact catalog ref in the phase envelope")
    tests = report.get("tests")
    if not isinstance(tests, list):
        tests = []
    if [case.get("id") if isinstance(case, dict) else None for case in tests] != ids:
        errors.append("test report IDs or order do not exactly match the phase catalog")
    if any(not isinstance(case, dict) or case.get("result") != "PASS" for case in tests):
        errors.append("every phase catalog case must have an individual PASS result")
    if report.get("catalog_matches_runner") is not True or report.get("execution_mode") != "EXECUTED":
        errors.append("test report does not record an executed runner aligned to its exact catalog")
    if report.get("passed") != len(ids) or report.get("total") != len(ids):
        errors.append("test report totals do not match the phase-specific catalog")
    return errors


def validate_phase_envelope_v3(
    envelope: dict[str, Any], root: Path, source_head: str, expected_input_head: str, expected_master_head: str
) -> list[str]:
    from jsonschema import Draft202012Validator

    schema = json.loads((BASE / "D10_PHASE_ENVELOPE_SCHEMA_V003.json").read_text(encoding="utf-8"))
    errors = [item.message for item in Draft202012Validator(schema).iter_errors(envelope)]
    phase = envelope.get("phase")
    errors.extend(verify_test_report(root, source_head, phase, envelope.get("test_catalog_ref", {}), envelope.get("validation_report_ref", {})))

    # Preserve V002's publication, audit, history and approval checks, replacing only
    # its D10-hard-coded report verifier and advancing D10's latest documentary gate.
    previous_verifier = v2.verify_test_report
    previous_d10_handoff = v2.HANDOFFS.get("D10")
    v2.verify_test_report = lambda r, h, p, report: verify_test_report(
        r, h, p, envelope.get("test_catalog_ref", {}), report
    )
    v2.HANDOFFS["D10"] = f"{DELIVERABLES}/HANDOFF_D10_V003.json"
    try:
        compatible_envelope = {key: value for key, value in envelope.items() if key != "test_catalog_ref"}
        errors.extend(v2.validate_phase_envelope_v2(compatible_envelope, root, source_head, expected_input_head, expected_master_head))
    finally:
        v2.verify_test_report = previous_verifier
        if previous_d10_handoff is None:
            v2.HANDOFFS.pop("D10", None)
        else:
            v2.HANDOFFS["D10"] = previous_d10_handoff
    return errors


def _fixture_commit(root: Path, message: str) -> str:
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", message], check=True)
    return v2.run(root, "rev-parse", "HEAD")


def self_test(report_path: Path | None = None) -> int:
    names = [
        "D10 catalog accepts only its own phase report",
        "D11 phase-specific catalog and report are accepted",
        "D12 phase-specific catalog and report are accepted",
        "D10 catalog cannot masquerade as D11",
        "catalog phase mismatch is rejected",
        "wrong report ID order is rejected",
        "wrong report totals are rejected",
        "symlink phase catalog is rejected",
        "symlink phase report is rejected",
        "runner path must match its catalog",
    ]
    results: dict[str, str] = {name: "FAIL" for name in names}
    details: dict[str, str | None] = {name: "not executed" for name in names}

    def record(name: str, fn: Any) -> None:
        try:
            fn()
            results[name] = "PASS"
            details[name] = None
        except Exception as exc:
            details[name] = f"{type(exc).__name__}: {exc}"

    def make_docs(root: Path, phase: str, ids: list[str], runner: str) -> tuple[dict[str, str], dict[str, str]]:
        catalog_path = root / f"{DELIVERABLES}/{phase}_CATALOG.json"
        report_path_local = root / f"{DELIVERABLES}/{phase}_REPORT.json"
        catalog_path.parent.mkdir(parents=True, exist_ok=True)
        catalog = {"document_id": f"{phase}_CATALOG", "version": "V003", "phase": phase, "test_runner": runner,
                   "test_cases": [{"id": item, "category":"fixture", "description":"Pinned phase fixture assertion.", "expected": "PASS"} for item in ids]}
        catalog_path.write_text(json.dumps(catalog, sort_keys=True) + "\n", encoding="utf-8")
        catalog_ref = {"path":catalog_path.relative_to(root).as_posix(), "blob_sha":v2.blob_sha(catalog_path.read_bytes())}
        runner_file = root / runner
        report = {"phase": phase, "status": "PASS", "catalog_ref": catalog_ref,
                  "runner_ref": {"path":runner, "blob_sha":v2.blob_sha(runner_file.read_bytes())},
                  "tests": [{"id": item, "result": "PASS", "detail":None} for item in ids], "passed": len(ids), "total": len(ids),
                  "catalog_matches_runner": True, "execution_mode": "EXECUTED"}
        report_path_local.write_text(json.dumps(report, sort_keys=True) + "\n", encoding="utf-8")
        return catalog_ref, \
               {"path": report_path_local.relative_to(root).as_posix(), "blob_sha": v2.blob_sha(report_path_local.read_bytes())}

    with tempfile.TemporaryDirectory(prefix="novydres-d10-v3-") as temp:
        root = Path(temp) / "repo"
        root.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "master", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "D10 V003 Fixture"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "fixture@example.invalid"], check=True)
        runner_path = f"{DELIVERABLES}/D10_VALIDATE_V003.py"
        runner_file = root / runner_path
        runner_file.parent.mkdir(parents=True, exist_ok=True)
        runner_file.write_bytes(Path(__file__).read_bytes())
        for schema_name in ("D10_PHASE_TEST_CATALOG_SCHEMA_V003.json", "D10_PHASE_TEST_REPORT_SCHEMA_V003.json"):
            schema_source = BASE / schema_name
            schema_target = root / f"{DELIVERABLES}/{schema_name}"
            schema_target.parent.mkdir(parents=True, exist_ok=True)
            schema_target.write_bytes(schema_source.read_bytes())
        fixtures: dict[tuple[str, str], tuple[dict[str, str], dict[str, str]]] = {}
        for phase, ids in (("D10", ["D10-X1"]), ("D11", ["D11-X1", "D11-X2"]), ("D12", ["D12-X1"])):
            fixtures[(phase, "valid")] = make_docs(root, phase, ids, runner_path)
        head = _fixture_commit(root, "valid phase catalogs and reports")

        def check_valid(phase: str) -> None:
            catalog_ref, report_ref = fixtures[(phase, "valid")]
            errors = verify_test_report(root, head, phase, catalog_ref, report_ref)
            if errors:
                raise AssertionError(errors)

        record(names[0], lambda: check_valid("D10"))
        record(names[1], lambda: check_valid("D11"))
        record(names[2], lambda: check_valid("D12"))

        d10_catalog, d10_report = fixtures[("D10", "valid")]
        record(names[3], lambda: _expect_errors(verify_test_report(root, head, "D11", d10_catalog, d10_report), "exact phase"))

        wrong_phase_path = root / f"{DELIVERABLES}/WRONG_PHASE_CATALOG.json"
        wrong_phase_path.write_text(json.dumps({"phase": "D10", "test_runner": runner_path, "test_cases": [{"id":"X1"}]}), encoding="utf-8")
        wrong_phase_ref = {"path": wrong_phase_path.relative_to(root).as_posix(), "blob_sha": v2.blob_sha(wrong_phase_path.read_bytes())}
        wrong_phase_report_path = root / f"{DELIVERABLES}/WRONG_PHASE_REPORT.json"
        wrong_phase_report_path.write_text(json.dumps({"phase":"D11","status":"PASS","catalog_ref":wrong_phase_ref,
            "runner_ref":{"path":runner_path,"blob_sha":v2.blob_sha(runner_file.read_bytes())},"tests":[{"id":"X1","result":"PASS"}],
            "passed":1,"total":1,"catalog_matches_runner":True,"execution_mode":"EXECUTED"}), encoding="utf-8")
        head2 = _fixture_commit(root, "phase mismatch fixture")
        wrong_phase_report_ref = {"path":wrong_phase_report_path.relative_to(root).as_posix(), "blob_sha":v2.blob_sha(wrong_phase_report_path.read_bytes())}
        record(names[4], lambda: _expect_errors(verify_test_report(root, head2, "D11", wrong_phase_ref, wrong_phase_report_ref), "exact phase"))

        def bad_report_case(label: str, mutate: Any, expected: str) -> None:
            path = root / f"{DELIVERABLES}/{label}.json"
            report = json.loads((root / fixtures[("D11", "valid")][1]["path"]).read_text(encoding="utf-8"))
            report["catalog_ref"] = fixtures[("D11", "valid")][0]
            report["runner_ref"] = {"path":runner_path,"blob_sha":v2.blob_sha(runner_file.read_bytes())}
            mutate(report)
            path.write_text(json.dumps(report, sort_keys=True) + "\n", encoding="utf-8")
            local_head = _fixture_commit(root, label)
            ref = {"path":path.relative_to(root).as_posix(), "blob_sha":v2.blob_sha(path.read_bytes())}
            errs = verify_test_report(root, local_head, "D11", fixtures[("D11", "valid")][0], ref)
            _expect_errors(errs, expected)

        record(names[5], lambda: bad_report_case("WRONG_ORDER", lambda report: report["tests"].reverse(), "order"))
        record(names[6], lambda: bad_report_case("WRONG_TOTAL", lambda report: report.update(total=99), "totals"))

        symlink_catalog = root / f"{DELIVERABLES}/SYMLINK_CATALOG.json"
        symlink_catalog.symlink_to(Path(fixtures[("D11", "valid")][0]["path"]).name)
        symlink_head = _fixture_commit(root, "symlink catalog fixture")
        symlink_cat_ref = {"path":symlink_catalog.relative_to(root).as_posix(), "blob_sha":v2.tree_blob(root, symlink_head, symlink_catalog.relative_to(root).as_posix())}
        record(names[7], lambda: _expect_errors(verify_test_report(root, symlink_head, "D11", symlink_cat_ref, fixtures[("D11", "valid")][1]), "regular tracked file"))

        symlink_report = root / f"{DELIVERABLES}/SYMLINK_REPORT.json"
        symlink_report.symlink_to(Path(fixtures[("D11", "valid")][1]["path"]).name)
        symlink_head2 = _fixture_commit(root, "symlink report fixture")
        symlink_rep_ref = {"path":symlink_report.relative_to(root).as_posix(), "blob_sha":v2.tree_blob(root, symlink_head2, symlink_report.relative_to(root).as_posix())}
        record(names[8], lambda: _expect_errors(verify_test_report(root, symlink_head2, "D11", fixtures[("D11", "valid")][0], symlink_rep_ref), "regular tracked file"))

        def mismatched_runner_rejected() -> None:
            path = root / f"{DELIVERABLES}/WRONG_RUNNER_REPORT.json"
            report = json.loads((root / fixtures[("D11", "valid")][1]["path"]).read_text(encoding="utf-8"))
            report["catalog_ref"] = fixtures[("D11", "valid")][0]
            report["runner_ref"] = {"path":f"{DELIVERABLES}/MISSING_RUNNER.py", "blob_sha":"0" * 40}
            path.write_text(json.dumps(report, sort_keys=True) + "\n", encoding="utf-8")
            local_head = _fixture_commit(root, "runner mismatch fixture")
            report_ref = {"path":path.relative_to(root).as_posix(), "blob_sha":v2.blob_sha(path.read_bytes())}
            _expect_errors(verify_test_report(root, local_head, "D11", fixtures[("D11", "valid")][0], report_ref), "runner")
        record(names[9], mismatched_runner_rejected)

    catalog_file = BASE / "D10_PHASE_BINDING_TESTS_V003.json"
    try:
        catalog = json.loads(catalog_file.read_text(encoding="utf-8"))
        expected = [case["id"] for case in catalog["test_cases"]]
        aligned = expected == names
    except (OSError, KeyError, json.JSONDecodeError):
        expected, aligned = [], False
    for name in names:
        print(f"{name}: {results[name]}" + (f" ({details[name]})" if details[name] else ""))
    if not aligned:
        print("CATALOG ALIGNMENT: FAIL")
    passed = sum(value == "PASS" for value in results.values())
    print(f"RESULT {passed}/{len(names)}; gate={'PASS_WITH_UNKNOWN' if passed == len(names) and aligned else 'FAIL'}")
    if report_path:
        catalog_raw = catalog_file.read_bytes() if catalog_file.exists() else b""
        runner_raw = Path(__file__).read_bytes()
        report = {"phase":"D10","status":"PASS" if passed == len(names) and aligned else "FAIL",
                  "catalog_ref":{"path":f"{DELIVERABLES}/D10_PHASE_BINDING_TESTS_V003.json","blob_sha":v2.blob_sha(catalog_raw)},
                  "runner_ref":{"path":f"{DELIVERABLES}/D10_VALIDATE_V003.py","blob_sha":v2.blob_sha(runner_raw)},
                  "execution_mode":"EXECUTED","passed":passed,"total":len(names),"catalog_matches_runner":aligned,
                  "tests":[{"id":name,"result":results[name],"detail":details[name]} for name in names]}
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if passed == len(names) and aligned else 1


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
        errors = validate_phase_envelope_v3(json.loads(args.envelope.read_text()), args.repo_root,
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

#!/usr/bin/env python3
"""Validate the current CHR-001 authoring package without exposing hidden text."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
BASE = ROOT / "novydres/runtime/narrative-architecture/program/deliverables"
FILES = {
    "d04": "D04_PLOT_ADMISSIONS_V010.json",
    "d05": "D05_PLAYER_APPROVAL_QUEUE_V013.json",
    "d06": "D06_CHRONICLE_BIBLE_V021.json",
    "d06_baseline": "D06_CHRONICLE_BIBLE_V020.json",
    "d06_baseline_safe": "D06_CHRONICLE_BIBLE_V020_PLAYER_SAFE.md",
    "d07_predecessor": "D07_STORY_TRUTH_PACKAGE_V013_GM_HIDDEN.md",
    "d08_predecessor": "D08_STORY_PREPARATION_V013_GM_HIDDEN.md",
    "d06_safe": "D06_CHRONICLE_BIBLE_V021_PLAYER_SAFE.md",
    "d07": "D07_STORY_TRUTH_PACKAGE_V014_GM_HIDDEN.md",
    "d08": "D08_STORY_PREPARATION_V014_GM_HIDDEN.md",
    "d09": "D09_GUIDED_CREATION_PROGRESSION_V016_PLAYER_SAFE.json",
    "registry": "D10_SCHEMA_REGISTRY_V016.json",
    "adapters": "D10_ROLE_ADAPTERS_V011.json",
    "cases": "D11_ADVERSARIAL_CASES_V014_GM_HIDDEN.json",
    "runner": "D11_EXECUTE_ADVERSARIAL_V014.py",
    "d11_result": "D11_TEST_RESULTS_V014_PLAYER_SAFE.json",
    "review": "D11_INDEPENDENT_REVIEW_V009_GM_HIDDEN.json",
    "review_status": "D11_REVIEW_STATUS_V010_PLAYER_SAFE.json",
    "source_result": "D06_SOURCE_VALIDATION_RESULT_V001_PLAYER_SAFE.json",
    "source_runner": "D06_SOURCE_VALIDATE_V003.py",
    "decision": "../decisions/PLAYER_DECISION_AGENT_ACCESS_V003.json",
}
checks = []
def check(code, ok):
    checks.append((code, bool(ok)))
def path(key):
    return (BASE / FILES[key]).resolve()
def read_json(key):
    try:
        return json.loads(path(key).read_text(encoding="utf-8"))
    except Exception:
        return None
def blob(p):
    raw = p.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
def walk_refs(value):
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and isinstance(value.get("blob_sha"), str):
            yield value
        for child in value.values():
            yield from walk_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_refs(child)
def pinned(doc, target):
    target_path = str(target.relative_to(ROOT))
    matching = [r for r in walk_refs(doc) if r["path"] == target_path]
    return len(matching) == 1 and matching[0]["blob_sha"] == blob(target)
def walk_dicts(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_dicts(child)
def walk_strings(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from walk_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_strings(child)
    elif isinstance(value, str):
        yield value

# All current inputs and contracts must exist and parse.
loaded = {k: read_json(k) for k in ("d04", "d05", "d06", "d09", "registry", "adapters", "cases", "d11_result", "review", "review_status", "source_result")}
check("D10-01", all(v is not None for v in loaded.values()))
check("D10-02", all(path(k).is_file() for k in FILES))

# Crosswalk anchors are real, and all planned story units appear in both story contracts.
d04, d06 = loaded["d04"], loaded["d06"]
fragments = set()
for obj in walk_dicts(d04):
    ref = obj.get("contract_ref")
    if isinstance(ref, str) and "#" in ref:
        fragments.add(ref.split("#", 1)[1])
anchors = set(re.findall(r'<a\s+id="([^"]+)"\s*>\s*</a>', path("d07").read_text(encoding="utf-8")))
check("D10-03", len(fragments) == 6 and fragments <= anchors)
units = d06.get("story_units", []) if isinstance(d06, dict) else []
ids = [u.get("id") for u in units if isinstance(u, dict)]
d07_text = path("d07").read_text(encoding="utf-8")
d08_text = path("d08").read_text(encoding="utf-8")
check("D10-04", len(units) == 12 and len(set(ids)) == 12 and all(isinstance(i, str) and i in d07_text and i in d08_text for i in ids))

# Every dependency pin resolves to the exact current blob.
d04_path, d05_path, d06_path = path("d04"), path("d05"), path("d06")
d07_path, d08_path, d09_path = path("d07"), path("d08"), path("d09")
check("D10-05", "D04_PLOT_ADMISSIONS_V010.json" in d07_text and f"Git blob `{blob(d04_path)}`" in d07_text)
d06_v020 = BASE / "D06_CHRONICLE_BIBLE_V020.json"
check("D10-06", d06_v020.is_file() and f"D06_CHRONICLE_BIBLE_V020.json, Git blob `{blob(d06_v020)}`" in d07_text)
check("D10-25", f"D07_STORY_TRUTH_PACKAGE_V014_GM_HIDDEN.md`, Git blob `{blob(d07_path)}`" in d08_text)
check("D10-26", all(pinned(d06, p) for p in (d04_path, d07_path, d08_path)))
check("D10-28", "D06_CHRONICLE_BIBLE_V020.json" in d07_text and path("d07_predecessor").is_file() and path("d08_predecessor").is_file())
check("D10-07", all(pinned(loaded["d09"], p) for p in (d04_path, d06_path, d07_path, d08_path, d05_path)))
check("D10-08", all(pinned(loaded["cases"], p) for p in (d04_path, d06_path, d07_path, d08_path, d09_path)))
check("D10-09", pinned(loaded["d05"], path("decision")))

# Current source and adversarial runs are reproducible records, not scene executions.
source = loaded["source_result"] or {}
adv = loaded["d11_result"] or {}
check("D10-10", source.get("status") == "PASS" and source.get("checks_passed") == 33 and source.get("checks_total") == 33)
check("D10-11", adv.get("status") == "PASS" and adv.get("cases_total") == 29 and adv.get("passed") == 29 and adv.get("failed") == 0)
check("D10-12", adv.get("scenes_played") == 0 and adv.get("dice_simulated") is False and adv.get("persistent_state_mutated") is False)
case_bytes = path("cases").read_bytes()
case_blob = hashlib.sha1(b"blob " + str(len(case_bytes)).encode() + b"\0" + case_bytes).hexdigest()
runner_sha256 = hashlib.sha256(path("runner").read_bytes()).hexdigest()
check("D10-27", adv.get("input_artifact_refs") == [{"path": str(path("cases").relative_to(ROOT)), "blob_sha": case_blob}] and adv.get("runner_source_sha256") == runner_sha256)
review_status_value = (loaded["review_status"] or {}).get("status")
review_value = (loaded["review"] or {}).get("status")
check("D10-13", review_status_value in {"PASS", "PASS_WITH_LIMITATION"} and review_value in {"PASS", "PASS_WITH_LIMITATION"})
reviewed = {item.get("path"): item.get("blob_sha") for item in (loaded["review"] or {}).get("reviewed_artifact_refs", []) if isinstance(item, dict)}
check("D10-14", all(reviewed.get(str(p.relative_to(ROOT))) == blob(p) for p in (d04_path, d05_path, d06_path, d07_path, d08_path, d09_path, path("cases"))))

# Role adapters enforce all four distinct knowledge ledgers and current agent access.
adapters = loaded["adapters"] or {}
ledgers = adapters.get("knowledge_ledgers", {})
roles = adapters.get("roles", {})
check("D10-15", set(ledgers) == {"AGENT_KNOWLEDGE", "PLAYER_KNOWLEDGE", "PC_KNOWLEDGE", "NPC_KNOWLEDGE"})
check("D10-16", all(isinstance(roles.get(r), dict) for r in ("DRAMATURGO", "NARRATOR", "PLAYER", "CHARACTER", "NPC")))
check("D10-17", all(isinstance(roles.get(r, {}).get(k), list) and roles[r][k] for r, k in (("DRAMATURGO", "must_not"), ("PLAYER", "must_not_receive"), ("NPC", "must"))))

# The safe summary carries no hidden story headings and preserves the known checkpoint.
safe_text = path("d06_safe").read_text(encoding="utf-8")
hidden_headings = [ln.lstrip("# ").strip() for ln in d07_text.splitlines() if ln.startswith("### ")]
check("D10-18", "C05" in safe_text and "C06" in safe_text and "mortal" in safe_text.lower() and "não foi Abraçado" in safe_text)
check("D10-19", all(h not in safe_text for h in hidden_headings if len(h) >= 28))

# Scene, narrator, D07 activation, and persistence gates stay closed.
readiness = d06.get("readiness", {}) if isinstance(d06, dict) else {}
checkpoint = d06.get("checkpoint", {}) if isinstance(d06, dict) else {}
check("D10-20", readiness.get("SCENE_READY") is False and readiness.get("NARRATOR_PERMISSION") is False and readiness.get("D07_activation", "").startswith("NOT_GRANTED"))
check("D10-21", checkpoint.get("last_played") == "C05" and checkpoint.get("next_scene") == "C06 not started" and checkpoint.get("bartolomeu") == "mortal" and checkpoint.get("embrace_recorded") is False)

# Registry/adapters point to this executable contract and preserve an auditable predecessor.
registry = loaded["registry"] or {}
check("D10-22", registry.get("version") == "V016" and registry.get("runner", "").endswith(FILES["registry"].replace("D10_SCHEMA_REGISTRY_V016.json", "D10_VALIDATE_V016.py")) and registry.get("test_report", "").endswith("D10_TEST_RESULTS_V016.json"))
check("D10-23", loaded["adapters"].get("version") == "V011" and pinned(adapters, path("registry")))
check("D10-24", len(registry.get("required_story_contract", [])) == 12 and len(registry.get("knowledge_levels", [])) == 4)

passed = sum(ok for _, ok in checks)
failed = [code for code, ok in checks if not ok]
result = {
    "validator": "D10_VALIDATE_V016.py",
    "version": "V016",
    "status": "PASS" if not failed else "FAIL",
    "checks_passed": passed,
    "checks_total": len(checks),
    "failed_check_ids": failed,
    "source_validation": {"status": source.get("status"), "checks_passed": source.get("checks_passed"), "checks_total": source.get("checks_total")},
    "adversarial_case_count": adv.get("cases_total"),
    "independent_review": (loaded["review_status"] or {}).get("status"),
    "operational_state": "C05 closed; C06 unstarted; mortal; no Embrace; no persistent state change.",
    "scene_ready": readiness.get("SCENE_READY"),
    "narrator_permission": readiness.get("NARRATOR_PERMISSION"),
    "D07_activation": "NOT_GRANTED",
    "result_detail_disclosed": False,
}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if not failed else 1)

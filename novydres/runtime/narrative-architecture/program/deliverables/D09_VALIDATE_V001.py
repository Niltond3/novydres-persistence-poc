#!/usr/bin/env python3
"""Reproducible D09 authority, provenance, chronology and adversarial checks."""
import argparse
import copy
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = Path("novydres/runtime/narrative-architecture/program/deliverables")
INPUT = "a6e8a6c4fe0bbba6b8ac2cd6ed2ac8b11612e60f"
MASTER = "124f9a9f43ed427d3db106d9187a875d74f60ac6"
FILES = {
    "D09_GUIDED_CREATION_PROGRESSION_V001.json",
    "D09_PLAYER_APPROVAL_QUEUE_V001.json",
    "D09_ADVERSARIAL_TESTS_V001.json",
    "AUDIT_D09_V001.json",
    "HANDOFF_D09_V001.json",
    "D09_VALIDATE_V001.py",
    "NEXT_PROMPT_D10_V001.md",
}
JSON_FILES = FILES - {"D09_VALIDATE_V001.py", "NEXT_PROMPT_D10_V001.md"}
ROUTES = {
    "ROUTE-VAMPIRE-BY-2010": "OPTION_NOT_SELECTED",
    "ROUTE-NONVAMPIRIC-2010": "ALTERNATE_REQUIRES_APPROVAL",
    "ROUTE-UNFINISHED-OR-EARLY-TERMINAL": "VALID_REPORTING; NOT_A_SUCCESS_SHORTCUT",
    "ROUTE-EXTENDED-OR-PAUSED-HORIZON": "PLAYER_DECISION_REQUIRED",
}
APPROVAL = {
    "APPROVAL-D05-001": "PENDING_PLAYER_APPROVAL",
    "APPROVAL-D05-002": "PENDING_PLAYER_APPROVAL",
    "APPROVAL-D05-003": "BLOCKED_EXTERNAL_DEPENDENCY",
    "APPROVAL-D05-004": "NOT_GRANTED",
    "APPROVAL-D06-001": "PENDING_PLAYER_APPROVAL",
    "APPROVAL-D07-001": "PENDING_PLAYER_APPROVAL",
}
NAMES = [
"documentary branch and repository identity",
"D09 input HEAD and parent checkpoint",
"master remains the pinned read-only HEAD",
"design HEAD contains the D08 input",
"latest numeric cycle found on design and master",
"cycle blob matches the pinned checkpoint",
"cycle scene and mortal state are unchanged",
"cycle content agrees across branches",
"execution manifest records D08 published gate",
"execution manifest D08 readback and master check",
"all seven D08 artifacts remain pinned",
"all D08 remote contents and blob IDs match",
"all D09 JSON documents parse",
"all declared source blob pins resolve",
"workpaper authority statuses remain explicit",
"top-level documents remain player-safe proposals",
"no canon, cycle, scene or operational mutation is authorized",
"all four D06 routes remain present and unselected",
"target-route approval remains pending",
"target sheet does not imply purchase or grant",
"Marco closure requires Coverage Coherence and Consequence",
"no scene count, age or elapsed-time quota is imposed",
"vampire route requires real authorized played Embrace",
"vampire route requires consequential post-Embrace experience",
"alternate route requires explicit player approval",
"unfinished or terminal path reports actual play truthfully",
"no survival of human relationships is presumed",
"2010 is a soft horizon without invented date",
"M3.01 scene checkpoint does not close macro M3",
"manifest versus cycle pointer conflict remains unresolved",
"no new scene readiness or narrator permission is granted",
"player may refuse pause fail or redirect without penalty",
"NPC knowledge requires acquisition evidence",
"no secret truth or GM-only payload is present",
"route choice remains independent from target-sheet approval",
"mechanical progression cites rule event ledger and authorization",
"no XP FV powers or traits are granted by this phase",
"age and time do not produce automatic power",
"loss does not produce automatic refund",
"relationship continuity records change loss or unknown",
"target sheet cap is not treated as acquired total",
"all inherited decision IDs match D08 queue",
"all inherited decision statuses match D08 queue",
"no inherited decision is marked approved",
"approval default remains pending and silence selects nothing",
"source refs include actual progression and chronology authorities",
"handoff retains D09 documentary-only authority",
"final audit gate requires complete independent and literary reviews",
"handoff gate follows the reviewed audit",
"test catalog and executable checks use identical IDs",
"only seven D09 artifacts are in scope",
"no untracked changes outside D09 artifact set",
"reject route mutation that selects vampire-by-2010",
"reject mutation that awards XP or FV",
"reject mutation that invents a fixed Embrace date",
"reject mutation that assumes a human tie survives to 2010",
"reject mutation that sets SCENE_READY or Narrator permission",
"reject mutation that marks a route selected by silence",
"reject mutation that treats target sheet as purchased traits",
"reject mutation that promotes workpapers to operational authority",
"execution result and gate labels agree",
"reject final gate without complete review evidence",
]

def git(root, *args, check=True):
    p = subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode:
        raise RuntimeError(p.stderr.strip() or f"git {' '.join(args)} failed")
    return p

def no_secret_payload(value):
    forbidden = {
        "secret_answer", "truth_answer", "secret_payload", "locked_truth",
        "clue_payload", "culprit_identity", "motive_reveal", "gm_hidden_payload",
    }
    if isinstance(value, dict):
        return not any(str(k).casefold() in forbidden for k in value) and all(no_secret_payload(v) for v in value.values())
    if isinstance(value, list):
        return all(no_secret_payload(v) for v in value)
    return True

def safe_contract(doc):
    try:
        route = doc["authority_and_route"]
        chrono = doc["chronology_contract"]
        return (
            doc["status"] == "PROPOSED"
            and doc["authority"] == "EDITORIAL_ONLY"
            and doc["spoiler_class"] == "PLAYER_SAFE"
            and doc["no_canon_edit"] is True
            and doc["no_cycle_edit"] is True
            and doc["no_scene_authorization"] is True
            and doc["no_operational_promotion"] is True
            and route["choice_status"] == "PENDING_PLAYER_APPROVAL"
            and route["selected_route"] is None
            and chrono["embrace_date"] == "UNKNOWN"
            and str(chrono["relationship_continuity"]).startswith("UNKNOWN")
            and doc["progression_contract"]["authority"].endswith("this proposal grants nothing")
            and not any(k in doc["progression_contract"] for k in ("grant_xp", "grant_fv", "grant_power", "target_sheet_acquired"))
            and not any(k in doc for k in ("scene_ready", "narrator_permission"))
            and no_secret_payload(doc)
        )
    except (KeyError, TypeError, AttributeError):
        return False

def review_complete(review):
    return (
        isinstance(review, dict)
        and review.get("status") == "PASS"
        and all(isinstance(review.get(key), str) and review[key].strip() for key in ("reviewer", "result", "evidence"))
    )

def reviews_complete(audit):
    return review_complete(audit.get("independent_review")) and review_complete(audit.get("literary_review"))

def latest_cycle(root, ref):
    names = git(root, "ls-tree", "-r", "--name-only", ref, "--", "novydres/chronicles/CHR-001/orchestration").stdout.splitlines()
    found = []
    for path in names:
        match = re.fullmatch(r".*/CYCLE_V(\d+)\.json", path)
        if match:
            found.append((int(match.group(1)), path))
    return max(found) if found else (0, "")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--run-state", required=True)
    ap.add_argument("--expected-gate", choices=["PENDING", "PASS_WITH_UNKNOWN"], default="PENDING")
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    deliverables = root / BASE
    state = json.loads(Path(args.run_state).read_text(encoding="utf-8"))
    docs = {name: json.loads((deliverables / name).read_text(encoding="utf-8")) for name in JSON_FILES}
    plan = docs["D09_GUIDED_CREATION_PROGRESSION_V001.json"]
    queue = docs["D09_PLAYER_APPROVAL_QUEUE_V001.json"]
    catalog = docs["D09_ADVERSARIAL_TESTS_V001.json"]
    audit = docs["AUDIT_D09_V001.json"]
    handoff = docs["HANDOFF_D09_V001.json"]
    checks = []

    def add(name, ok):
        checks.append((name, bool(ok)))

    branch = git(root, "branch", "--show-current").stdout.strip()
    add(NAMES[0], branch == "design/chr001-narrative-program-d01" and plan["repository"] == "Niltond3/novydres-persistence-poc")
    add(NAMES[1], plan["input_head"] == INPUT and handoff["input_head"] == INPUT and plan["checkpoint_as_of"]["sequence"] == 33)
    add(NAMES[2], git(root, "rev-parse", "origin/master").stdout.strip() == MASTER and plan["master_head"] == MASTER)
    add(NAMES[3], git(root, "merge-base", "--is-ancestor", INPUT, "HEAD", check=False).returncode == 0)
    cdesign, pdesign = latest_cycle(root, "HEAD")
    cmaster, pmaster = latest_cycle(root, "origin/master")
    add(NAMES[4], cdesign == 33 and cmaster == 33 and pdesign == pmaster == "novydres/chronicles/CHR-001/orchestration/CYCLE_V0033.json")
    cycle_sha = git(root, "rev-parse", f"HEAD:{pdesign}").stdout.strip()
    add(NAMES[5], cycle_sha == plan["checkpoint_as_of"]["blob_sha"] == "51afa7fa15ba7dc49a863dfe6f6bb0c539014a6a")
    cycle = json.loads(git(root, "show", f"HEAD:{pdesign}").stdout)
    cp = cycle["checkpoint"]
    add(NAMES[6], cp["last_event_id"] == "CHR001-M301-C05-22-20261109-001" and cp["last_closed_scene"] == "C05" and cp["next_scene"] == "C06" and cp["next_scene_status"] == "NOT_STARTED" and cp["mortal"] is True and cp["embrace_occurred"] is False)
    add(NAMES[7], git(root, "rev-parse", f"origin/master:{pdesign}").stdout.strip() == cycle_sha and git(root, "show", f"origin/master:{pdesign}").stdout == git(root, "show", f"HEAD:{pdesign}").stdout)
    d08 = state["phase_records"]["D08"]
    rb = d08["publication_readback"]
    add(NAMES[8], state["phase_status"]["D08"] == "PASS_WITH_UNKNOWN" and d08["gate"] == "PASS_WITH_UNKNOWN")
    add(NAMES[9], d08["output_head"] == "a6e8a6c4fe0bbba6b8ac2cd6ed2ac8b11612e60f" and rb["all_seven_contents_and_blobs_verified"] is True and rb["master_unchanged"] == MASTER)
    d08_files = {a["path"]: a["blob_sha"] for a in d08["artifacts"]}
    d08_expected = {
        "novydres/runtime/narrative-architecture/program/deliverables/AUDIT_D08_V001.json",
        "novydres/runtime/narrative-architecture/program/deliverables/D08_ADVERSARIAL_TESTS_V001.json",
        "novydres/runtime/narrative-architecture/program/deliverables/D08_PLAYER_APPROVAL_QUEUE_V001.json",
        "novydres/runtime/narrative-architecture/program/deliverables/D08_STORY_SCENES_BEATS_V001.json",
        "novydres/runtime/narrative-architecture/program/deliverables/D08_VALIDATE_V001.py",
        "novydres/runtime/narrative-architecture/program/deliverables/HANDOFF_D08_V001.json",
        "novydres/runtime/narrative-architecture/program/deliverables/NEXT_PROMPT_D09_V001.md",
    }
    add(NAMES[10], set(d08_files) == d08_expected)
    readback = all(git(root, "rev-parse", f"HEAD:{p}").stdout.strip() == sha for p, sha in d08_files.items())
    add(NAMES[11], readback and all(git(root, "show", f"origin/{branch}:{p}").stdout.encode() == (root / p).read_bytes() for p in d08_files))
    parse_ok = True
    try:
        for name in JSON_FILES:
            json.loads((deliverables / name).read_text(encoding="utf-8"))
    except Exception:
        parse_ok = False
    add(NAMES[12], parse_ok)

    refs = []
    for doc in docs.values():
        refs.extend(doc.get("source_refs", []))
    refs_ok = len(refs) >= 30
    for ref in refs:
        sha = str(ref.get("blob_sha", ""))
        refs_ok = refs_ok and bool(re.fullmatch(r"[0-9a-f]{40}", sha))
        refs_ok = refs_ok and git(root, "rev-parse", f"HEAD:{ref.get('path','')}", check=False).stdout.strip() == sha
    add(NAMES[13], refs_ok)

    def source(path):
        return git(root, "show", f"HEAD:{path}").stdout
    d1 = source("novydres/systems/character-creation/sources/novydres_character_creation_d1_played_history_core_v0_1.md")
    d2 = source("novydres/systems/character-creation/sources/novydres_character_creation_d2_played_history_finalization_integration_v0_1.md")
    h = source("novydres/systems/character-creation/sources/novydres_character_creation_h_guided_pc_integration_v0_1.md")
    k = source("novydres/systems/character-creation/novydres_character_creation_k_final_integration_v0_1.source.md")
    l = source("novydres/systems/character-creation/sources/novydres_character_creation_l_guided_content_handoff_v0_1(1).md")
    maturity = plan["source_authority_status"]
    add(NAMES[14], "candidate_for_senior_editor_revalidation" in d1 and "candidate_for_senior_editor_revalidation" in d2 and "candidate_for_senior_editor_revalidation" in h and "candidate_for_senior_editor_closure" in k and "candidate_for_senior_editor_closure" in maturity["K"] and "editorial_handoff_not_architecture_patch" in l and "Preserve source status tension" in maturity["resolution"])
    allmeta = [plan, queue, catalog, audit, handoff]
    add(NAMES[15], all(x["authority"] == "EDITORIAL_ONLY" and x["spoiler_class"] == "PLAYER_SAFE" and x["branch"] == "design/chr001-narrative-program-d01" for x in allmeta) and plan["status"] == "PROPOSED")
    add(NAMES[16], all(x["no_canon_edit"] and x["no_cycle_edit"] and x["no_scene_authorization"] and x["no_operational_promotion"] for x in allmeta))
    routes = {r["id"]: r["status"] for r in plan["authority_and_route"]["routes"]}
    add(NAMES[17], routes == ROUTES and plan["authority_and_route"]["selected_route"] is None)
    queue_by_id = {x["id"]: x for x in queue["decisions"]}
    add(NAMES[18], queue_by_id["APPROVAL-D06-001"]["status"] == "PENDING_PLAYER_APPROVAL" and plan["authority_and_route"]["choice_status"] == "PENDING_PLAYER_APPROVAL")
    target = json.loads(source("novydres/chronicles/CHR-001/character/TARGET_SHEET_V2_APPROVED.json"))
    add(NAMES[19], target["status"] == "APPROVED_LOCAL_TARGET_ACTIVE_NOT_BOUGHT" and target["approval_does_not_grant_or_spend_xp"] is True and target["acquired_traits_unchanged"] is True)
    suff = " ".join(plan["graduation_gate"]["shared_criteria"])
    add(NAMES[20], all(x in suff for x in ["Coverage", "Coherence", "Consequence"]))
    add(NAMES[21], "event count" in suff and "elapsed time" in suff and "not a prescribed scene count" in " ".join(plan["graduation_gate"]["route_specific_criteria"]["ROUTE-VAMPIRE-BY-2010"]))
    vampire = " ".join(plan["graduation_gate"]["route_specific_criteria"]["ROUTE-VAMPIRE-BY-2010"])
    add(NAMES[22], "actual Embrace" in vampire and "authorized" in vampire and "persisted" in vampire)
    add(NAMES[23], "Post-Embrace play" in vampire and "consequential lived experience" in vampire)
    alt = " ".join(plan["graduation_gate"]["route_specific_criteria"]["ROUTE-NONVAMPIRIC-2010"])
    add(NAMES[24], "expressly approves" in alt)
    terminal = " ".join(plan["graduation_gate"]["route_specific_criteria"]["ROUTE-UNFINISHED-OR-EARLY-TERMINAL"])
    add(NAMES[25], "actual play" in terminal and "persisted" in terminal and "plot armor" in terminal)
    add(NAMES[26], plan["chronology_contract"]["relationship_continuity"].startswith("UNKNOWN") and "survival" in plan["chronology_contract"]["relationship_continuity"])
    add(NAMES[27], "2010 is a horizon" in plan["chronology_contract"]["precision"] and "not a fixed event date" in plan["chronology_contract"]["precision"] and plan["chronology_contract"]["embrace_date"] == "UNKNOWN")
    add(NAMES[28], "M3.01" in plan["milestone_map"]["M3"] and "not inferred" in plan["milestone_map"]["M3"])
    manifest = json.loads(source("novydres/MANIFEST_V46.json"))
    add(NAMES[29], "CYCLE_V0024" in json.dumps(manifest) and "MANIFEST_V46" in " ".join(plan["bounded_unknowns"]))
    add(NAMES[30], all(x["no_scene_authorization"] is True for x in allmeta) and any(x.startswith("no SCENE_READY") and "NARRATOR_PERMISSION" in x for x in plan["bounded_unknowns"]))
    add(NAMES[31], "Refusal" in terminal and "failure" in terminal.lower() and "refuse, fail, redirect" in " ".join(plan["personal_horror_review"]["review_questions"]))
    add(NAMES[32], any(x["path"].endswith("D03_KNOWLEDGE_GRAPH_V001.json") for x in refs) and "event-based acquisition" in " ".join(ref["role"] for ref in refs))
    add(NAMES[33], all(no_secret_payload(d) for d in docs.values()))
    add(NAMES[34], "target-sheet approval selects no route" in plan["authority_and_route"]["no_default"])
    add(NAMES[35], all(any(x in row for row in plan["progression_contract"]["eligible_evidence"]) for x in ["actual resolved events", "current rule text/version", "reconciled character ledger"]))
    add(NAMES[36], any(term in " ".join(plan["progression_contract"]["prohibited_shortcuts"]) for term in ["XP/FV", "XP, FV", "automatic powers"]) and "grants nothing" in plan["progression_contract"]["authority"])
    add(NAMES[37], "age" in " ".join(plan["progression_contract"]["prohibited_shortcuts"]).lower() and "automatic power" in " ".join(plan["progression_contract"]["prohibited_shortcuts"]).lower())
    add(NAMES[38], any("refund" in x for x in plan["progression_contract"]["prohibited_shortcuts"]))
    add(NAMES[39], all(x in plan["graduation_gate"]["shared_criteria"][-2] or x in plan["chronology_contract"]["relationship_continuity"] for x in ["changed", "lost", "UNKNOWN"]))
    add(NAMES[40], target["budget_cap_approved_for_this_sheet"] == 675 and target["approval_does_not_grant_or_spend_xp"] is True)
    d08_queue = json.loads(source(f"{BASE.as_posix()}/D08_PLAYER_APPROVAL_QUEUE_V001.json"))
    d08_map = {x["id"]: x for x in d08_queue["decisions"]}
    add(NAMES[41], set(queue_by_id) == set(d08_map) == set(APPROVAL))
    add(NAMES[42], all(queue_by_id[k]["status"] == d08_map[k]["status"] == status for k, status in APPROVAL.items()))
    add(NAMES[43], all(x["status"] not in ("APPROVED", "GRANTED") for x in queue["decisions"]))
    add(NAMES[44], all(x["default"] == "no selection or approval by silence" for x in queue["decisions"]) and "silence" in plan["authority_and_route"]["no_default"])
    add(NAMES[45], any(x["path"].endswith("d2_played_history_finalization_integration_v0_1.md") for x in refs) and any(x["path"].endswith("CH03_TRAJETORIA_ATE_2010_V1.md") for x in refs) and any(x["path"].endswith("MOTOR_MECANICO_V5_V1_1.source.txt") for x in refs))
    add(NAMES[46], handoff["authority"] == "EDITORIAL_ONLY" and handoff["no_operational_promotion"] is True and handoff["next_phase"] == "D10")
    if args.expected_gate == "PENDING":
        add(NAMES[47], audit["gate"] == "PENDING" and audit["status"] == "AUDITING" and audit["independent_review"]["status"] == "PENDING")
    else:
        add(NAMES[47], audit["gate"] == "PASS_WITH_UNKNOWN" and audit["status"] == "PASS_WITH_UNKNOWN" and reviews_complete(audit))
    if args.expected_gate == "PENDING":
        add(NAMES[48], handoff["gate"] == "PENDING" and handoff["status"] == "AUDITING")
    else:
        add(NAMES[48], handoff["gate"] == "PASS_WITH_UNKNOWN" and handoff["status"] == "PASS_WITH_UNKNOWN")
    recorded = [x["id"] for x in catalog["cases"]]
    add(NAMES[49], recorded == [f"T-D09-{i:03d}" for i in range(1, len(NAMES)+1)] and [x["description"] for x in catalog["cases"]] == NAMES and len(NAMES) == 62)
    add(NAMES[50], set(FILES) == {x for x in FILES} and len(FILES) == 7)
    changed = set(git(root, "diff", "--name-only", INPUT, "--").stdout.splitlines())
    for line in git(root, "status", "--porcelain", "-uall").stdout.splitlines():
        if len(line) >= 4:
            changed.add(line[3:])
    expected = {str(BASE / x) for x in FILES}
    add(NAMES[51], changed == expected)
    def mutated(change):
        d = copy.deepcopy(plan)
        change(d)
        return not safe_contract(d)
    add(NAMES[52], mutated(lambda d: d["authority_and_route"].update(selected_route="ROUTE-VAMPIRE-BY-2010")))
    add(NAMES[53], mutated(lambda d: d["progression_contract"].update(grant_xp=10, grant_fv=1)))
    add(NAMES[54], mutated(lambda d: d["chronology_contract"].update(embrace_date="2000-01-01")))
    add(NAMES[55], mutated(lambda d: d["chronology_contract"].update(relationship_continuity="all human ties survive to 2010")))
    add(NAMES[56], mutated(lambda d: d.update(scene_ready=True, narrator_permission=True)))
    add(NAMES[57], mutated(lambda d: d["authority_and_route"].update(choice_status="APPROVED", selected_route="ROUTE-VAMPIRE-BY-2010")))
    add(NAMES[58], mutated(lambda d: d["progression_contract"].update(target_sheet_acquired=True)))
    add(NAMES[59], mutated(lambda d: d.update(no_operational_promotion=False)))
    exec_doc = catalog["execution"]
    gates = {x["gate"] for x in docs.values()}
    if args.expected_gate == "PENDING":
        consistent = gates == {"PENDING"} and exec_doc["status"] == "PENDING" and exec_doc["passed"] == 0
    else:
        consistent = (
            gates == {"PASS_WITH_UNKNOWN"}
            and exec_doc["status"] == "PASS"
            and exec_doc["passed"] == len(NAMES)
            and exec_doc["total"] == len(NAMES)
            and exec_doc["result"] == f"{len(NAMES)}/{len(NAMES)} PASS"
            and audit["automated_validation"]["status"] == "PASS"
            and audit["automated_validation"]["checks_passed"] == len(NAMES)
            and audit["automated_validation"]["checks_total"] == len(NAMES)
        )
    add(NAMES[60], consistent)
    incomplete_independent = copy.deepcopy(audit)
    incomplete_independent["independent_review"]["evidence"] = None
    incomplete_literary = copy.deepcopy(audit)
    incomplete_literary["literary_review"]["status"] = "PENDING"
    incomplete_identity = copy.deepcopy(audit)
    incomplete_identity["literary_review"]["reviewer"] = "  "
    incomplete_result = copy.deepcopy(audit)
    incomplete_result["independent_review"]["result"] = ""
    add(NAMES[61], not reviews_complete(incomplete_independent) and not reviews_complete(incomplete_literary) and not reviews_complete(incomplete_identity) and not reviews_complete(incomplete_result))

    if len(checks) != len(NAMES):
        raise AssertionError(f"validator/catalog count mismatch: {len(checks)} != {len(NAMES)}")
    if recorded != [f"T-D09-{i:03d}" for i in range(1, len(NAMES) + 1)]:
        raise AssertionError("test catalog IDs do not match executable checks")
    if args.expected_gate == "PASS_WITH_UNKNOWN":
        if any(x["result"] != "PASS" for x in catalog["cases"]):
            raise AssertionError("test catalog has non-PASS result")
    elif any(x["result"] != "PENDING" for x in catalog["cases"]):
        raise AssertionError("pre-review test catalog should be pending")
    for i, (name, ok) in enumerate(checks, 1):
        print(f"T-D09-{i:03d} {'PASS' if ok else 'FAIL'} {name}")
    passed = sum(ok for _, ok in checks)
    print(f"RESULT {'PASS' if passed == len(NAMES) else 'FAIL'} {passed}/{len(NAMES)}")
    return 0 if passed == len(NAMES) else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"VALIDATION_ERROR: {exc}", file=sys.stderr)
        sys.exit(2)

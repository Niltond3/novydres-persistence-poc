#!/usr/bin/env python3
"""Reproducible D07 contract and source-integrity checks; standard library only."""
import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path

FILES = [
    "D07_PLOT_BIBLES_V001.json",
    "D07_TRUTH_LOCKS_V001.json",
    "D07_PLAYER_APPROVAL_QUEUE_V001.json",
    "D07_ADVERSARIAL_TESTS_V001.json",
    "AUDIT_D07_V001.json",
    "HANDOFF_D07_V001.json",
]
EXPECTED_EDGES = {
    "D04-EDGE-001", "D04-EDGE-002", "D04-EDGE-003", "D04-EDGE-004",
    "D04-EDGE-024", "D04-EDGE-025", "D04-EDGE-026", "D04-EDGE-027",
    "D04-EDGE-029", "D04-EDGE-030", "D04-EDGE-032",
}
FORBIDDEN_KEYS = {"answer", "truth_answer", "culprit", "suspect", "secret_payload", "clue_payload", "gm_hidden_value"}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def has_forbidden_payload(value):
    if isinstance(value, dict):
        return any(k.lower() in FORBIDDEN_KEYS or has_forbidden_payload(v) for k, v in value.items())
    if isinstance(value, list):
        return any(has_forbidden_payload(v) for v in value)
    return False


def safe_contract(bible):
    contracts = bible.get("contracts", [])
    if len(contracts) != 1 or contracts[0].get("plot_id") != "D04-PC01":
        return False
    c = contracts[0]
    if c.get("status") != "DRAFT" or c.get("proposal_status") != "CONDITIONAL_PROPOSED_EDITORIAL_ONLY":
        return False
    if c.get("D04_status") != "PROVISIONAL_PLOT_EDITORIAL_ONLY":
        return False
    projection = c.get("D01_plot_projection", {})
    if projection.get("status") != "DRAFT" or projection.get("spoiler_class") != "PLAYER_SAFE":
        return False
    if any(e.get("promotes_plot_or_cause") is not False for e in c.get("typed_links", {}).get("edges", [])):
        return False
    if c.get("participants_and_agency", {}).get("NPC_autonomy") != "ONLY_ARCHIVED_ACTIONS":
        return False
    if c.get("locked_mystery_dependency", {}).get("play_status") != "BLOCKED_FOR_TRUTH_DEPENDENT_INVESTIGATION":
        return False
    return not has_forbidden_payload(bible)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--expected-gate", choices=["PENDING", "PASS_WITH_UNKNOWN"], default="PENDING")
    args = parser.parse_args()
    repo_root = args.repo_root or Path(__file__).resolve().parents[4]
    artifact_dir = Path(__file__).resolve().parent
    data = {name: load_json(artifact_dir / name) for name in FILES}
    bible = data[FILES[0]]
    locks = data[FILES[1]]
    queue = data[FILES[2]]
    declared = data[FILES[3]]
    audit = data[FILES[4]]
    handoff = data[FILES[5]]
    c = bible["contracts"][0]
    checks = []

    def check(name, condition):
        checks.append((name, bool(condition)))

    current_branch = subprocess.check_output(["git", "-C", str(repo_root), "branch", "--show-current"], text=True).strip()
    check("repository_metadata_and_scope", bible["repository"] == "Niltond3/novydres-persistence-poc" and bible["branch"] == "design/chr001-narrative-program-d01" and current_branch == bible["branch"] and all(x["authority"] == "EDITORIAL_ONLY" for x in data.values()))
    check("all_json_documents_parse", len(data) == len(FILES))
    check("one_contract_only", len(bible.get("contracts", [])) == 1)
    check("PC01_is_only_admitted_plot", c.get("plot_id") == "D04-PC01")
    check("PC01_retains_provisional_editorial_status", c.get("D04_status") == "PROVISIONAL_PLOT_EDITORIAL_ONLY" and c.get("status") == "DRAFT" and c.get("proposal_status") == "CONDITIONAL_PROPOSED_EDITORIAL_ONLY")
    check("PC02_PC03_PC04_not_admitted", all(x.get("plot_id") not in {"D04-PC02", "D04-PC03", "D04-PC04"} for x in bible.get("contracts", [])))
    edges = c["typed_links"]["edges"]
    check("all_eleven_D04_links_present", {x["edge_id"] for x in edges} == EXPECTED_EDGES)
    d04_map_path = repo_root / "novydres/runtime/narrative-architecture/program/deliverables/D04_THREAD_TO_PLOT_MAP_V001.json"
    d04_map = load_json(d04_map_path)
    source_edges = {x["edge_id"]: x for x in d04_map["edges"] if x.get("plot_id") == "D04-PC01"}
    check("link_edge_ids_match_D04_map", all(x["edge_id"] in source_edges and x["thread_id"] == source_edges[x["edge_id"]]["thread_id"] for x in edges))
    check("typed_relation_classes_preserved", all(x["relation_kind"] == source_edges[x["edge_id"]]["relation_kind"] and x["epistemic_class"] == source_edges[x["edge_id"]]["epistemic_class"] for x in edges))
    check("edge_source_metadata_preserved", all(x.get("confidence") == source_edges[x["edge_id"]]["confidence"] and x.get("checkpoint") == source_edges[x["edge_id"]]["checkpoint"] and x.get("source") == source_edges[x["edge_id"]]["source"] for x in edges))
    schema_path = repo_root / "novydres/runtime/narrative-architecture/program/deliverables/D01_CONTRACTS_V001.json"
    plot_schema = load_json(schema_path)["$defs"]["plot"]
    projection = c["D01_plot_projection"]
    req = set(plot_schema["required"])
    props = set(plot_schema["properties"])
    outcomes_schema = load_json(schema_path)["$defs"]["outcome"]
    provenance_schema = load_json(schema_path)["$defs"]["provenance"]
    valid_projection = (req <= set(projection) <= props and projection["scope"] in plot_schema["properties"]["scope"]["enum"] and projection["status"] in plot_schema["properties"]["status"]["enum"] and projection["spoiler_class"] in plot_schema["properties"]["spoiler_class"]["enum"] and not projection["plot_links"] and all(set(outcomes_schema["required"]) <= set(o) and o["route"] in outcomes_schema["properties"]["route"]["enum"] for o in projection["outcomes"]) and set(provenance_schema["required"]) <= set(projection["provenance"]))
    check("D01_plot_projection_matches_contract_shape", valid_projection)
    check("no_link_claims_causality", all(x.get("promotes_plot_or_cause") is False for x in edges) and c["causality_contract"]["global_causal_edges"] == "NONE_ESTABLISHED")
    check("derived_archive_provenance_disclosed", c["historical_basis"]["authority"] == "CURRENT_DERIVED_ARCHIVE_NOT_ORIGINAL_AUTHENTICATED" and c["historical_basis"]["current_condition"] == "UNKNOWN_UNTIL_REVALIDATED")
    check("current_state_requires_revalidation", "latest cycle/manifest/event pointers reconciled under current protocol" in c["entry_conditions"]["future_scene_requires"])
    check("C06_not_started_and_no_scene_created", bible["checkpoint_as_of"]["C06"] == "NOT_STARTED" and bible["no_scene_authorization"] is True and c["entry_conditions"]["design_only"].startswith("No current scene"))
    check("opposition_motives_remain_unknown", c["participants_and_agency"]["opposition"] == "NONE_ESTABLISHED" and c["participants_and_agency"]["opposition_objectives"] == "UNKNOWN")
    check("no_future_NPC_autonomy_authorized", c["participants_and_agency"]["NPC_autonomy"] == "ONLY_ARCHIVED_ACTIONS")
    check("no_new_agents_created", c["participants_and_agency"]["new_agents"] == "NONE_CREATED")
    check("player_entry_is_optional", "não é obrigatório" in c["participants_and_agency"]["protagonist"])
    route_ids = {x["id"] for x in c["conditional_routes"]}
    check("refusal_suspension_abandonment_and_failure_supported", {"ROUTE-D07-PC01-DECLINE-SUSPEND-ABANDON", "ROUTE-D07-PC01-FAILURE"} <= route_ids)
    check("repair_and_release_are_conditional", c["conditional_routes"][0]["conditions"] and "not assumed" in c["conditional_routes"][0]["possible_disposition"])
    check("local_closure_requires_actual_evidence_and_persistence", {"actual evidence-backed assessment or choice", "cycle/ledger persistence and readback complete"} <= set(c["closure_contract"]["local_disposition_requires"]))
    check("full_thread_closure_not_claimed", c["closure_contract"]["full_thread_closure"].startswith("Not proposed"))
    check("report_authorship_answer_not_created", locks["locks"][0]["materialized_truth"] == "NOT_CREATED" and c["locked_mystery_dependency"]["thread_id"] == "m201-report-authorship")
    check("truth_dependent_play_blocked_without_segregation", locks["effective_gm_hidden_segregation"] is False and locks["locks"][0]["play_status"] == "BLOCKED_EXTERNAL_DEPENDENCY")
    check("no_secret_payload_fields_or_values", not has_forbidden_payload(bible) and not has_forbidden_payload(locks))
    approval_ids = {x["id"]: x for x in queue["decisions"]}
    check("all_pending_approvals_retained", {"APPROVAL-D05-001", "APPROVAL-D05-002", "APPROVAL-D05-003", "APPROVAL-D05-004", "APPROVAL-D06-001", "APPROVAL-D07-001"} <= set(approval_ids) and approval_ids["APPROVAL-D07-001"]["status"] == "PENDING_PLAYER_APPROVAL")
    check("no_operational_or_narrator_authority", bible["authority"] == "EDITORIAL_ONLY" and bible["no_scene_authorization"] is True and "APPROVAL-D05-004" in bible["pending_approvals"])
    head = subprocess.check_output(["git", "-C", str(repo_root), "rev-parse", "HEAD"], text=True).strip()
    master = subprocess.check_output(["git", "-C", str(repo_root), "rev-parse", "origin/master"], text=True).strip()
    input_is_ancestor = subprocess.run(["git", "-C", str(repo_root), "merge-base", "--is-ancestor", bible["input_head"], head], check=False).returncode == 0
    check("cycle_and_master_refs_exact", bible["checkpoint_as_of"]["sequence"] == 33 and bible["master_head"] == "124f9a9f43ed427d3db106d9187a875d74f60ac6" and master == bible["master_head"] and input_is_ancestor)
    verified = True
    for document in data.values():
        for src in document.get("source_refs", []):
            path = repo_root / src["path"]
            if not path.is_file():
                verified = False
                break
            content = path.read_bytes()
            actual = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
            if actual != src["blob_sha"]:
                verified = False
                break
        if not verified:
            break
    check("all_source_blob_hashes_verified", verified)
    expected_gates = {bible["gate"], locks["gate"], queue["gate"], audit["gate"], handoff["gate"]}
    if args.expected_gate == "PENDING":
        aligned = expected_gates == {"PENDING"} and handoff["status"] == "PROPOSED" and audit["independent_review"]["status"] in {"PENDING", "PASS"} and audit["automated_validation"]["status"] in {"PENDING", "PASS"}
    else:
        aligned = expected_gates == {"PASS_WITH_UNKNOWN"} and audit["independent_review"]["status"] == "PASS" and audit["automated_validation"]["status"] == "PASS" and handoff["status"] == "PASS_WITH_UNKNOWN"
    check("all_gate_fields_aligned", aligned)
    check("adversarial_answer_injection_rejected", not safe_contract({**bible, "contracts": [{**copy.deepcopy(c), "truth_answer": "injected"}]}))
    mutated = copy.deepcopy(bible); mutated["contracts"][0]["typed_links"]["edges"][0]["promotes_plot_or_cause"] = True
    check("adversarial_causal_edge_rejected", not safe_contract(mutated))
    mutated = copy.deepcopy(bible); mutated["contracts"][0]["status"] = "OPERATIONAL"
    check("adversarial_promotion_rejected", not safe_contract(mutated))
    mutated = copy.deepcopy(bible); mutated["contracts"][0]["participants_and_agency"]["NPC_autonomy"] = "AUTONOMOUS"
    check("adversarial_NPC_knowledge_rejected", not safe_contract(mutated))
    mutated = copy.deepcopy(locks); mutated["secret_payload"] = "injected"
    check("adversarial_secret_payload_rejected", not safe_contract({**bible, "secret_payload": "injected"}))
    mutated = copy.deepcopy(bible); mutated["contracts"].append({"plot_id": "D04-PC02"})
    check("adversarial_candidate_fusion_rejected", not safe_contract(mutated))
    declared_names = [x["name"] for x in declared["checks"]]
    actual_names = [name for name, _ in checks]
    expected_names = set(actual_names) | {"declared_test_catalog_matches_runner"}
    check("declared_test_catalog_matches_runner", declared["test_count"] == len(declared_names) == len(expected_names) and set(declared_names) == expected_names)
    failed = [name for name, passed in checks if not passed]
    for index, (name, passed) in enumerate(checks, 1):
        print(f"T-D07-{index:03} {'PASS' if passed else 'FAIL'} {name}")
    print(f"RESULT {'PASS' if not failed else 'FAIL'} {len(checks)-len(failed)}/{len(checks)}")
    if failed:
        raise SystemExit(1)

if __name__ == "__main__":
    main()

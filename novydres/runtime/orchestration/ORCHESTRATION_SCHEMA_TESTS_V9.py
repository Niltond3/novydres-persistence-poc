#!/usr/bin/env python3
"""Synthetic schema coverage for V9; creates no cycle, event, or player decision."""
import copy
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
ORCH = ROOT / "novydres/runtime/orchestration"
PREP_SCHEMAS = ROOT / "novydres/runtime/provocation-prep"
PREP = ROOT / "novydres/chronicles/CHR-001/preparations"
CYCLE_DIR = ROOT / "novydres/chronicles/CHR-001/orchestration"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def schema(path):
    value = load(path)
    Draft202012Validator.check_schema(value)
    return value


def errors(document_schema, document):
    return list(Draft202012Validator(document_schema).iter_errors(document))


def ref(path, char):
    return {"path": path, "blob_sha": char * 40}


def synthetic_cycle(cycle_schema, sequence=35, transition="OPERATIONAL_ACTIVATED"):
    fixed = {
        "orchestration_contract": "novydres/runtime/orchestration/ORCHESTRATION_CONTRACT_V7.md",
        "cycle_schema": "novydres/runtime/orchestration/CYCLE_SCHEMA_V9.json",
        "cycle_validator": "novydres/runtime/orchestration/ORCHESTRATION_VALIDATOR_V9.mjs",
        "cycle_tests": "novydres/runtime/orchestration/ORCHESTRATION_TESTS_V9.mjs",
        "cycle_schema_tests": "novydres/runtime/orchestration/ORCHESTRATION_SCHEMA_TESTS_V9.py",
        "preparation_dossier_schema": "novydres/runtime/provocation-prep/PROVOCATION_DOSSIER_SCHEMA_V6.json",
        "preparation_sidecar_schema": "novydres/runtime/provocation-prep/PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V5.json",
        "start_here": "novydres/runtime/orchestration/START_HERE_V6.md",
        "agent_entry": "novydres/.AGENT_V4.md",
        "context_gateway": "novydres/.CONTEXTG_V3.md",
        "player_authorization": "novydres/runtime/narrative-architecture/program/decisions/PLAYER_DECISION_AGENT_ACCESS_V004.json",
    }
    arch = {}
    for i, key in enumerate(cycle_schema["properties"]["architecture"]["properties"]):
        arch[key] = ref(f"synthetic/architecture/{key}", str(i % 10))
    for key, path in fixed.items():
        arch[key]["path"] = path
    refs = {key: ref(f"synthetic/state/{key}.json", str((i + 1) % 10)) for i, key in enumerate(cycle_schema["properties"]["refs"]["properties"])}
    mechanical = {key: ref(f"synthetic/rules/{key}", str((i + 2) % 10)) for i, key in enumerate(cycle_schema["properties"]["operational_gates"]["properties"]["mechanical_sources"]["properties"])}
    activated = transition == "OPERATIONAL_ACTIVATED"
    gates = {
        "architecture_active": True, "d07_active": True,
        "story_preparation_ready": False if activated else False,
        "mechanical_scene_ready": False, "scene_ready": False, "narrator_permission": False,
        "mechanical_matrix_ref": ref("synthetic/mechanical-matrix.md", "a"), "mechanical_sources": mechanical,
    }
    return {
        "schema_id": "NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V9",
        "cycle_id": f"CHR001-CYCLE-{sequence:04d}", "sequence": sequence,
        "chronicle_id": "CHR-001", "provocation_id": "M3.01",
        "manifest_path": "novydres/MANIFEST_V49.json" if sequence == 35 else "novydres/MANIFEST_V50.json",
        "manifest_ref": ref("novydres/MANIFEST_V49.json" if sequence == 35 else "novydres/MANIFEST_V50.json", "b"),
        "source_head_sha": "c" * 40,
        "previous_cycle": ref(f"novydres/chronicles/CHR-001/orchestration/CYCLE_V{sequence - 1:04d}.json", "d"),
        "transition": transition,
        "status": "READY_FOR_DRAMATURGO" if activated else "PROVOCATION_CLOSURE_PENDING",
        "next_role": "DRAMATURGO" if activated else "NONE",
        "checkpoint": {"last_event_id": "CHR001-M301-C05-22-20261109-001", "last_closed_scene": "C05", "next_scene": "C06", "next_scene_status": "NOT_STARTED", "pending_persistence": False, "mortal": True, "embrace_occurred": False},
        "refs": refs, "architecture": arch,
        "plan": {"preparation_id": "CHR001-PREP-M301-20261111-V9", "dossier": ref("synthetic/dossier.json", "e"), "sidecar": ref("synthetic/sidecar.json", "f"), "validity": "STALE" if activated else "REVISED", "reviewed_against_event_id": "CHR001-M301-C05-22-20261109-001"},
        "review": {"decision": "NOT_REVIEWED" if activated else "CLOSURE_RECOMMENDED", "against_last_event_id": "CHR001-M301-C05-22-20261109-001", "public_rationale": None if activated else "Synthetic route recommendation only; no event or player choice is recorded."},
        "blocking": {"code": None if activated else "PLAYER_DECISION_REQUIRED", "reason": None if activated else "The player choice remains outstanding; no closure is recorded."},
        "guards": {"no_story_delta_in_prep": True, "no_xp_fv_delta_in_prep": True, "g28_scene_only": True, "frozen_unchanged": True, "no_public_spoilers": True},
        "activation": {"authorization": ref("novydres/runtime/narrative-architecture/program/decisions/PLAYER_DECISION_AGENT_ACCESS_V004.json", "1"), "d07_activation": ref("novydres/runtime/narrative-architecture/program/deliverables/D07_ACTIVATION_V004_PLAYER_SAFE.json", "2"), "truth_package": ref("synthetic/d07.md", "3"), "architecture_contract": ref("novydres/runtime/orchestration/ORCHESTRATION_CONTRACT_V7.md", "4")},
        "operational_gates": gates,
        "pending_player_decision": None if activated else "CLOSE_M3_01_AS_ALTERNATE_OR_CONTINUE",
    }


def synthetic_prep(source, source_cycle, sidecar=False):
    doc = copy.deepcopy(source)
    doc["preparation_id"] = "CHR001-PREP-M301-20261111-V9"
    cp = doc["source_checkpoint"]
    if sidecar:
        doc["schema_id"] = "NOVYDRES_PROVOCATION_LONGITUDINAL_SIDECAR_V5"
        cp["dossier_path"] = "novydres/chronicles/CHR-001/preparations/M3.01_DOSSIER_V9.json"
        cp["dossier_blob_sha"] = "f" * 40
        doc["predecessor_ref"] = {"path": "novydres/chronicles/CHR-001/preparations/M3.01_DOSSIER_V7.json", "blob_sha": "7" * 40}
    else:
        doc["schema_id"] = "NOVYDRES_PROVOCATION_DOSSIER_V6"
        doc["dossier_version"] = 8
    cp["base_commit_sha"] = "c" * 40
    cp["cycle_path"] = "novydres/chronicles/CHR-001/orchestration/CYCLE_V0035.json"
    cp["cycle_blob_sha"] = "e" * 40
    cp["manifest_path"] = "novydres/MANIFEST_V49.json"
    cp["manifest_blob_sha"] = "d" * 40
    cp["knowledge_path"] = source_cycle["refs"]["knowledge"]["path"]
    cp["knowledge_blob_sha"] = source_cycle["refs"]["knowledge"]["blob_sha"]
    cp["open_threads_path"] = source_cycle["refs"]["threads"]["path"]
    cp["open_threads_blob_sha"] = source_cycle["refs"]["threads"]["blob_sha"]
    for item in doc.get("source_refs", []):
        if item["path"].endswith("/CYCLE_V0034.json"):
            item["path"] = cp["cycle_path"]
            item["blob_sha"] = cp["cycle_blob_sha"]
        elif item["path"].endswith("/MANIFEST_V48.json"):
            item["path"] = cp["manifest_path"]
            item["blob_sha"] = cp["manifest_blob_sha"]
    return doc


cycle_schema_path = ORCH / "CYCLE_SCHEMA_V9.json"
cycle_schema = schema(cycle_schema_path)
dossier_schema = schema(PREP_SCHEMAS / "PROVOCATION_DOSSIER_SCHEMA_V6.json")
sidecar_schema = schema(PREP_SCHEMAS / "PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V5.json")

c35 = synthetic_cycle(cycle_schema, 35, "OPERATIONAL_ACTIVATED")
assert not errors(cycle_schema, c35), f"synthetic C35 activation rejected: {errors(cycle_schema, c35)[0].message}"
c36 = synthetic_cycle(cycle_schema, 36, "CLOSURE_RECOMMENDED")
c36["architecture"] = copy.deepcopy(c35["architecture"])
assert not errors(cycle_schema, c36), f"synthetic C36 closure routing rejected: {errors(cycle_schema, c36)[0].message}"

negative_cycle_cases = {}
bad = copy.deepcopy(c35); bad["architecture"]["cycle_schema"]["path"] = "novydres/runtime/orchestration/CYCLE_SCHEMA_V7.json"; negative_cycle_cases["stale schema path"] = bad
bad = copy.deepcopy(c35); bad["architecture"]["cycle_validator"]["path"] = "novydres/runtime/orchestration/ORCHESTRATION_VALIDATOR_V7.mjs"; negative_cycle_cases["stale validator path"] = bad
bad = copy.deepcopy(c35); bad["architecture"]["cycle_tests"]["path"] = "novydres/runtime/orchestration/ORCHESTRATION_TESTS_V7.mjs"; negative_cycle_cases["stale test path"] = bad
bad = copy.deepcopy(c35); bad["architecture"]["preparation_dossier_schema"]["path"] = "novydres/runtime/provocation-prep/PROVOCATION_DOSSIER_SCHEMA_V5.json"; negative_cycle_cases["stale dossier schema path"] = bad
bad = copy.deepcopy(c35); bad["architecture"]["preparation_sidecar_schema"]["path"] = "novydres/runtime/provocation-prep/PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V4.json"; negative_cycle_cases["stale sidecar schema path"] = bad
bad = copy.deepcopy(c35); bad["architecture"]["start_here"]["path"] = "novydres/runtime/orchestration/START_HERE_V4.md"; negative_cycle_cases["stale entrypoint path"] = bad
bad = copy.deepcopy(c35); bad["architecture"]["agent_entry"]["path"] = "novydres/.AGENT.md"; negative_cycle_cases["legacy operational entry path"] = bad
bad = copy.deepcopy(c35); bad["architecture"]["context_gateway"]["path"] = "novydres/.CONTEXTG.md"; negative_cycle_cases["legacy context gateway path"] = bad
bad = copy.deepcopy(c35); bad["activation"]["d07_activation"]["path"] = "novydres/runtime/narrative-architecture/program/deliverables/D07_ACTIVATION_V003_PLAYER_SAFE.json"; negative_cycle_cases["stale D07 activation V003 path"] = bad
bad = copy.deepcopy(c35); bad["activation"]["authorization"]["path"] = "novydres/runtime/narrative-architecture/program/decisions/PLAYER_DECISION_AGENT_ACCESS_V003.json"; negative_cycle_cases["stale authorization V003 path"] = bad
bad = copy.deepcopy(c35); bad["architecture"]["player_authorization"]["path"] = "novydres/runtime/narrative-architecture/program/decisions/PLAYER_DECISION_AGENT_ACCESS_V003.json"; negative_cycle_cases["stale architecture authorization path"] = bad
bad = copy.deepcopy(c36); bad["operational_gates"]["scene_ready"] = True; negative_cycle_cases["closure with false scene gate"] = bad
bad = copy.deepcopy(c36); bad["pending_player_decision"] = None; negative_cycle_cases["closure without player decision"] = bad
for label, bad_cycle in negative_cycle_cases.items():
    assert errors(cycle_schema, bad_cycle), f"cycle schema accepted {label}"

source_cycle = load(CYCLE_DIR / "CYCLE_V0034.json")
dossier_source = load(PREP / "M3.01_DOSSIER_V7.json")
sidecar_source = load(PREP / "M3.01_LONGITUDINAL_SIDECAR_V7.json")
dossier = synthetic_prep(dossier_source, source_cycle, sidecar=False)
sidecar = synthetic_prep(sidecar_source, source_cycle, sidecar=True)
assert not errors(dossier_schema, dossier), f"synthetic V9 dossier rejected: {errors(dossier_schema, dossier)[0].message}"
assert not errors(sidecar_schema, sidecar), f"synthetic V9 sidecar rejected: {errors(sidecar_schema, sidecar)[0].message}"

prep_negative_cases = 0
for source, source_schema, label in [(dossier, dossier_schema, "dossier"), (sidecar, sidecar_schema, "sidecar")]:
    cases = []
    bad = copy.deepcopy(source); bad["source_checkpoint"].pop("knowledge_path"); cases.append(("missing knowledge checkpoint", bad))
    bad = copy.deepcopy(source); bad["source_checkpoint"]["open_threads_blob_sha"] = "z" * 40; cases.append(("malformed threads blob", bad))
    bad = copy.deepcopy(source); bad["scene_ready"] = True; cases.append(("scene ready without scene", bad))
    bad = copy.deepcopy(source); bad["handoff"]["stakes"] = "invented stakes"; cases.append(("invented scene stakes", bad))
    bad = copy.deepcopy(source); bad["source_checkpoint"]["provocation_status"] = "CLOSED"; cases.append(("false closed state", bad))
    bad = copy.deepcopy(source); bad["handoff"]["next_decision"]["decision_recorded"] = True; cases.append(("unrecorded player choice", bad))
    for reason, candidate in cases:
        assert errors(source_schema, candidate), f"{label} schema accepted {reason}"
        prep_negative_cases += 1

published_v9_cycles = []
for path in sorted(CYCLE_DIR.glob("CYCLE_V*.json")):
    cycle = load(path)
    if cycle.get("schema_id") != "NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V9":
        continue
    cycle_errors = errors(cycle_schema, cycle)
    assert not cycle_errors, f"{path.name} rejected: {cycle_errors[0].message}"
    published_v9_cycles.append(path.name)

print(json.dumps({
    "suite": "ORCHESTRATION_SCHEMA_TESTS_V9.py",
    "status": "PASS",
    "schema_meta_validation": "PASS",
    "synthetic_cycles_accepted": ["C35_OPERATIONAL_ACTIVATED", "C36_CLOSURE_RECOMMENDED_PROVOCATION_CLOSURE_PENDING"],
    "cycle_negative_cases_rejected": list(negative_cycle_cases),
    "synthetic_preparations_accepted": ["dossier V9-shaped / schema V6", "sidecar V9-shaped / schema V5"],
    "preparation_negative_cases_rejected": prep_negative_cases,
    "published_v9_cycles": published_v9_cycles,
    "real_cycle_created": False,
    "real_event_created": False,
    "player_choice_recorded": False,
    "jsonschema_version": __import__("importlib.metadata").metadata.version("jsonschema"),
}, indent=2))

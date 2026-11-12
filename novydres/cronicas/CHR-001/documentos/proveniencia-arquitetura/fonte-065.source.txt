#!/usr/bin/env python3
"""Validate the exact current CHR-001 D04-D12 candidate source graph."""
from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve()
DEL=Path("novydres/runtime/narrative-architecture/program/deliverables")
OPS=Path("novydres/runtime/orchestration")
PREP=Path("novydres/chronicles/CHR-001/preparations")
DEC=Path("novydres/runtime/narrative-architecture/program/decisions")
N={
 "d04":DEL/"D04_PLOT_ADMISSIONS_V010.json", "d05":DEL/"D05_PLAYER_APPROVAL_QUEUE_V013.json",
 "d06":DEL/"D06_CHRONICLE_BIBLE_V028.json", "d06_validator":DEL/"D06_SOURCE_VALIDATE_V003.py",
 "d06_recon":DEL/"D06_SOURCE_RECONCILIATION_V003.json", "d07":DEL/"D07_STORY_TRUTH_PACKAGE_V018_GM_HIDDEN.md",
 "d08":DEL/"D08_STORY_PREPARATION_V018_GM_HIDDEN.md", "d09":DEL/"D09_GUIDED_CREATION_PROGRESSION_V021_PLAYER_SAFE.json",
 "decision":DEC/"PLAYER_DECISION_AGENT_ACCESS_V004.json", "activation":DEL/"D07_ACTIVATION_V004_PLAYER_SAFE.json",
 "cases":DEL/"D11_ADVERSARIAL_CASES_V019_GM_HIDDEN.json", "runner":DEL/"D11_EXECUTE_ADVERSARIAL_V019.py",
 "d11_result":DEL/"D11_TEST_RESULTS_V019_PLAYER_SAFE.json", "review":DEL/"D11_INDEPENDENT_REVIEW_V011_GM_HIDDEN.json",
 "review_status":DEL/"D11_REVIEW_STATUS_V012_PLAYER_SAFE.json", "mechanics":DEL/"D12_MECHANICAL_SOURCE_REFS_V001_PLAYER_SAFE.json",
 "matrix":DEL/"D12_MECHANICAL_GATES_MATRIX_V003_PLAYER_SAFE.md", "d10_validator":DEL/"D10_VALIDATE_V023.py", "registry":DEL/"D10_SCHEMA_REGISTRY_V021.json",
 "adapters":DEL/"D10_ROLE_ADAPTERS_V016.json", "inventory":DEL/"D12_PROMOTION_INVENTORY_V005_PLAYER_SAFE.json",
 "contract":OPS/"ORCHESTRATION_CONTRACT_V7.md", "schema":OPS/"CYCLE_SCHEMA_V9.json",
 "cycle_validator":OPS/"ORCHESTRATION_VALIDATOR_V9.mjs", "cycle_tests":OPS/"ORCHESTRATION_TESTS_V9.mjs",
 "schema_tests":OPS/"ORCHESTRATION_SCHEMA_TESTS_V9.py", "start":OPS/"START_HERE_V6.md",
 "dossier":PREP/"M3.01_DOSSIER_V7.json", "sidecar":PREP/"M3.01_LONGITUDINAL_SIDECAR_V7.json",
 "dossier_schema":Path("novydres/runtime/provocation-prep/PROVOCATION_DOSSIER_SCHEMA_V6.json"),
 "sidecar_schema":Path("novydres/runtime/provocation-prep/PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V5.json"),
 "agent":Path("novydres/.AGENT_V4.md"), "context":Path("novydres/.CONTEXTG_V3.md"),
 "cycle":Path("novydres/chronicles/CHR-001/orchestration/CYCLE_V0034.json"),
}
def blob(p):
 b=p.read_bytes(); return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def sha256(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.as_posix()
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def refmap(doc,key="source_refs"):
 return {x.get("path"):x.get("blob_sha") for x in doc.get(key,[]) if isinstance(x,dict)}
def check(code,ok): checks.append((code,bool(ok)))
checks=[]
check("D10-01-current-inputs-present",all((ROOT/p).is_file() for p in N.values()))
try:
 docs={k:load(p) for k,p in N.items() if p.suffix==".json"}
 check("D10-02-json-inputs-parse",True)
except Exception:
 docs={}; check("D10-02-json-inputs-parse",False)
# Current version and source relationships; D07/D08 preserve their approved D06 V026 derivation.
d06=docs.get("d06",{}); d09=docs.get("d09",{}); d04=docs.get("d04",{})
d06refs=refmap(d06)
check("D10-03-current-authoring-identity",d06.get("document_id")=="D06_CHRONICLE_BIBLE_V028" and d09.get("document_id")=="D09_GUIDED_CREATION_PROGRESSION_V021_PLAYER_SAFE")
check("D10-04-d06-current-operative-pins",all(d06refs.get(rel(N[k]))==blob(ROOT/N[k]) for k in ("d04","d07","d08","decision","activation")))
check("D10-05-d06-preserves-historical-only-baselines",all(any(r.get("path")==path and r.get("reference_role","").startswith("HISTORICAL") for r in d06.get("source_refs",[])) for path in ("novydres/runtime/narrative-architecture/program/deliverables/D07_STORY_TRUTH_PACKAGE_V015_GM_HIDDEN.md","novydres/runtime/narrative-architecture/program/deliverables/D08_STORY_PREPARATION_V015_GM_HIDDEN.md")))
d07=(ROOT/N["d07"]).read_text(encoding="utf-8"); d08=(ROOT/N["d08"]).read_text(encoding="utf-8")
check("D10-06-d07-current-lineage",all(x in d07 for x in ("V018","D06_CHRONICLE_BIBLE_V026.json","761f99f1e6d42d2a6a175c83d992c67424b914b8","D04_PLOT_ADMISSIONS_V010.json","260364032af2bd231b89c8fc7ac389f8543d4b79","PLAYER_DECISION_AGENT_ACCESS_V004.json","507eea0d797ddcafb0f19730c5dd20dd0d4594f1")))
check("D10-07-d08-current-lineage",all(x in d08 for x in ("V018","D06_CHRONICLE_BIBLE_V026.json","761f99f1e6d42d2a6a175c83d992c67424b914b8","D07_STORY_TRUTH_PACKAGE_V018_GM_HIDDEN.md","537c4260c1d024cea144511596a9b54599b737b8","D04_PLOT_ADMISSIONS_V010.json","260364032af2bd231b89c8fc7ac389f8543d4b79","PLAYER_DECISION_AGENT_ACCESS_V004.json","507eea0d797ddcafb0f19730c5dd20dd0d4594f1")))
d09refs=refmap(d09)
check("D10-08-d09-exact-source-pins",all(d09refs.get(rel(N[k]))==blob(ROOT/N[k]) for k in ("d04","d06","d07","d08","decision","activation")))
check("D10-09-d09-independent-runtime-gates",d09.get("operational_gate",{}).get("scene_ready") is False and d09.get("operational_gate",{}).get("narrator_permission") is False)
# D04 currently contains no admission of the C06 re-entry unit; an authorial target cannot create one.
admissions=d04.get("admissions",[])
c06_admitted=any("ST-C06-REENTRY" in str(a.get("contract_ref","")) or a.get("plot_id")=="PLOT-C06-REENTRY" for a in admissions if isinstance(a,dict))
check("D10-10-d04-does-not-admit-c06-reentry",not c06_admitted)
check("D10-11-last-played-state-preserved",d06.get("checkpoint",{}).get("cycle")=="CYCLE_V0034" and d06.get("checkpoint",{}).get("last_played")=="C05" and d06.get("checkpoint",{}).get("next_scene")=="C06 not started" and d06.get("checkpoint",{}).get("bartolomeu")=="mortal" and d06.get("checkpoint",{}).get("embrace_recorded") is False)
# Activation is a candidate record; cycle/manifest pin is still required for effect.
a=docs.get("activation",{})
check("D10-12-v004-activation-candidate-exact",a.get("document_id")=="D07_ACTIVATION_V004_PLAYER_SAFE" and a.get("status")=="ACTIVE" and a.get("activation_kind")=="D07_RUNTIME_TRUTH_PACKAGE" and a.get("runtime_activation",{}).get("d07_active") is True and a.get("truth_package_ref")=={"path":rel(N["d07"]),"blob_sha":blob(ROOT/N["d07"])} and a.get("authorization_ref",{}).get("blob_sha")==blob(ROOT/N["decision"]))
activation_scope=" ".join(a.get("activation_scope", "").casefold().split())
check("D10-13-activation-keeps-scene-gates-independent", all(phrase in activation_scope for phrase in ("candidate runtime activation", "does not activate runtime", "only after validated selective integration is committed", "current valid cycle and manifest pin", "scene readiness and narrator permission remain independent cycle gates", "are not asserted here")))
# D11 deterministic reducer and independent review bind exact final V019 material.
cases=docs.get("cases",{}).get("cases",[]); ids=[c.get("id") for c in cases]
check("D10-14-d11-v019-case-set",docs.get("cases",{}).get("version")=="V019" and len(cases)==58 and len(ids)==len(set(ids)))
case_refs=refmap(docs.get("cases",{}))
check("D10-15-d11-cases-pin-current-authors",all(case_refs.get(rel(N[k]))==blob(ROOT/N[k]) for k in ("d04","d05","d06","d07","d08","d09","decision","activation")))
result=docs.get("d11_result",{}); runner=ROOT/N["runner"]
inputrefs=result.get("input_artifact_refs",[]); inputmap={x.get("path"):x.get("blob_sha") for x in inputrefs}
check("D10-16-d11-executor-pass-58",result.get("document_id")=="D11_TEST_RESULTS_V019_PLAYER_SAFE" and result.get("status")=="PASS" and result.get("cases_total")==58 and result.get("passed")==58 and result.get("failed")==0)
check("D10-17-d11-result-and-runner-pins",inputmap.get(rel(N["cases"]))==blob(ROOT/N["cases"]) and inputmap.get(rel(N["d04"]))==blob(ROOT/N["d04"]) and result.get("runner_source_sha256")==sha256(runner))
check("D10-18-d11-no-play-or-state-mutation",result.get("scenes_played")==0 and result.get("dice_simulated") is False and result.get("persistent_state_mutated") is False)
review=docs.get("review",{}); reviewstatus=docs.get("review_status",{})
review_targets=("d04","d05","d06","d07","d08","d09","cases","runner","d11_result","activation")
expected_review={rel(N[k]):blob(ROOT/N[k]) for k in review_targets}
check("D10-19-independent-review-current-exact-pins",review.get("version")=="V011" and review.get("status")=="PASS_WITH_LIMITATION" and refmap(review,"reviewed_artifact_refs")==expected_review)
check("D10-20-independent-review-covers-every-case",sorted(review.get("reviewed_case_ids",[]))==sorted(ids) and review.get("finding_ids")==[] and review.get("scene_played") is False and review.get("state_mutated") is False)
check("D10-21-review-status-exact",reviewstatus.get("version")=="V012" and reviewstatus.get("status")=="PASS_WITH_LIMITATION" and reviewstatus.get("case_count")==58 and reviewstatus.get("open_findings")==0 and reviewstatus.get("independent_review_ref",{}).get("blob_sha")==blob(ROOT/N["review"]))
check("D10-22-current-c06-limit-explicit","admits no C06 cause" in review.get("prospective_limitation","") and "positive target-route transition" in reviewstatus.get("limitation","") and "does not establish scene readiness" in review.get("prospective_limitation","").lower())
# Mechanical index validates every present local source and keeps the three gates distinct.
mechanics=docs.get("mechanics",{}); mrefs=mechanics.get("source_refs",[])
mismatches=[r.get("path") for r in mrefs if not (ROOT/r.get("path","")).is_file() or blob(ROOT/r.get("path",""))!=r.get("blob_sha")]
g=mechanics.get("gate_status",{})
check("D10-23-mechanics-index-source-pins",mechanics.get("document_id")=="D12_MECHANICAL_SOURCE_REFS_V001_PLAYER_SAFE" and len(mrefs)==20 and not mismatches)
check("D10-24-mechanical-gates-distinct",g.get("mortal_next_scene","").startswith("MECHANICALLY_CONDITIONAL") and g.get("future_embrace_and_vampiric_development","").startswith("NOT_ELIGIBLE") and g.get("final_2010_sheet_certification","").startswith("PENDING"))
mt=(ROOT/N["matrix"]).read_text(encoding="utf-8")
check("D10-25-rulebook-limit-does-not-block-covered-mortal-action","não bloqueia" in mt.lower() and "ação mortal" in mt.lower() and "não localizado" in mt.lower() and "2010" in mt.lower())
# D06 source reconciliation is rerun, not inferred from a stored report.
src=subprocess.run([sys.executable,str(ROOT/N["d06_validator"]),str(ROOT)],capture_output=True,text=True)
try: sr=json.loads(src.stdout)
except Exception: sr={}
check("D10-26-d06-source-validator-33-of-33",src.returncode==0 and sr.get("status")=="PASS" and sr.get("checks_passed")==33 and sr.get("checks_total")==33)
# V9 operational contract and exact bootstrap paths are the current contracts; no V9 cycle exists yet.
contract=(ROOT/N["contract"]).read_text(encoding="utf-8")
check("D10-27-v9-ops-paths-and-entrypoint",all(x in contract for x in ("CYCLE_SCHEMA_V9.json","ORCHESTRATION_VALIDATOR_V9.mjs","ORCHESTRATION_TESTS_V9.mjs","ORCHESTRATION_SCHEMA_TESTS_V9.py","START_HERE_V6.md","PROVOCATION_DOSSIER_SCHEMA_V6.json","PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V5.json","D07_ACTIVATION_V004_PLAYER_SAFE.json")))
check("D10-28-v9-start-here-is-contract-entry",N["start"].as_posix() in contract and N["start"].is_file())
# Existing M3.01 preparation is deliberately a stale, pre-activation snapshot; post-C35 V8 is pending.
dossier=docs.get("dossier",{}); sidecar=docs.get("sidecar",{})
try:
 from jsonschema import Draft202012Validator
 Draft202012Validator.check_schema(docs["dossier_schema"]); Draft202012Validator.check_schema(docs["sidecar_schema"])
 prep_schemas_ok=docs["dossier_schema"].get("$id","").endswith("PROVOCATION_DOSSIER_SCHEMA_V6.json") and docs["sidecar_schema"].get("$id","").endswith("PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V5.json")
except Exception: prep_schemas_ok=False
check("D10-29-current-preparation-schemas-validate",prep_schemas_ok)
route=dossier.get("handoff",{}).get("next_decision",{}); choices={x.get("choice_id"):x for x in route.get("choices",[]) if isinstance(x,dict)}
check("D10-30-v7-no-cause-remains-quiet",route.get("cause_status")=="NO_C06_CAUSE_ADMITTED_OR_AVAILABLE" and route.get("default_if_no_action")=="KEEP_OPEN_QUIET" and route.get("decision_recorded") is False and dossier.get("handoff",{}).get("cause") is None and dossier.get("scene_ready") is False and dossier.get("NARRATOR_PERMISSION") is False and not dossier.get("handoff",{}).get("prepared_scenes"))
check("D10-31-v7-separate-options",set(choices)=={"KEEP_OPEN_QUIET","CONTINUE_AFTER_ADMISSION","REQUEST_ALTERNATE_CLOSURE"} and choices.get("KEEP_OPEN_QUIET",{}).get("availability")=="AVAILABLE_NOW" and choices.get("CONTINUE_AFTER_ADMISSION",{}).get("availability")=="UNAVAILABLE_UNTIL_CAUSE_ADMITTED_AND_AVAILABLE" and choices.get("REQUEST_ALTERNATE_CLOSURE",{}).get("availability")=="AVAILABLE_ON_EXPLICIT_PLAYER_REQUEST" and sidecar.get("handoff",{}).get("next_decision")==route)
check("D10-32-v7-is-pre-activation-snapshot",dossier.get("source_checkpoint",{}).get("cycle_path")==rel(N["cycle"]) and dossier.get("source_checkpoint",{}).get("manifest_path")=="novydres/MANIFEST_V48.json" and sidecar.get("source_checkpoint",{}).get("dossier_blob_sha")==blob(ROOT/N["dossier"]) and not (ROOT/PREP/"M3.01_DOSSIER_V8.json").exists())
# Inventory contains every exact current promotion input; successor outputs are not hash-cycled back into it.
inventory=docs.get("inventory",{}); pinned={x.get("path"):x.get("blob_sha") for x in inventory.get("pinned_artifacts",[]) if isinstance(x,dict)}
inv_fail=[p for p,h in pinned.items() if not (ROOT/p).is_file() or blob(ROOT/p)!=h]
check("D10-33-inventory-pins-all-existing-blobs",inventory.get("document_id")=="D12_PROMOTION_INVENTORY_V005_PLAYER_SAFE" and len(pinned)>=45 and not inv_fail)
for k in ("d04","d05","d06","d07","d08","d09","decision","activation","cases","runner","d11_result","review","review_status","mechanics","matrix","d06_validator","d10_validator","contract","schema","cycle_validator","cycle_tests","schema_tests","start","dossier","sidecar","dossier_schema","sidecar_schema","agent","context","cycle"):
 check("D10-34-inventory-source-"+k,pinned.get(rel(N[k]))==blob(ROOT/N[k]))
outputs={x.get("path"):x for x in inventory.get("acyclic_output_paths",[]) if isinstance(x,dict)}
check("D10-35-inventory-dependency-graph-acyclic",all(outputs.get(p,{}).get("hash_policy")=="OMITTED_TO_KEEP_DEPENDENCY_GRAPH_ACYCLIC" for p in (rel(N["registry"]),rel(N["adapters"]),"novydres/runtime/narrative-architecture/program/deliverables/D10_TEST_RESULTS_V023.json","novydres/runtime/narrative-architecture/program/deliverables/D12_RELEASE_CANDIDATE_V019.json","novydres/runtime/narrative-architecture/program/deliverables/D12_VALIDATE_V018_RESULT.json")))
check("D10-36-inventory-pending-post-promotion",all(any(x.get("path")==p and x.get("status")=="PENDING_CREATION" for x in inventory.get("pending_operational_artifacts",[])) for p in ("novydres/chronicles/CHR-001/orchestration/CYCLE_V0035.json","novydres/chronicles/CHR-001/orchestration/CYCLE_V0036.json","novydres/MANIFEST_V49.json","novydres/MANIFEST_V50.json","novydres/runtime/narrative-architecture/program/deliverables/D12_PUBLICATION_READBACK_V002_PLAYER_SAFE.json")))
# Registry exact source refs mirror inventory pins plus this validator; its output is a separate leaf.
registry=docs.get("registry",{}); regrefs=refmap(registry)
expected={**pinned,rel(N["inventory"]):blob(ROOT/N["inventory"])}
check("D10-37-registry-v021-identity",registry.get("document_id")=="D10_SCHEMA_REGISTRY_V021" and registry.get("version")=="V021" and registry.get("runner")=="D10_VALIDATE_V023.py" and registry.get("test_report")=="D10_TEST_RESULTS_V023.json")
check("D10-38-registry-current-exact-source-refs",all(regrefs.get(p)==h for p,h in expected.items()) and len(regrefs)==len(expected))
check("D10-39-registry-catalog-current-successors",all(x in registry.get("catalog",[]) for x in ("D10_SCHEMA_REGISTRY_V021.json","D10_ROLE_ADAPTERS_V016.json","D10_VALIDATE_V023.py","D10_TEST_RESULTS_V023.json","D11_ADVERSARIAL_CASES_V019_GM_HIDDEN.json","D11_EXECUTE_ADVERSARIAL_V019.py","D11_TEST_RESULTS_V019_PLAYER_SAFE.json","D11_INDEPENDENT_REVIEW_V011_GM_HIDDEN.json","D11_REVIEW_STATUS_V012_PLAYER_SAFE.json","D12_PROMOTION_INVENTORY_V005_PLAYER_SAFE.json","D12_RELEASE_CANDIDATE_V019.json","D12_VALIDATE_V018.py","D12_VALIDATE_V018_RESULT.json")))
adapters=docs.get("adapters",{}); arefs=refmap(adapters)
check("D10-40-adapter-v016-identity",adapters.get("document_id")=="D10_ROLE_ADAPTERS_V016" and adapters.get("version")=="V016" and adapters.get("version_pins",{}).get("schema_registry")=="D10_SCHEMA_REGISTRY_V021.json" and registry.get("document_id")=="D10_SCHEMA_REGISTRY_V021")
check("D10-41-adapter-separate-knowledge-ledgers",set(adapters.get("knowledge_ledgers",{}))=={"AGENT_KNOWLEDGE","PLAYER_KNOWLEDGE","PC_KNOWLEDGE","NPC_KNOWLEDGE"} and set(adapters.get("roles",{}))>={"DRAMATURGO","NARRATOR","PLAYER","CHARACTER","NPC"})
check("D10-42-adapter-exact-current-refs",all(arefs.get(rel(p))==blob(ROOT/p) for p in (N["registry"],N["decision"],N["activation"],N["contract"],N["schema"],N["cycle_validator"],N["cycle_tests"],N["schema_tests"],N["start"],N["mechanics"],N["dossier_schema"],N["sidecar_schema"],N["agent"],N["context"])))
global_rules=[" ".join(x.casefold().split()) for x in adapters.get("global_rules", [])]
role_rules=adapters.get("roles", {})
dramaturgo_bans=[" ".join(x.casefold().split()) for x in role_rules.get("DRAMATURGO", {}).get("must_not", [])]
narrator_rules=[" ".join(x.casefold().split()) for x in role_rules.get("NARRATOR", {}).get("must", [])]
check("D10-43-adapter-no-readiness-grant", any(x.startswith("no automatic scene readiness, narrator permission") for x in global_rules) and any("issue narrator permission" in x for x in dramaturgo_bans) and any("stop if cycle or permission is absent" in x for x in narrator_rules))

# Promotion inventory is an exact diff against the immutable base tree, not a moving remote ref.
def tree_blob(commit,path):
 r=subprocess.run(["git","cat-file","blob",f"{commit}:{path}"],cwd=ROOT,capture_output=True)
 if r.returncode:
  return None
 data=r.stdout
 return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
base=inventory.get("source_checkpoint",{}).get("master_head_sha")
expected_add_update={}; expected_same={}
for pth,h in pinned.items():
 old=tree_blob(base,pth) if base else None
 if old is None: expected_add_update[pth]=("ADD",h)
 elif old!=h: expected_add_update[pth]=("UPDATE",h)
 else: expected_same[pth]=h
promotion_rows=inventory.get("promotion_files",[])
already_rows=inventory.get("already_present_files",[])
excluded_rows=inventory.get("excluded_from_promotion",[])
promotion_paths=[x.get("path") for x in promotion_rows if isinstance(x,dict)] if isinstance(promotion_rows,list) else []
already_paths=[x.get("path") for x in already_rows if isinstance(x,dict)] if isinstance(already_rows,list) else []
excluded_paths_list=[x.get("path") for x in excluded_rows if isinstance(x,dict)] if isinstance(excluded_rows,list) else []
promotion_rows_valid=isinstance(promotion_rows,list) and all(isinstance(x,dict) and isinstance(x.get("path"),str) and bool(x.get("path")) and isinstance(x.get("blob_sha"),str) and x.get("action") in ("ADD","UPDATE") for x in promotion_rows)
already_rows_valid=isinstance(already_rows,list) and all(isinstance(x,dict) and isinstance(x.get("path"),str) and bool(x.get("path")) and isinstance(x.get("blob_sha"),str) for x in already_rows)
excluded_rows_valid=isinstance(excluded_rows,list) and all(isinstance(x,dict) and isinstance(x.get("path"),str) and bool(x.get("path")) for x in excluded_rows)
promotion_unique=promotion_rows_valid and len(promotion_paths)==len(promotion_rows) and len(set(promotion_paths))==len(promotion_paths)
already_unique=already_rows_valid and len(already_paths)==len(already_rows) and len(set(already_paths))==len(already_paths)
check("D10-50-promotion-rows-unique-before-mapping",promotion_unique and len(promotion_rows)==len(expected_add_update))
check("D10-51-already-present-rows-unique-before-mapping",already_unique and len(already_rows)==len(expected_same))
got_add_update={x.get("path"):(x.get("action"),x.get("blob_sha")) for x in promotion_rows if isinstance(x,dict)} if promotion_unique else {}
got_same={x.get("path"):x.get("blob_sha") for x in already_rows if isinstance(x,dict)} if already_unique else {}
tree_ok=bool(base) and subprocess.run(["git","cat-file","-e",f"{base}^{{tree}}"],cwd=ROOT,capture_output=True).returncode==0
comparison=inventory.get("promotion_comparison",{}); excluded_paths=set(excluded_paths_list)
expected_counts={"ADD":sum(1 for action,_ in expected_add_update.values() if action=="ADD"),"UPDATE":sum(1 for action,_ in expected_add_update.values() if action=="UPDATE")}
actual_counts={"ADD":sum(1 for x in promotion_rows if isinstance(x,dict) and x.get("action")=="ADD"),"UPDATE":sum(1 for x in promotion_rows if isinstance(x,dict) and x.get("action")=="UPDATE")}
check("D10-45-promotion-files-exact-against-immutable-master-tree",base=="492457805e080a0049eb275e2ad59a0b4fac577d" and tree_ok and got_add_update==expected_add_update and got_same==expected_same)
check("D10-46-excluded-history-not-promoted",not (excluded_paths & (set(got_add_update)|set(got_same))) and all(x.get("status") in ("HISTORICAL_ONLY","UNAVAILABLE_HISTORICAL_SUPERSEDED","HISTORICAL_DRAFT_ONLY") for x in excluded_rows if isinstance(x,dict)))
check("D10-52-excluded-paths-disjoint-from-promotion-and-same",excluded_rows_valid and not (excluded_paths & (set(got_add_update)|set(got_same))))
check("D10-53-promotion-comparison-head-and-counts-exact",comparison.get("baseline_master_head_sha")=="492457805e080a0049eb275e2ad59a0b4fac577d" and comparison.get("promotion_files_count")==len(expected_add_update) and comparison.get("already_present_count")==len(expected_same) and comparison.get("counts")==expected_counts and actual_counts==expected_counts and len(already_rows)==len(expected_same))
lineage={x.get("path"):x.get("blob_sha") for x in inventory.get("pinned_artifacts",[]) if x.get("reference_role")=="HISTORICAL_INVENTORY_PREDECESSOR_ONLY"}
check("D10-47-inventory-v003-v004-lineage-only",lineage=={
 "novydres/runtime/narrative-architecture/program/deliverables/D12_PROMOTION_INVENTORY_V003_PLAYER_SAFE.json":"373d3a1c9046be4cc631ca2ad2ac2a88bc3debc0",
 "novydres/runtime/narrative-architecture/program/deliverables/D12_PROMOTION_INVENTORY_V004_PLAYER_SAFE.json":"00422b7c9cf96f138a94bcded5a661d8e6acff96"
} and inventory.get("historical_lineage_limit",{}).get("predecessors_before_v003_promoted") is False and inventory.get("historical_lineage_limit",{}).get("decision_v001_runtime_authority") is False)
check("D10-48-v018-validator-pinned",pinned.get("novydres/runtime/narrative-architecture/program/deliverables/D12_VALIDATE_V018.py")==blob(ROOT/Path("novydres/runtime/narrative-architecture/program/deliverables/D12_VALIDATE_V018.py")))
control={x.get("path"):x for x in inventory.get("publication_control_set",[]) if isinstance(x,dict)}
control_required=("novydres/runtime/narrative-architecture/program/deliverables/D10_SCHEMA_REGISTRY_V021.json","novydres/runtime/narrative-architecture/program/deliverables/D10_ROLE_ADAPTERS_V016.json","novydres/runtime/narrative-architecture/program/deliverables/D10_TEST_RESULTS_V023.json","novydres/runtime/narrative-architecture/program/deliverables/D12_RELEASE_CANDIDATE_V019.json","novydres/runtime/narrative-architecture/program/deliverables/D12_VALIDATE_V018_RESULT.json","novydres/runtime/narrative-architecture/program/deliverables/D12_PROMOTION_INVENTORY_V005_PLAYER_SAFE.json")
check("D10-49-publication-control-set-acyclic",all(control.get(p,{}).get("action") in ("ADD","SELF_ADD") and control.get(p,{}).get("hash_policy")=="OMITTED_IN_INVENTORY_TO_AVOID_HASH_CYCLE" and control.get(p,{}).get("hash_fixed_by")=="D12_PUBLICATION_READBACK_V002_PLAYER_SAFE.json" for p in control_required))

# No operational cursor or publication artifact is created by D10.
check("D10-44-no-cycle-or-manifest-created",not (ROOT/"novydres/chronicles/CHR-001/orchestration/CYCLE_V0035.json").exists() and not (ROOT/"novydres/MANIFEST_V49.json").exists())
passed=sum(ok for _,ok in checks); failed=[c for c,ok in checks if not ok]
report={"document_id":"D10_TEST_RESULTS_V023","validator":"D10_VALIDATE_V023.py","version":"V023","status":"PASS" if not failed else "FAIL","checks_passed":passed,"checks_total":len(checks),"failed_check_ids":failed,"d11_cases":len(cases),"d11_result":result.get("status"),"independent_review":reviewstatus.get("status"),"d06_source_reconciliation":{"status":sr.get("status"),"checks_passed":sr.get("checks_passed"),"checks_total":sr.get("checks_total")},"mechanical_source_index":{"path":rel(N["mechanics"]),"blob_sha":blob(ROOT/N["mechanics"])},"promotion_inventory":{"path":rel(N["inventory"]),"blob_sha":blob(ROOT/N["inventory"])},"orchestration_refs":{rel(N[k]):{"blob_sha":blob(ROOT/N[k])} for k in ("contract","schema","cycle_validator","cycle_tests","schema_tests","start","dossier_schema","sidecar_schema")},"operational_checkpoint":{"cycle":"CYCLE_V0034 baseline","last_event_id":"CHR001-M301-C05-22-20261109-001","next_scene":"C06 NOT_STARTED","protagonist":"mortal","embrace_recorded":False},"SCENE_READY":False,"NARRATOR_PERMISSION":False,"d07_activation_record":"ACTIVE_CANDIDATE_ONLY_NOT_EFFECTIVE_UNTIL_CYCLE_AND_MANIFEST_PIN","result_detail_disclosed":False,"limitation":"D10 validates sources and candidate contracts only. No C06 cause is admitted by current D04; scene and Narrator gates remain separate and false. D10 does not create a cycle, manifest, event, scene, state change, XP or FV change."}
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(1 if failed else 0)

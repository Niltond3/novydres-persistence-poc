#!/usr/bin/env python3
"""Read-only D12 gate validator for CHR-001 selective promotion candidate V019."""
from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve()
DEL=Path("novydres/runtime/narrative-architecture/program/deliverables")
INV=DEL/"D12_PROMOTION_INVENTORY_V005_PLAYER_SAFE.json"
CAND=DEL/"D12_RELEASE_CANDIDATE_V019.json"
REG=DEL/"D10_SCHEMA_REGISTRY_V021.json"
ADAPT=DEL/"D10_ROLE_ADAPTERS_V016.json"
D10R=DEL/"D10_TEST_RESULTS_V023.json"
D10V=DEL/"D10_VALIDATE_V023.py"
D11R=DEL/"D11_TEST_RESULTS_V019_PLAYER_SAFE.json"
REVIEW=DEL/"D11_INDEPENDENT_REVIEW_V011_GM_HIDDEN.json"
REVIEW_STATUS=DEL/"D11_REVIEW_STATUS_V012_PLAYER_SAFE.json"
D06R=DEL/"D06_SOURCE_VALIDATE_V003_RESULT.json"
D06=DEL/"D06_CHRONICLE_BIBLE_V028.json"
D07=DEL/"D07_STORY_TRUTH_PACKAGE_V018_GM_HIDDEN.md"
D08=DEL/"D08_STORY_PREPARATION_V018_GM_HIDDEN.md"
D09=DEL/"D09_GUIDED_CREATION_PROGRESSION_V021_PLAYER_SAFE.json"
ACT=DEL/"D07_ACTIVATION_V004_PLAYER_SAFE.json"
D12V=DEL/"D12_VALIDATE_V018.py"
SCENE=Path("novydres/chronicles/CHR-001/orchestration/CYCLE_V0034.json")
checks=[]
def blob(path):
 b=path.read_bytes(); return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def check(code, ok): checks.append((code,bool(ok)))
def load(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
def refmap(rows): return {x.get("path"):x.get("blob_sha") for x in rows if isinstance(x,dict)}
def git_blob(commit,path):
 r=subprocess.run(["git","rev-parse",f"{commit}:{path}"],cwd=ROOT,capture_output=True,text=True)
 return r.stdout.strip() if r.returncode==0 else None
paths=[INV,CAND,REG,ADAPT,D10R,D10V,D11R,REVIEW,REVIEW_STATUS,D06R,D06,D07,D08,D09,ACT,D12V,SCENE]
check("D12-01-current-candidate-inputs-present",all((ROOT/x).is_file() for x in paths))
try:
 inv=load(INV); cand=load(CAND); reg=load(REG); adapt=load(ADAPT); d10=load(D10R); d11=load(D11R); rev=load(REVIEW); revs=load(REVIEW_STATUS); d06r=load(D06R); d06=load(D06); act=load(ACT); cycle=load(SCENE)
 check("D12-02-input-json-parses",True)
except Exception:
 inv=cand=reg=adapt=d10=d11=rev=revs=d06r=d06=act=cycle={}
 check("D12-02-input-json-parses",False)
# Pin all committed sources and compare the selective promotion list to the immutable baseline tree.
pinned=inv.get("pinned_artifacts",[]); pinmap=refmap(pinned); bad=[]
for path,h in pinmap.items():
 try:
  if not (ROOT/path).is_file() or blob(ROOT/path)!=h: bad.append(path)
 except Exception: bad.append(path)
check("D12-03-inventory-pinned-blobs-exact",not bad and len(pinmap)==len(pinned))
base=inv.get("source_checkpoint",{}).get("master_head_sha")
expected={}; present={}; baseline_errors=[]
for path,h in pinmap.items():
 old=git_blob(base,path) if base else None
 if old is None: expected[path]=("ADD",h)
 elif old!=h: expected[path]=("UPDATE",h)
 else: present[path]=h
promos=inv.get("promotion_files",[]); already=inv.get("already_present_files",[]); excluded=inv.get("excluded_from_promotion",[])
promo_paths=[x.get("path") for x in promos if isinstance(x,dict)] if isinstance(promos,list) else []
present_paths=[x.get("path") for x in already if isinstance(x,dict)] if isinstance(already,list) else []
excluded_paths=[x.get("path") for x in excluded if isinstance(x,dict)] if isinstance(excluded,list) else []
promo_rows_valid=isinstance(promos,list) and all(isinstance(x,dict) and isinstance(x.get("path"),str) and bool(x.get("path")) and isinstance(x.get("blob_sha"),str) and x.get("action") in ("ADD","UPDATE") for x in promos)
present_rows_valid=isinstance(already,list) and all(isinstance(x,dict) and isinstance(x.get("path"),str) and bool(x.get("path")) and isinstance(x.get("blob_sha"),str) for x in already)
excluded_rows_valid=isinstance(excluded,list) and all(isinstance(x,dict) and isinstance(x.get("path"),str) and bool(x.get("path")) for x in excluded)
promo_paths_unique=promo_rows_valid and len(promo_paths)==len(promos) and len(set(promo_paths))==len(promo_paths)
present_paths_unique=present_rows_valid and len(present_paths)==len(already) and len(set(present_paths))==len(present_paths)
check("D12-26-promotion-rows-unique-before-mapping",promo_paths_unique and len(promos)==len(expected))
check("D12-27-already-present-rows-unique-before-mapping",present_paths_unique and len(already)==len(present))
got={x.get("path"):(x.get("action"),x.get("blob_sha")) for x in promos if isinstance(x,dict)} if promo_paths_unique else {}
got_present={x.get("path"):x.get("blob_sha") for x in already if isinstance(x,dict)} if present_paths_unique else {}
tree_ok=bool(base) and subprocess.run(["git","cat-file","-e",f"{base}^{{tree}}"],cwd=ROOT,capture_output=True).returncode==0
check("D12-04-immutable-baseline-head",base=="492457805e080a0049eb275e2ad59a0b4fac577d" and tree_ok)
check("D12-05-promotion-set-exact-against-baseline",base=="492457805e080a0049eb275e2ad59a0b4fac577d" and got==expected and not baseline_errors)
check("D12-06-already-present-set-exact",got_present==present)
check("D12-07-promotion-items-have-reasons",all(bool(x.get("reason")) and x.get("action") in ("ADD","UPDATE") for x in promos))
excluded_path_set=set(excluded_paths)
check("D12-08-excluded-historical-not-promoted",not (excluded_path_set & (set(got)|set(got_present))) and all(x.get("status") in ("HISTORICAL_ONLY","UNAVAILABLE_HISTORICAL_SUPERSEDED","HISTORICAL_DRAFT_ONLY") for x in excluded if isinstance(x,dict)))
comparison=inv.get("promotion_comparison",{}); expected_counts={"ADD":sum(1 for action,_ in expected.values() if action=="ADD"),"UPDATE":sum(1 for action,_ in expected.values() if action=="UPDATE")}
actual_counts={"ADD":sum(1 for x in promos if isinstance(x,dict) and x.get("action")=="ADD"),"UPDATE":sum(1 for x in promos if isinstance(x,dict) and x.get("action")=="UPDATE")}
check("D12-28-excluded-paths-disjoint-from-promotion-and-same",excluded_rows_valid and not (excluded_path_set & (set(got)|set(got_present))))
check("D12-29-promotion-comparison-head-and-counts-exact",comparison.get("baseline_master_head_sha")=="492457805e080a0049eb275e2ad59a0b4fac577d" and comparison.get("promotion_files_count")==len(expected) and comparison.get("already_present_count")==len(present) and comparison.get("counts")==expected_counts and actual_counts==expected_counts and len(already)==len(present))
check("D12-09-inventory-predecessor-lineage-only",inv.get("predecessor_ref",{}).get("path")=="novydres/runtime/narrative-architecture/program/deliverables/D12_PROMOTION_INVENTORY_V004_PLAYER_SAFE.json" and inv.get("predecessor_ref",{}).get("blob_sha")==blob(ROOT/(DEL/"D12_PROMOTION_INVENTORY_V004_PLAYER_SAFE.json")) and inv.get("predecessor_ref",{}).get("reference_role")=="HISTORICAL_AUDIT_LINEAGE_ONLY")
# Current CHR-001 sources and their readback identities are exact and unambiguous.
source=inv.get("source_checkpoint",{})
check("D12-10-baseline-checkpoint",source.get("cycle_path")==SCENE.as_posix() and source.get("cycle_blob_sha")==blob(ROOT/SCENE) and source.get("last_event_id")=="CHR001-M301-C05-22-20261109-001" and source.get("next_scene")=="C06 NOT_STARTED" and source.get("protagonist")=="MORTAL" and source.get("embrace_occurred") is False)
check("D12-11-D06-source-reconciliation",d06r.get("status")=="PASS" and d06r.get("checks_passed")==33 and d06r.get("checks_total")==33)
check("D12-12-D11-current-adversarial-result",d11.get("document_id")=="D11_TEST_RESULTS_V019_PLAYER_SAFE" and d11.get("status")=="PASS" and d11.get("cases_total")==58 and d11.get("passed")==58 and d11.get("failed")==0 and d11.get("scenes_played")==0 and d11.get("persistent_state_mutated") is False)
check("D12-13-D11-independent-review",rev.get("version")=="V011" and rev.get("status")=="PASS_WITH_LIMITATION" and rev.get("finding_ids")==[] and revs.get("version")=="V012" and revs.get("status")=="PASS_WITH_LIMITATION" and revs.get("case_count")==58 and revs.get("open_findings")==0)
check("D12-14-D10-validator-result",d10.get("document_id")=="D10_TEST_RESULTS_V023" and d10.get("status")=="PASS" and d10.get("checks_passed")==d10.get("checks_total") and d10.get("checks_total",0)>0 and d10.get("promotion_inventory",{}).get("blob_sha")==blob(ROOT/INV))
# D07 candidate activation does not grant scene permission; runtime starts only through cycle/manifest.
check("D12-15-activation-candidate-exact",act.get("document_id")=="D07_ACTIVATION_V004_PLAYER_SAFE" and act.get("status")=="ACTIVE" and act.get("activation_kind")=="D07_RUNTIME_TRUTH_PACKAGE" and act.get("runtime_activation",{}).get("d07_active") is True and act.get("truth_package_ref",{}).get("path")==D07.as_posix() and act.get("truth_package_ref",{}).get("blob_sha")==blob(ROOT/D07))
check("D12-16-scene-and-narrator-gates-independent",cand.get("gates",{}).get("SCENE_READY") is False and cand.get("gates",{}).get("NARRATOR_PERMISSION") is False and cand.get("authorizations",{}).get("scene_execution") is False and cand.get("authorizations",{}).get("narrator_permission") is False)
check("D12-17-D07-runtime-awaits-cycle-manifest",cand.get("gates",{}).get("D07_activation") in ("ACTIVE_CANDIDATE_ONLY", "ACTIVE_CANDIDATE_PENDING_EXACT_CYCLE_MANIFEST_PIN") and cand.get("authorizations",{}).get("D07_activation_effective") is False)
check("D12-18-no-scene-start-or-retcon",cand.get("operational_state",{}).get("next_scene")=="C06 NOT_STARTED" and cand.get("operational_state",{}).get("last_scene")=="C05 CLOSED" and cand.get("operational_state",{}).get("last_event_id")=="CHR001-M301-C05-22-20261109-001" and cand.get("operational_state",{}).get("embrace_recorded") is False and cand.get("authorizations",{}).get("scene_execution") is False)
check("D12-19-no-prompt-issued",cand.get("narrator_prompt") is None and cand.get("authorizations",{}).get("narrator_prompt_issued") is False)
# Candidate must pin every current source plus the exact inventory and D10 outputs; no self/hash cycles.
crefs=refmap(cand.get("source_refs",[])); expected_refs=dict(pinmap)
for path in (INV.as_posix(),REG.as_posix(),ADAPT.as_posix(),D10R.as_posix()): expected_refs[path]=blob(ROOT/Path(path))
check("D12-20-candidate-source-pins-exact",crefs==expected_refs)
check("D12-21-release-candidate-identity",cand.get("document_id")=="D12_RELEASE_CANDIDATE_V019" and cand.get("version")=="V019" and cand.get("status")=="VALIDATED_AUTHORING_AND_OPERATIONAL_CANDIDATE_PENDING_CYCLE_TRANSITIONS")
check("D12-22-registry-exact-inventory-binding",reg.get("document_id")=="D10_SCHEMA_REGISTRY_V021" and reg.get("version")=="V021" and refmap(reg.get("source_refs",[]))=={**pinmap,INV.as_posix():blob(ROOT/INV)})
check("D12-23-adapter-exact-current-contracts",adapt.get("document_id")=="D10_ROLE_ADAPTERS_V016" and adapt.get("version")=="V016" and adapt.get("version_pins",{}).get("schema_registry")==REG.name and adapt.get("version_pins",{}).get("promotion_inventory")==INV.name)
# Current cycle and manifest are not created by this validation package.
check("D12-24-no-C35-C36-or-manifest-created",not (ROOT/"novydres/chronicles/CHR-001/orchestration/CYCLE_V0035.json").exists() and not (ROOT/"novydres/chronicles/CHR-001/orchestration/CYCLE_V0036.json").exists() and not (ROOT/"novydres/MANIFEST_V49.json").exists() and not (ROOT/"novydres/MANIFEST_V50.json").exists())
control={x.get("path"):x for x in inv.get("publication_control_set",[]) if isinstance(x,dict)}
control_required=("novydres/runtime/narrative-architecture/program/deliverables/D10_SCHEMA_REGISTRY_V021.json","novydres/runtime/narrative-architecture/program/deliverables/D10_ROLE_ADAPTERS_V016.json","novydres/runtime/narrative-architecture/program/deliverables/D10_TEST_RESULTS_V023.json","novydres/runtime/narrative-architecture/program/deliverables/D12_RELEASE_CANDIDATE_V019.json","novydres/runtime/narrative-architecture/program/deliverables/D12_VALIDATE_V018_RESULT.json","novydres/runtime/narrative-architecture/program/deliverables/D12_PROMOTION_INVENTORY_V005_PLAYER_SAFE.json")
check("D12-25-publication-control-set-acyclic",all(control.get(p,{}).get("action") in ("ADD","SELF_ADD") and control.get(p,{}).get("hash_policy")=="OMITTED_IN_INVENTORY_TO_AVOID_HASH_CYCLE" and control.get(p,{}).get("hash_fixed_by")=="D12_PUBLICATION_READBACK_V002_PLAYER_SAFE.json" for p in control_required))
passed=sum(ok for _,ok in checks); failed=[code for code,ok in checks if not ok]
report={"document_id":"D12_VALIDATE_V018_RESULT","validator":"D12_VALIDATE_V018.py","version":"V018","status":"PASS" if not failed else "FAIL","checks_passed":passed,"checks_total":len(checks),"failed_check_ids":failed,"baseline_master_head_sha":base,"promotion_counts":{"ADD":sum(1 for x in promos if x.get("action")=="ADD"),"UPDATE":sum(1 for x in promos if x.get("action")=="UPDATE"),"already_present":len(already),"excluded":len(excluded)},"artifact_blobs":{"inventory":blob(ROOT/INV),"candidate":blob(ROOT/CAND),"registry":blob(ROOT/REG),"adapters":blob(ROOT/ADAPT),"D10_result":blob(ROOT/D10R),"D11_result":blob(ROOT/D11R),"D06_source_result":blob(ROOT/D06R)},"operational_state":{"cycle":"CYCLE_V0034","last_event_id":"CHR001-M301-C05-22-20261109-001","last_scene":"C05 CLOSED","next_scene":"C06 NOT_STARTED","protagonist":"MORTAL","embrace_occurred":False,"SCENE_READY":False,"NARRATOR_PERMISSION":False,"D07_activation_effective":False},"limitations":["No C06 cause is currently admitted; no scene readiness is asserted.","The D11 prospective positive-route transition remains unproven until D04 admits a cause.","The full primary rules book is unavailable for final 2010 sheet cost certification; this does not block covered mortal actions."],"result_detail_disclosed":False}
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(1 if failed else 0)

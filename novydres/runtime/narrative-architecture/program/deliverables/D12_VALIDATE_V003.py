#!/usr/bin/env python3
"""Validate the CHR-001 D12 V003 decision and gate delta from the pinned branch base."""
import hashlib, json, subprocess
from pathlib import Path
BASE = "44ba5ade7de825c3f4781c3fc04ca9a510f6b290"
MASTER = "124f9a9f43ed427d3db106d9187a875d74f60ac6"
BRANCH = "design/chr001-narrative-program-d01"
D = Path("novydres/runtime/narrative-architecture/program/deliverables")
CYCLE_DIR = Path("novydres/chronicles/CHR-001/orchestration")
EXPECTED_JSON = [
 "D05_PLAYER_APPROVAL_QUEUE_V003.json", "AUDIT_D05_V004.json", "HANDOFF_D05_V005.json",
 "D06_CHRONICLE_BIBLE_V003.json", "D06_TRANSFORMATION_PATHS_V003.json", "D06_PLAYER_APPROVAL_QUEUE_V003.json", "AUDIT_D06_V003.json", "HANDOFF_D06_V003.json",
 "D07_PLAYER_APPROVAL_QUEUE_V003.json", "AUDIT_D12_V003.json", "HANDOFF_D12_V003.json", "D12_RELEASE_CANDIDATE_V003.json"
]
EXPECTED = {str(D / n) for n in EXPECTED_JSON} | {str(D / "D12_VALIDATE_V003.py")}
checks=[]
def require(i, ok, detail): checks.append({"id":i,"result":"PASS" if ok else "FAIL","detail":detail})
def git(*args): return subprocess.check_output(["git",*args],text=True).strip()
def load(name): return json.loads((D/name).read_text(encoding="utf-8"))
def blob(path):
 b=Path(path).read_bytes(); return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def approve(doc, ident): return next(x for x in doc["decisions"] if x["id"]==ident)

a05=load("D05_PLAYER_APPROVAL_QUEUE_V003.json"); a06=load("D06_PLAYER_APPROVAL_QUEUE_V003.json"); a07=load("D07_PLAYER_APPROVAL_QUEUE_V003.json")
bible=load("D06_CHRONICLE_BIBLE_V003.json"); routes=load("D06_TRANSFORMATION_PATHS_V003.json")
a12=load("AUDIT_D12_V003.json"); h12=load("HANDOFF_D12_V003.json"); rel=load("D12_RELEASE_CANDIDATE_V003.json")
h05=load("HANDOFF_D05_V005.json")
parsed=True
try:
 for name in EXPECTED_JSON: load(name)
except Exception: parsed=False
require("D12V3-01", parsed, "all 12 new JSON artifacts parse")
changed=set(git("diff","--name-only",BASE).splitlines()) | set(git("ls-files","--others","--exclude-standard").splitlines())
require("D12V3-02", changed==EXPECTED, "working/committed paths equal the scoped V003 artifacts")
head=git("rev-parse","HEAD")
require("D12V3-03", git("merge-base","--is-ancestor",BASE,head) == "", "pinned input HEAD is an ancestor of the result")
remote={}
for line in git("ls-remote","origin",f"refs/heads/{BRANCH}","refs/heads/master").splitlines():
 fields=line.split(); remote[fields[1]]=fields[0]
require("D12V3-04", remote.get(f"refs/heads/{BRANCH}") in {BASE,head}, "remote design ref is unchanged base or current result HEAD")
require("D12V3-05", remote.get("refs/heads/master")==MASTER, "master remains at the approved read-only HEAD")
cycle_path="novydres/chronicles/CHR-001/orchestration/CYCLE_V0033.json"
cycle=json.loads(Path(cycle_path).read_text(encoding="utf-8"))
require("D12V3-06", blob(cycle_path)=="51afa7fa15ba7dc49a863dfe6f6bb0c539014a6a" and cycle["sequence"]==33 and cycle["next_role"]=="DRAMATURGO" and cycle["checkpoint"]["mortal"] is True and cycle["checkpoint"]["embrace_occurred"] is False, "latest cycle blob is V0033, READY_FOR_DRAMATURGO, mortal, no Embrace")
chain_ok=True
for n in range(1,34):
 p=CYCLE_DIR/f"CYCLE_V{n:04}.json"; c=json.loads(p.read_text(encoding="utf-8"))
 if c.get("sequence")!=n: chain_ok=False
 if n>1:
  prev=CYCLE_DIR/f"CYCLE_V{n-1:04}.json"
  if c.get("previous_cycle",{}).get("path")!=str(prev) or c.get("previous_cycle",{}).get("blob_sha")!=blob(prev): chain_ok=False
require("D12V3-07", chain_ok, "cycle sequence V0001–V0033 and predecessor paths/blob SHAs verify")
refs_ok=True
for name,ref in cycle.get("refs",{}).items():
 if ref and ref.get("path") and blob(ref["path"])!=ref.get("blob_sha"): refs_ok=False
 if name=="live" and ref:
  live=json.loads(Path(ref["path"]).read_text(encoding="utf-8"))
  if live.get("last_confirmed_event_id")!=cycle["checkpoint"].get("last_event_id"): refs_ok=False
require("D12V3-08", refs_ok, "cycle source refs and LIVE last event verify")
manifest=json.loads(Path("novydres/MANIFEST_V46.json").read_text(encoding="utf-8"))
require("D12V3-09", blob("novydres/MANIFEST_V46.json")=="be1c859bf5ae3f954cb9f0e07caab5c4800728ba" and manifest["runtime"]["orchestration"]["current_cycle"].endswith("CYCLE_V0024.json"), "MANIFEST_V46 blob and V0024 pointer are pinned")
contract=Path("novydres/runtime/orchestration/ORCHESTRATION_CONTRACT_V1.md").read_text(encoding="utf-8")
require("D12V3-10", "cursor VIGENTE é o CYCLE_VNNNN.json de maior sequencial" in contract and "Manifesto e ciclo divergentes geram BLOCKED_CONFLICT" in contract, "contract supports cycle cursor authority and preserves divergence blocker")
require("D12V3-11", approve(a05,"APPROVAL-D05-001")["status"]=="CURSOR_AUTHORITY_ADJUDICATED_BLOCKER_REMAINS" and "CYCLE_V0033" in approve(a05,"APPROVAL-D05-001")["investigation_result"]["current_cycle"]["path"], "D05-001 selects CYCLE authority and keeps operational blocker")
require("D12V3-12", approve(a05,"APPROVAL-D05-002")["status"]=="APPROVED_PENDING_GATES" and approve(a05,"APPROVAL-D05-002")["promotion_performed"] is False, "D05-002 records future promotion approval without promotion")
require("D12V3-13", approve(a05,"APPROVAL-D05-003")["status"]=="COMMITMENT_RECORDED_BLOCKER_REMAINS" and approve(a05,"APPROVAL-D05-004")["status"]=="NOT_GRANTED", "D05-003 commitment is not ACL; no scene permission")
inherited={x["id"]:x for x in a06["decisions"] if x["id"].startswith("APPROVAL-D05-")}
require("D12V3-25", inherited["APPROVAL-D05-001"]["status"]=="CURSOR_AUTHORITY_ADJUDICATED_BLOCKER_REMAINS" and inherited["APPROVAL-D05-002"]["status"]=="APPROVED_PENDING_GATES" and inherited["APPROVAL-D05-003"]["status"]=="COMMITMENT_RECORDED_BLOCKER_REMAINS" and inherited["APPROVAL-D05-004"]["status"]=="NOT_GRANTED", "D06 inherited queue carries current D05 decisions")
d=approve(a06,"APPROVAL-D06-001")
require("D12V3-14", d["status"]=="DECIDED_TARGET_BLOCKED_CONFLICT" and d["selected_target"]=="Abraço vampírico antes de 1970-12-25", "D06-001 target is explicit and remains blocked")
require("D12V3-15", "ingressar, entender e se adaptar" in d["response"] and "sociedade cainita" in d["response"], "player's adaptation rationale is recorded")
sel="novydres/chronicles/CHR-001/character/FUTURE_SIRE_PLAYER_SELECTION_V1.json"
selection=json.loads(Path(sel).read_text(encoding="utf-8"))
require("D12V3-16", selection["selection"]["future_sire_name_exact"]=="Kuthulun" and bible["player_intent"]["sire"].startswith("Kuthulun"), "Kuthulun is retained as player-selected future sire")
state_path=cycle["refs"]["character"]["path"]; episode_path=cycle["refs"]["episode"]["path"]
state=Path(state_path).read_text(encoding="utf-8").lower(); episode=Path(episode_path).read_text(encoding="utf-8").lower()
require("D12V3-17", "fim dos anos 1970" in state and "mortal" in state and "nenhum abraço" in state, "linked character state documents late-1970s mortal/no Embrace")
require("D12V3-18", "fim dos anos 1970" in episode and "sem abraço" in episode, "linked episode independently preserves late-1970s no Embrace")
require("D12V3-19", bible["operational_target_gate"]=="BLOCKED_CONFLICT" and routes["routes"][0]["status"]=="PLAYER_SELECTED_TARGET_BLOCKED_CONFLICT" and d["actual_event"]=="NOT_ESTABLISHED", "chronology conflict remains blocked without retcon/event")
d7=approve(a07,"APPROVAL-D07-001")
require("D12V3-20", d7["status"]=="APPROVED_PENDING_SOURCE_RECONCILIATION" and d7["player_response"]=="Uso operacional.", "D07 future operational consideration remains conditional")
require("D12V3-26", all(blob(ref["path"])==ref["blob_sha"] for ref in a07["source_refs"][-3:]), "D07 follow-up source refs pin the latest D05/D06 records")
require("D12V3-21", a12["operational_gate"]=="BLOCKED_CONFLICT" and a12["operational_release"]=="AUTHORIZED_PENDING_GATES" and a12["promotion_performed"] is False, "D12 keeps approval separate from operational release")
require("D12V3-22", rel["status"]=="BLOCKED_CONFLICT" and rel["narrator_status"]=="NOT_READY_FOR_NARRATOR" and rel["promotion_performed"] is False, "release candidate blocks promotion and Narrator")
require("D12V3-27", rel["pending_decisions"]==[] and rel["authorizations"]["promotion_to_operational_use"] is True and rel["authorizations"]["master_write"] is False, "all player decisions are recorded; future promotion is approved but no master write occurred")
require("D12V3-23", h12["narrator_release"]=="NOT_READY_FOR_NARRATOR" and "Sem retcon, cena ou prompt" in h12["next_action"], "handoff preserves no-scene/no-Narrator boundary")
require("D12V3-24", a12["readback"]["D12"].startswith("PENDING_REMOTE_READBACK") and h12["publication_readback"]["status"]=="PENDING", "remote readback remains pending until push")
require("D12V3-28", h05["publication_readback"]["status"]=="PENDING" and h05["prior_readback_evidence"]["record_after_push"]["commit"]=="38ed1270d83a3fc31ab05fc881535849f3045211", "D05 handoff separates prior readback from this version's pending readback")
failed=[x for x in checks if x["result"]!="PASS"]
print(json.dumps({"result":"FAIL" if failed else "PASS","checks_passed":len(checks)-len(failed),"checks_total":len(checks),"failures":failed,"assertions":checks},ensure_ascii=False,indent=2))
raise SystemExit(1 if failed else 0)

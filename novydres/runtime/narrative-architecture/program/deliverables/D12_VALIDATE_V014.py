#!/usr/bin/env python3
"""Release integrity gate for the current CHR-001 design package; no operational writes."""
from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
DEL=Path('novydres/runtime/narrative-architecture/program/deliverables')
checks=[]
def require(label,ok):
 if not ok: raise SystemExit(f'D12_V014_BLOCK: check_{len(checks)+1:03d}')
 checks.append(label)
def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
try:
 candidate=load(DEL/'D12_RELEASE_CANDIDATE_V018.json')
 d10=load(DEL/'D10_TEST_RESULTS_V016.json')
 d11=load(DEL/'D11_TEST_RESULTS_V014_PLAYER_SAFE.json')
 review=load(DEL/'D11_INDEPENDENT_REVIEW_V009_GM_HIDDEN.json')
 review_status=load(DEL/'D11_REVIEW_STATUS_V010_PLAYER_SAFE.json')
 cases=load(DEL/'D11_ADVERSARIAL_CASES_V014_GM_HIDDEN.json')
 registry=load(DEL/'D10_SCHEMA_REGISTRY_V016.json')
 cycle=load('novydres/chronicles/CHR-001/orchestration/CYCLE_V0034.json')
 live=load('novydres/chronicles/CHR-001/LIVE_v038.json')
except Exception as exc:
 raise SystemExit(f'D12_V014_BLOCK: input read/parse failed ({type(exc).__name__})')
required_outputs=set(registry.get('catalog',[])) | {'D12_RELEASE_CANDIDATE_V018.json','D12_VALIDATE_V014.py','D12_VALIDATE_V014_RESULT.json','PROGRAM_EXECUTION_LOG_V002_PLAYER_SAFE.md'}
require('candidate identity and version',candidate.get('document_id')=='D12_RELEASE_CANDIDATE_V018' and candidate.get('version')=='V018')
require('release output catalog includes current package',required_outputs.issubset(set(candidate.get('outputs',[]))))
for output in candidate.get('outputs',[]):
 path=ROOT/output if output.startswith('novydres/') else ROOT/DEL/output
 require('release output exists',path.is_file())
require('D10 current execution passes',d10.get('status')=='PASS' and d10.get('checks_passed')==d10.get('checks_total') and d10.get('checks_total',0)>0)
require('D10 source reconciliation passes',d10.get('source_validation',{}).get('status')=='PASS' and d10.get('source_validation',{}).get('checks_passed')==33 and d10.get('source_validation',{}).get('checks_total')==33)
require('D11 seeded contract reducer passes',d11.get('status')=='PASS' and d11.get('cases_total')==29 and d11.get('passed')==29 and d11.get('failed')==0 and d11.get('scenes_played')==0 and d11.get('persistent_state_mutated') is False)
case_path=ROOT/DEL/'D11_ADVERSARIAL_CASES_V014_GM_HIDDEN.json'
runner_path=ROOT/DEL/'D11_EXECUTE_ADVERSARIAL_V014.py'
case_raw=case_path.read_bytes()
case_blob=hashlib.sha1(b'blob '+str(len(case_raw)).encode()+b'\0'+case_raw).hexdigest()
runner_sha=hashlib.sha256(runner_path.read_bytes()).hexdigest()
require('D11 result binds exact cases and runner',d11.get('input_artifact_refs')==[{'path':'novydres/runtime/narrative-architecture/program/deliverables/D11_ADVERSARIAL_CASES_V014_GM_HIDDEN.json','blob_sha':case_blob}] and d11.get('runner_source_sha256')==runner_sha)
case_ids={case['id'] for case in cases.get('cases',[])}
require('independent review covers all current cases',review.get('status')=='PASS_WITH_LIMITATION' and set(review.get('reviewed_case_ids',[]))==case_ids)
require('player-safe review status has no open findings',review_status.get('status')=='PASS_WITH_LIMITATION' and review_status.get('case_count')==len(case_ids) and review_status.get('open_findings')==0)
require('candidate reflects executed D10 and D11 gates',candidate.get('gates',{}).get('D10_current_execution')==f"PASS_{d10['checks_passed']}_OF_{d10['checks_total']}" and candidate.get('gates',{}).get('D11_independent_review')=='PASS_WITH_LIMITATION_29_OF_29')
require('cycle remains at C05 with C06 not started',cycle.get('checkpoint',{}).get('last_event_id')=='CHR001-M301-C05-22-20261109-001' and cycle.get('checkpoint',{}).get('next_scene_status')=='NOT_STARTED')
require('current state stays mortal and no-Embrace',live.get('stage',{}).get('embrace_occurred') is False and '1970' in live.get('stage',{}).get('diegetic_period',''))
require('candidate withholds all operational authorization',candidate.get('narrator_prompt') is None and candidate.get('authorizations',{}).get('scene_execution') is False and candidate.get('authorizations',{}).get('narrator_permission') is False and candidate.get('authorizations',{}).get('D07_activation') is False and candidate.get('authorizations',{}).get('master_write') is False)
require('all operational readiness flags remain false',candidate.get('gates',{}).get('SCENE_READY')=='FALSE' and candidate.get('gates',{}).get('NARRATOR_PERMISSION')=='FALSE' and candidate.get('gates',{}).get('D07_activation')=='NOT_GRANTED')
source_result=subprocess.run([sys.executable,str(ROOT/DEL/'D06_SOURCE_VALIDATE_V003.py'),str(ROOT)],capture_output=True,text=True)
source=json.loads(source_result.stdout) if source_result.returncode==0 else {}
require('source validator reruns successfully',source_result.returncode==0 and source.get('status')=='PASS' and source.get('checks_passed')==33)
report={'validator':'D12_VALIDATE_V014.py','version':'V014','status':'PASS','checks_passed':len(checks),'checks_total':len(checks),'d10_checks':d10.get('checks_total'),'source_checks':source.get('checks_total'),'d11_cases':len(case_ids),'d11_review':'PASS_WITH_LIMITATION','scene_ready':False,'narrator_permission':False,'D07_activation':False,'publication_readback':'PENDING'}
print(json.dumps(report,ensure_ascii=False,indent=2))

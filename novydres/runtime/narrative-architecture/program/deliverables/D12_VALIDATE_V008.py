#!/usr/bin/env python3
import hashlib,json,re
from pathlib import Path
D=Path(__file__).resolve().parent
ROOT=D.parents[4]
checks=[]
def ck(ok,label):
 checks.append(label)
 if not ok: raise SystemExit('D12_V008_BLOCK: '+label)
def read(rel): return (ROOT/rel).read_text(encoding='utf-8')
def j(rel): return json.loads(read(rel))
def sha(path):
 b=Path(path).read_bytes(); return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
DEL='novydres/runtime/narrative-architecture/program/deliverables/'
# Direct validator evidence
sv=j(DEL+'D06_SOURCE_VALIDATE_V003_RESULT.json')
ck(sv['status']=='PASS' and sv['checks_passed']==33 and sv['checks_total']==33,'D06 source validator 33/33')
ck(sv['validator']=='D06_SOURCE_VALIDATE_V003.py','D06 validator version')
cycle=j('novydres/chronicles/CHR-001/orchestration/CYCLE_V0034.json')
prev=j('novydres/chronicles/CHR-001/orchestration/CYCLE_V0033.json')
manifest=j('novydres/MANIFEST_V48.json')
live=j('novydres/chronicles/CHR-001/LIVE_v038.json')
idx=j('novydres/chronicles/CHR-001/HISTORY_INDEX_v038.json')
ck(cycle['transition']=='SOURCE_RECONCILED' and cycle['sequence']==34,'source-only transition V0034')
ck(cycle['checkpoint']['last_event_id']==prev['checkpoint']['last_event_id']=='CHR001-M301-C05-22-20261109-001','last event preserved at C05')
ck(cycle['checkpoint']['last_closed_scene']=='C05' and cycle['checkpoint']['next_scene']=='C06' and cycle['checkpoint']['next_scene_status']=='NOT_STARTED','C05/C06 cursor')
ck(cycle['next_role']=='DRAMATURGO' and cycle['checkpoint']['mortal'] is True and cycle['checkpoint']['embrace_occurred'] is False,'role and mortal state')
ck(manifest['runtime']['orchestration']['current_cycle'].endswith('CYCLE_V0034.json'),'MANIFEST_V48 current pointer')
ck(manifest['runtime']['orchestration']['next_scene_executable'] is False,'manifest does not enable a scene')
ck(live['scene']['last_event_id']==cycle['checkpoint']['last_event_id'] and live['stage']['embrace_occurred'] is False and '1970' in live['stage']['diegetic_period'],'LIVE aligned; no Embrace')
ck(idx['entrypoints']['current_episode'].endswith('M3.01_v006.source.txt') and idx['entrypoints']['current_character_state'].endswith('state_v044.source.txt'),'index points to current source versions')
# Orchestration run records
ov=json.loads(read('novydres/runtime/orchestration/ORCHESTRATION_V4_VALIDATION_RESULT.json'))
otest=json.loads(read('novydres/runtime/orchestration/ORCHESTRATION_TESTS_V4_RESULT.json'))
ck(ov['status']=='PASS' and ov['transition']=='SOURCE_RECONCILED','ORCHESTRATION_VALIDATOR_V4 result')
ck(ov['validator_blob_sha']==sha(ROOT/'novydres/runtime/orchestration/ORCHESTRATION_VALIDATOR_V4.mjs'),'V4 validator hash recorded')
ck(otest['status']=='PASS' and otest['passed']==7 and otest['total']==7,'ORCHESTRATION_TESTS_V4 result 7/7')
ck(otest['validator_blob_sha']==sha(ROOT/'novydres/runtime/orchestration/ORCHESTRATION_TESTS_V4.mjs'),'V4 test source hash recorded')
# Current decisions and history distinction
q5=j(DEL+'D05_PLAYER_APPROVAL_QUEUE_V006.json')
q6=j(DEL+'D06_PLAYER_APPROVAL_QUEUE_V007.json')
q7=j(DEL+'D07_PLAYER_APPROVAL_QUEUE_V005.json')
bible=j(DEL+'D06_CHRONICLE_BIBLE_V007.json')
rec=j(DEL+'D06_SOURCE_RECONCILIATION_V003.json')
variant=j(DEL+'D12_PLAYER_OPEN_VARIANT_V001.json')
ck(next(x for x in q5['decisions'] if x['id']=='APPROVAL-D05-002')['status'].startswith('APPROVED_CONDITIONALLY'),'D05-002 authorization is conditional')
ck('CYCLE_V0034' in str(next(x for x in q5['decisions'] if x['id']=='APPROVAL-D05-001')['investigation_result']['current_cycle']['path']),'D05 pointer reconciled')
ck(next(x for x in q6['decisions'] if x['id']=='APPROVAL-D06-001')['status']=='SUPERSEDED_BY_APPROVAL-D06-002_FOR_TEMPORAL_SCOPE','old D06 decision marked historical')
ck(bible['player_intent']['approval_id']=='APPROVAL-D06-002' and '1970' in bible['player_intent']['target_window'],'Bible current chronology')
ck(bible['graduation_gate']['status']=='NOT_MET_LONG_RANGE_REQUIREMENTS','long-range graduation is not mistaken for promotion conflict')
ck(bible['operational_target_gate']=='SOURCE_RECONCILED_FOR_DRAMATURGE_PLANNING','planning gate current')
ck(rec['gate_disposition']['documentary_evidence']=='PASS_WITH_UNKNOWN','reconciliation gate evidence')
ck(variant['status']=='APPROVED_LIMITED_SCOPE' and variant['authorized_scope']=='Dramaturge continuity planning for CHR-001 only','variant limited scope')
ck(next(x for x in q7['decisions'] if x['id']=='APPROVAL-D07-001')['status'].startswith('APPROVED_FOR_FUTURE_CONSIDERATION_AFTER_SOURCE_RECONCILIATION'),'D07 consideration only; activation remains separate')
ck(q7['no_scene_authorization'] is True,'D07 queue grants no scene')
# D11 closure and D12 gate separation
x11=j(DEL+'AUDIT_D11_V002.json'); h11=j(DEL+'HANDOFF_D11_V002.json')
ck(x11['status']=='PASS_WITH_UNKNOWN' and x11['resolved_finding']['status']=='RESOLVED','D11 documentary audit closed')
ck(h11['status']=='PASS_WITH_UNKNOWN','D11 handoff gate')
a12=j(DEL+'AUDIT_D12_V008.json'); h12=j(DEL+'HANDOFF_D12_V008.json'); rel=j(DEL+'D12_RELEASE_CANDIDATE_V008.json')
ck(a12['documentary_gate']=='PASS_WITH_UNKNOWN','D12 documentary gate')
ck(a12['gates']['documentary_promotion']=='PASS_WITH_UNKNOWN_AFTER_DIRECT_VALIDATORS_AND_REMOTE_READBACK','public promotion gate is scoped')
ck(a12['gates']['operational_state']=='SOURCE_RECONCILED_FOR_DRAMATURGE_PLANNING','operational state kept distinct')
ck(a12['gates']['out_of_scope_hidden_truth']=='BLOCKED_EXTERNAL_DEPENDENCY','additional secret dependency remains blocked')
ck(a12['gates']['D07_activation']=='NOT_ACTIVATED' and a12['gates']['SCENE_READY']=='NOT_VERIFIED' and a12['gates']['NARRATOR_PERMISSION']=='NOT_GRANTED','D07/scene/Narrator remain separate')
ck(h12['status']=='PASS_WITH_UNKNOWN' and h12['master_promotion_performed'] is False,'D12 handoff does not claim a master write')
ck(rel['status']=='READY_FOR_PUBLIC_DOCUMENTARY_MASTER_PROMOTION_AFTER_READBACK','release candidate status')
ck(rel['timeline']['M3.01']=='1970' and rel['timeline']['Bartolomeu_during_M3.01']=='MORTAL','release chronology')
ck(rel['authorizations']['promotion_performed'] is False and rel['authorizations']['scene_execution'] is False,'promotion and scene not falsely marked performed')
ck(rel['secret_boundary']['hidden_truth_payloads_in_release'] is False,'no hidden truth payload in release')
# Prompt carries required scope and limits.
prompt=read(DEL+'DRAMATURGO_CONTINUITY_PROMPT_V003.md')
for token,label in [('25/12/1970','forced Embrace deadline'),('C05','last played checkpoint'),('C06','next scene not started'),('Sistema Circulatório','approved carrier direction'),('Kuthulun','selected future sire'),('Bart deve continuar mortal em todas as cenas','mortality boundary'),('SCENE_READY','scene gate distinguished'),('NARRATOR_PERMISSION','Narrator gate distinguished'),('não produza prompt de Narrador','no Narrator prompt'),('PLAYER_OPEN_VARIANT','variant labeled')]: ck(token in prompt,label)
# No current promotion blocker; preserved history may still mention prior blocker strings.
current=[str(q5['promotion_disposition']),str(a12['gates']['documentary_promotion']),str(rel['status']),str(h12['status'])]
ck(all('BLOCKED_CONFLICT' not in x and 'BLOCKED_EXTERNAL_DEPENDENCY' not in x for x in current),'no current public promotion blocker')
result={'validator':'D12_VALIDATE_V008.py','version':'V008','status':'PASS','checks_passed':len(checks),'checks_total':len(checks),'checks':[{'id':f'D12-{i:02d}','label':v,'result':'PASS'} for i,v in enumerate(checks,1)],'inputs':{'design_branch_base':'9148095a273f9fa72a54a49a48651ebf4a54615e','master_base':'735fe5d52e2761c4d492fe873a4b6bbcce17654a','M2.03_v018':sha(ROOT/'novydres/chronicles/CHR-001/episodes/M2.03_v018.source.txt'),'M2.04_v018':sha(ROOT/'novydres/chronicles/CHR-001/episodes/M2.04_v018.source.txt'),'M3.01_v006':sha(ROOT/'novydres/chronicles/CHR-001/episodes/M3.01_v006.source.txt'),'state_v044':sha(ROOT/'novydres/chronicles/CHR-001/character/state_v044.source.txt'),'D06_SOURCE_VALIDATE_V003_result':sha(D/'D06_SOURCE_VALIDATE_V003_RESULT.json'),'ORCHESTRATION_VALIDATOR_V4':sha(ROOT/'novydres/runtime/orchestration/ORCHESTRATION_VALIDATOR_V4.mjs'),'ORCHESTRATION_TESTS_V4':sha(ROOT/'novydres/runtime/orchestration/ORCHESTRATION_TESTS_V4.mjs'),'prompt':sha(D/'DRAMATURGO_CONTINUITY_PROMPT_V003.md')},'validator_blob_sha':sha(Path(__file__))}
(D/'D12_VALIDATE_V008_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'validator':result['validator'],'status':'PASS','checks':f"{len(checks)}/{len(checks)}",'result_path':str(D/'D12_VALIDATE_V008_RESULT.json'),'validator_blob_sha':result['validator_blob_sha']},ensure_ascii=False))

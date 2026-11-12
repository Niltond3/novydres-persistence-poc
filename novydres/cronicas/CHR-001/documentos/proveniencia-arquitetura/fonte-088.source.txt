#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
D='novydres/runtime/narrative-architecture/program/deliverables/'
INV=D+'D12_PROMOTION_INVENTORY_V006_PLAYER_SAFE.json'
CAND=D+'D12_RELEASE_CANDIDATE_V020.json'
D10R=D+'D10_TEST_RESULTS_V024.json'
D10V=D+'D10_VALIDATE_V024.py'
REG=D+'D10_SCHEMA_REGISTRY_V022.json'
AD=D+'D10_ROLE_ADAPTERS_V017.json'
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def sha(p):
    b=(ROOT/p).read_bytes()
    return hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
checks=[]
def ck(label,ok): checks.append({'id':f'D12-{len(checks)+1:02d}','label':label,'result':'PASS' if ok else 'FAIL'})

def main():
    inv,cand,d10=read(INV),read(CAND),read(D10R)
    cycle='novydres/chronicles/CHR-001/orchestration/CYCLE_V0036.json'; manifest='novydres/MANIFEST_V51.json'
    ck('source checkpoint hashes match C36 and M51',inv['source_checkpoint']['cycle_ref']=={'path':cycle,'blob_sha':sha(cycle)} and inv['source_checkpoint']['manifest_ref']=={'path':manifest,'blob_sha':sha(manifest)})
    ck('candidate records only episode closure',cand['document_id']=='D12_RELEASE_CANDIDATE_V020' and cand['scope'].startswith('M3.01 episode-only closure at C05-22'))
    ck('candidate distinguishes route and persistent threads',cand['criteria']['persistent_threads']=='UNCHANGED_AND_CARRIED_FORWARD' and cand['criteria']['route_and_target']=='PENDING_UNCHANGED')
    ck('D10 V024 passes against exact current inventory',d10['status']=='PASS' and d10['checks_passed']==d10['checks_total'] and d10['inputs'].get(INV)==sha(INV) and d10['inputs'].get(D10V)==sha(D10V))
    reg,ad=read(REG),read(AD)
    ck('registry and adapters bind current inventory',any(x['path']==INV and x['blob_sha']==sha(INV) for x in reg['source_refs']) and any(x['path']==INV and x['blob_sha']==sha(INV) for x in ad['source_refs']))
    promotion_paths={x['path'] for x in inv['promotion_files']}
    required=[REG,AD,D10V,D10R,CAND,D+'D12_VALIDATE_V019.py',D+'D12_VALIDATE_V019_RESULT.json', 'novydres/chronicles/CHR-001/orchestration/CYCLE_V0037.json','novydres/MANIFEST_V52.json']
    ck('inventory lists every successor output but does not self-pin',all(p in promotion_paths for p in required) and INV not in promotion_paths)
    historical_sources={cycle,manifest,'novydres/chronicles/CHR-001/knowledge/OPEN_THREADS_V23.json'}
    ck('historical checkpoint and thread ledger remain read-only inputs',not (promotion_paths & historical_sources))
    ck('candidate records the completed D10 and D12 gates',cand['status']=='D12_VALIDATED_CANDIDATE_PENDING_CYCLE_VALIDATION_AND_READBACK' and cand['validation']['D10_V024']=='PASS_16_OF_16' and cand['validation']['D12_V019']=='PASS_13_OF_13')
    expected=[x['path'] for x in inv['pinned_artifacts']]
    ck('all pinned source artifacts exist and match',all((ROOT/p).is_file() for p in expected) and all(x['blob_sha']==sha(x['path']) for x in inv['pinned_artifacts']))
    ck('candidate outputs exist',all((ROOT/p).is_file() for p in cand['outputs']))
    ck('no story, scene, Marco, or Narrator authority',cand['authorizations']['scene_execution'] is False and cand['authorizations']['C06_start'] is False and cand['authorizations']['M3_02'] is False and cand['authorizations']['narrator_permission'] is False and cand['criteria']['scene_ready'] is False)
    ck('D11 remains historical and is not represented as closure validation','D11' not in cand['validation'] and 'D11' in read(REG)['version_gates'])
    ck('transition waits for runtime tests and readback',inv['promotion_plan']['order'][-2:]==['runtime V11 validator/tests PASS','remote readback PASS'] and inv['gate_status']['cycle_transition']=='PENDING_VALIDATION_AND_REMOTE_READBACK')
    result={'document_id':'D12_VALIDATE_V019_RESULT','validator':'D12_VALIDATE_V019.py','version':'V019','status':'PASS' if all(x['result']=='PASS' for x in checks) else 'FAIL','checks_passed':sum(x['result']=='PASS' for x in checks),'checks_total':len(checks),'failed_check_ids':[x['id'] for x in checks if x['result']=='FAIL'],'checks':checks,'artifact_blobs':{'inventory':sha(INV),'candidate':sha(CAND),'D10_validator':sha(D10V),'D10_result':sha(D10R),'D12_validator':sha(D+'D12_VALIDATE_V019.py'),'registry':sha(REG),'adapters':sha(AD)},'operational_state':{'source_cycle':'CYCLE_V0036','event_id':'CHR001-M301-C05-22-20261109-001','C06':'NOT_STARTED_NOT_DECLINED','M3.01_episode':'CLOSURE_CANDIDATE','guided_creation_route':'PENDING','scene_ready':False,'narrator_permission':False},'D11':'HISTORICAL_ONLY_NOT_A_CLOSURE_GATE','result_detail_disclosed':False}
    out=ROOT/(D+'D12_VALIDATE_V019_RESULT.json'); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'validator':result['validator'],'status':result['status'],'checks':f"{result['checks_passed']}/{result['checks_total']}",'result':str(out)}))
    if result['status']!='PASS': sys.exit(1)
if __name__=='__main__': main()

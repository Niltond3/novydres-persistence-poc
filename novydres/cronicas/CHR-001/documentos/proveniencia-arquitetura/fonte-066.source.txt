#!/usr/bin/env python3
import hashlib, json, subprocess, sys
from pathlib import Path

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
D='novydres/runtime/narrative-architecture/program/deliverables/'
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def sha(p):
    b=(ROOT/p).read_bytes()
    return hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
def ref(p): return {'path':p,'blob_sha':sha(p)}
checks=[]
def ck(label,ok): checks.append({'id':f'D10-{len(checks)+1:02d}','label':label,'result':'PASS' if ok else 'FAIL'})

def main():
    d6p=D+'D06_CHRONICLE_BIBLE_V031.json'; d8p=D+'D08_STORY_PREPARATION_V021_GM_HIDDEN.md'; d9p=D+'D09_GUIDED_CREATION_PROGRESSION_V024_PLAYER_SAFE.json'
    dec='novydres/runtime/narrative-architecture/program/decisions/PLAYER_DECISION_M301_EPISODIC_CLOSURE_V001_PLAYER_SAFE.json'
    inv=D+'D12_PROMOTION_INVENTORY_V006_PLAYER_SAFE.json'; regp=D+'D10_SCHEMA_REGISTRY_V022.json'; adp=D+'D10_ROLE_ADAPTERS_V017.json'
    c36='novydres/chronicles/CHR-001/orchestration/CYCLE_V0036.json'; m51='novydres/MANIFEST_V51.json'; thr='novydres/chronicles/CHR-001/knowledge/OPEN_THREADS_V23.json'
    runtime=['novydres/runtime/orchestration/ORCHESTRATION_CONTRACT_V9.md','novydres/runtime/orchestration/CYCLE_SCHEMA_V11.json','novydres/runtime/orchestration/ORCHESTRATION_VALIDATOR_V11.mjs','novydres/runtime/orchestration/ORCHESTRATION_TESTS_V11.mjs','novydres/runtime/orchestration/ORCHESTRATION_SCHEMA_TESTS_V11.py','novydres/runtime/orchestration/START_HERE_V8.md']
    d6,d9,decision,c,ledger=read(d6p),read(d9p),read(dec),read(c36),read(thr)
    head=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()
    ck('source HEAD is approved master parent',head=='cb9aa9e422fb0327e04e9eb0929e4ab678785405')
    ck('C36 is latest source cycle',not (ROOT/'novydres/chronicles/CHR-001/orchestration/CYCLE_V0037.json').exists())
    ck('C36 manifest and checkpoint reconcile',c['sequence']==36 and c['manifest_ref']==ref(m51) and c['checkpoint']['last_event_id']=='CHR001-M301-C05-22-20261109-001')
    ck('decision is explicit and episode-only',decision['decision']=='CLOSE_M3_01_EPISODIC_ALTERNATE' and decision['scope']=='M3.01_EPISODE_ONLY' and decision['checkpoint_event_id']==c['checkpoint']['last_event_id'])
    ck('decision preserves exact thread ledger',decision['preserved_threads_ref']==ref(thr) and c['refs']['threads']==ref(thr) and bool(ledger.get('threads')))
    ck('D06 episode gate evidence is satisfied',d6['document_id']=='D06_CHRONICLE_BIBLE_V031' and d6['finite_progression']['episode_closure_gate']['status']=='SATISFIED_FOR_M3_01_EPISODE_ONLY')
    ck('D06 keeps route disposition independent',d6['authorial_decisions']['episode_boundary']['scope'].startswith('Episode only; no route-level disposition') and d6['finite_progression']['episode_closure_gate']['scope'].startswith('Finite episode boundary only'))
    d8_text=(ROOT/d8p).read_text()
    ck('D08 has no admitted C06 cause or scene','D04 V010 não admite causa para C06' in d8_text and 'não há cena pronta' in d8_text)
    ck('D09 route target remains pending',d9['authorial_target_closure']['status']=='PENDING_UNTIL_ACTUAL_EVIDENCE' and d9['status']=='M3_01_EPISODE_CLOSED_GUIDED_ROUTE_PENDING_THREADS_PRESERVED')
    ck('D09 scene and Narrator gates remain closed',d9['operational_gate']['scene_ready'] is False and d9['operational_gate']['narrator_permission'] is False)
    ck('D09 leaves C06 unstarted and not declined','C06 remains NOT_STARTED' in d9['checkpoint']['episode_boundary'] and 'not an offer or refusal' in d9['target_route']['fallback'])
    reg,ad=read(regp),read(adp); got={x['path']:x['blob_sha'] for x in reg['source_refs']}
    expected={d6p,d8p,d9p,dec,c36,m51,thr,inv,*runtime,'novydres/.AGENT_V4.md','novydres/.CONTEXTG_V3.md','novydres/runtime/narrative-architecture/program/deliverables/D10_VALIDATE_V024.py'}
    ck('D10 registry pins every current source exactly',all(got.get(p)==sha(p) for p in expected) and reg['document_id']=='D10_SCHEMA_REGISTRY_V022')
    pins=ad['version_pins']
    ck('D10 adapters pin exact registry and V9/V11 runtime/docs',ad['document_id']=='D10_ROLE_ADAPTERS_V017' and any(x['path']==regp and x['blob_sha']==sha(regp) for x in ad['source_refs']) and pins['schema_registry']=='D10_SCHEMA_REGISTRY_V022.json' and pins['cycle_schema']=='CYCLE_SCHEMA_V11.json' and pins['cycle_validator']=='ORCHESTRATION_VALIDATOR_V11.mjs' and pins['promotion_inventory']=='D12_PROMOTION_INVENTORY_V006_PLAYER_SAFE.json')
    invd=read(inv)
    ck('inventory binds exact source checkpoint',invd['source_checkpoint']['cycle_ref']==ref(c36) and invd['source_checkpoint']['manifest_ref']==ref(m51) and invd['source_checkpoint']['source_head_sha']==head)
    ck('no scene, state change, or next Marco is authorized',decision['explicit_boundaries'][2].startswith('No new scene') and invd['gate_status']['scene_ready'] is False and invd['gate_status']['narrator_permission'] is False)
    ck('runtime V11 schema declares the new cycle id',read('novydres/runtime/orchestration/CYCLE_SCHEMA_V11.json')['properties']['schema_id']['const']=='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V11')
    result={'document_id':'D10_TEST_RESULTS_V024','validator':'D10_VALIDATE_V024.py','version':'V024','status':'PASS' if all(x['result']=='PASS' for x in checks) else 'FAIL','checks_passed':sum(x['result']=='PASS' for x in checks),'checks_total':len(checks),'failed_check_ids':[x['id'] for x in checks if x['result']=='FAIL'],'checks':checks,'inputs':{p:sha(p) for p in sorted(expected|{regp,adp,'novydres/runtime/narrative-architecture/program/deliverables/D10_VALIDATE_V024.py'})},'operational_state':{'cycle':'CYCLE_V0036','last_event_id':c['checkpoint']['last_event_id'],'C06':'NOT_STARTED','episode_closure':'AUTHORIZED_PENDING_CYCLE_VALIDATION','guided_creation_route':'PENDING','scene_ready':False,'narrator_permission':False},'result_detail_disclosed':False}
    out=ROOT/(D+'D10_TEST_RESULTS_V024.json'); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'validator':result['validator'],'status':result['status'],'checks':f"{result['checks_passed']}/{result['checks_total']}",'result':str(out)}))
    if result['status']!='PASS': sys.exit(1)
if __name__=='__main__': main()

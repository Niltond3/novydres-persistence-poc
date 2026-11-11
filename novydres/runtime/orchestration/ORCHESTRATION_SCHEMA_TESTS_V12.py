#!/usr/bin/env python3
import json,sys
from pathlib import Path
from jsonschema import Draft202012Validator
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
p=lambda x:root/x
def load(x):return json.loads(p(x).read_text(encoding='utf-8'))
cs=load('novydres/runtime/orchestration/CYCLE_SCHEMA_V12.json')
ds=load('novydres/runtime/provocation-prep/PROVOCATION_DOSSIER_SCHEMA_V7.json')
ss=load('novydres/runtime/provocation-prep/PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V7.json')
cycle=load('novydres/chronicles/CHR-001/orchestration/CYCLE_V0038.json')
dossier=load('novydres/chronicles/CHR-001/preparations/M3.02_DOSSIER_V1.json')
sidecar=load('novydres/chronicles/CHR-001/preparations/M3.02_LONGITUDINAL_SIDECAR_V1.json')
for schema in [cs,ds,ss]:Draft202012Validator.check_schema(schema)
validators=[Draft202012Validator(s) for s in [cs,ds,ss]]
for v,x in zip(validators,[cycle,dossier,sidecar]):
 errors=list(v.iter_errors(x))
 assert not errors,[(list(e.path),e.message) for e in errors]
cases=0
def bad(v,x,change):
 global cases
 y=json.loads(json.dumps(x));change(y)
 assert list(v.iter_errors(y)), 'invalid fixture mistakenly accepted'
 cases+=1
bad(validators[0],cycle,lambda j:j['checkpoint'].__setitem__('last_event_id','fabricated'))
bad(validators[0],cycle,lambda j:j['operational_gates'].__setitem__('narrator_permission',True))
bad(validators[0],cycle,lambda j:j.__setitem__('status','READY_FOR_NARRATOR'))
bad(validators[0],cycle,lambda j:j['administrative_opening'].__setitem__('new_scene_started',True))
bad(validators[0],cycle,lambda j:j.__setitem__('episode_closure',{}))
bad(validators[0],cycle,lambda j:j['administrative_opening'].__setitem__('guided_route_pending',False))
bad(validators[1],dossier,lambda j:j['first_incident'].__setitem__('actual_cause_present',True))
bad(validators[1],dossier,lambda j:j['first_scene_review'].__setitem__('scene_ready',True))
bad(validators[1],dossier,lambda j:j['mechanics'].__setitem__('xp_credit_available',10))
bad(validators[1],dossier,lambda j:j['act_contracts'].__setitem__(0,dict(j['act_contracts'][0],xp='GRANTED')))
bad(validators[2],sidecar,lambda j:j['scene_queue'].__setitem__('entry_realized',True))
bad(validators[2],sidecar,lambda j:j.__setitem__('no_new_event',False))
print(json.dumps({'ok':True,'schema_suite':'V12+PREPARATION_V7','positive_docs':3,'negative_cases':cases,'cycle':cycle['cycle_id'],'scene_ready':False,'narrator_permission':False}))

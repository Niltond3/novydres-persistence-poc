#!/usr/bin/env python3
import json,sys
from pathlib import Path
from jsonschema import Draft202012Validator
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
load=lambda p:json.loads((root/p).read_text(encoding='utf-8'))
schema=load('novydres/runtime/orchestration/CYCLE_SCHEMA_V13.json')
ds=load('novydres/runtime/provocation-prep/PROVOCATION_DOSSIER_SCHEMA_V7.json')
ss=load('novydres/runtime/provocation-prep/PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V7.json')
cycle=load('novydres/chronicles/CHR-001/orchestration/CYCLE_V0039.json')
dossier=load('novydres/chronicles/CHR-001/preparations/M3.02_DOSSIER_V1.json')
sidecar=load('novydres/chronicles/CHR-001/preparations/M3.02_LONGITUDINAL_SIDECAR_V1.json')
for s in [schema,ds,ss]:Draft202012Validator.check_schema(s)
vs=[Draft202012Validator(s) for s in [schema,ds,ss]]
for v,doc in zip(vs,[cycle,dossier,sidecar]):
 errors=list(v.iter_errors(doc))
 assert not errors,[(list(x.path),x.message) for x in errors]
count=0
def reject(v,obj,mut):
 global count
 d=json.loads(json.dumps(obj));mut(d)
 assert list(v.iter_errors(d)), 'bad mutation passed schema'
 count+=1
reject(vs[0],cycle,lambda x:x['checkpoint'].__setitem__('last_event_id','fake'))
reject(vs[0],cycle,lambda x:x['operational_gates'].__setitem__('narrator_permission',True))
reject(vs[0],cycle,lambda x:x['operational_gates'].__setitem__('scene_ready',True))
reject(vs[0],cycle,lambda x:x['causal_handoff'].__setitem__('future_incident_realized',True))
reject(vs[0],cycle,lambda x:x['causal_handoff'].__setitem__('pc_action_assumed',True))
reject(vs[0],cycle,lambda x:x['causal_handoff'].__setitem__('elapsed_time_or_travel',True))
reject(vs[0],cycle,lambda x:x['causal_handoff'].__setitem__('npc_presence_assumed',True))
reject(vs[0],cycle,lambda x:x['causal_handoff'].__setitem__('intention_executed',True))
reject(vs[0],cycle,lambda x:x.__setitem__('pending_player_decision','RETURN_TO_WORKSHOP'))
reject(vs[0],cycle,lambda x:x.__setitem__('status','READY_FOR_NARRATOR'))
reject(vs[0],cycle,lambda x:x.__setitem__('administrative_opening',{}))
reject(vs[1],dossier,lambda x:x['first_incident'].__setitem__('actual_cause_present',True))
reject(vs[1],dossier,lambda x:x['first_scene_review'].__setitem__('scene_ready',True))
reject(vs[2],sidecar,lambda x:x['scene_queue'].__setitem__('entry_realized',True))
reject(vs[2],sidecar,lambda x:x.__setitem__('no_new_event',False))
print(json.dumps({'ok':True,'positive_docs':3,'negative_cases':count,'schema':'CYCLE_V13 with Dossier/Sidecar V7','narrator_permission':False}))

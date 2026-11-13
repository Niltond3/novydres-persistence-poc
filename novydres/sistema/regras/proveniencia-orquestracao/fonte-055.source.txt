#!/usr/bin/env python3
import json,sys
from pathlib import Path
from jsonschema import Draft202012Validator
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
read=lambda p:json.loads((root/p).read_text(encoding='utf-8'))
schemas=[
 read('novydres/runtime/orchestration/CYCLE_SCHEMA_V14.json'),
 read('novydres/runtime/provocation-prep/PROVOCATION_DOSSIER_SCHEMA_V8.json'),
 read('novydres/runtime/provocation-prep/PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V8.json')
]
objects=[
 read('novydres/chronicles/CHR-001/orchestration/CYCLE_V0040.json'),
 read('novydres/chronicles/CHR-001/preparations/M3.02_DOSSIER_V2.json'),
 read('novydres/chronicles/CHR-001/preparations/M3.02_LONGITUDINAL_SIDECAR_V2.json')
]
for s in schemas:Draft202012Validator.check_schema(s)
validators=[Draft202012Validator(s) for s in schemas]
for validator,obj in zip(validators,objects):
 issues=list(validator.iter_errors(obj))
 assert not issues, [(list(z.path),z.message) for z in issues]
cases=0
def reject(i,mutation):
 global cases
 a=json.loads(json.dumps(objects[i]));mutation(a)
 assert list(validators[i].iter_errors(a)), 'invalid fixture accepted'
 cases+=1
reject(0,lambda x:x.__setitem__('status','INTENTION_PENDING'))
reject(0,lambda x:x.__setitem__('pending_player_decision','NEXT_INTENTION_FROM_C05_22'))
reject(0,lambda x:x['operational_gates'].__setitem__('scene_ready',False))
reject(0,lambda x:x['operational_gates'].__setitem__('narrator_permission',False))
reject(0,lambda x:x['scene_frame'].__setitem__('elapsed_time_persisted',True))
reject(0,lambda x:x['scene_frame'].__setitem__('pc_travel_assumed',True))
reject(0,lambda x:x['scene_frame'].__setitem__('consequential_pc_action_assumed',True))
reject(0,lambda x:x['scene_frame'].__setitem__('npc_contact_already_recorded',True))
reject(0,lambda x:x['scene_frame'].__setitem__('future_incident_realized',True))
reject(0,lambda x:x['scene_frame'].__setitem__('scene_started',True))
reject(0,lambda x:x['scene_frame'].__setitem__('meaningful_choice_available',False))
reject(0,lambda x:x['checkpoint'].__setitem__('last_event_id','fabricated'))
reject(1,lambda x:x['first_incident'].__setitem__('actual_cause_present',True))
reject(1,lambda x:x['first_incident'].__setitem__('scene_ready',False))
reject(1,lambda x:x['causal_guards'].__setitem__('no_elapsed_time',False))
reject(1,lambda x:x['causal_guards'].__setitem__('no_pc_action',False))
reject(1,lambda x:x['temporal_framing'].__setitem__('mode','LITERAL_EVERY_DAY'))
reject(2,lambda x:x['scene_queue'].__setitem__('entry_realized',True))
reject(2,lambda x:x['scene_queue'].__setitem__('narrator_permission',False))
reject(2,lambda x:x['causal_entry'].__setitem__('player_must_unload',True))
reject(2,lambda x:x['causal_entry'].__setitem__('event_realized',True))
reject(2,lambda x:x.__setitem__('no_new_event',False))
print(json.dumps({'ok':True,'schema':'V14 plus dossier and sidecar V8','positive_docs':3,'negative_cases':cases,'scene_ready':True,'scene_started':False}))

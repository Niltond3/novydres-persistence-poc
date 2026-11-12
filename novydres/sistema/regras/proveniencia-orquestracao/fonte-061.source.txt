import json,copy
from pathlib import Path
from jsonschema import Draft202012Validator
R=lambda x:json.loads(Path(x).read_text())
P='novydres/chronicles/CHR-001/'
m=R('novydres/MANIFEST_V63.json');c=R(P+'orchestration/CYCLE_V0045.json');d=R(P+'preparations/M3.02_DOSSIER_V6.json');s=R(P+'preparations/M3.02_LONGITUDINAL_SIDECAR_V6.json')
C=R('novydres/runtime/orchestration/CYCLE_SCHEMA_V22.json');D=R('novydres/runtime/provocation-prep/PROVOCATION_DOSSIER_SCHEMA_V12.json');S=R('novydres/runtime/provocation-prep/PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V12.json')
for sh,obj in [(C,c),(D,d),(S,s)]:
 Draft202012Validator.check_schema(sh)
 assert Draft202012Validator(sh).is_valid(obj)
mutations=[
(C,c,lambda x:x.update(status='READY_FOR_DRAMATURGO')),
(C,c,lambda x:x.update(narrator_prompt_required=False)),
(C,c,lambda x:x['checkpoint'].update(next_scene_status='STARTED')),
(C,c,lambda x:x['operational_gates'].update(narrator_permission=False)),
(C,c,lambda x:x['causal_gate'].update(c01_recycled=True)),
(C,c,lambda x:x['temporal_gate'].update(mode='ELLIPSIS')),
(D,d,lambda x:x['c02_causal_entry'].update(invitation_delivered=True)),
(D,d,lambda x:x['c02_causal_entry'].update(target_identity_verified=True)),
(D,d,lambda x:x['c02_causal_entry'].update(actual_scene_event=True)),
(D,d,lambda x:x['temporal_decision'].update(significant_ellipsis=True)),
(D,d,lambda x:x['temporal_decision']['threads'].pop()),
(S,s,lambda x:x['scene_queue'].update(scene_ready=False)),
(S,s,lambda x:x['scene_queue'].update(event_created_in_preparation=True))
]
for sh,obj,fn in mutations:
 v=copy.deepcopy(obj);fn(v)
 assert not Draft202012Validator(sh).is_valid(v),'negative not rejected'
assert m['runtime']['orchestration']['current_cycle']==P+'orchestration/CYCLE_V0045.json'
print(json.dumps({'schemas':'PASS','negative_rejected':len(mutations),'negative_total':len(mutations)}))

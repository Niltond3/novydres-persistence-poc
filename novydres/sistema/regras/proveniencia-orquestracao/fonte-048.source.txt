import json,copy
from pathlib import Path
from jsonschema import Draft202012Validator
D=Path('novydres/chronicles/CHR-001/preparations/M3.02_DOSSIER_V5.json')
S=Path('novydres/chronicles/CHR-001/preparations/M3.02_LONGITUDINAL_SIDECAR_V5.json')
A=Path('novydres/runtime/provocation-prep/PROVOCATION_DOSSIER_SCHEMA_V11.json')
B=Path('novydres/runtime/provocation-prep/PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V11.json')
d=json.loads(D.read_text());s=json.loads(S.read_text());a=json.loads(A.read_text());b=json.loads(B.read_text())
for schema,obj in [(a,d),(b,s)]:
 Draft202012Validator.check_schema(schema)
 assert Draft202012Validator(schema).is_valid(obj)
cases=[(a,d,lambda x:x['c02_causal_entry'].update(c01_replay=True)),(a,d,lambda x:x['c02_causal_entry'].update(actual_scene_event=True)),(a,d,lambda x:x['c02_causal_entry'].update(invitation_delivered=True)),(a,d,lambda x:x['temporal_decision'].update(mode='ELLIPSIS')),(a,d,lambda x:x['temporal_decision']['threads'].pop()),(b,s,lambda x:x['scene_queue'].update(narrator_permission=True)),(b,s,lambda x:x['temporal_policy'].update(significant_ellipsis=True))]
for schema,original,mutation in cases:
 x=copy.deepcopy(original);mutation(x)
 assert not Draft202012Validator(schema).is_valid(x),'negative not rejected'
print(json.dumps({'schema':'PASS','negative_rejected':len(cases),'negative_total':len(cases)}))

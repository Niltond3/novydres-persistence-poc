#!/usr/bin/env python3
import pathlib,json,copy
from jsonschema import Draft202012Validator
root=pathlib.Path(__file__).resolve().parents[3]
schema=json.loads((root/'novydres/runtime/orchestration/CYCLE_SCHEMA_V16.json').read_text())
cycle=json.loads((root/'novydres/chronicles/CHR-001/orchestration/CYCLE_V0042.json').read_text())
v=Draft202012Validator(schema)
errors=list(v.iter_errors(cycle))
assert not errors,[(str(e.path),e.message) for e in errors]
for key,value in [('status','READY_FOR_NARRATOR'),('next_role','NARRADOR'),('transition','TEMPORAL_GOVERNANCE_REFINED')]:
 d=copy.deepcopy(cycle);d[key]=value;assert list(v.iter_errors(d))
d=copy.deepcopy(cycle);d['transition_readiness']['effective_narrator_permission']=True;assert list(v.iter_errors(d))
d=copy.deepcopy(cycle);del d['architecture']['temporal_transition_packet'];assert list(v.iter_errors(d))
print(json.dumps({'ok':True,'schema':'V16','negative_cases':5}))

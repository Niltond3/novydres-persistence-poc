#!/usr/bin/env python3
import copy,json,pathlib
from jsonschema import Draft202012Validator
root=pathlib.Path(__file__).resolve().parents[3]
schema=json.loads((root/'novydres/runtime/scene-execution/TEMPORAL_TRANSITION_SCHEMA_V1.json').read_text())
packet=json.loads((root/'novydres/chronicles/CHR-001/preparations/M3.02_TEMPORAL_TRANSITION_V2_PLAYER_SAFE.json').read_text())
v=Draft202012Validator(schema)
errors=list(v.iter_errors(packet))
assert not errors,[(str(e.path),e.message) for e in errors]
for mutate in (
 lambda p:p.pop('thread_dispositions'),
 lambda p:p['prelude'].__setitem__('distinct_test_count',3),
 lambda p:p['source_refs']['live'].__setitem__('blob_sha','bad'),
 lambda p:p.__setitem__('chat_opening_status','unknown'),
):
 x=copy.deepcopy(packet);mutate(x);assert list(v.iter_errors(x))
print(json.dumps({'ok':True,'schema':'TEMPORAL_TRANSITION_V1','packet':'V2','negative_cases':4}))

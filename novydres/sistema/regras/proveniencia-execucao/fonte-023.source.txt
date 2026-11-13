#!/usr/bin/env python3
import copy,json,pathlib
from jsonschema import Draft202012Validator
root=pathlib.Path(__file__).resolve().parents[3]
schema=json.loads((root/'novydres/runtime/scene-execution/TEMPORAL_TRANSITION_SCHEMA_V1.json').read_text())
packet=json.loads((root/'novydres/chronicles/CHR-001/preparations/M3.02_TEMPORAL_TRANSITION_V1_PLAYER_SAFE.json').read_text())
v=Draft202012Validator(schema)
assert not list(v.iter_errors(packet))
bad=copy.deepcopy(packet);del bad['thread_dispositions'];assert list(v.iter_errors(bad))
bad=copy.deepcopy(packet);bad['prelude']['distinct_test_count']=3;assert list(v.iter_errors(bad))
bad=copy.deepcopy(packet);bad['source_refs']['live']['blob_sha']='not-a-sha';assert list(v.iter_errors(bad))
print(json.dumps({'ok':True,'positive_schema':1,'negative_schema_cases':3}))

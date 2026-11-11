#!/usr/bin/env python3
import json,sys
from pathlib import Path
from jsonschema import Draft202012Validator
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
schema=json.loads((root/'novydres/runtime/orchestration/CYCLE_SCHEMA_V11.json').read_text())
cycle=json.loads((root/'novydres/chronicles/CHR-001/orchestration/CYCLE_V0037.json').read_text())
Draft202012Validator.check_schema(schema)
v=Draft202012Validator(schema)
def valid(doc): return not list(v.iter_errors(doc))
assert valid(cycle), 'CYCLE_V0037 rejected by V11 schema'
assert cycle['transition']=='EPISODIC_CLOSURE_APPROVED' and cycle['episode_closure']['scope']=='M3.01_EPISODE_ONLY'
missing=dict(cycle); missing.pop('episode_closure'); assert not valid(missing), 'closure transition accepted without episode_closure'
bad_scope=json.loads(json.dumps(cycle)); bad_scope['episode_closure']['scope']='M3.01_AND_M3.02'; assert not valid(bad_scope), 'schema accepted widened closure scope'
bad_status=json.loads(json.dumps(cycle)); bad_status['status']='READY_FOR_NARRATOR'; assert not valid(bad_status), 'schema accepted Narrator status for closure'
extra=json.loads(json.dumps(cycle)); extra['episode_closure']['offscreen_event']=True; assert not valid(extra), 'schema accepted undeclared event field'
route=json.loads(json.dumps(cycle)); route['episode_closure']['creation_route_disposition']='ALTERNATE'; assert not valid(route), 'schema accepted a route disposition change'
print(json.dumps({'ok':True,'schema_id':schema['$id'],'checks_passed':6,'checks_total':6,'cycle_id':cycle['cycle_id']}))

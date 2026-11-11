#!/usr/bin/env python3
import json,sys
from pathlib import Path
from jsonschema import Draft202012Validator
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
read=lambda p:json.loads((root/p).read_text(encoding='utf-8'))
schema=read('novydres/runtime/orchestration/CYCLE_SCHEMA_V15.json')
data=read('novydres/chronicles/CHR-001/orchestration/CYCLE_V0041.json')
Draft202012Validator.check_schema(schema)
v=Draft202012Validator(schema)
assert not list(v.iter_errors(data)),[(list(e.path),e.message) for e in v.iter_errors(data)]
count=0
def reject(mod):
 global count
 x=json.loads(json.dumps(data))
 mod(x)
 errors=list(v.iter_errors(x))
 assert errors, 'bad temporal fixture accepted'
 count+=1
reject(lambda x:x.__setitem__('transition','SCENE_COMMITTED'))
reject(lambda x:x.__setitem__('status','INTENTION_PENDING'))
reject(lambda x:x.__setitem__('next_role','PLAYER_INTENTION'))
reject(lambda x:x.__setitem__('sequence',40))
reject(lambda x:x.__setitem__('pending_player_decision','NEXT_INTENTION'))
reject(lambda x:x['temporal_governance'].__setitem__('ellipse_per_scene_required',True))
reject(lambda x:x['temporal_governance'].__setitem__('ellipse_per_act_required',True))
reject(lambda x:x['temporal_governance'].__setitem__('ellipse_per_provocation_required',True))
reject(lambda x:x['temporal_governance'].__setitem__('continuity_if_meaningful',False))
reject(lambda x:x['temporal_governance'].__setitem__('world_advances_causally_during_ellipse',False))
reject(lambda x:x['temporal_governance'].__setitem__('prelude_mandatory',True))
reject(lambda x:x['temporal_governance'].__setitem__('prelude_distinct_tests_max',3))
reject(lambda x:x['temporal_governance'].__setitem__('prelude_tests_planned_now',1))
reject(lambda x:x['temporal_governance'].__setitem__('prelude_results_recorded',True))
reject(lambda x:x['temporal_governance'].__setitem__('pc_action_assumed',True))
reject(lambda x:x['temporal_governance'].__setitem__('elapsed_time_recorded',True))
reject(lambda x:x['temporal_governance'].__setitem__('xp_fv_changed',True))
reject(lambda x:x['temporal_governance'].__setitem__('new_event_recorded',True))
reject(lambda x:x['temporal_governance'].__setitem__('scene_started',True))
reject(lambda x:x['operational_gates'].__setitem__('narrator_permission',False))
reject(lambda x:x['checkpoint'].__setitem__('embrace_occurred',True))
reject(lambda x:x['architecture'].__setitem__('role_narrador',{}))
print(json.dumps({'ok':True,'positive_schema':1,'negative_cases':count,'continuity_default_allowed':True,'ellipse_mandatory':False,'prelude_mandatory':False}))

import copy
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / 'novydres'
DP = P / 'chronicles/CHR-001/preparations/M3.02_DOSSIER_V4.json'
SP = P / 'chronicles/CHR-001/preparations/M3.02_LONGITUDINAL_SIDECAR_V4.json'
DS = P / 'runtime/provocation-prep/PROVOCATION_DOSSIER_SCHEMA_V10.json'
SS = P / 'runtime/provocation-prep/PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V10.json'
load = lambda p: json.loads(p.read_text(encoding='utf-8'))
d,s,ds,ss = map(load,(DP,SP,DS,SS))
Draft202012Validator.check_schema(ds)
Draft202012Validator.check_schema(ss)
vd,vs = Draft202012Validator(ds), Draft202012Validator(ss)
assert vd.is_valid(d), list(vd.iter_errors(d))
assert vs.is_valid(s), list(vs.iter_errors(s))
negative = [
('dossier status', lambda x: x.__setitem__('status','READY')),
('wrong C01 source', lambda x: x['source_checkpoint'].__setitem__('last_event_id','CHR001-M301-C05-22-20261109-001')),
('C02 already started', lambda x: x['source_checkpoint'].__setitem__('next_scene_status','STARTED')),
('fake A1 resolution', lambda x: x['act_contracts'][0].__setitem__('status','CLOSED_G28')),
('fabricated cause', lambda x: x['c02_causal_entry'].__setitem__('independent_eligible_cause_confirmed',True)),
('witness claim', lambda x: x['c02_causal_entry'].__setitem__('actor_knowledge_verified',True)),
('C01 replay', lambda x: x['c02_causal_entry'].__setitem__('c01_replay_forbidden',False)),
('narrator grant', lambda x: x['c02_causal_entry'].__setitem__('narrator_permission',True)),
('automatic ellipse', lambda x: x['temporal_decision'].__setitem__('ellipsis_mandatory',True)),
('fabricated temporal pass', lambda x: x['temporal_decision'].__setitem__('gate_ready',True)),
('XP change', lambda x: x['mechanics'].__setitem__('xp_spent',271)),
('META becomes event', lambda x: x['guards'].__setitem__('meta_comment_not_diegetic',False)),
]
neg_side = [
('sidecar ready', lambda x: x['scene_queue'].__setitem__('scene_ready',True)),
('sidecar narrator', lambda x: x['scene_queue'].__setitem__('narrator_permission',True)),
('sidecar elapsed time', lambda x: x['temporal_policy'].__setitem__('post_c01_elapsed_time','ONE_WEEK')),
('sidecar fabricated gate', lambda x: x['temporal_policy'].__setitem__('temporal_gate_ready',True)),
('knowledge mutation', lambda x: x['protected_state'].__setitem__('npc_knowledge_unchanged',False)),
('improper immersion meta', lambda x: x['immersion'].__setitem__('meta_not_event',False)),
]
for name,mutate in negative:
 x=copy.deepcopy(d);mutate(x)
 assert not vd.is_valid(x), 'negative incorrectly accepted: '+name
for name,mutate in neg_side:
 x=copy.deepcopy(s);mutate(x)
 assert not vs.is_valid(x), 'negative incorrectly accepted: '+name
print(json.dumps({'schema_positive':2,'schema_negative_rejected':len(negative)+len(neg_side),'schema_negative_total':len(negative)+len(neg_side),'status':'PASS'}))

#!/usr/bin/env python3
"""Seeded-state contract reducer for D11; never plays or persists a scene."""
from __future__ import annotations
import copy, hashlib, json, sys
from pathlib import Path
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
DEL=Path('novydres/runtime/narrative-architecture/program/deliverables')
def read_json(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def deep_merge(target,overlay):
 for key,value in overlay.items():
  if isinstance(value,dict) and isinstance(target.get(key),dict): deep_merge(target[key],value)
  else: target[key]=copy.deepcopy(value)
 return target
def initial(case):
 state={'episode_m301_open':True,'m302_unlocked':False,'next_scene':'C06','scene_started':False,'scene_ready':False,'narrator_permission':False,'persistent_state_mutated':False,'bart':{'mortal':True,'embrace_recorded':False},'pc_knowledge':{'box_contents':'UNKNOWN'},'npc_knowledge':{},'family':{'identity':'UNKNOWN','location':'UNKNOWN','response':'UNKNOWN'},'optional_story':{'status':'NOT_STARTED'},'route':'TARGET_PENDING','npc_generation':'UNKNOWN','npc_blood_potency':None,'transition':{'allowed':False,'reason':'NOT_ATTEMPTED'}}
 return deep_merge(state,case.get('initial_state',{}))
def knowledge_delta(before,after):
 delta=[]
 def walk(a,b,prefix=''):
  for key in sorted(set(a)|set(b)):
   path=f'{prefix}.{key}' if prefix else key
   if key not in a: delta.append({'path':path,'change':'ADDED'})
   elif key not in b: delta.append({'path':path,'change':'REMOVED'})
   elif isinstance(a[key],dict) and isinstance(b[key],dict): walk(a[key],b[key],path)
   elif a[key]!=b[key]: delta.append({'path':path,'change':'CHANGED'})
 walk(before,after)
 return delta
def reduce(state,event):
 s=copy.deepcopy(state); t=event['type']
 if t=='box_search': s['pc_knowledge']['box_contents']='UNKNOWN'
 elif t=='unobserved_contact': s['invitation']={'status':'NOT_EMITTED','reason':'NO_OBSERVATION'}; s['location_disclosed']=False
 elif t=='relay_refused': s['delivery_attempt']['status']='REFUSED'; s['invitation']={'status':'NOT_EMITTED','reason':'RELAY_REFUSED'}; s['location_disclosed']=False
 elif t=='relay_delayed': s['delivery_attempt']['status']='PENDING'; s['invitation']={'status':'NOT_EMITTED_PENDING_RELAY','reason':'RELAY_PENDING'}; s['location_disclosed']=False
 elif t=='early_document_discovery': s['pc_knowledge']['document_scope']='TEXTUAL_ASSOCIATION_ONLY'
 elif t=='abandon_optional': s['optional_story']={'status':'CLOSED','disposition':'ABANDONED'}
 elif t=='decline_invitation': s['route']='ALTERNATE'; s['scene_started']=False
 elif t=='leave_first_contact': s['route']='CONTACT_CLOSED'; s['new_invitation_emitted']=False
 elif t=='attempt_transition':
  closure=event.get('closure',{})
  required=('required_units_closed','optional_started_closed','player_confirmed','sources_reconciled','supported_cycle_transition','c06_started','c06_closed')
  ok=all(closure.get(k) is True for k in required)
  s['transition']={'allowed':ok,'reason':'ALL_FUTURE_GATES_MET' if ok else 'MISSING_OR_UNSUPPORTED_EVIDENCE'}
  s['m302_unlocked']=ok
  if ok: s['episode_m301_open']=False
 elif t=='do_not_attend': s['route']='ALTERNATE'; s['scene_started']=False
 elif t=='escape': s['route']='ESCAPED'; s['bart']['embrace_recorded']=False
 elif t=='mechanical_divergence': s['route']='DIVERGED'; s['actual_outcome']=event['actual_outcome']; s['bart']['embrace_recorded']=False
 elif t=='generic_threat': s['family_threat']={'scope':'GENERIC_FAMILY','names_added':[],'locations_added':[],'actions_added':[],'responses_added':[]}
 elif t=='no_actual_embrace': s['bart']['embrace_recorded']=False
 elif t=='family_unavailable': s['family_contact_attempt']={'attempted':True,'channel':event["channel"],'result':'NO_CONTACT_ESTABLISHED_THIS_ATTEMPT'}
 elif t=='refuse_social_task':
  task=event.get('task_id','unspecified')
  s.setdefault('story_task',{})[task]={'status':'REFUSED','local_scene_status':'CLOSED'}
  s['route_abandoned']=False; s['route_advanced']=False
 elif t=='refuse_optional_ethics': s.setdefault('optional_stories',{})['ST-ETHICAL-COST']={'status':'CLOSED','disposition':'REFUSED'}
 elif t=='uninformed_npc': pass
 elif t=='review_with_optional_open':
  s['graduation_review_available']=True
  evidence=event.get('evidence',{})
  required=('route_critical_closures','player_choice_recorded','sheet_and_xp_reconciled','player_chooses_principal_2010')
  choice=evidence.get('player_chooses_principal_2010')
  if choice is False: s['graduation_status']='ALTERNATE'
  elif all(evidence.get(k) is True for k in required) and evidence.get('optional_threads') in ('RESOLVED','ABANDONED','QUIET','CARRIED_BY_PLAYER_CHOICE'): s['graduation_status']='COMPLETE'
  else: s['graduation_status']='INCOMPLETE'
 elif t=='elide_to_2010': s['exact_intermediate_dates']='UNKNOWN'; s['graduation_review_available']=True
 elif t=='xp_review': s['xp_review_available']=True; s['xp_awarded_delta']=0; s['xp_spent_delta']=0
 elif t=='narrator_attempt': s['transition']={'allowed':False,'reason':'NO_OPERATIONAL_PERMISSION'}; s['scene_started']=False
 elif t=='read_prospective_profile': s['npc_generation']='UNKNOWN'; s['npc_blood_potency']=event['blood_potency']
 elif t=='final_death_before_embrace': s['bart']['final_death']=True; s['bart']['embrace_recorded']=False; s['route']='DIVERGED'
 else: raise ValueError(f'Unknown reducer event: {t}')
 s['npc_knowledge_delta']=knowledge_delta(state.get('npc_knowledge',{}),s.get('npc_knowledge',{}))
 return s
MISSING=object()
def get_path(obj,path):
 cur=obj
 for part in path.split('.'):
  if not isinstance(cur,dict) or part not in cur: return MISSING
  cur=cur[part]
 return cur
def matches(actual,expected,before,path):
 if expected=='__MISSING__': return actual is MISSING
 if isinstance(expected,dict):
  if expected.get('$unchanged_from_initial') is True: return actual==get_path(before,path)
  if expected.get('$absent') is True: return actual is MISSING
  if '$in' in expected: return actual in expected['$in']
  if '$equals' in expected: return actual==expected['$equals']
 return actual==expected
def resolve_pointer(obj,pointer):
 if not pointer: return obj
 cur=obj
 for token in pointer.lstrip('/').split('/'):
  token=token.replace('~1','/').replace('~0','~')
  cur=cur[int(token)] if isinstance(cur,list) else cur[token]
 return cur
def resolve_contract(case):
 source,anchor=case['contract_ref'].split('#',1)
 path=ROOT/DEL/source
 if not path.is_file(): return False
 if path.suffix.lower()=='.md':
  text=path.read_text(encoding='utf-8')
  return anchor in text and len(case.get('pass_criterion','').strip())>=12
 if path.suffix.lower()=='.json':
  try: target=resolve_pointer(json.loads(path.read_text(encoding='utf-8')),anchor)
  except Exception: return False
  return target is not None and len(case.get('pass_criterion','').strip())>=12
 return False
cases_path=ROOT/DEL/'D11_ADVERSARIAL_CASES_V014_GM_HIDDEN.json'
cases_raw=cases_path.read_bytes()
cases_blob=hashlib.sha1(b'blob '+str(len(cases_raw)).encode()+b'\0'+cases_raw).hexdigest()
runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
cases_doc=json.loads(cases_raw.decode('utf-8'))
cases=cases_doc['cases']
for case in cases:
 if not resolve_contract(case): raise SystemExit('D11_V014_BLOCK: unresolved contract or missing pass criterion')
 if not isinstance(case.get('assert'),dict) or not case['assert']: raise SystemExit('D11_V014_BLOCK: missing contract assertions')
results=[]
for case in cases:
 before=initial(case); actual=reduce(before,case['event']); failures=[]
 for path,want in case['assert'].items():
  if not matches(get_path(actual,path),want,before,path): failures.append(path)
 results.append(not failures)
failed=sum(not x for x in results)
report={'document_id':'D11_TEST_RESULTS_V014_PLAYER_SAFE','version':'V014','status':'PASS' if failed==0 else 'FAIL','execution_mode':'DETERMINISTIC_SEEDED_STATE_CONTRACT_REDUCER','cases_total':len(results),'passed':len(results)-failed,'failed':failed,'scenes_played':0,'dice_simulated':False,'persistent_state_mutated':False,'result_detail_disclosed':False,'input_artifact_refs':[{'path':'novydres/runtime/narrative-architecture/program/deliverables/D11_ADVERSARIAL_CASES_V014_GM_HIDDEN.json','blob_sha':cases_blob}],'runner_source_sha256':runner_sha256,'limitation':'The reducer checks prepared state-transition contracts with seeded ledgers. It is not the game engine and proves no live cycle transition, V5 roll result, or scene permission.'}
print(json.dumps(report,ensure_ascii=False,indent=2))
if failed: raise SystemExit(1)

#!/usr/bin/env python3
"""Reproducible D08 contract, provenance, authority and adversarial checks."""
import argparse, copy, json, re, subprocess, sys
from pathlib import Path

TEST_IDS=[f'T-D08-{i:03d}' for i in range(1,55)]
EXPECTED_FILES={
 'AUDIT_D08_V001.json','D08_ADVERSARIAL_TESTS_V001.json','D08_PLAYER_APPROVAL_QUEUE_V001.json',
 'D08_STORY_SCENES_BEATS_V001.json','D08_VALIDATE_V001.py','HANDOFF_D08_V001.json','NEXT_PROMPT_D09_V001.md'}
EXPECTED_MASTER='124f9a9f43ed427d3db106d9187a875d74f60ac6'
BASE=Path('novydres/runtime/narrative-architecture/program/deliverables')

def git(root,*args,check=True):
 p=subprocess.run(['git',*args],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if check and p.returncode: raise RuntimeError(p.stderr.strip() or 'git command failed')
 return p

def safe_contract(doc):
 try:
  allowed_top_level={'program_id','phase','version','status','authority','spoiler_class','repository','branch','input_head','master_head','no_canon_edit','no_cycle_edit','no_scene_authorization','no_operational_promotion','document_id','checkpoint_as_of','source_refs','design_policy','story_selection','stories','scenes','beats','local_end_contract','gate','gate_limits'}
  if set(doc)!=allowed_top_level: return False
  stories=doc['stories']; scenes=doc['scenes']; beats=doc['beats']
  if len(stories)!=1 or stories[0]['state']!='DRAFT' or stories[0]['plot_ids']!=['D04-PC01'] or stories[0]['npc_agendas']!=[]: return False
  if stories[0]['story_kind']!='STORY' or stories[0]['marco_id']!='M2': return False
  if {x['route'] for x in stories[0]['closure_routes']}!={'SUCCESS','PARTIAL','ALTERNATIVE','REFUSAL','FAILURE','OFFSCREEN'}: return False
  allowed_view_refs={
   'D08-SC01-OPTIONAL-SCOPE-AND-SOURCE-REVIEW':['D03_KNOWLEDGE_GRAPH_V001.json: each NPC knowledge item requires demonstrated acquisition.','D07_PLOT_BIBLES_V001.json#/contracts/0/participants_and_agency: future presence and objective UNKNOWN.','CYCLE_V0033.json#/refs/knowledge: checkpoint source only; refresh before use.'],
   'D08-SC02-OPTIONAL-LOCAL-DISPOSITION-AND-END':['D03_KNOWLEDGE_GRAPH_V001.json: no NPC knows a result without recorded acquisition.','D07_TRUTH_LOCKS_V001.json#/locks/id=D07-TL-001: truth-dependent investigation blocked.','D07_PLOT_BIBLES_V001.json#/contracts/0/closure_contract: local disposition is not global closure.']}
  if {x['scene_id'] for x in scenes}!=set(allowed_view_refs): return False
  if any(x['viewpoint_limit_refs']!=allowed_view_refs.get(x['scene_id']) for x in scenes): return False
  if not all(x['state']=='PREPARED' and x['present_actor_ids']==[] and x['forces_pc_action'] is False for x in scenes): return False
  if not all(x['actor'] in {'NARRATOR_REACTION','PLAYER_ONLY'} and x['forces_pc_action'] is False for x in beats): return False
  if doc['no_scene_authorization'] is not True or doc['no_operational_promotion'] is not True: return False
  if doc['local_end_contract']['full_plot_closure_claimed'] is not False: return False
  forbidden={'secret_answer','truth_answer','answer','secret_payload','locked_truth','clue_payload','culprit_identity','motive_reveal','forced_choice'}
  def walk(v):
   if isinstance(v,dict):
    if any(k.casefold() in forbidden for k in v): return False
    return all(walk(x) for x in v.values())
   if isinstance(v,list): return all(walk(x) for x in v)
   return True
  return walk(doc)
 except (KeyError,TypeError): return False

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--repo-root',default='.')
 ap.add_argument('--run-manifest',required=True)
 ap.add_argument('--expected-gate',choices=['PENDING','PASS_WITH_UNKNOWN'],default='PENDING')
 args=ap.parse_args(); root=Path(args.repo_root).resolve(); dm=Path(args.run_manifest).resolve()
 d=root/BASE
 docs={n:json.loads((d/n).read_text()) for n in ['D08_STORY_SCENES_BEATS_V001.json','D08_PLAYER_APPROVAL_QUEUE_V001.json','D08_ADVERSARIAL_TESTS_V001.json','AUDIT_D08_V001.json','HANDOFF_D08_V001.json']}
 storydoc=docs['D08_STORY_SCENES_BEATS_V001.json']; queue=docs['D08_PLAYER_APPROVAL_QUEUE_V001.json']; tests=docs['D08_ADVERSARIAL_TESTS_V001.json']; audit=docs['AUDIT_D08_V001.json']; handoff=docs['HANDOFF_D08_V001.json']
 results=[]
 def check(name,ok):
  results.append((name,bool(ok))); print(f"T-D08-{len(results):03d} {'PASS' if ok else 'FAIL'} {name}")
 def resolve(ref):
  return git(root,'rev-parse',f"HEAD:{ref}",check=False).stdout.strip()
 # 001-010: branch, cycle and completed D07 handoff.
 check('repository branch and input metadata',git(root,'branch','--show-current').stdout.strip()=='design/chr001-narrative-program-d01' and storydoc['repository']=='Niltond3/novydres-persistence-poc' and storydoc['input_head']=='b8a814549ef8ea106c026154fbab1708e9052374')
 check('read-only master exact',git(root,'rev-parse','origin/master').stdout.strip()==EXPECTED_MASTER and storydoc['master_head']==EXPECTED_MASTER)
 check('D07 input ancestor',git(root,'merge-base','--is-ancestor',storydoc['input_head'],'HEAD',check=False).returncode==0)
 def latest_cycle(ref):
  names=git(root,'ls-tree','-r','--name-only',ref,'--','novydres/chronicles/CHR-001/orchestration').stdout.splitlines()
  found=[]
  for p in names:
   m=re.fullmatch(r'.*/CYCLE_V(\d+)\.json',p)
   if m: found.append((int(m.group(1)),p))
  return max(found) if found else (0,'')
 cur_path=latest_cycle('HEAD')[1]; master_path=latest_cycle('origin/master')[1]
 check('latest numeric cycle on both refs',latest_cycle('HEAD')[0]==33 and latest_cycle('origin/master')[0]==33 and cur_path==master_path)
 cycsha=resolve(cur_path)
 check('cycle blob pin',cur_path==storydoc['checkpoint_as_of']['path'] and cycsha==storydoc['checkpoint_as_of']['blob_sha'])
 cycle=json.loads(git(root,'show',f'HEAD:{cur_path}').stdout)
 cp=cycle['checkpoint']
 check('scene/current checkpoint',cp['last_event_id']=='CHR001-M301-C05-22-20261109-001' and cp['last_closed_scene']=='C05' and cp['next_scene']=='C06' and cp['next_scene_status']=='NOT_STARTED' and cp['mortal'] is True and cp['embrace_occurred'] is False and cycle['status']=='READY_FOR_DRAMATURGO')
 check('cycle same on master and design',resolve(cur_path)==git(root,'rev-parse',f'origin/master:{cur_path}').stdout.strip())
 manifest=json.loads(dm.read_text()); d07=manifest['phase_records']['D07']; rb=d07['publication_readback']
 check('run manifest D07 gate/readback',manifest['phase_status']['D07']=='PASS_WITH_UNKNOWN' and d07['status']=='PASS_WITH_UNKNOWN' and d07['output_head']=='b8a814549ef8ea106c026154fbab1708e9052374' and rb['remote_head_matches_local'] and rb['all_8_file_blobs_verified'] and rb['all_8_contents_match_remote'] and rb['master_unchanged'])
 expected_d07={a['path']:a['blob_sha'] for a in d07['artifacts']}
 readback_ok=len(expected_d07)==8
 for p,s in expected_d07.items():
  readback_ok=readback_ok and resolve(p)==s and git(root,'show',f"origin/design/chr001-narrative-program-d01:{p}").stdout.encode()==(root/p).read_bytes()
 check('all eight D07 blobs/content',readback_ok)
 parse_ok=True
 for n in docs:
  try: json.loads((d/n).read_text())
  except Exception: parse_ok=False
 check('all D08 JSON parse',parse_ok)
 # 011-020: main story constraints.
 check('PLAYER_SAFE editorial metadata',all(x.get('phase')=='D08' and x.get('spoiler_class')=='PLAYER_SAFE' and x.get('authority')=='EDITORIAL_ONLY' for x in [storydoc,queue,tests,audit,handoff]))
 check('one story only',len(storydoc['stories'])==1)
 s=storydoc['stories'][0]
 check('PC01 only plot',s['plot_ids']==['D04-PC01'] and storydoc['story_selection']['count']==1)
 check('story remains DRAFT',s['state']=='DRAFT' and storydoc['no_operational_promotion'] is True)
 check('M2 remains an editorial proposal',s['marco_id']=='M2' and s['state']=='DRAFT' and storydoc['status']=='PROPOSED' and storydoc['authority']=='EDITORIAL_ONLY' and storydoc['no_operational_promotion'] is True)
 check('inciting incident UNKNOWN','UNKNOWN' in s['inciting_incident'])
 check('why-now UNKNOWN and no calendar trigger','UNKNOWN' in s['why_now'] and 'not triggers' in storydoc['design_policy']['inciting_event_and_why_now'])
 check('optional entry and refusal','player' in s['nonmandatory_entry'].lower() and any(r['route']=='REFUSAL' for r in s['closure_routes']) and bool(s['refusal_path']))
 check('no NPC agenda',s['npc_agendas']==[] and storydoc['design_policy']['npc_autonomy'].startswith('No future agenda'))
 routes={r['route'] for r in s['closure_routes']}
 check('success/partial/alternative/refusal/failure/offscreen routes',routes=={'SUCCESS','PARTIAL','ALTERNATIVE','REFUSAL','FAILURE','OFFSCREEN'})
 # 021-030: local exits and scene/beat optionality.
 check('local endings only',storydoc['local_end_contract']['must_end_locally'] is True and storydoc['local_end_contract']['full_plot_closure_claimed'] is False and storydoc['local_end_contract']['unrelated_plot_may_remain_open'] is True)
 check('no mandatory scene order','NONLINEAR_OPTIONAL' in storydoc['design_policy']['scene_order'])
 check('unique scenes',len({x['scene_id'] for x in storydoc['scenes']})==len(storydoc['scenes']))
 check('all scenes PREPARED',all(x['state']=='PREPARED' for x in storydoc['scenes']))
 check('no actors assigned',all(x['present_actor_ids']==[] for x in storydoc['scenes']))
 check('SCENE_READY and NARRATOR_PERMISSION gates',all(any('SCENE_READY' in q for q in x['entry_preconditions']) and any('NARRATOR_PERMISSION' in q for q in x['entry_preconditions']) for x in storydoc['scenes']))
 check('refusal/suspension exits',all(bool(x['refusal_path']) and any('suspend' in q.lower() or 'stop' in q.lower() for q in x['exit_conditions']) for x in storydoc['scenes']))
 check('unique beats',len({x['beat_id'] for x in storydoc['beats']})==len(storydoc['beats']))
 check('no NPC-initiated beat',all(x['actor'] in {'NARRATOR_REACTION','PLAYER_ONLY'} for x in storydoc['beats']))
 check('no beat forces player action',all(x['forces_pc_action'] is False for x in storydoc['beats']) and all(x['forces_pc_action'] is False for x in storydoc['scenes']))
 check('no speculative triggers',all(x['trigger'].lower().startswith('only') for x in storydoc['beats']))
 check('beats forbid unsupported claims',all(len(x['forbidden_claims'])>=3 for x in storydoc['beats']))
 # 031-040: contracts, provenance, secrecy and mechanics.
 contracts=json.loads((d/'D01_CONTRACTS_V001.json').read_text())['$defs']
 check('D01 story fields',set(s)==set(contracts['story']['required']))
 scene_req=set(contracts['scene']['required'])|{'forces_pc_action'}
 check('D01 scene fields',all(set(x)==scene_req for x in storydoc['scenes']))
 beat_req=set(contracts['beat']['required'])|{'forces_pc_action'}
 check('D01 beat fields',all(set(x)==beat_req for x in storydoc['beats']))
 refs=[]
 def collect(v):
  if isinstance(v,dict):
   if 'path' in v and 'blob_sha' in v: refs.append(v)
   for x in v.values(): collect(x)
  elif isinstance(v,list):
   for x in v: collect(x)
 for obj in docs.values(): collect(obj)
 source_ok=bool(refs)
 for r in refs:
  source_ok=source_ok and bool(re.fullmatch(r'[0-9a-f]{40}',str(r['blob_sha']))) and resolve(r['path'])==r['blob_sha']
 check('all source SHAs resolve',source_ok)
 check('current state limited to derived archive',storydoc['checkpoint_as_of']['blob_sha']==cycsha and 'derived archive' in storydoc['design_policy']['epistemic_scope'])
 lock=json.loads((d/'D07_TRUTH_LOCKS_V001.json').read_text())
 check('truth lock remains blocked',lock['effective_gm_hidden_segregation'] is False and lock['locks'][0]['play_status']=='BLOCKED_EXTERNAL_DEPENDENCY' and lock['locks'][0]['access_status']=='NO_EFFECTIVE_SEGREGATION' and lock['locks'][0]['materialized_truth']=='NOT_CREATED')
 forbidden_keys={'secret_answer','truth_answer','answer','secret_payload','locked_truth','clue_payload','culprit_identity','motive_reveal'}
 def no_payload(v):
  if isinstance(v,dict): return not any(k.casefold() in forbidden_keys for k in v) and all(no_payload(x) for x in v.values())
  if isinstance(v,list): return all(no_payload(x) for x in v)
  return True
 check('no secret answer/clue payload',all(no_payload(x) for x in docs.values()) and storydoc['design_policy']['truth_lock'].find('remains blocked')>=0)
 check('no causal promotion','causal_edges' not in storydoc and 'no cross-thread causal link added' in storydoc['design_policy']['causality'].casefold())
 check('no mechanical grant or result',storydoc['design_policy']['mechanics'].startswith('No roll or result'))
 required_approvals={x['id'] for x in json.loads((d/'D07_PLAYER_APPROVAL_QUEUE_V001.json').read_text())['decisions']}
 check('all inherited approvals retained',{x['id'] for x in queue['decisions']}==required_approvals)
 check('approval statuses remain pending/not granted',all(x['status'] in {'PENDING_PLAYER_APPROVAL','BLOCKED_EXTERNAL_DEPENDENCY','NOT_GRANTED'} for x in queue['decisions']) and all(x['status']!='APPROVED' for x in queue['decisions']))
 # 041-050: gates, reproducibility and adversarial mutations.
 gates={x.get('gate') for x in docs.values()}
 aligned=(gates=={args.expected_gate})
 if args.expected_gate=='PENDING':
  lr=audit['literary_review']
  literary_pending_or_complete=(lr['status']=='PENDING' or (lr['status']=='PASS_WITH_UNKNOWN' and bool(lr.get('reviewer')) and bool(lr.get('result')) and bool(lr.get('evidence'))))
  aligned=aligned and audit['status']=='AUDITING' and handoff['status']=='AUDITING' and audit['independent_review']['status']=='PENDING' and literary_pending_or_complete
 else: aligned=aligned and audit['status']=='PASS_WITH_UNKNOWN' and handoff['status']=='PASS_WITH_UNKNOWN' and audit['independent_review']['status']=='PASS' and bool(audit['independent_review'].get('result')) and audit['literary_review']['status']=='PASS_WITH_UNKNOWN' and bool(audit['literary_review'].get('reviewer')) and bool(audit['literary_review'].get('result')) and bool(audit['literary_review'].get('evidence')) and audit['independent_review']['status']=='PASS' and bool(audit['independent_review'].get('result')) and bool(audit['independent_review'].get('evidence')) and audit.get('schema_validation',{}).get('status')=='PASS' and audit['automated_validation']['status']=='PASS'
 check('top-level gates aligned',aligned)
 check('catalog matches runner',[x['id'] for x in tests['cases']]==TEST_IDS and tests['execution']['total']==54)
 prompt=(d/'NEXT_PROMPT_D09_V001.md').read_text()
 check('D09 prompt requires blob/content readback',('blob' in prompt.casefold() or 'sha' in prompt.casefold()) and ('relido' in prompt.casefold() or 'readback' in prompt.casefold()) and 'D09' in prompt)
 def reject(mutator):
  m=copy.deepcopy(storydoc); mutator(m); return not safe_contract(m)
 check('forced choice mutation rejected',reject(lambda m:m['scenes'][0].update(forces_pc_action=True)))
 check('NPC agenda mutation rejected',reject(lambda m:m['stories'][0].update(npc_agendas=['invented future agenda'])))
 check('READY scene mutation rejected',reject(lambda m:m['scenes'][0].update(state='READY')))
 check('secret answer/PC02/causal mutation rejected',all([
  reject(lambda m:m['stories'][0].update(secret_answer='payload')),
  reject(lambda m:m['stories'][0].update(plot_ids=['D04-PC02'])),
  reject(lambda m:m.update(causal_edges=['unsupported']))
 ]))
 check('NPC knowledge mutation without acquisition rejected',reject(lambda m:m['scenes'][0]['viewpoint_limit_refs'].append('TEST-NPC-X knows a future result without D03 acquisition evidence.')))
 check('generic truth/answer metadata mutations rejected',all([reject(lambda m:m['design_policy'].update(truth_answer='payload')),reject(lambda m:m['design_policy'].update(answer='payload'))]))
 # Ensure the only delta from the D07 input is the seven authorized D08 artifacts.
 changed=set(git(root,'diff','--name-only',storydoc['input_head'],'--').stdout.splitlines())
 changed.update(line[3:] for line in git(root,'status','--porcelain','-uall').stdout.splitlines() if len(line)>=4)
 expected={str(BASE/n) for n in EXPECTED_FILES}
 check('only seven proposed D08 files changed',changed==expected)
 # execution fields are consistent with the actual requested gate.
 exec_status=tests['execution']['status']
 check('execution status matches gate',(args.expected_gate=='PENDING' and exec_status=='PENDING') or (args.expected_gate=='PASS_WITH_UNKNOWN' and exec_status=='PASS' and tests['execution']['passed']==54 and tests['execution']['total']==54 and tests['execution']['result']=='54/54 PASS'))
 passed=sum(ok for _,ok in results); total=len(results)
 print(f'RESULT {"PASS" if passed==total else "FAIL"} {passed}/{total}')
 return 0 if passed==total and total==54 else 1
if __name__=='__main__': sys.exit(main())

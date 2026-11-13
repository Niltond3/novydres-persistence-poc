// D04/ADR-001: prove the approved CHR-001 provisional-mechanics scope, never spend XP.
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const M='c9fcfc0c558cd17d58ec8c8272da3ed70182ff37';
const path='novydres/cronicas/CHR-001/configuracao/mecanica-c45.json';
const fail=code=>{const e=new Error(code);e.code=code;throw e;};
const git=(...args)=>execFileSync('git',args,{encoding:'utf8',maxBuffer:1024*1024,stdio:['ignore','pipe','ignore']});
const read=p=>JSON.parse(git('show',M+':'+p));
export function verifyMechanics({override=null}={}){
 const d=override||JSON.parse(readFileSync(path,'utf8'));
 const refs=new Map((d.source_refs||[]).map(x=>[x.id,x]));
 if(d.subject_id!=='chr001-table-config'||d.status!=='CANDIDATE_NOT_OPERATIONAL'||
    d.visibility!=='SYSTEM_AUDIT'||d.authority?.no_runtime_activation!==true||
    d.owner_scope!=='novydres/cronicas/CHR-001/configuracao'||d.source_commit!==M||refs.size!==6)
    fail('D04_MECHANICS_SCOPE_DRIFT');
 const find=n=>[...refs.entries()].find(([p])=>p.endsWith('/'+n));
 const get=n=>{const entry=find(n);if(!entry)fail('D04_MECHANICS_REQUIRED_SOURCE_MISSING');return entry};
 for(const [p,r] of refs)if(!p.startsWith('novydres/')||p.includes('..')||
   r.source_commit!==M||!/^[a-f0-9]{40}$/.test(r.sha)||git('rev-parse',M+':'+p).trim()!==r.sha)
   fail('D04_MECHANICS_SOURCE_DRIFT');
 const source=read(get('MECHANICAL_GUIDED_CREATION_RULES_PROVENANCE_V3.json')[0]);
 const target=read(get('TARGET_SHEET_V2_APPROVED.json')[0]);
 const cycle=read(get('CYCLE_V0045.json')[0]);
 const live=read(get('LIVE_v039.json')[0]);
 const gate=git('show',M+':'+get('MECHANICAL_ADJUDICATION_GATE_V1.md')[0]);
 const engine=git('show',M+':'+get('MOTOR_MECANICO_V5_V1_1.source.txt')[0]);
 const mechanical=cycle.operational_gates?.mechanical_sources;
 if(source.status!=='APPROVED_LOCAL_EXCEPTION_DEC_CR_019_PROVISIONAL_GRAPPLE'||
    source.active_decision!=='DEC-CR-019'||target.status!=='APPROVED_LOCAL_TARGET_ACTIVE_NOT_BOUGHT'||
    target.scope!=='CHR-001'||target.approval_does_not_grant_or_spend_xp!==true||
    mechanical?.rules_provenance?.blob_sha!==get('MECHANICAL_GUIDED_CREATION_RULES_PROVENANCE_V3.json')[1].sha||
    mechanical?.target_sheet?.blob_sha!==get('TARGET_SHEET_V2_APPROVED.json')[1].sha||
    mechanical?.adjudication_gate?.blob_sha!==get('MECHANICAL_ADJUDICATION_GATE_V1.md')[1].sha||
    mechanical?.motor_manual?.blob_sha!==get('MOTOR_MECANICO_V5_V1_1.source.txt')[1].sha||
    !gate.includes('Briga (Agarrar)')||!engine.includes('Pegar Metade'))
    fail('D04_MECHANICS_AUTHORITY_DRIFT');
 if(JSON.stringify(d.source_distinctions)!==JSON.stringify(source.distinctions))
   fail('D04_MECHANICS_ACTUAL_VS_PROVISIONAL_DRIFT');
 const a=d.application||{},s=d.source_distinctions?.provisional_specialization_scope||{};
 if(a.provisional_attributes_and_skills_for_guided_tests_only!==true||
    a.acquired_traits_distinct_from_provisional_test_pools!==true||
    a.target_dots_not_auto_purchased!==true||
    a.target_future_disciplines_unavailable_before_embrace!==true||
    a.grapple_specialization!=='Briga (Agarrar)'||a.grapple_provisional_bonus_dice!==1||
    s.bonus_dice!==1||s.no_xp_spent!==true||
    a.other_target_specializations_unpurchased_do_not_apply!==true||
    a.historical_rolls_not_recomputed!==true||
    a.future_dice_face_or_seed_log_mandatory!==false||
    a.no_fabricated_rng_results!==true||a.willpower_requires_explicit_player_authorization!==true||
    a.no_unearned_xp_spend_or_award!==true||
    d.procedural_succession?.DEC23_no_universal_ledger!==true||
    d.procedural_succession?.DEC24_no_mandatory_rng_faces!==true)
    fail('D04_MECHANICS_UNAUTHORIZED_RULE');
 const resources=live.character.resources;
 if(JSON.stringify(d.current?.resources)!==JSON.stringify(Object.fromEntries(Object.keys(d.current?.resources||{}).map(k=>[k,resources[k]])))||
    d.current.mortal!==true||d.current.embraced!==false||
    resources.xp_total!==675||resources.xp_spent!==270||resources.xp_remaining!==405||
    resources.xp_credit_available!==0)
    fail('D04_MECHANICS_RESOURCE_MISMATCH');
 return {ok:true,source_commit:M,gate:'D04_MECHANICAL_LOCAL_SOURCE_SCOPE_CONFIRMED_NOT_RUNTIME_PASS',
  acquired_vs_provisional_preserved:true,provisional_specialization:'Briga (Agarrar)',
  local_bonus_dice:1,auto_xp_awards:0,future_powers_active:false};
}
if(process.argv[1]?.endsWith('/verificar-mecanica-c45.mjs'))
 console.log(JSON.stringify(verifyMechanics()));

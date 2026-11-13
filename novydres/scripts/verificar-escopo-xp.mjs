// ADR-001 D03-D04: prove local XP boundaries from pinned master content, no new credits.
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const M='c9fcfc0c558cd17d58ec8c8272da3ed70182ff37';
const err=code=>{const e=new Error(code);e.code=code;throw e;};
const get=p=>JSON.parse(readFileSync(p,'utf8'));
const git=(...x)=>execFileSync('git',x,{encoding:'utf8',maxBuffer:1024*1024,stdio:['ignore','pipe','ignore']});
const pin=(r,path,sha)=>{
 if(r.id!==path||r.sha!==sha||r.source_commit!==M||
   git('rev-parse',M+':'+path).trim()!==sha)err('D04_XP_PIN_DRIFT');
};
export function verifyXP({localOverride=null,globalOverride=null,scopeOverride=null}={}){
 const root='novydres/cronicas/CHR-001/estado/',rp='novydres/sistema/regras/experiencia/';
 const local=localOverride||get(root+'xp-autoridade-c45.json');
 const common=globalOverride||get(rp+'principios-credito.json');
 const scope=scopeOverride||get(rp+'escopos.json');
 const pol='novydres/runtime/xp/XP_ACT_CREDIT_POLICY_V1.md';
 const env='novydres/runtime/xp/XP_ENVELOPE_V3.json';
 const live='novydres/chronicles/CHR-001/LIVE_v039.json';
 const P=local.source_refs.find(x=>x.id===pol),E=local.source_refs.find(x=>x.id===env),L=local.source_refs.find(x=>x.id===live);
 if(!P||!E||!L)err('D04_XP_MISSING_SOURCE');
 pin(P,pol,'d22278b02d35b967045432b5d65bc7b13e3fd2ce');
 pin(E,env,'461af62f9404a6e895950843b39a596b0b73b7ab');
 pin(L,live,'b7096d7fc44854d4964ae7bf6a052fcb948ebf19');
 const sourcePolicy=git('show',M+':'+pol);
 const sourceEnvelope=JSON.parse(git('show',M+':'+env));
 const sourceLive=JSON.parse(git('show',M+':'+live));
 if(!sourcePolicy.includes('nominal = 10')||!sourcePolicy.includes('BUDGET_TOTAL')||
    sourceEnvelope.current.xp_total!==675||sourceEnvelope.current.xp_spent!==270||
    sourceEnvelope.current.xp_remaining!==405||sourceEnvelope.current.xp_credit_available!==0)
    err('D04_XP_HISTORICAL_SOURCE_MISMATCH');
 const res=sourceLive.character.resources;
 const expected={xp_total:res.xp_total,xp_spent:res.xp_spent,
 xp_remaining:res.xp_remaining,xp_credit_available:res.xp_credit_available};
 if(local.status!=='CANDIDATE_NOT_OPERATIONAL'||local.visibility!=='SYSTEM_AUDIT'||
    local.owner_scope!==root.slice(0,-1)||local.scope!=='CHR-001_ONLY'||
    JSON.stringify(local.current)!==JSON.stringify(expected)||
    Object.values(expected).some(x=>!Number.isInteger(x)||x<0)||
    expected.xp_total!==675||expected.xp_spent!==270||expected.xp_remaining!==405||
    expected.xp_credit_available!==0||expected.xp_total-expected.xp_spent!==expected.xp_remaining)
    err('D04_XP_STATE_DRIFT');
 const rule=local.local_credit_rule;
 if(rule.nominal_per_eligible_resolved_act!==10||rule.maximum_creditable_acts_per_provocation!==5||
    !rule.once_per_distinct_act||!rule.source_resolution_event_required||!rule.no_credit_on_preparation||
    !rule.credit_is_part_of_cap_not_extra||!rule.credit_does_not_modify_total_or_spent||
    local.credits_derived_from_source_not_new_awards!==true||local.no_target_auto_purchase!==true)
    err('D04_XP_UNAUTHORIZED_CREDIT');
 if(local.temporal_precedence?.length!==3||
    local.temporal_precedence[0].reported_spent!==170||
    local.temporal_precedence[1].reported_spent!==270||
    local.temporal_precedence[2].reported_spent!==270||
    !local.temporal_precedence[2].latest_state||
    local.temporal_precedence[0].latest_state!==false)
    err('D04_XP_HISTORY_OVERWRITTEN');
 if(common.subject_id!=='rule-experience-novydres'||common.owner_scope!==rp.slice(0,-1)||
    common.local_owner_subject_id!=='chr001-state-checkpoint'||
    common.operational_promotion!==false||
    common.global_invariants.no_xp_total_inflation_on_credit!==true||
    common.global_invariants.no_double_credit!==true||
    !common.scope_disclaimer.includes('NOT_GLOBAL_V5_RULES'))
    err('D03_GLOBAL_LOCAL_XP_PROMOTION');
 if(scope.field_semantics_fully_partitioned!==true||scope.source_records?.length!==8||
    scope.source_records.some(row=>row.semantic_owner_current==='UNRESOLVED')||
    scope.field_owners?.local_xp_balance?.subject_id!=='chr001-state-checkpoint')
    err('D03_XP_FIELD_OWNER_MISSING');
 return {ok:true,gate:'XP_SCOPE_PINNED_NOT_COMPLETE_D04_OR_RUNTIME_PASS',owner:'chr001-state-checkpoint',
  snapshot:M,current:expected,history:'170_TO_270_NOT_RESET',records:8};
}
if(process.argv[1]?.endsWith('/verificar-escopo-xp.mjs'))console.log(JSON.stringify(verifyXP()));

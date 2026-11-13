// ADR-001 D05: per-reference honest verdict coverage; policy replacement != live runtime parity.
import {readFileSync} from 'node:fs';
const P='novydres/sistema/arquitetura/fase-d/execucao-d05.json';
const fail=code=>{const e=new Error(code);e.code=code;throw e;};
const expected=new Map([
 ['novydres/runtime/G26_NONBLOCKING_PERSISTENCE_V1.md','491e3d9d059bb4277df121c5abce3297c24adee4'],
 ['novydres/runtime/G28_SCENE_END_BATCH_AND_DYNAMIC_CONFLICT_V1.md','231cb78d712c4c7d2be88a41a4058d21e1cf88ea']
]);
export function verifyD05Verdicts({override=null}={}){
 const d=override||JSON.parse(readFileSync(P,'utf8'));
 if(d.phase!=='D05'||d.gate==='D05_PASS'||d.no_runtime_activation!==true||
    d.active_reference_records!==121||d.functional_review_by_successor?.is_d05_pass!==false||
    d.functional_review_by_successor?.behavioral_equivalence_approved!==0)
   fail('D05_FALSE_GATE_APPROVAL');
 const f=d.functional_review_by_successor,per=f.per_reference_verdicts;
 if(f.grouped_results?.length!==9||per?.reference_rows!==121||
    per.equivalent_verified!==0||per.approved_replacements_policy_only!==2||
    per.blocked!==119||per.no_end_to_end_chronicle_runtime_proof!==true)
   fail('D05_VERDICT_COUNTS_OR_PROOF_DRIFT');
 const groups=new Map(f.grouped_results.map(g=>[g.successor,g]));
 const rows=d.source_records.filter(x=>x.active_original_reference===true);
 if(rows.length!==121||new Set(rows.map(x=>x.origin)).size!==121)
   fail('D05_ACTIVE_REFERENCE_COVERAGE');
 let direct=0,manifest=0,replacements=0,blocked=0;
 const grouped=new Map();
 for(const row of rows){
   const v=row.functional_review,g=groups.get(row.proposed_successor);
   if(!g||!v||!['EQUIVALENT_VERIFIED','APPROVED_REPLACEMENT','BLOCKED'].includes(v.verdict)||
      v.source_blob_sha!==row.original_git_blob_sha)
     fail('D05_VERDICT_MISSING_OR_UNTRUSTED');
   if(row.reference_kind==='C45_CYCLE_DIRECT')direct++;
   else if(row.reference_kind==='M63_MANIFEST_ONLY_NOT_PROVEN_INACTIVE')manifest++;
   else fail('D05_REFERENCE_KIND_CHANGED');
   grouped.set(row.proposed_successor,(grouped.get(row.proposed_successor)||0)+1);
   if(expected.has(row.origin)){
     if(row.original_git_blob_sha!==expected.get(row.origin)||
        v.verdict!=='APPROVED_REPLACEMENT'||v.decision!=='ADR-001_DEC-18'||
        v.isolated_ci_run_id!==43236381679||v.isolated_ci_status!=='SUCCESS'||
        v.scope!=='APPROVED_POLICY_REPLACEMENT_WITH_ISOLATED_ATOMICITY_PROOF_NOT_LIVE_RUNTIME_EQUIVALENCE'||
        v.unverified_boundary!=='E02_NOT_AUTHORIZED_REAL_CHRONICLE_RUNTIME_NOT_TESTED'||
        v.implementation_contract!=='novydres/sistema/narrativa/contrato.md'||
        v.isolated_transaction_proof!=='novydres/scripts/transacao-git.mjs')
       fail('D05_POLICY_REPLACEMENT_UNSUPPORTED');
     replacements++;
   }else{
     if(v.verdict!=='BLOCKED'||v.scope!=='GROUPED_FUNCTIONAL_TRIAGE_ONLY_NO_PER_SOURCE_BEHAVIORAL_APPROVAL'||
        v.successor!==row.proposed_successor||
        v.unverified_boundary!==g.remaining_behavioral_proof||
        v.evidence_available!==g.observed_candidate_evidence||
        !v.unverified_boundary)
       fail('D05_UNPROVEN_FUNCTION_FALSE_PASS');
     blocked++;
   }
 }
 if(replacements!==2||blocked!==119||direct!==48||manifest!==73||
    [...groups].some(([id,g])=>grouped.get(id)!==g.reference_count))
   fail('D05_REFERENCE_COVERAGE_OR_GROUP_DRIFT');
 const adr=readFileSync('novydres/sistema/arquitetura/adr/001-subject-oriented.md','utf8'),
       contract=readFileSync('novydres/sistema/narrativa/contrato.md','utf8'),
       tx=readFileSync('novydres/scripts/transacao-git.mjs','utf8');
 if(!adr.includes('DEC-18')||!contract.includes('uma transação por resposta')||
    !tx.includes('ATOMIC_TEXT_AND_STATE_REQUIRED')||
    !tx.includes('READBACK_BLOB_MISMATCH'))
   fail('D05_REPLACEMENT_IMPLEMENTATION_NOT_FOUND');
 return {ok:true,reference_rows:121,cycle_direct:direct,manifest_only:manifest,
    policy_replacements:replacements,behavioral_blocked:blocked,equivalent_verified:0,
    proof_level:'NORMATIVE_APPROVED_REPLACEMENTS_AND_GROUPED_BLOCKED_TRIAGE',
    gate:'D05_NOT_PASS_FUNCTIONAL_PROOF_PENDING'};
}
if(process.argv[1]?.endsWith('/verificar-vereditos-d05.mjs'))
 console.log(JSON.stringify(verifyD05Verdicts()));

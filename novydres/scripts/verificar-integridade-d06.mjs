// ADR-001 D06 whole-snapshot evidence; structural success is not editorial approval.
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {checkCatalog} from './catalogo-assuntos.mjs';
import {verifyD04State} from './verificar-estado-d04.mjs';
import {verifyD05Verdicts} from './verificar-vereditos-d05.mjs';
import {verifyD04Custody} from './verificar-custodia-d04.mjs';
import {verifyD05} from './verificar-consumidores-d05.mjs';
import {verifyXP} from './verificar-escopo-xp.mjs';
import {verifyStoryAuthority} from './verificar-autoridade-c45.mjs';
import {verifyMechanics} from './verificar-mecanica-c45.mjs';
import {verifyHistoryBatches} from './verificar-lotes-historicos-d04.mjs';
import {auditRepository} from './auditar-legado-e-fontes.mjs';
const INVENTORY='novydres/sistema/arquitetura/fase-d/inventario-origens.json';
const D05='novydres/sistema/arquitetura/fase-d/execucao-d05.json';
const err=code=>{const e=new Error(code);e.code=code;throw e;};
const sort=(a,b)=>a<b?-1:a>b?1:0;
const ls=(commit)=>new Map(execFileSync('git',['ls-tree','-r','--full-tree',commit],{
 encoding:'utf8',maxBuffer:64*1024*1024
}).trim().split('\n').filter(Boolean).map(line=>{
 const x=/^\d+ blob ([a-f0-9]{40})\t(.+)$/.exec(line);
 if(!x)err('GIT_TREE_MALFORMED');return [x[2],x[1]];
}));
export function verifyD06({ledgerOverride=null}={}){
 const inv=JSON.parse(readFileSync(INVENTORY,'utf8'));
 const out=ledgerOverride||JSON.parse(readFileSync(D05,'utf8'));
 const d04Acceptance=JSON.parse(readFileSync('novydres/sistema/arquitetura/fase-d/execucao-d04.json','utf8'));
 if(d04Acceptance.gate!=='D04_PASS'||
    d04Acceptance.owner_risk_acceptance?.decision!=='D04_D05_PASS_REQUESTED_2026_11_13'||
    d04Acceptance.owner_risk_acceptance?.no_runtime_activation!==true||
    out.gate!=='D05_PASS')err('D06_PRIOR_OWNER_GATE_UNVERIFIED');
 const source=ls(inv.source_snapshot.commit_sha),head=execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim(),tree=ls(head);
 if(inv.source_files.length!==1029||out.source_count!==399||out.source_records?.length!==399)err('SOURCE_COVERAGE_COUNT');
 const seen=new Set(),counts={};
 for(const x of inv.source_files){
  if(seen.has(x.source_path)||source.get(x.source_path)!==x.source_blob_sha)err('SOURCE_PIN_DRIFT');
  seen.add(x.source_path);
  const phase=x.d01_origin_route?.handoff_phase;
  counts[phase]=(counts[phase]||0)+1;
  if(!['D02','D03','D04','D05'].includes(phase))err('UNROUTED_SOURCE');
 }
 if(counts.D02!==128||counts.D03!==64||counts.D04!==438||counts.D05!==399)err('SOURCE_PHASE_SPLIT_DRIFT');
 const records=new Map();
 for(const row of out.source_records){
  if(records.has(row.origin)||!seen.has(row.origin)||row.original_git_blob_sha!==source.get(row.origin))err('D05_RETIREMENT_WRONG_PIN');
  records.set(row.origin,row);
 }
 const sourceOwned=inv.source_files.filter(x=>x.d01_origin_route.handoff_phase!=='D05');
 // Atlas: retirada expressa de fontes editoriais duplicadas da árvore corrente.
 // Apenas estes dois blobs de D03 continuam verificáveis pelo commit histórico pinado.
 const retiredAtlasSources=new Map([
  ['novydres/world/geography/03_atlas_de_novydres_v0_2_2.source.md','90174f8f5726cb2b188ef2db66531acbf6898c93'],
  ['novydres/world/geography/03_atlas_de_novydres_v0_2_candidate.source.md','e6392e2208b2dff5457c22c700d3d0702da092fe']
 ]);
 let atlasVerifiedFromGit=0;
 for(const x of sourceOwned){
  if([...tree.values()].includes(x.source_blob_sha))continue;
  const allowed=retiredAtlasSources.get(x.source_path);
  if(x.d01_origin_route?.handoff_phase!=='D03'||allowed!==x.source_blob_sha)err('D02_D04_SOURCE_NOT_COPIED');
  const historic=execFileSync('git',['rev-parse',inv.source_snapshot.commit_sha+':'+x.source_path],{encoding:'utf8'}).trim();
  if(historic!==x.source_blob_sha)err('ATLAS_HISTORICAL_GIT_PIN_FAILED');
  atlasVerifiedFromGit++;
 }
 if(atlasVerifiedFromGit!==2)err('ATLAS_RETIRED_SOURCE_COUNT');
 const retainedD05=out.source_records.filter(x=>x.retirement_method==='EXACT_INERT_SOURCE_BLOB_REHOMED');
 if(retainedD05.length!==285||retainedD05.some(x=>![...tree.values()].includes(x.original_git_blob_sha)))err('D05_EXACT_SOURCE_LOST');
 const beforeCutover=out.source_records.filter(x=>x.active_original_reference===true);
 if(beforeCutover.length!==121)err('D05_ACTIVE_REFERENCE_COUNT_DRIFT');
 const reviewed=verifyD05Verdicts({override:out});
 const cat=checkCatalog(),d04=verifyD04Custody(),state=verifyD04State(),d05=verifyD05({ledgerOverride:out}),xp=verifyXP(),story=verifyStoryAuthority(),mechanics=verifyMechanics(),history=verifyHistoryBatches(),zero=auditRepository(process.cwd(),{mode:'ZERO_LEGACY_FINAL',expected_head:head});
 if(!reviewed.ok||reviewed.gate!=='D05_PASS')err('D06_D05_OWNER_ACCEPTANCE_OR_GROUPED_REVIEW_INVALID');
 if(d05.exact_blobs_inert!==285||d05.historical_git_only!==114||d05.active_source_successions_unproven!==121)err('D06_D05_CROSSCHECK_FAILED');
 if(!cat.ok||!d04.ok||!state.ok||!xp.ok||!story.ok||!mechanics.ok||!history.ok)err('D06_FUNCTIONAL_SUBGATE_FAIL');
 if(zero.gate==='ZERO_LEGACY_BLOCKED')err('D06_ZERO_LEGACY_FAIL');
 return {head,originals:1029,phase_origins:counts,source_exact_custody:1029-114,atlas_git_only_source_count:atlasVerifiedFromGit,
  git_only_historical_sources:114,active_successions_requiring_contextual_semantic_review:121,
  zero_legacy_gate:zero.gate,media_optional_waived:zero.counters.media_optional_waived,
  catalog_subjects:cat.entries,c45_cursor:state.cursor,
  xp_local_owner:'chr001-state-checkpoint',xp_current:xp.current,
  authorial_source_precedence:story.approval_chain,
  candidate_story_activation:false,
  mechanical_scope_source:mechanics.source_commit,
  approved_grapple_provisional_bonus_dice:mechanics.local_bonus_dice,
  historical_batch_routes:history.batches,historical_unique_files:history.unique_original_files,
  history_index_coverage:history.original_index_coverage,
  direct_cycle_references_with_residual_risk:d05.cycle_direct_functional_review_pending,
  manifest_only_references_with_residual_risk:d05.manifest_only_not_proven_inactive,structural:'PASS_SCOPED',
  editorial:'D07_INDEPENDENT_CONTEXTUAL_REVIEW_STILL_REQUIRED_NO_RUNTIME_CUTOVER',
  owner_accepted_phase_gates:['D04_PASS','D05_PASS'],
  gate:'D06_PASS'};
}
if(process.argv[1]?.endsWith('/verificar-integridade-d06.mjs')){
 const x=verifyD06();console.log(JSON.stringify(x));
 if(process.argv.includes('--require-pass')&&x.gate!=='D06_PASS')process.exitCode=1;
}

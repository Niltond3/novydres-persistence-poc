// ADR-001 B04 — synthetic, non-operational regression harness. No network or CHR-001 edits.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
const load = name => JSON.parse(readFileSync(new URL(name, import.meta.url), 'utf8'));
const negatives = load('./fixtures-negativos.json').cases;
const journeys = load('./fixtures-mutacoes.json').cases;
const clone = x => structuredClone(x);
const stable = x => JSON.stringify(x);
const baseline = {
  actor_id: 'artificial-npc-001', aliases: ['Test Alias'],
  confirmed: ['synthetic observed fact'],
  claims: [{ text:'synthetic unverified claim', epistemic:'NPC_CLAIM', known_by:['artificial-npc-001'] }],
  unknown: ['synthetic unknown'], future_contact:false, pc_obligation:false,
  technical_ledger_proven:false, last_event_id:'synthetic-event-001',
  resources:{ xp:10, fv:4 }, scene_started:false, source_sha:'a'.repeat(40)
};
const guards = [
  ['identity',x=>x.actor_id===baseline.actor_id],
  ['aliases',x=>stable(x.aliases)===stable(baseline.aliases)],
  ['claim-promotion',x=>stable(x.claims)===stable(baseline.claims)],
  ['unknown-suppression',x=>stable(x.unknown)===stable(baseline.unknown)],
  ['future-contact',x=>x.future_contact===baseline.future_contact],
  ['invent-pc-obligation',x=>x.pc_obligation===baseline.pc_obligation],
  ['forge-technical-ledger',x=>x.technical_ledger_proven===baseline.technical_ledger_proven],
  ['event-id-corruption',x=>x.last_event_id===baseline.last_event_id],
  ['xp-resource-change',x=>x.resources.xp===baseline.resources.xp],
  ['fv-resource-change',x=>x.resources.fv===baseline.resources.fv],
  ['unauthorized-scene-start',x=>x.scene_started===baseline.scene_started],
  ['source-hash-change',x=>x.source_sha===baseline.source_sha]
];
const mutations = {
  'identity':x=>x.actor_id='fake-id',
  'aliases':x=>x.aliases=[],
  'claim-promotion':x=>x.claims[0].epistemic='CONFIRMED',
  'unknown-suppression':x=>x.unknown=[],
  'future-contact':x=>x.future_contact=true,
  'invent-pc-obligation':x=>x.pc_obligation=true,
  'forge-technical-ledger':x=>x.technical_ledger_proven=true,
  'event-id-corruption':x=>x.last_event_id='fake',
  'xp-resource-change':x=>x.resources.xp=999,
  'fv-resource-change':x=>x.resources.fv=999,
  'unauthorized-scene-start':x=>x.scene_started=true,
  'source-hash-change':x=>x.source_sha='0'.repeat(40)
};
function validateSubject(x) {
  for (const [id, check] of guards) if(!check(x)) throw new Error('REJECT_'+id);
  return 'ACCEPT';
}
assert.equal(validateSubject(clone(baseline)), 'ACCEPT');
const negativeResults=[];
for (const tc of negatives) {
  assert.equal(tc.expected, 'REJECT');
  assert.ok(Object.hasOwn(mutations,tc.mutation), 'missing payload for '+tc.id);
  const sample=clone(baseline);mutations[tc.mutation](sample);
  let observed='ACCEPT'; try { validateSubject(sample); } catch { observed='REJECT'; }
  assert.equal(observed,tc.expected,tc.id);negativeResults.push({id:tc.id,observed});
}
function transact(store, tx) {
  if(tx.branch!=='test/adr001-local-isolation') throw new Error('branch_not_test');
  if(tx.frozen_file || tx.owner_duplicate || tx.activate_candidate_route || tx.synthetic_event_roll) throw new Error('scope');
  if(tx.visibility && !['PLAYER_SAFE','SYSTEM_AUDIT'].includes(tx.visibility)) throw new Error('visibility');
  if(tx.dangling_ref || tx.non_fast_forward) throw new Error('invalid_ref');
  const prev=store.transactions[tx.id];
  if(prev!==undefined) { if(prev!==tx.payload) throw new Error('conflicting_transaction_id'); return 'NO_OP'; }
  if(tx.expected_sha!==store.head) throw new Error('stale_sha');
  store.transactions[tx.id]=tx.payload;store.head='artificial-head-'+Object.keys(store.transactions).length;
  return 'COMMITTED';
}
const seed=()=>({head:'artificial-head-1',transactions:{'tx-seed':'value-one'}});
const normal={branch:'test/adr001-local-isolation',id:'tx-new',payload:'value-two',expected_sha:'artificial-head-1'};
assert.equal(transact(seed(),normal),'COMMITTED');
const journeyCases={
 'B-M01':{...normal,id:'tx-seed',payload:'value-one'},
 'B-M02':{...normal,id:'tx-seed',payload:'other-value'},
 'B-M03':{...normal,expected_sha:'obsolete-head'},
 'B-M04':{...normal,non_fast_forward:true},
 'B-M05':{...normal,branch:'master'},
 'B-M06':{...normal,dangling_ref:true},
 'B-M07':{...normal,owner_duplicate:true},
 'B-M08':{...normal,frozen_file:true},
 'B-M09':{...normal,visibility:'INVALID'},
 'B-M10':{...normal,activate_candidate_route:true},
 'B-M11':{...normal,synthetic_event_roll:true},
 'B-M12':{...normal,expected_sha:'obsolete-head'}
};
const journeyResults=[];
for(const tc of journeys){
  const tx=journeyCases[tc.id];assert.ok(tx,'missing executable journey '+tc.id);
  const s=seed(),before=stable(s);let observed;
  try { observed=transact(s,tx); } catch { observed='BLOCK'; }
  assert.equal(observed,tc.expected,tc.id);
  if(observed==='BLOCK'||observed==='NO_OP')assert.equal(stable(s),before,'state changed on '+tc.id);
  journeyResults.push({id:tc.id,observed});
}
assert.equal(negativeResults.length,12);
assert.equal(journeyResults.length,12);
console.log(JSON.stringify({status:'PASS_SYNTHETIC_LOCAL_REFERENCE_IMPLEMENTATION',negative_total:12,negative_rejected:negativeResults.length,journey_total:12,journey_expected:journeyResults.length,remote_cas_test:'NOT_TESTED_BY_THIS_SCRIPT',independent_semantic_review:'NOT_EXECUTED',factual_canonicity:'NOT_EVALUATED'}));

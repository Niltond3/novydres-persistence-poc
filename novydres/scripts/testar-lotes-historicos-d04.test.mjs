import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyHistoryBatches} from './verificar-lotes-historicos-d04.mjs';
const base='novydres/cronicas/CHR-001/historico/history-index/lotes-c45.json';
const get=()=>JSON.parse(readFileSync(base,'utf8'));
test('all 27 historical ranges map to 26 exact existing source blobs, not transcriptions',()=>{
 const x=verifyHistoryBatches();
 assert.equal(x.ok,true);
 assert.equal(x.batches,27);
 assert.equal(x.unique_original_files,26);
 assert.equal(x.no_ledger_reconstruction,true);
});
test('source-based historical projection refuses changed facts and fake audit ledgers',()=>{
 const a=get();a.source_rows[0].episode_range='INVENTED';
 assert.throws(()=>verifyHistoryBatches({override:a}),{code:'D04_HISTORY_BATCH_SOURCE_MISMATCH'});
 const b=get();b.source_rows[1].technical_ledger_committed=true;
 assert.throws(()=>verifyHistoryBatches({override:b}),{code:'D04_HISTORY_BATCH_SOURCE_MISMATCH'});
 const c=get();c.no_claim_of_complete_history_index=false;
 assert.throws(()=>verifyHistoryBatches({override:c}),{code:'D04_HISTORY_SEMANTIC_OVERCLAIM'});
});

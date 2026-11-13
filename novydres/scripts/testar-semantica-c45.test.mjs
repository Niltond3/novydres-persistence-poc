import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyC45KnowledgeThreads} from './verificar-semantica-c45.mjs';

const read=p=>JSON.parse(readFileSync(p,'utf8'));
const actor='chr001-knowledge-npc-anna-morozova-vice-diretora';
const path='novydres/cronicas/CHR-001/conhecimento/atores/npc-anna-morozova-vice-diretora/conhecimento.json';
const threads='novydres/cronicas/CHR-001/tramas/abertas/atual-c45.json';
test('D04 C45 all 47 actor rows, four epistemic buckets and 44 threads equal original source',()=>{
 const result=verifyC45KnowledgeThreads();
 assert.equal(result.actors,38);
 assert.equal(result.knowledge_rows,47);
 assert.equal(result.open_threads,44);
 assert.equal(result.evidence_and_unknowns_preserved,true);
 assert.notEqual(result.gate,'D04_PASS');
});
test('D04 refuses promoted NPC suspicion as confirmed knowledge',()=>{
 const a=read(path);
 a.records[0].record.confirmed.push('Invented actor knowledge');
 assert.throws(()=>verifyC45KnowledgeThreads({actorOverrides:{[actor]:a}}),{code:'D04_KNOWLEDGE_SEMANTIC_DIFFERENCE'});
});
test('D04 refuses accidental loss of a source row',()=>{
 const a=read(path);a.records=[];
 assert.throws(()=>verifyC45KnowledgeThreads({actorOverrides:{[actor]:a}}),{code:'D04_KNOWLEDGE_UNMAPPED_SOURCE_ROW'});
});
test('D04 refuses silent change of unknown thread to confirmed outcome',()=>{
 const t=read(threads);t.threads[0].unknown='Resolved without a played scene';
 assert.throws(()=>verifyC45KnowledgeThreads({threadsOverride:t}),{code:'D04_OPEN_THREADS_SEMANTIC_DIFFERENCE'});
});
test('D04 refuses actor promotion into player disclosure',()=>{
 const a=read(path);a.no_player_disclosure=false;
 assert.throws(()=>verifyC45KnowledgeThreads({actorOverrides:{[actor]:a}}),{code:'D04_KNOWLEDGE_SCOPE_OR_DISCLOSURE'});
});

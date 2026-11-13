#!/usr/bin/env node
// NOVYDRES — deterministic source reconciliation; no story generation or writes.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const sha=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const requirePath=(root,p)=>{
 if(typeof p!=='string'||!p.startsWith('novydres/')||p.split(/[\/\\]/).includes('..'))throw Error('unsafe source path: '+p);
 const f=path.resolve(root,p),base=path.resolve(root);
 if(!f.startsWith(base+path.sep))throw Error('escaped source path');
 return f;
};
export function salientIds(threads,lastEventId){
 const important=/^OPEN_OBJECT_|^OPEN_PLAYER_CHARACTERIZATION_|^OPEN_RELATIONAL$|^OPEN_SCHOOL_FAMILY_|^BUSINESS_OPEN_|^OPEN_CONTACT_OPPORTUNITY_/;
 return threads.filter(t=>t.updated_by_event_id===lastEventId||important.test(t.kind||'')).map(t=>t.id).sort();
}
export function assessTemporalTransition(packet,live,openThreads){
 const issues=[],raise=s=>{if(!issues.includes(s))issues.push(s)};
 const last=live.last_confirmed_event_id;
 if(packet.source_checkpoint?.last_event_id!==last)raise('CHECKPOINT_MISMATCH');
 const originals=openThreads.threads||[],seen=new Set(),base=new Map(originals.map(t=>[t.id,t]));
 for(const entry of packet.thread_dispositions||[]){
  if(seen.has(entry.id))raise('DUPLICATE_THREAD:'+entry.id);
  seen.add(entry.id);
  const source=base.get(entry.id);
  if(!source)raise('EXTRANEOUS_THREAD:'+entry.id);
  else if((entry.source_event_id||null)!==(source.updated_by_event_id||null))raise('UNSOURCED_THREAD:'+entry.id);
 }
 for(const t of originals)if(!seen.has(t.id))raise('MISSING_THREAD:'+t.id);
 const attention=salientIds(originals,last);
 const bridged=new Set();
 for(const x of packet.salient_bridges||[]){
  if(bridged.has(x.id))raise('DUPLICATE_SALIENT:'+x.id);
  bridged.add(x.id);
  if(!attention.includes(x.id))raise('EXTRANEOUS_SALIENT:'+x.id);
  if(!x.opening_treatment||x.opening_treatment.length<12||!x.provenance)raise('SALIENT_NOT_EXPLAINED:'+x.id);
 }
 for(const id of attention)if(!bridged.has(id))raise('MISSING_SALIENT:'+id);
 if(packet.mode==='ELLIPSIS'||packet.mode==='MONTAGE'){
  const i=packet.interval||{};
  if(!Number.isInteger(i.min_nights)||!Number.isInteger(i.max_nights)||i.min_nights>i.max_nights||i.max_nights<1)
   raise('INTERVAL_UNBOUNDED');
 } else if(packet.mode==='CONTINUITY'&&(packet.interval?.min_nights!==0||packet.interval?.max_nights!==0))raise('FALSE_ELAPSE_IN_CONTINUITY');
 const mat=packet.contexts?.material_custody||{};
 if(!base.has(mat.thread_id))raise('MATERIAL_NOT_SOURCED');
 if(mat.current_frame_status==='UNKNOWN')raise('MATERIAL_CUSTODY_UNRESOLVED');
 if(mat.current_frame_status==='PLAYER_DECLARED'&&mat.pc_choice_status!=='DECLARED_AND_VERIFIED')raise('UNVERIFIED_PC_CUSTODY');
 if(packet.contexts?.family_knowledge?.contact_claimed&&packet.contexts?.family_knowledge?.mary_box_knowledge==='UNKNOWN')raise('UNSOURCED_FAMILY_CONTACT');
 if(packet.contexts?.workshop?.revenue_delta_claimed)raise('UNSOURCED_REVENUE_DELTA');
 const p=packet.prelude||{};
 if((p.required_player_decisions||[]).length&&!p.all_essential_decisions_resolved)raise('PLAYER_CHOICE_PENDING');
 if((p.distinct_test_count||0)>2)raise('TOO_MANY_PRELUDE_TESTS');
 for(const k of ['obstacle_type','position','main_entrance_effect','lateral_access_effect','movement_options','ownership_status']){
  const v=packet.scene_affordances?.[k]||'';
  if(!v||v==='UNKNOWN'||v==='UNSPECIFIED')raise('GEOMETRY_UNSPECIFIED:'+k);
 }
 const o=packet.opening||{};
 if(!o.ready||o.interval_and_life.length<24||o.pending_carryovers.length<24||o.physical_stakes.length<24)raise('OPENING_INCOMPLETE');
 if(packet.no_story_delta!==true||packet.chat_opening_status!=='PLAYER_VISIBLE_OPENING_PAUSED_NOT_G28_PERSISTED')raise('STORY_DELTA_OR_CHAT_ERASURE');
 return {ready:issues.length===0,issues,disposition_count:seen.size,source_thread_count:originals.length,salient_ids:attention};
}
export function validateTemporalTransition(root,packetPath){
 const file=p=>fs.readFileSync(requirePath(root,p));
 const packet=JSON.parse(file(packetPath).toString('utf8'));
 if(packet.schema_id!=='NOVYDRES_TEMPORAL_TRANSITION_V1')throw Error('bad temporal schema_id');
 if(packet.mode==='CONTINUITY'&&packet.prelude?.distinct_test_count!==0)throw Error('prelude in continuity');
 const source={};
 for(const k of ['live','history_index','episode','character','knowledge','threads']){
  const pin=packet.source_refs?.[k];
  if(!pin?.path||!pin.blob_sha||sha(file(pin.path))!==pin.blob_sha)throw Error('SOURCE_PIN_MISMATCH:'+k);
  source[k]=file(pin.path);
 }
 const live=JSON.parse(source.live.toString('utf8')),threads=JSON.parse(source.threads.toString('utf8'));
 const report=assessTemporalTransition(packet,live,threads);
 if(packet.status==='READY'&&!report.ready)throw Error('FALSE_READY:'+report.issues.join(','));
 if(packet.status==='REVIEW_REQUIRED'&&report.ready)throw Error('FALSE_BLOCKER: review is complete');
 if(live.last_confirmed_event_id!==packet.source_checkpoint.last_event_id)throw Error('LIVE_CHECKPOINT_MISMATCH');
 return {...report,package_status:packet.status,packet:packetPath};
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname)){
 try{
  const n=process.argv.indexOf('--root'),p=process.argv.indexOf('--packet');
  const root=path.resolve(n<0?process.cwd():process.argv[n+1]);
  console.log(JSON.stringify(validateTemporalTransition(root,p<0?'novydres/chronicles/CHR-001/preparations/M3.02_TEMPORAL_TRANSITION_V1_PLAYER_SAFE.json':process.argv[p+1])));
 }catch(e){console.error(String(e));process.exitCode=1;}
}

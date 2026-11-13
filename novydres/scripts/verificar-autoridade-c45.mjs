// D04: independently pin prior activation V018 and C45 prospective V019; no new story authority.
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const M='c9fcfc0c558cd17d58ec8c8272da3ed70182ff37';
const path='novydres/cronicas/CHR-001/documentos/proveniencia-arquitetura/autoridade-c45.json';
const fail=code=>{const e=new Error(code);e.code=code;throw e;};
const git=(...args)=>execFileSync('git',args,{encoding:'utf8',maxBuffer:1024*1024,stdio:['ignore','pipe','ignore']});
export function verifyStoryAuthority({override=null}={}){
 const doc=override||JSON.parse(readFileSync(path,'utf8'));
 const refs=new Map((doc.source_refs||[]).map(x=>[x.id,x]));
 if(doc.subject_id!=='chr001-runtime-story-architecture'||doc.status!=='CANDIDATE_NON_OPERATIONAL'||
   doc.visibility!=='SYSTEM_AUDIT'||doc.source_commit!==M||refs.size!==6)
   fail('D04_STORY_SCOPE_DRIFT');
 for(const [source,ref] of refs){
   if(!source.startsWith('novydres/')||source.includes('..')||
      ref.source_commit!==M||!/^[a-f0-9]{40}$/.test(ref.sha)||
      git('rev-parse',M+':'+source).trim()!==ref.sha)
      fail('D04_STORY_BLOB_DRIFT');
 }
 const name=n=>[...refs.entries()].find(([p])=>p.endsWith('/'+n));
 const source=(n)=>{const [p]=name(n)||[];if(!p)fail('D04_STORY_REQUIRED_SOURCE_MISSING');return git('show',M+':'+p);};
 const pin=n=>name(n)?.[1]?.sha;
 const approval=JSON.parse(source('PLAYER_DECISION_AGENT_ACCESS_V004.json'));
 const activation=JSON.parse(source('D07_ACTIVATION_V004_PLAYER_SAFE.json'));
 const cycle=JSON.parse(source('CYCLE_V0045.json'));
 const v19=source('D07_STORY_TRUTH_PACKAGE_V019_GM_HIDDEN.md');
 const v18=source('D07_STORY_TRUTH_PACKAGE_V018_GM_HIDDEN.md');
 const prep=source('D08_STORY_PREPARATION_V022_GM_HIDDEN.md');
 if(!approval||!v18||!prep||activation.status!=='ACTIVE'||
    activation.runtime_activation?.d07_active!==true||
    activation.authorization_ref?.blob_sha!==pin('PLAYER_DECISION_AGENT_ACCESS_V004.json')||
    activation.truth_package_ref?.blob_sha!==pin('D07_STORY_TRUTH_PACKAGE_V018_GM_HIDDEN.md')||
    cycle.activation?.d07_activation?.blob_sha!==pin('D07_ACTIVATION_V004_PLAYER_SAFE.json')||
    cycle.activation?.truth_package?.blob_sha!==pin('D07_STORY_TRUTH_PACKAGE_V019_GM_HIDDEN.md')||
    cycle.cycle_id!=='CHR001-CYCLE-0045'||cycle.checkpoint?.next_scene!=='C02'||
    !v19.includes(pin('D07_STORY_TRUTH_PACKAGE_V018_GM_HIDDEN.md')))
    fail('D04_STORY_AUTHORITY_LINEAGE_DRIFT');
 const b=doc.boundaries||{},c=doc.c45_authority||{};
 if(b.V018_activation_record_not_silently_rewritten_to_V019!==true||
    b.V019_cycle_binding_not_silently_reverted_to_V018!==true||
    b.gm_hidden_player_disclosure!==false||
    b.actor_knowledge_not_promoted!==true||
    b.preparation_is_not_played_event!==true||
    c.candidate_runtime_activation!==false||c.source_scene_ready!==cycle.operational_gates.scene_ready||
    c.source_narrator_permission!==cycle.operational_gates.narrator_permission||
    c.source_narrator_prompt_required!==cycle.narrator_prompt_required||
    c.last_confirmed_event_id!==cycle.checkpoint.last_event_id||
    c.next_scene!==cycle.checkpoint.next_scene||c.next_scene_started!==false)
    fail('D04_STORY_UNAUTHORIZED_PROMOTION');
 return {ok:true,gate:'D04_SOURCE_AUTHORIAL_CHAIN_CONFIRMED_NO_RUNTIME_PROMOTION',
 source_commit:M,source_pins:6,approval_chain:'V004_ACTIVATES_V018_C45_PINS_V019_PROSPECTIVELY',
 candidate_runtime_activation:false,gm_disclosure:false};
}
if(process.argv[1]?.endsWith('/verificar-autoridade-c45.mjs'))
 console.log(JSON.stringify(verifyStoryAuthority()));

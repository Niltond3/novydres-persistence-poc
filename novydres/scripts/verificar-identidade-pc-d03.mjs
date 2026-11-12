// D03 exact global identity from approved local target name; no CHR-001 state promotion.
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const read=p=>JSON.parse(readFileSync(p,'utf8'));
const fail=code=>{let e=new Error(code);e.code=code;throw e;};
const sha=b=>createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
export function verifyD03PC({profileOverride=null}={}){
 const id='pc-bartholomeu-krauser',dir='novydres/personagens/'+id;
 const p=profileOverride||read(dir+'/perfil.json'),meta=read(dir+'/assunto.json'),
  s=read('novydres/catalogo.json').subjects.find(x=>x.id===id);
 const src='novydres/chronicles/CHR-001/character/TARGET_SHEET_V2_APPROVED.json';
 const file=readFileSync(src),target=JSON.parse(file),digest=sha(file);
 if(!s||s.path!==dir||s.visibility!=='SYSTEM_AUDIT'||meta.subject_id!==id||meta.status!=='CANDIDATE')
   fail('D03_PC_OWNER_INVALID');
 if(target.status!=='APPROVED_LOCAL_TARGET_ACTIVE_NOT_BOUGHT'||
    p.subject_id!==id||p.status!=='CANDIDATE_NONOPERATIONAL'||p.scope!=='GLOBAL_IDENTITY_ONLY'||
    p.identity_name?.value!==target.name||p.identity_name?.source_blob_sha!==digest||
    p.identity_name?.epistemic_status!=='CONFIRMED'||
    p.identity_name?.no_other_target_properties_promoted!==true||
    p.local_knowledge_copied!==false||p.character_sheet_or_xp_copied!==false||
    p.not_operational!==true)fail('D03_PC_IDENTITY_AUTHORITY');
 const rel=read('novydres/cronicas/CHR-001/elenco/npc-samir-haddad/relacoes.json');
 if(rel.external_target_id_not_migrated_in_phase_b===true||
    !rel.relations.some(x=>x.to_subject_id===id&&x.inverse_is_derived===true&&x.owner_subject_id==='chr001-npc-samir-haddad'))
    fail('D03_PC_LINK_NOT_RESOLVED');
 return {ok:true,global_subject:id,source_sha:digest,local_state_promoted:false,deferred_reference_resolved:true};
}

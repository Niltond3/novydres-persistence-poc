import {readFileSync} from 'node:fs';
export function verifyD03Segments(root=process.cwd(),override=null){
  const base='novydres/sistema/arquitetura/fase-d/';
  const idx=override||JSON.parse(readFileSync(base+'fragmentos-d03.json','utf8'));
  if(idx.not_operational!==true || idx.visibility!=='SYSTEM_AUDIT' ||
    idx.epistemic_policy!=='SOURCE_LITERAL_UNEVALUATED_NO_AUTOMATIC_FACT_PROMOTION'||
    idx.editorial_authority!=='DECLARATIONS_ARE_LITERALS_NOT_APPROVAL_VERDICTS')
    throw Object.assign(new Error('D03_SEGMENT_AUTHORITY_PROMOTION'),{code:'D03_SEGMENT_AUTHORITY_PROMOTION'});
  if(idx.documents?.length!==64||new Set(idx.documents.map(x=>x.source_path)).size!==64)
    throw Object.assign(new Error('D03_SEGMENT_ORIGIN_COVERAGE'),{code:'D03_SEGMENT_ORIGIN_COVERAGE'});
  const catalog=JSON.parse(readFileSync('novydres/catalogo.json','utf8'));
  const entries=new Map();
  for(const d of idx.documents){
    if(!d.owner_subject_id||!d.source_blob_sha||!Array.isArray(d.sections_or_fields))
      throw Object.assign(new Error('D03_SEGMENT_PROVENANCE_MISSING'),{code:'D03_SEGMENT_PROVENANCE_MISSING'});
    if(d.epistemic_status!=='SOURCE_LITERAL_UNEVALUATED'||d.visibility!=='SYSTEM_AUDIT')
      throw Object.assign(new Error('D03_SEGMENT_TRUTH_PROMOTION'),{code:'D03_SEGMENT_TRUTH_PROMOTION'});
    const subject=catalog.subjects.find(s=>s.id===d.owner_subject_id);
    if(!subject)throw Object.assign(new Error('D03_SEGMENT_OWNER_UNKNOWN'),{code:'D03_SEGMENT_OWNER_UNKNOWN'});
    const ledger=JSON.parse(readFileSync(subject.path+'/registro.json','utf8'));
    const source=ledger.source_records.find(x=>x.source_path===d.source_path&&x.source_blob_sha===d.source_blob_sha);
    if(!source)throw Object.assign(new Error('D03_SEGMENT_LEDGER_MISMATCH'),{code:'D03_SEGMENT_LEDGER_MISMATCH'});
    const literal=readFileSync(source.target_path,'utf8'),lines=literal.split(/\r?\n/);
    if(lines.length!==d.line_count)throw Object.assign(new Error('D03_SEGMENT_LINE_COUNT'),{code:'D03_SEGMENT_LINE_COUNT'});
    if(!d.sections_or_fields.length)
      throw Object.assign(new Error('D03_SEGMENT_NO_LOCATOR'),{code:'D03_SEGMENT_NO_LOCATOR'});
    for(const f of d.sections_or_fields){
      if(f.kind==='MARKDOWN_SECTION'||f.kind==='DOCUMENT_WHOLE'){
        if(f.kind==='MARKDOWN_SECTION'){
          const actual=(lines[f.line_start-1]||'').trim();
          if(!/^#{1,5}\s/.test(actual)||actual.replace(/^#+\s*/,'').slice(0,160)!==f.label)
            throw Object.assign(new Error('D03_SEGMENT_LABEL_MISMATCH'),{code:'D03_SEGMENT_LABEL_MISMATCH'});
        }
        if(!Number.isInteger(f.line_start)||f.line_start<1||!Number.isInteger(f.line_end)||
          f.line_end<f.line_start||f.line_end>d.line_count)
          throw Object.assign(new Error('D03_SEGMENT_INVALID_RANGE'),{code:'D03_SEGMENT_INVALID_RANGE'});
      }else if(f.kind==='JSON_TOP_LEVEL_FIELD' && typeof f.json_pointer==='string' && f.json_pointer.startsWith('/') && !f.json_pointer.slice(1).includes('/')){
        const field=f.json_pointer.slice(1).replace(/~1/g,'/').replace(/~0/g,'~');
        if(!Object.hasOwn(JSON.parse(literal),field))
          throw Object.assign(new Error('D03_SEGMENT_JSON_FIELD_MISSING'),{code:'D03_SEGMENT_JSON_FIELD_MISSING'});
      }else if(f.kind==='PY_DECLARATION'&&Number.isInteger(f.line_start)){
        if(!/^(class|def) \w+/.test(lines[f.line_start-1]||''))
          throw Object.assign(new Error('D03_SEGMENT_PY_ANCHOR_MISSING'),{code:'D03_SEGMENT_PY_ANCHOR_MISSING'});
      }else throw Object.assign(new Error('D03_SEGMENT_INVALID_LOCATOR'),{code:'D03_SEGMENT_INVALID_LOCATOR'});
    }
    entries.set(d.source_path,d);
  }
  const inv=JSON.parse(readFileSync(base+'inventario-origens.json','utf8'));
  const original=inv.source_files.filter(x=>x.d01_origin_route?.handoff_phase==='D03');
  for(const x of original){
    const row=entries.get(x.source_path);
    if(!row||row.source_blob_sha!==x.source_blob_sha)
      throw Object.assign(new Error('D03_SEGMENT_SOURCE_SHA'),{code:'D03_SEGMENT_SOURCE_SHA'});
  }
  return {ok:true,documents:idx.documents.length,locators:idx.documents.reduce((n,d)=>n+d.sections_or_fields.length,0),not_operational:true};
}

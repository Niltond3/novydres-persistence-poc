import hashlib, json, re
from pathlib import Path
BASE=Path(__file__).resolve().parent
checks=[]
def blob(p):
 d=p.read_bytes(); return hashlib.sha1(f"blob {len(d)}\0".encode()+d).hexdigest()
def check(ok,label):
 checks.append((label,bool(ok)))
 if not ok: raise AssertionError(label)
ep=BASE/"source-candidates/M3.01_v007.source.txt"
st=BASE/"source-candidates/state_v045.source.txt"
rec=BASE/"D06_SOURCE_RECONCILIATION_V002.json"
e=ep.read_text(encoding="utf-8"); s=st.read_text(encoding="utf-8"); r=json.loads(rec.read_text(encoding="utf-8"))
check(blob(ep)=="4192586d8561c89c7e759b921038bee0422b7512","M3.01 v007 blob SHA")
check(blob(st)=="197e015135626508c07372b257c29cf889284f6d","state v045 blob SHA")
check("APPROVAL-D06-002" in e[:1500],"episode cites current player correction")
check("M3.01 e a criação do personagem se passam em 1970" in e[:1500],"M3.01 and character creation in 1970")
check("Bartolomeu permanece mortal em todas as cenas" in e[:1500],"Bart mortal throughout M3.01")
check("nenhum Abraço é registrado em M3.01" in e[:1500],"no Embrace in M3.01")
check("depois do checkpoint M3.01 C05 e antes de 1970-12-25" in e[:1500],"forced Embrace target after C05 and before cutoff")
check(re.search(r"(?:antes de|before) 1970(?!-\d)", e, re.I) is None,"no active pre-1970 rule remains")
check("UNKNOWN" in e[:1500],"exact dates remain unknown")
check("last played section; C06 not started" in s,"C05 last played and C06 not started")
check("CHR001-M301-C05-22-20261109-001" in s,"cycle event preserved")
check("Bartholomeu Krauser remains mortal; no Abraço has occurred." in s,"current mortal/no-Embrace state preserved")
check("state_v043.source.txt | BLOB_SHA: 46612796f44c9b75cbd7ab43854dcec33283804a" in s,"old state blob identity preserved")
check("not silently relabeled" in s,"old state provenance not reinterpreted")
check("NON_OPERATIONAL; NOT PROMOTED" in s,"state candidate stays non-operational")
check(r["design_branch"]["head_read"]=="1360dbd2bad2124859f1d145c69b0c41ec589347","current documentary branch base recorded")
check(r["master"]["head_read"]=="735fe5d52e2761c4d492fe873a4b6bbcce17654a" and r["master"]["modified_by_this_run"] is False,"master unchanged")
check(r["correction_record"]["id"]=="APPROVAL-D06-002","player correction registered")
check(r["timeline_reconciliation"]["approval"]=="APPROVAL-D06-002","timeline follows current approval")
check("C05 is the last played" in r["state_provenance_reconciliation"]["correction"],"state correction recorded")
check("BLOCKED_CONFLICT" in r["gate_disposition"]["operational_gate"],"operational conflict stays blocked")
check("BLOCKED_EXTERNAL_DEPENDENCY" in r["gate_disposition"]["secret_truth"],"secret-dependent content stays blocked")
check(r["gate_disposition"]["scene_ready"]=="NOT_VERIFIED","scene readiness not inferred")
check(r["gate_disposition"]["narrator_permission"]=="NOT_GRANTED","Narrator permission not inferred")
result={"validator":"D06_SOURCE_VALIDATE_V002.py","status":"PASS","checks_passed":len(checks),"checks_total":len(checks),"checks":[{"id":f"SRC-{i:02d}","label":l,"result":"PASS"} for i,(l,_) in enumerate(checks,1)],"validator_blob_sha":blob(Path(__file__)),"inputs":{"episode_blob_sha":blob(ep),"state_blob_sha":blob(st),"reconciliation_blob_sha":blob(rec)}}
(BASE/"D06_SOURCE_VALIDATE_V002_RESULT.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"PASS: {len(checks)}/{len(checks)} D06 source checks")

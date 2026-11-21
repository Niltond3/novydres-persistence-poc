"""Negative regressions for real Web closure, retry, and road junctions."""
import copy
import io
import json
import sys
import zipfile
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import web_bridge as bridge
import orchestration as ledger
import contracts
import infra_checks as spatial
from test_infra_deterministic import scene, audit


def _crossing_scene(tmp_path):
    geo, output, profile = scene(tmp_path)
    geo["network"]["nodes"] += [
        {"id":"C","point":[5,0],"level":0},
        {"id":"D","point":[5,5],"level":0},
        {"id":"J","point":[5,1],"level":0}]
    geo["network"]["edges"].append({
        "id":"rail","mode":"rail","from":"C","to":"D",
        "points":[[5,0],[5,5]],"level":0,"width_units":1})
    return geo, output, profile


def test_reject_fictitious_and_unsplit_junctions(tmp_path):
    data, output, profile=_crossing_scene(tmp_path)
    data["network"]["crossings"]=[{
        "a":"road-01","b":"rail","kind":"at_grade",
        "authorized_junction_id":"fabricated"}]
    output.write_text(json.dumps(data))
    with pytest.raises(spatial.InfraInvalid,match="existing node"):
        audit(output,profile)
    data["network"]["crossings"][0]["authorized_junction_id"]="J"
    output.write_text(json.dumps(data))
    with pytest.raises(spatial.InfraInvalid,match="split"):
        audit(output,profile)


def test_actual_split_junction_requires_rail_authority(tmp_path):
    data,output,profile=_crossing_scene(tmp_path)
    data["network"]["edges"]=[
        {"id":name,"mode":mode,"from":start,"to":end,
         "points":[data["network"]["nodes"][0]["point"],[5,1]] if name=="r1" else
                  [[5,1],data["network"]["nodes"][1]["point"]] if name=="r2" else
                  [[5,0],[5,1]] if name=="r3" else [[5,1],[5,5]],
         "level":0,"width_units":1}
        for name,mode,start,end in [
            ("r1","road","A","J"),("r2","road","J","B"),
            ("r3","rail","C","J"),("r4","rail","J","D")]]
    data["network"]["crossings"]=[{
        "a":"r1","b":"r3","kind":"at_grade","authorized_junction_id":"J"}]
    output.write_text(json.dumps(data))
    with pytest.raises(spatial.InfraInvalid,match="specific owner authority"):
        audit(output,profile)
    data["network"]["crossings"][0]["authority"]={
        "status":"APPROVED","decision_id":"REAL-APPROVED-ID",
        "evidence":"Owner approved this exact rail crossing"}
    output.write_text(json.dumps(data))
    assert audit(output,profile)["status"]=="PASS"


def test_declared_grade_separation_must_have_actual_crossing(tmp_path):
    data,output,profile=scene(tmp_path)
    data["network"]["nodes"] += [
        {"id":"X","point":[1,5],"level":-1},
        {"id":"Y","point":[10,5],"level":-1}]
    data["network"]["edges"] += [{
        "id":"metro","mode":"metro","from":"X","to":"Y",
        "points":[[1,5],[10,5]],"level":-1,"width_units":1}]
    data["network"]["crossings"]=[{
        "a":"road-01","b":"metro","kind":"grade_separated"}]
    output.write_text(json.dumps(data))
    with pytest.raises(spatial.InfraInvalid,match="does not intersect"):
        audit(output,profile)


def test_image_fourth_and_seventh_attempt_not_deadlocked():
    h="a"*64
    data={"schema":"NOVYDRES_MAPWORK_UNIT_LEDGER_1","units":{}}
    def start(strategy=None,evidence=None,request=None):
        return contracts.unit_transition(data,"u",event="START",input_sha256=h,
                    strategy_id=strategy,replan_evidence=evidence,request_id=request)
    def fail():
        return contracts.unit_transition(data,"u",event="AUDIT_FAIL",
                                        input_sha256=h,receipt={"failure":"road seam out of bounds"})
    for i in (1,2,3):
        start("method-1",request="req-"+str(i))
        state=fail()
    assert state["status"]=="REPLAN_REQUIRED"
    with pytest.raises(contracts.Blocked,match="strategy"):
        start("method-1",request="req-4")
    start("method-2",evidence="Replan the road crossing and resample all neighboring joins",
          request="req-4")
    assert data["units"]["u"]["attempts"]==4
    fail()
    for i in (5,6):
        start("method-2",request="req-"+str(i))
        state=fail()
    assert state["status"]=="METHOD_REASSESSMENT"
    with pytest.raises(contracts.Blocked,match="strategy"):
        start("method-2",request="req-7")
    start("new-decomposition",evidence="Reassess corridor geometry method and change decomposition into new work units",
          request="req-7")
    assert data["units"]["u"]["attempts"]==7
    assert fail()["status"]=="REPAIR_REQUIRED"


def test_hash_chain_detects_mutated_replay(tmp_path):
    from test_orchestration import failed,submit
    a=failed(1)
    assert submit(tmp_path,a)["status"]=="RECORDED"
    path=tmp_path/"ledger.json"
    data=json.loads(path.read_text())
    data["stages"]["INF-01"]["attempts"][0]["strategy_id"]="forged"
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError,match="hash chain"):
        submit(tmp_path,failed(2))


def test_zip_rejects_duplicate_and_unlisted_bytes(tmp_path):
    payload=b"print('verified')\n"
    directory=tmp_path/"target"
    file_path=directory/"scripts"/"a.py"
    file_path.parent.mkdir(parents=True)
    file_path.write_bytes(payload)
    item={"path":"scripts/a.py","provider":"github",
          "sha256":bridge.sha256(payload),"blob_sha":bridge.git_blob_sha(payload),
          "size_bytes":len(payload)}
    manifest={"schema":bridge.FILE_MANIFEST_SCHEMA,
              "source_commit":"1"*40,"files":[item]}
    blob=tmp_path/"source.zip"
    with zipfile.ZipFile(blob,"w") as z:
        z.writestr("scripts/a.py",payload)
        z.writestr("extra.txt","unlisted")
    with pytest.raises(bridge.WebBridgeError,match="inventory"):
        bridge.extract_verified_zip(blob,tmp_path/"extract",
                         manifest=manifest,source_commit="1"*40)
    dup=tmp_path/"duplicate.zip"
    with zipfile.ZipFile(dup,"w") as z:
        z.writestr("scripts/a.py",payload)
        z.writestr("scripts/a.py",payload)
    with pytest.raises(bridge.WebBridgeError,match="duplicate"):
        bridge.extract_verified_zip(dup,tmp_path/"extract2",
                         manifest=manifest,source_commit="1"*40)


def test_incomplete_source_manifest_never_executes(tmp_path):
    source=tmp_path/"scripts"/"a.py"
    source.parent.mkdir(parents=True)
    source.write_text("pass")
    payload=source.read_bytes()
    manifest={"schema":bridge.FILE_MANIFEST_SCHEMA,"source_commit":"1"*40,
              "files":[{"path":"scripts/a.py","provider":"github",
                        "sha256":bridge.sha256(payload),
                        "blob_sha":bridge.git_blob_sha(payload),
                        "size_bytes":len(payload)}]}
    (tmp_path/"scripts"/"injected.py").write_text("raise RuntimeError('do not execute')")
    with pytest.raises(bridge.WebBridgeError,match="unverified executable"):
        bridge.verify_files(manifest,root=tmp_path)

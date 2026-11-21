"""Single pipeline's synthetic branch cannot acquire canonical authority."""
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import flow
import synthetic_trial as trial
import topology
import infra_checks as infra
import web_bridge


OP = "a" * 64
BRANCH = "mapwork/consolidated-autonomous-20261121"
JOURNAL = "sessions/agent3-live-second-journal.json"
REF = "b" * 64


def prepared(tmp_path):
    journal = tmp_path / "journal.json"
    journal.write_text(json.dumps({"schema": "NOVYDRES_MAPWORK_AUTONOMOUS_SESSION",
        "branch": BRANCH, "journal_repo_path": JOURNAL, "source_commit": "2"*40,
        "publication_authorized": False, "steps": [{"operation_id": OP, "status": "PENDING"}]}))
    spec = {"schema": trial.SYNTHETIC_SCHEMA, "test_only": True,
        "scenario_id": "synthetic-rail-overpass", "canonical_target": None,
        "publication_authorized": False, "canonical_state_changed": False,
        "criteria_sha256": hashlib.sha256((ROOT/"docs/infra-acceptance.md").read_bytes()).hexdigest(),
        "reference_sha256": REF, "reference_size": [32, 32],
        "resume_operation_id": OP, "branch": BRANCH, "journal_repo_path": JOURNAL}
    file = tmp_path / "spec.json"
    file.write_text(json.dumps(spec))
    args = SimpleNamespace(synthetic_trial=str(file),autonomous_journal=str(journal),
        host_branch=BRANCH,host_journal_path=JOURNAL,intent=None,district="sulfok",
        execute=False,zone=None,reference=None,before=None,editable_mask=None,
        assets=None,recipe_unit=None,audit_unit=None,design_unit=None,
        spatial=None,unit_receipt=None,visual_review=None,record_attempt=None,ledger=None)
    return args, spec, journal


def geometry(tmp_path, args):
    nodes = [{"id": i, "point": p, "level": level} for i,p,level in (
        ("W",[2,16],1),("E",[30,16],1),("N",[16,2],0),("S",[16,30],0))]
    edges = [{"id": i,"from":a,"to":b,"points":points,"mode":mode,
              "level":level,"width_units":1} for i,a,b,points,mode,level in (
        ("ROAD","W","E",[[2,16],[30,16]],"road",1),
        ("RAIL","N","S",[[16,2],[16,30]],"rail",0))]
    source={"schema":"NOVYDRES_MAPWORK_INFRA_GEOMETRY","stage":"INF-01",
        "source_sha256":REF,"reference_size":[32,32],"target":"synthetic-rail-overpass",
        "network":{"nodes":nodes,"edges":edges,"crossings":[]}}
    classification={"schema":"NOVYDRES_MAPWORK_TOPOLOGY_CLASSIFICATIONS",
        "reference_sha256":REF,"network_sha256":topology.digest(source["network"]),
        "protected_edge_ids":[],"crossings":[{
            "id":"X","corridors":["RAIL","ROAD"],"point":[16,16],
            "status":"RESOLVED","relation":"grade_separated",
            "levels":{"RAIL":0,"ROAD":1},
            "visual":{"inspected_by":"AGENT","reference_sha256":REF,
                      "bbox":[0,0,32,32],"observation":"Crossing grade visually inspected"},
            "geometry_observation":"Grade-separated road over railway",
            "editorial":{"new_element":False}}]}
    candidate, report = topology.reconcile(source,classification)
    assert report["status"] == "RECONCILED_NOT_ACCEPTED"
    mask = tmp_path / "mask.png"
    Image.new("L", (32,32),255).save(mask)
    candidate.update(fixture_mode=True,zone_mask={"path":mask.name,"sha256":infra.sha(mask)})
    file = tmp_path / "geometry.json"
    file.write_text(json.dumps(candidate))
    args.spatial = str(file)
    return file


def test_isolated_trial_keeps_existing_journal_and_ignores_sulfok(tmp_path):
    args, _, journal = prepared(tmp_path)
    state = flow.run(args,None)
    assert state["target"] == "synthetic-rail-overpass"
    assert state["next_action"] == "RECONCILE_SYNTHETIC_TOPOLOGY"
    assert state["publication_authorized"] is False
    assert json.loads(journal.read_text())["steps"][0]["operation_id"] == OP


def test_real_zone_unsafe_outputs_and_unbound_trial_rejected(tmp_path):
    args, spec, _ = prepared(tmp_path)
    args.execute = True
    with pytest.raises(Exception,match="canonical renderer"):
        flow.run(args,None)
    args.execute = False
    spec["canonical_target"] = "sulfok"
    Path(args.synthetic_trial).write_text(json.dumps(spec))
    with pytest.raises(Exception,match="noncanonical authority"):
        flow.run(args,None)
    spec["canonical_target"] = None
    spec["resume_operation_id"] = "f"*64
    Path(args.synthetic_trial).write_text(json.dumps(spec))
    with pytest.raises(Exception,match="recovered operation"):
        flow.run(args,None)
    with pytest.raises(Exception,match="cannot overwrite canonical"):
        trial.synthetic_output_path(ROOT/"zones"/"cidade-velha"/"acceptance-ledger.json")


def test_topology_recomputed_and_native_png_required(tmp_path):
    args, _, _ = prepared(tmp_path)
    file = geometry(tmp_path,args)
    state = flow.run(args,None)
    assert state["audit"]["topology_status"] == "PASS"
    assert state["next_action"] == "GENERATE_AND_AUDIT_CANDIDATE"
    data = json.loads(file.read_text())
    data["network"]["crossings"] = []
    file.write_text(json.dumps(data))
    assert flow.run(args,None)["next_action"] == "REPAIR_SYNTHETIC_TOPOLOGY"


def test_png_readback_mismatch_refuses_visual_progress(tmp_path):
    args, _, _ = prepared(tmp_path)
    geometry(tmp_path,args)
    source=tmp_path/"native.png"
    Image.new("RGB",(32,32),(20,40,60)).save(source)
    remote=tmp_path/"get.png"
    remote.write_bytes(b"tampered")
    receipt=tmp_path/"receipt.json"
    receipt.write_text(json.dumps({"provider":"drive","remote_id":"drive-id",
        "native_generation":True,"path":str(source),"readback_path":str(remote),
        "sha256":hashlib.sha256(source.read_bytes()).hexdigest()}))
    args.unit_receipt = str(receipt)
    with pytest.raises(Exception,match="Drive image bytes/SHA"):
        flow.run(args,None)


def test_runtime_source_upgrade_must_preserve_old_journal(tmp_path):
    args, _, journal = prepared(tmp_path)
    recovery = tmp_path/"recovery.json"
    recovery.write_text(json.dumps({"schema":"NOVYDRES_MAPWORK_COLD_RECOVERY",
        "source_commit":"2"*40,"branch":BRANCH,"journal_repo_path":JOURNAL}))
    proof = tmp_path/"upgrade.json"
    original={"schema":"NOVYDRES_MAPWORK_SYNTHETIC_RUNTIME_UPGRADE",
        "test_only":True,"journal_sha256":hashlib.sha256(journal.read_bytes()).hexdigest(),
        "journal_source_commit":"2"*40,"runtime_source_commit":"3"*40,
        "branch":BRANCH,"journal_repo_path":JOURNAL,
        "github_compare":{"base":"2"*40,"head":"3"*40,"status":"ahead","ahead_by":1}}
    proof.write_text(json.dumps(original))
    argv=["--synthetic-trial",args.synthetic_trial,"--host-recovery",str(recovery),
        "--host-runtime-upgrade-proof",str(proof),"--autonomous-journal",str(journal),
        "--host-branch",BRANCH,"--host-journal-path",JOURNAL]
    web_bridge._verify_synthetic_runtime_upgrade(argv,"3"*40,"2"*40)
    original["github_compare"]["head"] = "2"*40
    proof.write_text(json.dumps(original))
    with pytest.raises(web_bridge.WebBridgeError,match="ancestry mismatch"):
        web_bridge._verify_synthetic_runtime_upgrade(argv,"3"*40,"2"*40)

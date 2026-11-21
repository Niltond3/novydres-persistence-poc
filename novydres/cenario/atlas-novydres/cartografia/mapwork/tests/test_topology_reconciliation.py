"""Classified batch topology: positive, negative, multimodal and real Kingswell boundaries."""
import copy
import json
import math
import sys
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import topology
import infra_checks
import urban_architecture as urban
import acceptance
import pipeline


def geo(edges, *, source="a"*64):
    nodes=[]
    roads=[]
    for ident, mode, p, q, level in edges:
        a,b=ident+"-A",ident+"-B"
        nodes += [{"id":a,"point":list(p),"level":level},
                  {"id":b,"point":list(q),"level":level}]
        roads.append({"id":ident,"from":a,"to":b,"points":[list(p),list(q)],
                      "mode":mode,"level":level,"width_units":1})
    return {"schema":"NOVYDRES_MAPWORK_INFRA_GEOMETRY",
            "stage":"INF-01","source_sha256":source,
            "reference_size":[32,32],
            "target":"kingswell",
            "network":{"nodes":nodes,"edges":roads,"crossings":[]}}


def crossing(a="H", b="V",relation="at_grade",point=(6,6),levels=(0,0),
             *, approved=False, new_element=False):
    entry={"id":"X-"+a+"-"+b+"-"+str(point),
           "corridors":sorted([a,b]),"point":list(point),
           "status":"RESOLVED","relation":relation,
           "levels":{a:levels[0],b:levels[1]},
           "visual":{"inspected_by":"AGENT","reference_sha256":"a"*64,
                     "bbox":[0,0,32,32],
                     "observation":"Observed both roadbeds at the exact source image locus."},
           "geometry_observation":"Source centerline intersections measured without snapping.",
           "editorial":{"new_element":new_element}}
    if approved:
        entry["editorial"].update(status="APPROVED",decision_id="KW-EXIST-01",
                                  evidence="Owner expressly authorized the existing crossing.")
    if relation=="no_connection":
        entry["barrier_evidence"]="Fenced separate physical carriageways."
    return entry


def classifications(data, *records):
    return {"schema":"NOVYDRES_MAPWORK_TOPOLOGY_CLASSIFICATIONS",
            "reference_sha256":data["source_sha256"],
            "network_sha256":topology.digest(data.get("network",data.get("transport"))),
            "crossings":list(records),"protected_edge_ids":[]}


def simple(level=0,mode="road"):
    return geo([("H","road",(1,6),(12,6),0),("V",mode,(6,1),(6,12),level)])


def run(data, *records, **kwargs):
    return topology.reconcile(data,classifications(data,*records),**kwargs)


def audit_network(tmp_path, data):
    mask=tmp_path/"mask.png"
    Image.new("L",(32,32),255).save(mask)
    data["zone_mask"]={"path":mask.name,"sha256":infra_checks.sha(mask)}
    candidate=tmp_path/"candidate.json"
    candidate.write_text(json.dumps(data),encoding="utf-8")
    return infra_checks.validate(candidate,source_sha="a"*64,
         dimensions=(32,32),profile=acceptance.criteria_contract()["profile"])


def test_atgrade_batch_splits_both_edges_and_proves_real_incidence(tmp_path):
    data=simple()
    result,report=run(data,crossing())
    assert report["status"]=="RECONCILED_NOT_ACCEPTED"
    assert report["observed_crossings"]==1
    assert report["result_edge_count"]==4
    assert report["created_nodes"]==1
    nodes={n["id"]:n for n in result["network"]["nodes"]}
    assert len(result["network"]["crossings"])==4
    assert len({c["authorized_junction_id"] for c in result["network"]["crossings"]})==1
    assert all(nodes[c["authorized_junction_id"]]["point"]==[6,6]
               for c in result["network"]["crossings"])
    assert audit_network(tmp_path,result)["status"]=="PASS"
    again,second=topology.reconcile(result,classifications(data,crossing()))
    assert again==result and second==report


def test_grade_separation_uses_two_nonincident_nodes_with_real_levels(tmp_path):
    data=simple(level=1)
    result,report=run(data,crossing(relation="grade_separated",levels=(0,1)))
    assert report["created_nodes"]==2
    assert len(result["network"]["crossings"])==4
    assert all(c["kind"]=="grade_separated" for c in result["network"]["crossings"])
    assert not ({e["from"] for e in result["network"]["edges"][:2]} &
                {e["from"] for e in result["network"]["edges"][2:]})
    assert audit_network(tmp_path,result)["status"]=="PASS"


def test_same_level_nonconnection_requires_barrier_without_graph_junction(tmp_path):
    data=simple()
    rec=crossing(relation="no_connection")
    with pytest.raises(topology.TopologyInvalid,match="barrier"):
        run(data,{k:v for k,v in rec.items() if k!="barrier_evidence"})
    result,_=run(data,rec)
    assert all(c["kind"]=="no_connection" for c in result["network"]["crossings"])
    assert len({n["id"] for n in result["network"]["nodes"]
                if n["point"]==[6,6]})==2
    assert audit_network(tmp_path,result)["status"]=="PASS"


def test_two_crossings_on_one_polyline_preserve_original_endpoints(tmp_path):
    data=geo([("H","road",(1,6),(14,6),0),
              ("V","road",(4,1),(4,12),0),
              ("W","road",(10,1),(10,12),0)])
    result,report=run(data,crossing("H","V",point=(4,6)),
                            crossing("H","W",point=(10,6)))
    h=[e for e in result["network"]["edges"] if e["id"].startswith("H~")]
    assert len(h)==3
    assert [e["points"] for e in h]==[[[1,6],[4,6]],
                                      [[4,6],[10,6]],[[10,6],[14,6]]]
    assert h[0]["from"]=="H-A" and h[-1]["to"]=="H-B"
    assert report["result_edge_count"]==7
    assert audit_network(tmp_path,result)["status"]=="PASS"


def test_near_crossing_is_not_snapped_or_declared():
    data=geo([("H","road",(1,6),(12,6),0),
              ("V","road",(6,1),(6,5.999),0)])
    result,report=run(data)
    assert report["observed_crossings"]==0
    assert result["network"]["edges"]==sorted(data["network"]["edges"],key=lambda e:e["id"])
    with pytest.raises(topology.TopologyInvalid,match="stale|schema"):
        run(data,crossing())


def test_two_coincident_distinct_endpoint_nodes_merge_only_if_classified(tmp_path):
    data=geo([("H","road",(1,6),(6,6),0),("V","road",(6,6),(6,12),0)])
    unresolved,diag=run(data)
    assert diag["status"]=="BLOCKED"
    assert len(unresolved["network"]["nodes"])==4
    result,ok=run(data,crossing())
    assert ok["created_nodes"]==0
    assert len(result["network"]["nodes"])==3
    assert audit_network(tmp_path,result)["status"]=="PASS"


def test_unknown_crossing_remains_blocked_and_never_infra_passes(tmp_path):
    data=simple()
    result,report=run(data)
    assert report["status"]=="BLOCKED"
    assert len(report["unresolved_crossings"])==1
    with pytest.raises(infra_checks.InfraInvalid,match="unresolved classified"):
        audit_network(tmp_path,result)


def test_unresolved_status_does_not_promote_an_edge(tmp_path):
    data=simple()
    x=crossing()
    x["status"]="UNRESOLVED"
    x.pop("relation")
    result,report=run(data,x)
    assert report["status"]=="BLOCKED"
    with pytest.raises(infra_checks.InfraInvalid,match="unresolved"):
        audit_network(tmp_path,result)


def test_reject_grade_invention_and_special_authority():
    data=simple()
    with pytest.raises(topology.TopologyInvalid,match="contradicts"):
        run(data,crossing(relation="grade_separated"))
    with pytest.raises(topology.TopologyInvalid,match="grade may not be invented"):
        run(data,crossing(levels=(0,1)))
    railway=simple(mode="rail")
    with pytest.raises(topology.TopologyInvalid,match="owner decision"):
        run(railway,crossing())
    assert run(railway,crossing(approved=True))[1]["status"]=="RECONCILED_NOT_ACCEPTED"


def test_missing_visual_editorial_or_geometry_evidence_is_rejected():
    data=simple()
    rec=crossing()
    rec["visual"]["reference_sha256"]="0"*64
    with pytest.raises(topology.TopologyInvalid,match="visual"):
        run(data,rec)
    rec=crossing(new_element=True)
    with pytest.raises(topology.TopologyInvalid,match="owner decision"):
        run(data,rec)
    rec=crossing()
    rec["geometry_observation"]=""
    with pytest.raises(topology.TopologyInvalid,match="geometric|schema"):
        run(data,rec)


def test_reject_stale_duplicate_and_protected_change():
    data=simple()
    cls=classifications(data,crossing())
    cls["network_sha256"]="bad"
    with pytest.raises(topology.TopologyInvalid,match="stale|schema"):
        topology.reconcile(data,cls)
    with pytest.raises(topology.TopologyInvalid,match="duplicate"):
        run(data,crossing(),crossing())
    with pytest.raises(topology.TopologyInvalid,match="protected"):
        run(data,crossing(),protected_edges=["H"])
    result,_=run(data,crossing())
    altered=copy.deepcopy(result)
    altered["network"]["edges"][0]["points"][0][0]=0
    with pytest.raises(topology.TopologyInvalid,match="drifted"):
        topology.reconcile(altered,classifications(data,crossing()))


def test_multi_modal_urban_fixture_and_existing_viaduct():
    data=json.loads((ROOT/"fixtures"/"topology-synthetic.json").read_text())
    data["source_sha256"]="a"*64
    observed,_,_=topology._observations(data["transport"],"urban")
    assert any(v["corridors"]==["RD-01","RL-01"] for v in observed.values())
    rec=crossing("RD-01","RL-01",relation="grade_separated",
                 point=(32,16),levels=(0,1))
    result,report=run(data,rec)
    assert report["status"]=="RECONCILED_NOT_ACCEPTED"
    assert report["resolved_crossings"]==1
    stats=urban.validate_transport(result["transport"],64,64)
    assert stats["rails"]==2
    assert stats["roads"]==5
    assert stats["trams"]==2


def test_region_connector_identity_survives_road_splitting():
    data=simple()
    data["network"]["edges"][0]["connector_id"]="KW-SULFOK-E01"
    result,_=run(data,crossing())
    h=[e for e in result["network"]["edges"] if e.get("source_edge_id")=="H"]
    assert len(h)==2
    assert all(e["connector_id"]=="KW-SULFOK-E01" for e in h)
    assert [e["from"] for e in h if e["points"][0]==[1,6]]==["H-A"]


def test_real_kingswell_diagnostic_remains_unapproved():
    source=json.loads((ROOT/"zones/cidade-velha/road-network-diagnostic.json").read_text())
    checkpoints=json.loads((ROOT/"zones/cidade-velha/checkpoint.json").read_text())
    ledger=json.loads((ROOT/"zones/cidade-velha/acceptance-ledger.json").read_text())
    assert len(source["candidates"])==98
    assert source["revisions"]["visual_grade_confirmation"] is False
    assert checkpoints["stage"]=="INF-01"
    assert checkpoints["official_attempt_count"]==0
    assert ledger["stages"]["INF-01"]["attempts"]==[]
    assert any(d.get("remaining_untyped_crossings")==217
               for d in ledger["diagnostics"])


def test_pipeline_only_writes_candidate_without_acceptance(tmp_path,capsys):
    data=simple()
    data["fixture_mode"]=True
    source=tmp_path/"source.json"
    source.write_text(json.dumps(data))
    labels=tmp_path/"classifications.json"
    labels.write_text(json.dumps(classifications(data,crossing())))
    out=tmp_path/"out"
    assert pipeline.main(["run","--district","kingswell","--topology-source",str(source),
                         "--topology-classifications",str(labels),
                         "--topology-out",str(out)])==0
    displayed=json.loads(capsys.readouterr().out)
    assert displayed["result"]["phase"]=="TOPOLOGY_RECONCILIATION"
    assert not displayed["result"]["publication_authorized"]
    assert (out/"topology-candidate.json").is_file()
    assert (out/"topology-diagnostic.json").is_file()
    assert not (out/"acceptance-ledger.json").exists()


def test_infra02_rejects_edits_to_accepted_prior_and_keeps_old_edges(tmp_path):
    previous=geo([("H","road",(1,6),(14,6),0)])
    previous["zone_mask"]={"path":"zone.png","sha256":"a"*64}
    parent=tmp_path/"INF-01.json"
    parent.write_text(json.dumps(previous),encoding="utf-8")
    proposed=geo([("H","road",(1,6),(14,6),0),
                  ("V","road",(6,1),(6,12),0)])
    proposed["zone_mask"]=copy.deepcopy(previous["zone_mask"])
    proposed["stage"]="INF-02"
    proposed["previous_stage_sha256"]=infra_checks.sha(parent)
    proposed["fixture_mode"]=True
    source=tmp_path/"INF-02.json"
    source.write_text(json.dumps(proposed),encoding="utf-8")
    classes=tmp_path/"classes.json"
    classes.write_text(json.dumps(classifications(proposed,crossing())))
    with pytest.raises(topology.TopologyInvalid,match="protected"):
        topology.reconcile_file(source,classes,tmp_path/"output",
                                prior_accepted=parent)
    assert json.loads(parent.read_text())==previous
    assert not (tmp_path/"output"/"topology-candidate.json").exists()


def test_infra02_adds_only_new_corridors_without_touching_prior(tmp_path):
    previous=geo([("H","road",(1,2),(14,2),0)])
    previous["zone_mask"]={"path":"zone.png","sha256":"a"*64}
    parent=tmp_path/"INF-01.json"
    parent.write_text(json.dumps(previous))
    proposed=geo([("H","road",(1,2),(14,2),0),
                  ("V","road",(6,5),(6,15),0),
                  ("W","road",(1,9),(14,9),0)])
    proposed["zone_mask"]=copy.deepcopy(previous["zone_mask"])
    proposed["stage"]="INF-02"
    proposed["previous_stage_sha256"]=infra_checks.sha(parent)
    proposed["fixture_mode"]=True
    source=tmp_path/"INF-02.json"
    source.write_text(json.dumps(proposed))
    classes=tmp_path/"classes.json"
    classes.write_text(json.dumps(classifications(proposed,
        crossing("V","W",point=(6,9)))))
    result=topology.reconcile_file(source,classes,tmp_path/"output",prior_accepted=parent)
    assert result["status"]=="RECONCILED_NOT_ACCEPTED"
    candidate=json.loads((tmp_path/"output"/"topology-candidate.json").read_text())
    old=next(e for e in candidate["network"]["edges"] if e["id"]=="H")
    assert old==previous["network"]["edges"][0]
    assert candidate["previous_stage_sha256"]==infra_checks.sha(parent)


def test_urban_neighbor_seam_remaps_to_correct_segment_and_idempotent():
    data=simple()
    network=data.pop("network")
    for node in network["nodes"]:
        node["kind"]="portal"
    for edge in network["edges"]:
        edge["class"]="collector"
        edge["owner"]="GLOBAL_NETWORK"
        edge["separates_blocks"]=True
        edge["profile"]="urban_at_grade"
        del edge["mode"]
    data.update(schema="NOVYDRES_MAPWORK_TERRITORY_NETWORK",
                grid={"width":32,"height":32},
                transport=network,
                neighbor_seams=[{"id":"SEAM-W","kind":"road","point":[1,6],
                                 "network_edge_id":"H","network_node_id":"H-A",
                                 "width_units":1,"profile":"urban_at_grade","level":0}])
    classes=classifications(data,crossing())
    result,report=topology.reconcile(data,classes)
    seam=result["neighbor_seams"][0]
    assert seam["network_edge_id"]=="H~001"
    urban._validate_seam_network(seam,result["transport"])
    again,_=topology.reconcile(result,classes)
    assert again==result
    tampered=copy.deepcopy(result)
    tampered["neighbor_seams"][0]["network_edge_id"]="H~002"
    with pytest.raises(topology.TopologyInvalid,match="connector"):
        topology.reconcile(tampered,classes)


def test_transitive_junction_must_not_connect_unreviewed_third_corridor():
    data=geo([("A","road",(1,6),(12,6),0),
              ("B","road",(6,1),(6,12),0),
              ("C","road",(1,1),(11,11),0)])
    with pytest.raises(topology.TopologyInvalid,match="transitive"):
        topology.reconcile(data,classifications(data,
            crossing("A","B"),crossing("A","C")))

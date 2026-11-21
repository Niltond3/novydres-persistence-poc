"""V3.3 positive and negative evidence tests: no fake model API handshake."""
import copy
import json
import sys
from pathlib import Path
import pytest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import visual as v
import contracts as c


def _checks(names):
    return {name:{"status":"PASS","note":"Inspected coherent built environment"}
            for name in names}


def _png(path):
    Image.new("RGBA",(4,4),(21,31,41,255)).save(path)
    return c.digest(path)


def _unit_review(uid,img,mask,peers=()):
    return {"schema":"NOVYDRES_MAPWORK_UNIT_VISUAL_REVIEW_1",
            "by":"AGENT","model":"GPT-6","status":"PASS",
            "work_unit_id":uid,"image_sha256":img,"mask_sha256":mask,
            "reference_sha256":"a"*64,"spatial_sha256":"b"*64,
            "checks":_checks(v.UNIT_CHECKS),"neighbors":list(peers),
            "summary":"Inspected image mask and urban connectivity"}


def test_unit_requires_current_neighbor_pixels_and_semantic_report(tmp_path):
    peer=tmp_path/"peer.png"; sha=_png(peer)
    uid="WU-0001";pid="WU-0002"
    units=[{"id":uid,"bbox":[0,0,4,4]},
           {"id":pid,"bbox":[4,0,8,4]}]
    context={pid:{"local_path":str(peer),"sha256":sha}}
    pair={"work_unit_id":pid,"side":"E","image_sha256":sha,
          "status":"PASS","note":"Rails and streets continue across seam"}
    review=_unit_review(uid,"d"*64,"c"*64,[pair])
    kw=dict(unit_id=uid,image_sha256="d"*64,mask_sha256="c"*64,
            reference_sha256="a"*64,spatial_sha256="b"*64,
            work_units=units,neighbor_receipts=context)
    assert v.validate_unit_visual_review(review,**kw)["peer_count"]==1
    for edit,reason in [
        (lambda r:r["neighbors"].clear(),"all face-neighbors"),
        (lambda r:r["neighbors"][0].update(side="N"),"wrong side"),
        (lambda r:r.update(image_sha256="e"*64),"stale visual review"),
        (lambda r:r["checks"]["micro_to_macro"].update(status="FAIL"),
         "unreviewed or failed")]:
        bad=copy.deepcopy(review);edit(bad)
        with pytest.raises(c.Blocked,match=reason):
            v.validate_unit_visual_review(bad,**kw)
    peer.write_bytes(b"changed")
    with pytest.raises(c.Blocked,match="neighbor.*stale"):
        v.validate_unit_visual_review(review,**kw)


def test_global_visual_report_binds_tiles_overviews_and_every_unit(tmp_path):
    inputs={}
    for key in ("tiles","before","after","reference"):
        f=tmp_path/(key+".png");_png(f);inputs[key]=f
    batch=tmp_path/"batch.json"
    batch.write_text(json.dumps({"images":[{"work_unit_id":"WU-0001"}]}))
    inputs["images"]=batch
    report={"schema":"NOVYDRES_MAPWORK_GLOBAL_VISUAL_REVIEW_1",
            "by":"AGENT","model":"GPT-6","status":"PASS",
            "tiles_sha256":c.digest(inputs["tiles"]),
            "before_sha256":c.digest(inputs["before"]),
            "after_sha256":c.digest(inputs["after"]),
            "reference_sha256":c.digest(inputs["reference"]),
            "image_receipts_sha256":c.digest(inputs["images"]),
            "checks":_checks(v.GLOBAL_CHECKS),
            "reviewed_units":["WU-0001"],
            "summary":"Inspected full assembled map and fine tile details"}
    kw=dict(tiles=inputs["tiles"],before_overview=inputs["before"],
            after_overview=inputs["after"],
            original_reference=inputs["reference"],image_receipts=inputs["images"])
    assert v.validate_global_visual_review(report,**kw)["unit_count"]==1
    bad=copy.deepcopy(report);bad["reviewed_units"]=[]
    with pytest.raises(c.Blocked,match="inventory"):
        v.validate_global_visual_review(bad,**kw)
    bad=copy.deepcopy(report);bad["checks"]["macro_to_micro"]["status"]="FAIL"
    with pytest.raises(c.Blocked,match="unreviewed or failed"):
        v.validate_global_visual_review(bad,**kw)
    inputs["after"].write_bytes(b"changed")
    with pytest.raises(c.Blocked,match="after_sha256.*stale"):
        v.validate_global_visual_review(report,**kw)


def test_native_preflight_not_a_future_api_handshake(tmp_path):
    caps={"schema":"NOVYDRES_MAPWORK_CAPABILITY_1"}
    for k in ("github_read","github_write","web_research","user_delivery",
              "native_image_generation","native_image_materialization"):
        caps[k]={"verified":True,"evidence":"I affirm the image tool is ready"}
    # Plain prose is deliberately NOT a real Web connector readback.
    assert set(c.capability_preflight(caps,require_native=False)["missing"])=={
        "github_read","github_write","web_research","user_delivery"}
    import hashlib
    source=tmp_path/"github-readback.bin"
    source.write_bytes(b"bytes independently retrieved from host connector")
    raw=source.read_bytes()
    git_sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    proof={"local_path":str(source),"sha256":c.digest(source),
           "blob_sha":git_sha,"commit_sha":"a"*40,
           "readback":True,"source_url":"https://example.org/source",
           "delivered_to_chat":True}
    for k in ("github_read","github_write","web_research","user_delivery"):
        caps[k]={"verified":True,"proof":dict(proof)}
    assert c.capability_preflight(caps,require_native=False)["missing"]==[]
    assert set(c.capability_preflight(caps)["missing"])=={
        "native_image_generation","native_image_materialization"}
    path=tmp_path/"image.png";sha=_png(path)
    caps["native_image_proof"]={"local_path":str(path),"sha256":sha}
    assert c.capability_preflight(caps)["missing"]==[]
    path.write_bytes(b"not a valid image")
    assert "native_image_generation" in c.capability_preflight(caps)["missing"]


def test_unit_ledger_rejects_old_pass_text():
    ledger={"schema":"NOVYDRES_MAPWORK_UNIT_LEDGER_1","units":{}}
    uid="WU-0001";inp="a"*64
    c.unit_transition(ledger,uid,event="START",input_sha256=inp)
    receipt={"technical_status":"PASS",
             "image_sha256":"b"*64,"mask_sha256":"c"*64}
    with pytest.raises(c.Blocked,match="hash-bound"):
        c.unit_transition(ledger,uid,event="AUDIT_PASS",input_sha256=inp,
                          receipt=receipt,
                          visual_review={"by":"AGENT","status":"PASS",
                                         "evidence":"Looks fine to me"})
    review=_unit_review(uid,"b"*64,"c"*64)
    assert c.unit_transition(ledger,uid,event="AUDIT_PASS",input_sha256=inp,
                             receipt=receipt,visual_review=review)["status"]=="VERIFIED"

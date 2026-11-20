"""Hash-bound visual-review receipts for Mapwork V3.3 single pipeline.

The ChatGPT host agent inspects real images using its native vision capabilities.
This module performs no model/API call and cannot certify that the reported
semantic judgment is true; it checks file integrity and review coverage.
"""
from pathlib import Path
from PIL import Image
import json
import v33_contracts as v33

SCHEMA="NOVYDRES_MAPWORK_V33"
UNIT_CHECKS=("mask_and_footprint","urban_structure","connections_and_access",
             "micro_to_macro","macro_to_micro")
GLOBAL_CHECKS=("regional_identity","transport_and_water_continuity",
               "seam_and_mask_integrity","micro_to_macro","macro_to_micro")


def neighbor_sides(work_units,unit_id):
    boxes={u["id"]:u["bbox"] for u in work_units}
    v33.require(unit_id in boxes,"visual review unit is not in spatial plan")
    a=boxes[unit_id]
    sides={}
    for peer,b in boxes.items():
        if peer==unit_id: continue
        if a[2]==b[0] and max(a[1],b[1])<min(a[3],b[3]): side="E"
        elif a[0]==b[2] and max(a[1],b[1])<min(a[3],b[3]): side="W"
        elif a[3]==b[1] and max(a[0],b[0])<min(a[2],b[2]): side="S"
        elif a[1]==b[3] and max(a[0],b[0])<min(a[2],b[2]): side="N"
        else: continue
        sides[peer]=side
    return sides


def _sha(value,label):
    v33.require(isinstance(value,str) and v33.SHA64.fullmatch(value),
                label+" must be an exact SHA-256")


def _notes(checks,required,scope):
    v33.require(isinstance(checks,dict) and set(checks)==set(required),
                scope+": missing or extra visual checks")
    for name in required:
        c=checks[name]
        v33.require(isinstance(c,dict) and c.get("status")=="PASS" and
                    isinstance(c.get("note"),str) and len(c["note"].strip())>=12,
                    scope+": unreviewed or failed visual aspect "+name)


def _base(review,schema):
    v33.require(isinstance(review,dict) and review.get("schema")==SCHEMA+schema and
                review.get("by")=="AGENT" and review.get("status")=="PASS" and
                isinstance(review.get("model"),str) and len(review["model"].strip())>=3 and
                isinstance(review.get("summary"),str) and len(review["summary"].strip())>=12,
                "agent visual review missing, malformed or not PASS")


def _file_hash(path,expected_sha,label):
    _sha(expected_sha,label)
    p=Path(path)
    v33.require(p.is_file() and v33.digest(p)==expected_sha,
                label+": file absent or stale")
    return p


def validate_unit_visual_review(review,*,unit_id,image_sha256,mask_sha256,
                                reference_sha256,spatial_sha256,work_units,
                                neighbor_receipts):
    """Bind semantic judgment to current unit+mask+U02+plan and every touching peer."""
    _base(review,"_UNIT_VISUAL_REVIEW_1")
    v33.require(review.get("work_unit_id")==unit_id,
                "visual review references a different work unit")
    for key,val in (("image_sha256",image_sha256),("mask_sha256",mask_sha256),
                    ("reference_sha256",reference_sha256),
                    ("spatial_sha256",spatial_sha256)):
        _sha(val,key)
        v33.require(review.get(key)==val,"stale visual review "+key)
    _notes(review.get("checks"),UNIT_CHECKS,"unit "+unit_id)
    sides=neighbor_sides(work_units,unit_id)
    supplied=review.get("neighbors")
    v33.require(isinstance(supplied,list) and len(supplied)==len(sides),
                "unit visual review must cover all face-neighbors")
    seen=set()
    for pair in supplied:
        v33.require(isinstance(pair,dict),"invalid visual neighbor receipt")
        peer=pair.get("work_unit_id")
        v33.require(peer in sides and peer not in seen and
                    pair.get("side")==sides[peer],
                    "visual neighbor is missing, duplicate, or wrong side")
        seen.add(peer)
        source=neighbor_receipts.get(peer)
        v33.require(isinstance(source,dict),
                    "neighbor image is not materialized: "+str(peer))
        _file_hash(source.get("local_path",""),source.get("sha256"),
                   "neighbor "+peer+" image")
        with Image.open(source["local_path"]) as im:
            v33.require(im.format in ("PNG","WEBP"),
                        "neighbor visual image has unsupported encoding")
            im.verify()
        v33.require(pair.get("image_sha256")==source["sha256"] and
                    pair.get("status")=="PASS" and
                    isinstance(pair.get("note"),str) and
                    len(pair["note"].strip())>=12,
                    "visual adjacency failed or bound to stale neighbor: "+peer)
    return {"status":"REVIEW_RECEIPT_VERIFIED","unit":unit_id,
            "peer_count":len(sides),"review_sha256":v33.evidence_digest(review)}


def validate_global_visual_review(review,*,tiles,before_overview,after_overview,
                                  original_reference,image_receipts):
    """The agent checks full assembled image; code checks report vs actual files."""
    _base(review,"_GLOBAL_VISUAL_REVIEW_1")
    paths={"tiles_sha256":tiles,"before_sha256":before_overview,
           "after_sha256":after_overview,"reference_sha256":original_reference,
           "image_receipts_sha256":image_receipts}
    for field,path in paths.items():
        _file_hash(path,review.get(field),field)
    _notes(review.get("checks"),GLOBAL_CHECKS,"global composition")
    v33.require(isinstance(review.get("reviewed_units"),list) and
                review["reviewed_units"] and
                len(review["reviewed_units"])==len(set(review["reviewed_units"])),
                "global visual review must inventory its reviewed units")
    batch=json.loads(Path(image_receipts).read_text(encoding="utf-8"))
    units={r["work_unit_id"] for r in batch["images"]}
    v33.require(set(review["reviewed_units"])==units,
                "global visual review does not cover all generated units")
    return {"status":"REVIEW_RECEIPT_VERIFIED","unit_count":len(units),
            "review_sha256":v33.evidence_digest(review)}

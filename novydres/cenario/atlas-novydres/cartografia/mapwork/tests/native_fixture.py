"""Synthetic local files for fail-closed image host protocol tests (not provider calls)."""
import hashlib
import json
from pathlib import Path

from PIL import Image

import native_generation as native


def fixture(tmp_path, operation_id="synthetic-operation", prefix="native"):
    images = {}
    ids = {"reference-image":"input-ref-id", "edit-mask":"input-mask-id", "image":"candidate-id"}
    for role, color in (("reference-image",(25,45,60)), ("edit-mask",(255,255,255)), ("image",(25,110,60))):
        local=tmp_path/f"{prefix}-{role}.png"
        remote=tmp_path/f"{prefix}-{role}-GET.png"
        Image.new("RGB",(16,16),color).save(local)
        remote.write_bytes(local.read_bytes())
        images[role]={"provider":"drive","remote_id":ids[role],"path":str(local),
                      "readback_path":str(remote),"sha256":native.digest(local.read_bytes())}
    composed=tmp_path/f"{prefix}-composed-image.png"
    proof=native.compose_masked(images["reference-image"]["path"],
        images["edit-mask"]["path"],images["image"]["path"],composed)
    composed_get=tmp_path/f"{prefix}-composed-image-GET.png"
    composed_get.write_bytes(composed.read_bytes())
    images["composed-image"]={"provider":"drive","remote_id":"composed-candidate-id",
        "path":str(composed),"readback_path":str(composed_get),
        "sha256":proof["composed_sha256"]}
    req=native.edit_request(reference_sha256=images["reference-image"]["sha256"],
        mask_sha256=images["edit-mask"]["sha256"],scope="SYNTHETIC",
        job_id="synthetic-rail-overpass",goal="Convert crossing into a road overpass, keeping rail and road continuous")
    result={"schema":native.HANDOFF_SCHEMA,"request":req,
            "request_sha256":native.json_digest(req),"operation_id":operation_id,
            "inputs":{role:images[role] for role in ("reference-image","edit-mask")},
            "dispatch":{"provider":"CHATGPT_NATIVE_IMAGE","mode":"EDIT_WITH_REFERENCE",
                "generation_id":"test-tool-result-001","request_sha256":native.json_digest(req),
                "prompt_sha256":req["prompt_sha256"],"result_sha256":images["image"]["sha256"],
                "attached_inputs":{role:{"remote_id":images[role]["remote_id"],
                                         "sha256":images[role]["sha256"]}
                                   for role in ("reference-image","edit-mask")}},
            "output":images["image"]}
    hand=tmp_path/f"{prefix}-handoff.json"
    hand.write_text(json.dumps(result, ensure_ascii=False))
    hand_get=tmp_path/f"{prefix}-handoff-GET.json"
    hand_get.write_bytes(hand.read_bytes())
    review={"status":"FAIL","by":"AGENT","image_sha256":images["composed-image"]["sha256"],
            "reference_sha256":req["reference_sha256"],"mask_sha256":req["mask_sha256"],
            "observations":[{"criterion":k,"status":"FAIL" if k=="grade" else "PASS",
                             "evidence":"Synthetic fixture observation for validation"}
                            for k in ("grade","continuity","coherence","format")]}
    visual=tmp_path/f"{prefix}-visual.json";visual.write_text(json.dumps(review))
    visual_get=tmp_path/f"{prefix}-visual-GET.json";visual_get.write_bytes(visual.read_bytes())
    extras={"native-edit-handoff":{"provider":"drive","remote_id":"handoff-id",
             "path":str(hand),"readback_path":str(hand_get),"sha256":native.digest(hand.read_bytes())},
            "visual-review":{"provider":"drive","remote_id":"review-id",
             "path":str(visual),"readback_path":str(visual_get),"sha256":native.digest(visual.read_bytes())}}
    artifacts=[dict(images[role],kind=role) for role in ("reference-image","edit-mask","image","composed-image")]
    artifacts.extend(dict(value,kind=role) for role,value in extras.items())
    return req,result,images,artifacts,review

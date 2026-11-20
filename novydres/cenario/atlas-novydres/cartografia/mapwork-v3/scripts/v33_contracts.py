#!/usr/bin/env python3
"""V3.3 deterministic contracts invoked ONLY from scripts/pipeline.py.

The agent performs semantic understanding, research and native image generation.
This module validates their evidence; it never invents canon, source URLs, owner
consent, image files, physical scale or a successful provider interaction.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image, ImageChops

SCHEMA = "NOVYDRES_MAPWORK_V33"
MODES = {"CREATE_REGION", "REFINE_AREA", "EDIT_ELEMENT", "ADD_ELEMENT"}
STATES = {"PROPOSED", "APPROVED", "REJECTED", "APPROVED_WITH_CONDITIONS"}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
PROPOSAL_ID = re.compile(r"^[A-Z][A-Z0-9-]*-PROP-[0-9]{3,6}$")


class Blocked(ValueError):
    """A genuine missing capability, authority, approval or integrity gate."""


def require(test, message):
    if not test:
        raise Blocked(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def evidence_digest(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def rect(value):
    return (isinstance(value, list) and len(value) == 4 and
            all(type(n) in (float, int) and n == n and abs(n) < 1e8 for n in value) and
            value[0] < value[2] and value[1] < value[3])


def contained(inner, outer):
    return all((inner[0] >= outer[0], inner[1] >= outer[1],
                inner[2] <= outer[2], inner[3] <= outer[3]))


def validate_intent(request, known_targets, world_bounds):
    """No fuzzy matching, unknown landmarks, fabricated geometry or implicit ADD."""
    require(isinstance(request, dict) and request.get("schema") == SCHEMA + "_INTENT_1",
            "invalid V3.3 intent contract")
    require(request.get("mode") in MODES, "invalid intervention mode")
    require(isinstance(request.get("original_request"), str) and
            request["original_request"].strip(), "original user request required")
    require(SHA40.fullmatch(request.get("source_commit", "")) is not None,
            "intent must pin an exact 40-character source commit")
    target = request.get("target")
    require(isinstance(target, dict) and isinstance(target.get("id"), str),
            "unresolved target; ask for exact identity")
    target_id = target["id"]
    require(target_id in known_targets and
            target.get("subject_id") == known_targets[target_id]["subject_id"],
            "target not uniquely resolved in canonical scope index")
    mode = request["mode"]
    boundary = known_targets[target_id].get("bounds")
    if mode == "CREATE_REGION":
        require(target.get("kind") == "region", "CREATE_REGION requires region identity")
        require(request.get("intervention") is None, "CREATE_REGION cannot imply an arbitrary edit mask")
    else:
        editable = request.get("intervention")
        require(isinstance(editable, dict) and rect(editable.get("bounds")),
                "refinement requires an explicit spatial edit mask")
        require(rect(boundary) and contained(editable["bounds"], boundary) and
                contained(editable["bounds"], world_bounds),
                "edit mask outside known canonical target")
        require(editable.get("source") in ("OWNER_APPROVED", "CANON_EXISTING"),
                "edit mask has no canon/owner authority")
        require(isinstance(editable.get("authority_ref"), str) and
                len(editable["authority_ref"]) >= 8, "edit mask authority missing")
    if mode in ("EDIT_ELEMENT", "ADD_ELEMENT"):
        require(isinstance(request.get("element_id"), str) and
                bool(request["element_id"]), "unresolved element identity")
    return {"target": target_id, "mode": mode, "edit_bounds":
            request.get("intervention", {}).get("bounds") if mode != "CREATE_REGION" else None}


def validate_research(records, *, required=True):
    """External analogues are mandatory even if existing canon contains a summary."""
    require(isinstance(records, list), "research must be a list of source records")
    externals = set()
    for row in records:
        require(isinstance(row, dict), "malformed research record")
        require(row.get("category") in ("TECHNICAL", "OPEN_ALTERNATIVE", "NEW_ELEMENT"),
                "research category must separate engineering from editorial novelty")
        for key in ("url", "accessed_on", "observation", "relevance", "adaptation",
                    "place", "source_type"):
            require(isinstance(row.get(key), str) and row[key].strip(),
                    "research record missing " + key)
        parsed = urlparse(row["url"])
        require(parsed.scheme in ("https", "http") and parsed.netloc,
                "research source needs a real HTTP(S) URL")
        try:
            date = datetime.date.fromisoformat(row["accessed_on"])
        except ValueError as exc:
            raise Blocked("research consultation date must be ISO YYYY-MM-DD") from exc
        require(date <= datetime.date.today(), "research cannot cite future consultation")
        require(row["source_type"] in ("REAL_WORLD", "CANON"),
                "research source_type must be REAL_WORLD or CANON")
        if row["source_type"] == "REAL_WORLD":
            externals.add(parsed.netloc.casefold())
        if row["category"] == "NEW_ELEMENT":
            require(bool(row.get("proposal_id")), "new elements need a proposed editorial ID")
    if required:
        require(len(externals) >= 2,
                "independent real-world research missing: at least two domains")
    return {"sources": len(records), "real_world_domains": len(externals)}


def validate_proposals(register, *, region, commit, referenced=None):
    require(isinstance(register, dict) and register.get("schema") ==
            SCHEMA + "_DECISIONS_1", "versioned proposal register required")
    require(register.get("region") == region and register.get("source_commit") == commit,
            "proposal register authority/region mismatch")
    items = register.get("proposals")
    require(isinstance(items, list), "proposal inventory missing")
    by_id = {}
    for item in items:
        require(isinstance(item, dict) and PROPOSAL_ID.fullmatch(item.get("id", "")),
                "proposal ID malformed")
        pid = item["id"]
        require(pid not in by_id, "duplicate proposal ID: " + pid)
        for field in ("description", "location", "origin", "rationale", "neighbor_impact"):
            require(isinstance(item.get(field), str) and item[field].strip(),
                    pid + ": missing " + field)
        status = item.get("status")
        require(status in STATES, pid + ": invalid editorial state")
        if status in ("APPROVED", "APPROVED_WITH_CONDITIONS"):
            decision = item.get("decision")
            require(isinstance(decision, dict) and decision.get("by") == "OWNER" and
                    isinstance(decision.get("evidence"), str) and
                    len(decision["evidence"]) >= 8 and
                    decision.get("source_commit") == commit and
                    decision.get("decision") == status,
                    pid + ": explicit owner approval receipt missing")
            if status == "APPROVED_WITH_CONDITIONS":
                require(isinstance(decision.get("conditions"), str) and
                        bool(decision["conditions"].strip()),
                        pid + ": conditional consent needs testable conditions")
        by_id[pid] = item
    for pid in referenced or []:
        require(pid in by_id and by_id[pid]["status"] in
                ("APPROVED", "APPROVED_WITH_CONDITIONS"),
                "new element unauthorized: " + str(pid))
    pending = [pid for pid, item in by_id.items() if item["status"] == "PROPOSED"]
    return {"inventory": len(by_id), "pending": pending,
            "approved": [pid for pid, item in by_id.items() if
                         item["status"] in ("APPROVED", "APPROVED_WITH_CONDITIONS")]}


def validate_inventory(elements, register, *, canonical_element_ids=()):
    """Every noncanonical installation must resolve to a precisely approved item."""
    known = set(canonical_element_ids)
    ids = set()
    referenced = []
    approved = {p["id"]: p for p in register["proposals"]
                if p["status"] in ("APPROVED", "APPROVED_WITH_CONDITIONS")}
    for item in elements:
        eid = item.get("id")
        require(isinstance(eid, str) and eid and eid not in ids,
                "duplicate or missing installed element identity")
        ids.add(eid)
        if eid in known:
            continue
        pid = item.get("proposal_id")
        require(pid in approved, "element lacks explicit owner proposal: " + eid)
        require(eid in approved[pid].get("authorized_ids", []),
                "proposal does not enumerate installed element: " + eid)
        referenced.append(pid)
    require(not any(p["status"] == "PROPOSED" for p in register["proposals"]),
            "pending substantive proposals must be decided before generation")
    return {"elements": len(ids), "proposals_used": sorted(set(referenced))}


def capability_preflight(receipts, *, reference=None):
    """Only on-disk SHA readback is technical proof; host features need real receipts."""
    require(isinstance(receipts, dict) and receipts.get("schema") ==
            SCHEMA + "_CAPABILITY_1", "real capability receipt required")
    verified = {}
    for item in ("github_read", "github_write", "web_research",
                 "native_image_generation", "native_image_materialization",
                 "user_delivery"):
        data = receipts.get(item)
        verified[item] = (isinstance(data, dict) and
                          data.get("verified") is True and
                          isinstance(data.get("evidence"), str) and
                          len(data["evidence"]) >= 12)
    if reference:
        path = Path(reference["path"])
        verified["reference"] = (path.is_file() and
                                 digest(path) == reference["sha256"])
    return {"verified": verified, "missing": sorted(
        key for key, passed in verified.items() if not passed)}


def image_receipt(receipt, *, expected_size, work_unit_id):
    """Reject host-provided IDs without actual on-disk readback."""
    require(isinstance(receipt, dict) and receipt.get("schema") ==
            SCHEMA + "_IMAGE_RECEIPT_1", "native image receipt required")
    require(receipt.get("work_unit_id") == work_unit_id,
            "image receipt bound to a different work unit")
    path = Path(receipt.get("local_path", ""))
    require(path.is_file(), "native image was not materialized to local compositor")
    require(SHA64.fullmatch(receipt.get("sha256", "")) and
            digest(path) == receipt["sha256"], "generated image SHA readback failed")
    with Image.open(path) as im:
        require(im.format in ("PNG", "WEBP") and
                im.size == tuple(expected_size),
                "generated image format or expected scale mismatch")
        im.verify()
    require(isinstance(receipt.get("generator_evidence"), str) and
            len(receipt["generator_evidence"]) >= 12,
            "native generator provenance is not evidenced")
    return {"path": str(path), "sha256": receipt["sha256"],
            "work_unit_id": work_unit_id}


def validate_edit_mask(edit_mask, bounds, protected):
    """An owner-defined 2D intervention cannot implicitly extend across the atlas."""
    from PIL import ImageDraw
    require(edit_mask.mode == "L" and edit_mask.size == protected.size,
            "edit/protection masks must align to immutable U02 resolution")
    require(rect(bounds), "authorized edit bounds required")
    x0,y0,x1,y1 = bounds
    allowed=Image.new("L",edit_mask.size,0)
    draw=ImageDraw.Draw(allowed)
    from math import ceil, floor
    draw.rectangle((ceil(x0),ceil(y0),floor(x1)-1,floor(y1)-1),fill=255)
    require(edit_mask.getbbox() is not None,
            "empty edit mask cannot authorize arbitrary image changes")
    require(ImageChops.subtract(edit_mask,allowed).getbbox() is None,
            "edit mask leaks outside authorized intervention")
    require(ImageChops.darker(edit_mask,protected).getbbox() is None,
            "edit mask overlaps protected canonical infrastructure")
    return {"editable_pixels":sum(1 for p in edit_mask.tobytes() if p)}


def verify_edit_pixels(before, after, editable, protected):
    """Pixel-exact exclusion outside approved edit area, including preapproved art."""
    require(before.size == after.size == editable.size == protected.size,
            "edit masks and raster dimensions differ")
    require(all(im.mode in ("L", "1") for im in (editable, protected)),
            "edit masks must be grayscale or binary")
    permitted = ImageChops.subtract(editable.convert("L"), protected.convert("L"))
    changed = ImageChops.difference(before.convert("RGBA"),
                                    after.convert("RGBA"))
    bands = changed.split()
    delta = bands[0]
    for band in bands[1:]:
        delta = ImageChops.lighter(delta, band)
    forbidden = ImageChops.subtract(delta, permitted)
    require(forbidden.getbbox() is None,
            "protected or unapproved edit-area pixels changed")
    return {"changed_bbox": delta.getbbox(), "protected_unchanged": True}


def make_generation_recipe(*, unit, intent, design_path, reference_path,
                           proposal_register, neighbor_digests, style):
    path = Path(design_path)
    require(path.is_file() and Path(reference_path).is_file(),
            "recipe requires materialized design and original reference")
    approved = validate_proposals(
        proposal_register, region=intent["target"]["id"],
        commit=intent["source_commit"])
    require(not approved["pending"], "pending decisions block generation recipes")
    require(isinstance(style, dict) and style.get("projection") == "TOP_DOWN_90",
            "image recipe must fix top-down perspective")
    return {
        "schema": SCHEMA + "_RECIPE_1",
        "work_unit_id": unit["id"],
        "bbox": unit["bbox"],
        "reference_sha256": digest(reference_path),
        "urban_design_sha256": digest(path),
        "decisions_sha256": evidence_digest(proposal_register),
        "neighbor_sha256": dict(neighbor_digests),
        "mask_edit_bounds": intent.get("intervention", {}).get("bounds"),
        "style": style,
        "generator": "CHATGPT_NATIVE_IMAGE_EXTERNAL_AGENT",
        "image_generated": False
    }


def resume_units(checkpoint, *, expected_inputs):
    """No source drift accepted; only hash-bound verified outputs can be skipped."""
    require(checkpoint.get("schema") == SCHEMA + "_UNITS_1",
            "invalid resume checkpoint")
    require(checkpoint.get("input_sha256") == evidence_digest(expected_inputs),
            "resume input drift: invalidate dependent units")
    completed = []
    for item in checkpoint.get("units", []):
        if item.get("status") != "VERIFIED":
            continue
        path = Path(item.get("local_path", ""))
        require(path.is_file() and digest(path) == item.get("sha256"),
                "checkpoint references missing or altered unit")
        completed.append(item["id"])
    return completed

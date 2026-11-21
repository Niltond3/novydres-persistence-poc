#!/usr/bin/env python3
"""Single fail-closed Mapwork pipeline. External research, approval and image tools are explicit handoffs.

Usage: python scripts/pipeline.py run --district sulfok
       python scripts/pipeline.py run --district kingswell --spatial ... --reference ...
       python scripts/pipeline.py run --zone ... --spatial ... --reference ... --assets ... --execute --out ...
No command in this module publishes a release or modifies canon.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

import mapwork as core
import urban_architecture as urban
import urban_content as content
import contracts as contract
import acceptance
import visual
import flow
import orchestration as controller
import topology
import infra_checks as infra

ROOT=Path(__file__).resolve().parents[1]
SCHEMA="NOVYDRES_MAPWORK_PIPELINE_CHECKPOINT"


def fingerprint(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def resolve_zone(district=None, supplied=None):
    if supplied is not None:
        file=Path(supplied)
        if not file.is_file():
            raise core.Invalid("zone manifest missing: "+str(file))
        return file
    if not district:
        raise core.Invalid("district or zone file required")
    matches=[]
    for file in sorted((ROOT/"zones").glob("*/zone.json")):
        z=core.load(file)
        if district.casefold() in (z["id"].casefold(),file.parent.name.casefold()):
            matches.append(file)
    if len(matches)>1:
        raise core.Invalid("ambiguous zone identity: "+district)
    return matches[0] if matches else None


def checkpoint(*,district,zone_path=None,zone=None,phase,action,blockers=(),spatial_path=None,
               architectural_report=None,artifacts=None):
    result={
        "schema":SCHEMA,
        "district":district,
        "phase":phase,
        "next_action":action,
        "blockers":list(blockers),
        "source_commit":zone.get("source_commit") if zone else None,
        "inputs":{
            "zone_path":str(zone_path) if zone_path else None,
            "zone_sha256":fingerprint(zone_path) if zone_path else None,
            "spatial_path":str(spatial_path) if spatial_path else None,
            "spatial_sha256":fingerprint(spatial_path) if spatial_path else None
        },
        "architectural_report":architectural_report,
        "candidate_artifacts":artifacts,
        "publication_authorized":False,
        "canonical_state_changed":False
    }
    return result


def load_verified_neighbors(plan):
    """Read existing peer spatial manifests from Git; reservations are future-only."""
    peers={}
    for seam in plan["neighbor_seams"]:
        neighbor=seam["to_zone"]
        matches=[]
        for path in (ROOT/"zones").glob("*/zone.json"):
            item=core.load(path)
            if item["id"]==neighbor:
                matches.append((path,item))
        if len(matches)>1:
            raise core.Invalid("duplicate neighbor ownership: "+neighbor)
        if not matches:
            continue
        zone_path,zone=matches[0]
        spatial=zone_path.parent/"global-spatial.json"
        if not spatial.is_file():
            # An existing visual reference is not a bilateral seam contract.
            raise core.Invalid("existing neighbor has no spatial manifest: "+neighbor)
        other=core.load(spatial)
        if other.get("zone",{}).get("id")!=neighbor or other.get("fixture_mode") is not False:
            raise core.Invalid("invalid neighbor identity or fixture: "+neighbor)
        if other.get("source_sha256")!=plan["source_sha256"]:
            raise core.Invalid("neighbor U02 authority mismatch: "+neighbor)
        digest=lambda network: hashlib.sha256(json.dumps(network,sort_keys=True,
                    separators=(",",":")).encode("utf-8")).hexdigest()
        if digest(other["transport"])!=digest(plan["transport"]):
            raise core.Invalid("neighbor global transport differs: "+neighbor)
        peers[neighbor]={"seams":other["neighbor_seams"],
                         "zone_polygon":other["zone"]["polygon"],
                         "transport":other["transport"]}
    return peers


def check_canonical_pois(zone_path, plan):
    # Exact approved identities come from the authoritative installation
    # Canonical POI identity is established by the verified installation inventory.
    inventory_path=zone_path.parent/"inventory.json"
    if not inventory_path.is_file():
        raise core.Invalid("authoritative approved POI inventory missing")
    inventory=core.load(inventory_path)
    if inventory.get("region")!=plan["zone"]["id"]:
        raise core.Invalid("approved POI inventory zone mismatch")
    ids=[p["id"] for p in inventory["elements"]]
    found=[p["id"] for p in plan["special_sites"]]
    if len(ids)!=len(set(ids)) or len(found)!=len(set(found)) or set(ids)!=set(found):
        raise core.Invalid("approved POI inventory differs (omitted, duplicate or unauthorized): "+
                           ", ".join(sorted(set(ids).symmetric_difference(set(found)))))


def affected_unit_ids(report,editable_u02=None):
    """Only raster work units crossing owner-authorized pixels require new art."""
    units={u["id"]:u for u in report["work_units"]}
    if editable_u02 is None:
        return set(units)
    affected=set()
    for uid,unit in units.items():
        bbox=unit["bbox"]
        if editable_u02.crop(tuple(bbox)).getbbox() is not None:
            affected.add(uid)
    core.fail(bool(affected),"refinement has no planned work-unit coverage")
    return affected


def validate_work_unit_bindings(zone,report,plan=None,required_units=None):
    """Every rendered asset belongs to one work unit and no global network layer."""
    expected={u["id"]:u for u in report["work_units"]}
    bound={}
    local={"lot","special_building","poi","finish"}
    designs={}
    context=None
    for e in zone["elements"]:
        uid=e.get("work_unit_id")
        if uid not in expected:
            raise core.Invalid(e["id"]+": absent or invalid work_unit_id")
        if e["kind"] not in local:
            raise core.Invalid(e["id"]+": global infrastructure is not a local art asset")
        if e["kind"]=="lot":
            if uid in bound:
                raise core.Invalid(uid+": duplicate atomic lot asset")
            if e["core"]!=expected[uid]["bbox"]:
                raise core.Invalid(uid+": asset core differs from planned work unit")
            bound[uid]=e
            continue
        if not core.rect(e["core"]) or not core.inside(e["core"],expected[uid]["bbox"]):
            raise core.Invalid(e["id"]+": artistic core extends beyond its work unit")
        building_id=e.get("building_id")
        if e["kind"] in ("special_building","poi") or building_id:
            if plan is None:
                raise core.Invalid(e["id"]+": special asset requires validated building plan")
            if uid not in designs:
                if context is None:
                    context=content.design_context(plan)
                designs[uid]={b["id"]:b for b in
                              content.design_unit(plan,report,uid,context=context)["buildings"]}
            building=designs[uid].get(building_id)
            if building is None or e["core"]!=building["footprint"]:
                raise core.Invalid(e["id"]+": special asset does not match approved building footprint")
            if e["kind"]=="poi" and (not building["site_id"] or
                e.get("site_id")!=building["site_id"]):
                raise core.Invalid(e["id"]+": POI asset lacks approved site identity")
    required=set(expected) if required_units is None else set(required_units)
    core.fail(required.issubset(expected),"unknown required native work unit")
    missing=required-set(bound)
    if missing:
        raise core.Invalid("planned work units lack bound art elements: "+", ".join(sorted(missing)[:6]))
    return bound


def _pixel_rect(rect,scale):
    from math import ceil
    return tuple(round(v*scale) for v in rect)


def verify_art_overlaps(plan,elements,assets,cfg):
    """Two visible alpha masks cannot overlap unless approved by owner per pair."""
    from PIL import ImageChops
    from collections import defaultdict
    by_unit=defaultdict(list)
    for e in elements:
        if e["status"]=="VERIFIED" and e.get("asset"):
            by_unit[e["work_unit_id"]].append(e)
    approvals=plan.get("owner_art_approval",{})
    approved=set()
    if plan.get("owner_art_authorized") is True and approvals.get("decision")=="APPROVED":
        for item in approvals.get("authorized_overlaps",[]):
            pair=item.get("elements",[])
            if (len(pair)==2 and pair[0]!=pair[1] and
                isinstance(item.get("evidence"),str) and len(item["evidence"])>=16):
                approved.add(frozenset(pair))
    scale=cfg["detail_pixels_per_unit"]
    for uid,members in by_unit.items():
        for i,a in enumerate(members):
            for b in members[i+1:]:
                rect_a=_pixel_rect(a["envelope"],scale)
                rect_b=_pixel_rect(b["envelope"],scale)
                intersection=(max(rect_a[0],rect_b[0]),max(rect_a[1],rect_b[1]),
                              min(rect_a[2],rect_b[2]),min(rect_a[3],rect_b[3]))
                if intersection[2]<=intersection[0] or intersection[3]<=intersection[1]:
                    continue
                def visible(e,rect):
                    bounds=_pixel_rect(e["envelope"],scale)
                    crop=(intersection[0]-bounds[0],intersection[1]-bounds[1],
                          intersection[2]-bounds[0],intersection[3]-bounds[1])
                    with Image.open(Path(assets)/e["asset"]["path"]) as art:
                        alpha=art.convert("RGBA").getchannel("A").crop(crop)
                    with Image.open(Path(assets)/e["mask"]["path"]) as mask:
                        coverage=mask.convert("L").crop(crop)
                    return ImageChops.darker(alpha,coverage)
                if ImageChops.darker(visible(a,rect_a),visible(b,rect_b)).getbbox() is not None:
                    if frozenset((a["id"],b["id"])) not in approved:
                        raise core.Invalid(uid+": unauthorized visible overlap between "+
                                           a["id"]+" and "+b["id"])


def verify_unit_art_masks(plan,report,elements,assets,cfg):
    """All local art masks, not only lots, obey exact unit + special footprints."""
    from PIL import ImageChops, ImageDraw
    from math import ceil, floor
    context=content.design_context(plan)
    w,h=context["w"],context["h"]
    scale=cfg["detail_pixels_per_unit"]
    if isinstance(elements,dict):
        entries=[(uid,e) for uid,e in elements.items()]
    else:
        entries=[(e.get("work_unit_id"),e) for e in elements]
    units={u["id"]:u for u in report["work_units"]}
    for uid,e in entries:
        if e["status"]!="VERIFIED":
            continue
        if uid not in units:
            raise core.Invalid(e["id"]+": art mask has no authorized work unit")
        if e["kind"] in ("road","rail","tram","water","terrain","ermo","bridge"):
            raise core.Invalid(e["id"]+": global network asset cannot be painted locally")
        x0,y0,x1,y1=e["envelope"]
        left,top=round(x0*scale),round(y0*scale)
        mask_file=Path(assets)/e["mask"]["path"]
        with Image.open(mask_file) as img:
            m=img.convert("L")
        allowed=Image.new("L",m.size,0)
        draw=ImageDraw.Draw(allowed)
        unit=units[uid]
        bx0,by0,bx1,by1=unit["bbox"]
        for y in range(by0,by1):
            for x in range(bx0,bx1):
                i=y*w+x
                if context["editable"][i] and context["labels"][i]==unit["block_label"]:
                    sx,sy=x*scale-left,y*scale-top
                    draw.rectangle([sx,sy,sx+scale-1,sy+scale-1],fill=255)
        if e["kind"] in ("special_building","poi") or e.get("building_id"):
            core_rect=e["core"]
            limited=Image.new("L",m.size,0)
            dr=ImageDraw.Draw(limited)
            dr.rectangle([ceil(core_rect[0]*scale-left),ceil(core_rect[1]*scale-top),
                          floor(core_rect[2]*scale-left)-1,floor(core_rect[3]*scale-top)-1],
                         fill=255)
            allowed=ImageChops.darker(allowed,limited)
        if ImageChops.subtract(m,allowed).getbbox() is not None:
            raise core.Invalid(e["id"]+": art mask paints outside its assigned editable cells or footprint")
    if not isinstance(elements,dict):
        verify_art_overlaps(plan,[e for _,e in entries],assets,cfg)


def validate_all_unit_designs(plan,report,design_root,cfg,*,allow_abstract=False):
    """One design check for the pipeline and the compositor's revalidation."""
    units=report["work_units"]
    ctx=content.design_context(plan)
    physical=urban.validated_physical_reference(plan,cfg)
    building_count=0
    physical_all=(physical is not None and
                  plan.get("work_policy",{}).get("parceling")!="URBAN_BLOCKS")
    for unit in units:
        uid=unit["id"]
        path=Path(design_root)/(uid+".json")
        if not path.is_file():
            raise core.Invalid(uid+": missing detailed building plan")
        item=core.load(path)
        expected=content.design_unit(plan,report,uid,context=ctx)
        structural=dict(item)
        structural.pop("physical_routes",None)
        if structural!=expected:
            raise core.Invalid(uid+": detailed building plan differs from validated urban geometry")
        if not expected["access_verified"]:
            raise core.Invalid(uid+": at least one building lacks abstract ground street access")
        if physical_all:
            try:
                physical_all=content.validate_unit_physical_access(plan,expected,item,ctx,physical)
            except urban.ContractError as exc:
                raise core.Invalid(uid+": physical route invalid: "+str(exc)) from exc
        building_count+=expected["building_count"]
    report["urban_design"]={"work_units_verified":len(units),
        "buildings_placed":building_count,"individual_footprints_verified":True,
        "all_abstract_access_paths_verified":True,
        "physical_routes_verified":physical_all}
    report["gates"]["physical_access_certified"]=physical_all
    required={key:value for key,value in report["gates"].items()
              if not allow_abstract or key!="physical_access_certified"}
    report["generation_ready"]=all(required.values()) and plan.get("fixture_mode") is False
    report["blocking_gates"]=[key for key,val in required.items() if not val]
    report["metric_certification_omitted"]=allow_abstract and not physical_all
    return report


def _asset_fingerprints(zone,assets):
    """Bind every rendered layer, including special buildings and finish layers."""
    result={}
    for e in zone["elements"]:
        if e["status"]!="VERIFIED":
            continue
        result[e["id"]]={
            "asset":fingerprint(Path(assets)/e["asset"]["path"]),
            "mask":fingerprint(Path(assets)/e["mask"]["path"])
        }
    return result


def verify_native_manifest(images,zone,report,cfg,assets,*,active_units=None,
                           reference_sha256=None,spatial_sha256=None):
    """Bind actual generated and reviewed image bytes to the exact composited lots."""
    core.fail(isinstance(images,dict) and
              images.get("schema")=="NOVYDRES_MAPWORK_IMAGE_BATCH" and
              isinstance(images.get("images"),list),
              " native-image batch missing or malformed")
    index={}
    for receipt in images["images"]:
        core.fail(isinstance(receipt,dict) and
                  receipt.get("work_unit_id") not in index and
                  isinstance(receipt.get("work_unit_id"),str),
                  " duplicate or invalid native-image work unit")
        index[receipt["work_unit_id"]]=receipt
    units={u["id"]:u for u in report["work_units"]}
    active=set(units) if active_units is None else set(active_units)
    core.fail(bool(active) and active.issubset(units) and set(index)==active,
              " native images must cover exactly the changed work units")
    bound={}
    for element in zone["elements"]:
        if element["kind"]=="lot":
            uid=element.get("work_unit_id")
            core.fail(uid not in bound and uid in units,
                      " duplicate/unknown lot asset per unit")
            bound[uid]=element
    core.fail(active.issubset(bound),
              " every changed unit must have a bound lot asset")
    context={r["work_unit_id"]:r for r in images.get("context_images",[])}
    core.fail(not (set(context)&set(index)) and
              all(k in units for k in context),
              " peer context overlaps generated units or is unknown")
    all_receipts={**context,**index}
    for uid in sorted(active):
        unit=units[uid]
        receipt=index[uid]
        bbox=unit["bbox"];scale=cfg["detail_pixels_per_unit"]
        contract.image_receipt(receipt,expected_size=[
            (bbox[2]-bbox[0])*scale,(bbox[3]-bbox[1])*scale
        ],work_unit_id=uid)
        element=bound[uid]
        core.fail(element["status"]=="VERIFIED" and
                  element["asset"]["sha256"]==receipt["sha256"] and
                  fingerprint(Path(assets)/element["asset"]["path"])==receipt["sha256"],
                  uid+": native image provenance is not the composited lot asset")
        core.fail(element["mask"]["sha256"]==receipt.get("mask_sha256") and
                  fingerprint(Path(assets)/element["mask"]["path"])==receipt["mask_sha256"],
                  uid+": native image receipt not bound to composited mask")
        peer_images={}
        for peer in visual.neighbor_sides(report["work_units"],uid):
            core.fail(peer in all_receipts,uid+": neighbor image receipt missing: "+peer)
            b=units[peer]["bbox"]
            contract.image_receipt(all_receipts[peer],expected_size=[
                (b[2]-b[0])*scale,(b[3]-b[1])*scale
            ],work_unit_id=peer)
            peer_images[peer]=all_receipts[peer]
        core.fail(reference_sha256 is not None and spatial_sha256 is not None,
                  " visual review requires reference and spatial file SHA")
        visual.validate_unit_visual_review(
            receipt.get("visual_review"),unit_id=uid,
            image_sha256=receipt["sha256"],mask_sha256=receipt["mask_sha256"],
            reference_sha256=reference_sha256,spatial_sha256=spatial_sha256,
            work_units=report["work_units"],neighbor_receipts=peer_images)
    return len(active)


def make_composition_contract(zone_path,spatial_path,design_root,zone,report,
                              base,assets,before):
    """Content-addressed capability description; never just a boolean pass flag."""
    return {
        "schema":"NOVYDRES_MAPWORK_COMPOSITION_CONTRACT",
        "zone_path":str(zone_path),
        "zone_sha256":fingerprint(zone_path),
        "spatial_path":str(spatial_path),
        "spatial_sha256":fingerprint(spatial_path),
        "design_root":str(design_root),
        "design_sha256":{u["id"]:fingerprint(Path(design_root)/(u["id"]+".json"))
                         for u in report["work_units"]},
        "reference_sha256":fingerprint(base),
        "asset_sha256":_asset_fingerprints(zone,assets),
        "before_manifest_sha256":fingerprint(Path(before)/"tiles.json") if before else None,
        "world_state_sha256":fingerprint(core.STATE)
    }


def verify_composition_contract(composition,zones,cfg,base,assets,before,protected_u02):
    """Rebuild all authorization gates at use time, then verify input hash binding."""
    core.fail(composition.get("schema")=="NOVYDRES_MAPWORK_COMPOSITION_CONTRACT",
              "invalid composition contract schema")
    core.fail(len(zones)==1 and cfg==core.load(core.CONFIG),
              "composition contract requires the current repository configuration and one zone")
    zone_path=Path(composition["zone_path"])
    spatial_path=Path(composition["spatial_path"])
    design_root=Path(composition["design_root"])
    core.fail(zone_path.is_file() and spatial_path.is_file(),
              "composition contract source files missing")
    core.fail(fingerprint(zone_path)==composition.get("zone_sha256") and
              fingerprint(spatial_path)==composition.get("spatial_sha256") and
              fingerprint(base)==composition.get("reference_sha256") and
              fingerprint(core.STATE)==composition.get("world_state_sha256"),
              "stale pipeline composition contract: source hash changed")
    zone=core.load(zone_path)
    plan=core.load(spatial_path)
    core.fail(zone==zones[0] and plan.get("zone",{}).get("id")==zone["id"] and
              plan.get("fixture_mode") is False and
              zone["status"] in ("GENERATING","VISUAL_REVIEW","OWNER_APPROVED"),
              "composition contract zone/plan authority mismatch")
    is_verified_protocol=bool(composition.get("execution_evidence"))
    core.fail(is_verified_protocol,
              "composition requires independent editorial evidence")
    bound_gate=composition.get("acceptance_evidence",{})
    ledger_file=Path(bound_gate.get("ledger_path","")) if isinstance(bound_gate,dict) else None
    core.fail(ledger_file is not None and ledger_file.is_file() and
              bound_gate.get("criteria_sha256")==acceptance.criteria_contract()["sha256"] and
              bound_gate.get("reference_sha256")==cfg["reference"]["sha256"] and
              bound_gate.get("ledger_sha256")==fingerprint(ledger_file) and
              bound_gate.get("accepted_stages")==list(acceptance.STAGES),
              "composition requires fresh SHA-bound acceptance ledger")
    gate=acceptance.evaluate(
        bound_gate["ledger_path"],reference_file=base,
        reference_sha256=cfg["reference"]["sha256"],
        reference_size=cfg["world_size_units"],require_urban=True,
        require_remote=True,expected_target=zone["id"])
    core.fail(gate["status"]=="PASS" and
              gate["accepted_stages"]==list(acceptance.STAGES),
              "composition requires independent INF-01 through URB-08 PASS")
    if is_verified_protocol:
        receipt=composition["execution_evidence"]
        required={
            "intent_path":"intent_sha256",
            "decisions_path":"decisions_sha256",
            "inventory_path":"inventory_sha256",
            "scope_index_path":"scope_index_sha256",
            "research_path":"research_sha256",
            "capabilities_path":"capabilities_sha256",
            "image_receipts_path":"image_receipts_sha256"
        }
        for key,sha_key in required.items():
            path=Path(receipt.get(key,""))
            core.fail(path.is_file() and fingerprint(path)==receipt.get(sha_key),
                      " composition authority drift: "+key)
        intent=core.load(receipt["intent_path"])
        index=core.load(receipt["scope_index_path"])
        core.fail(index["source_commit"]==intent["source_commit"],
                  " source commit mismatch")
        contract.validate_intent(intent,index["targets"],index["world_bounds"])
        register=core.load(receipt["decisions_path"])
        approvals=contract.validate_proposals(register,region=zone["id"],commit=intent["source_commit"])
        core.fail(not approvals["pending"]," has pending editorial decisions")
        inventory=core.load(receipt["inventory_path"])
        canon=set(index["targets"][zone["id"]].get("approved_element_ids",[]))
        core.fail(set(inventory.get("canonical_elements",[])).issubset(canon),
                  " asserted unsupported existing elements")
        contract.validate_inventory(inventory["elements"],register,canonical_element_ids=canon)
        contract.validate_research(core.load(receipt["research_path"]))
        caps=contract.capability_preflight(core.load(receipt["capabilities_path"]),require_native=False)
        core.fail(not caps["missing"]," required host capability not evidenced")
    core.audit_zone(zone,cfg,assets,strict=True)
    check_canonical_pois(zone_path,plan)
    report=urban.plan_city(plan,cfg,reference_file=base,
                           neighbor_manifests=load_verified_neighbors(plan))
    if is_verified_protocol:
        report["gates"]["owner_art_authorized"]=True
    expected={u["id"] for u in report["work_units"]}
    core.fail(set(composition.get("design_sha256",{}))==expected,
              "composition contract incomplete work-unit design hashes")
    for uid in sorted(expected):
        path=design_root/(uid+".json")
        core.fail(path.is_file() and
                  fingerprint(path)==composition["design_sha256"][uid],
                  uid+": stale/missing work-unit design in composition contract")
    validate_all_unit_designs(plan,report,design_root,cfg,allow_abstract=is_verified_protocol)
    core.fail(report["generation_ready"] and
              (is_verified_protocol or all(report["gates"].values())),
              "composition contract blocked by urban/art gates")
    affected=set(expected)
    if is_verified_protocol and intent["mode"]!="CREATE_REGION":
        mask_path=Path(composition["execution_evidence"].get("edit_mask_path",""))
        core.fail(mask_path.is_file()," edit mask missing before artwork binding")
        with Image.open(mask_path) as im:
            affected=affected_unit_ids(report,im.convert("L"))
    bound=validate_work_unit_bindings(zone,report,plan=plan,
                                     required_units=affected if is_verified_protocol else None)
    verify_unit_art_masks(plan,report,zone["elements"],assets,cfg)
    core.fail(_asset_fingerprints(zone,assets)==composition.get("asset_sha256"),
              "composition contract asset hash or ownership mismatch")
    core.fail(composition.get("before_manifest_sha256")==(
        fingerprint(Path(before)/"tiles.json") if before else None),
        "stale composition contract: approved-before manifest changed")
    world=core.load(core.STATE)
    core.fail(not world.get("last_approved_global_release") or before,
              "composition contract must preserve the previous approved release")
    protection=urban.spatial_protection_mask(plan)
    core.fail(protected_u02 is not None and
              protected_u02.mode=="L" and protected_u02.size==protection.size and
              protected_u02.tobytes()==protection.tobytes(),
              "composition contract requires the exact validated U02 protection mask")
    if is_verified_protocol:
        receipt=composition["execution_evidence"]
        if intent["mode"]!="CREATE_REGION":
            p=Path(receipt.get("edit_mask_path",""))
            core.fail(p.is_file() and fingerprint(p)==receipt.get("edit_mask_sha256"),
                      " edit mask is missing or changed")
            with Image.open(p) as im:
                contract.validate_edit_mask(im.convert("L"),intent["intervention"]["bounds"],protection)
        images=core.load(receipt["image_receipts_path"])
        verify_native_manifest(images,zone,report,cfg,assets,active_units=affected,
                               reference_sha256=fingerprint(base),
                               spatial_sha256=fingerprint(spatial_path))


def run(args):
    """One entrypoint: classified topology candidate repair or verified orchestration."""
    if getattr(args, "topology_source", None):
        if any((getattr(args,"execute",False),getattr(args,"record_attempt",None),
                getattr(args,"recipe_unit",None),getattr(args,"audit_unit",None))):
            raise core.Invalid("topology-only candidate operation cannot execute art or record acceptance")
        if not all((args.topology_classifications,args.topology_out,args.district)):
            raise core.Invalid("topology repair requires --district, --topology-classifications and --topology-out")
        candidate=core.load(args.topology_source)
        if candidate.get("fixture_mode") is not True:
            core.fail(candidate.get("stage") in ("INF-01","INF-02") and
                      candidate.get("target")==args.district,
                      "topology candidate must identify district and INF-01/INF-02 stage")
        cfg=core.load(core.CONFIG)
        report=topology.reconcile_file(
            args.topology_source,args.topology_classifications,args.topology_out,
            expected_reference_sha=(None if candidate.get("fixture_mode") is True else
                                    cfg["reference"]["sha256"]),
            original_reference=args.reference,prior_accepted=args.topology_prior)
        try:
            validation=infra.validate(
                report["candidate_path"], source_sha=candidate["source_sha256"],
                dimensions=tuple(candidate.get("reference_size",(
                    candidate.get("grid",{}).get("width"),
                    candidate.get("grid",{}).get("height")))),
                profile=acceptance.criteria_contract()["profile"],
                prior=args.topology_prior)
        except (infra.InfraInvalid,ValueError,TypeError,KeyError,OSError) as exc:
            validation={"status":"BLOCKED","reason":str(exc)}
        # This is a candidate geometry diagnostic, never an INF stage verdict.
        report["infra_audit"]=validation
        controller.atomic_json(report["diagnostic_path"],report)
        return {"schema":SCHEMA,"phase":"TOPOLOGY_RECONCILIATION",
                "target":args.district,"stage":candidate.get("stage"),
                "status":report["status"],
                "next_action":("CLASSIFY_AND_REVIEW_REMAINING_CROSSINGS" if
                               report["unresolved_crossings"] else
                               "REPAIR_AND_REVALIDATE_INFRA_GEOMETRY" if
                               validation["status"]!="PASS" else
                               "RECORD_REAL_VISUAL_INF_ACCEPTANCE_ATTEMPT"),
                "blockers":report["unresolved_crossings"],
                "audit":report,"publication_authorized":False,
                "canonical_state_changed":False}
    result = flow.run(args, _run_verified)
    result["execution"] = controller.execution_directive(result)
    return result


def _run_verified(args):
    if not getattr(args, "_editorial_verified", False):
        raise core.Invalid("urban renderer requires verified pipeline gate")
    cfg=core.load(core.CONFIG)
    core.config_check(cfg)
    expected=acceptance.criteria_contract()["sha256"]
    core.fail(getattr(args,"_accepted_criteria_sha256",None)==expected,
              "renderer acceptance Markdown contract mismatch")
    zone_path=resolve_zone(args.district,args.zone)
    core.fail(zone_path is not None,"renderer zone manifest missing")
    gate=acceptance.evaluate(
        getattr(args,"acceptance_ledger",None) or
        (zone_path.parent/"acceptance-ledger.json"),
        reference_file=getattr(args,"reference",None),
        reference_sha256=cfg["reference"]["sha256"],
        reference_size=cfg["world_size_units"],
        require_urban=bool(getattr(args,"execute",False) or
                           getattr(args,"recipe_unit",None) or
                           getattr(args,"audit_unit",None)),
        require_remote=True,
        expected_target=args.district)
    core.fail(gate["status"]=="PASS",
              "renderer blocked by independent infrastructure acceptance: "+
              gate["next_action"])
    zone=core.load(zone_path)
    district=zone["id"]
    core.audit_zone(zone,cfg,strict=False)
    def state(phase,action,blockers=(),spatial_path=None,report=None,artifacts=None):
        return checkpoint(district=district,zone_path=zone_path,zone=zone,
                          phase=phase,action=action,blockers=blockers,
                          spatial_path=spatial_path,architectural_report=report,artifacts=artifacts)

    spatial_path=Path(args.spatial) if args.spatial else zone_path.parent/"global-spatial.json"
    if not spatial_path.is_file():
        return state("SPATIAL_MODEL","BUILD_GLOBAL_TRANSPORT_AND_TERRITORY",
                     ["Missing real transport network, exclusive land-use polygons and authoritative zone seams; macro windows cannot substitute."],
                     spatial_path=None)
    plan=core.load(spatial_path)
    if plan.get("zone",{}).get("id")!=district:
        raise core.Invalid("spatial plan and zone ID differ")
    if plan.get("fixture_mode") is True:
        return state("SPATIAL_MODEL","REPLACE_SYNTHETIC_FIXTURE_WITH_REAL_GEOMETRY",
                     ["Synthetic fixtures never authorize real zone art."],spatial_path=spatial_path)
    check_canonical_pois(zone_path,plan)
    report=urban.plan_city(plan,cfg,reference_file=args.reference,
                           neighbor_manifests=load_verified_neighbors(plan))
    if getattr(args,"_editorial_verified",False):
        # Verified proposal register and inventory authorize review of candidate
        # work only; the independent infrastructure stages remain mandatory.
        report["gates"]["owner_art_authorized"]=True
    # Urban design is a mandatory deterministic phase, not an image-side suggestion.
    # A real declarative map can be planned in a hosted runner without private U02
    # bytes. Byte verification remains a hard gate before image generation/composition.
    prerequisites=("source_and_global_topology",
                   "territory_classification","urban_morphology",
                   "quadrants_derived_from_transport","work_unit_coverage",
                   "protected_network_coverage","neighbor_seams",
                   "poi_sites_placed_and_accessible","ground_access_and_clearance")
    unresolved=[x for x in prerequisites if not report["gates"][x]]
    if unresolved:
        return state("SPATIAL_VALIDATION","VERIFY_GLOBAL_SPATIAL_FOUNDATION",
                     unresolved,spatial_path,report)
    design_root=Path(args.design_root) if args.design_root else zone_path.parent/"urban-design"
    if args.design_unit:
        if args.execute or not args.out:
            raise core.Invalid("--design-unit requires --out and cannot be combined with --execute")
        design=content.design_unit(plan,report,args.design_unit)
        location=Path(args.out)/"urban-design"/(args.design_unit+".json")
        core.save(location,design)
        return state("URBAN_DESIGN","REVIEW_OR_PERSIST_UNIT_DESIGN",
                     [] if design["access_verified"] else design["inaccessible_buildings"],
                     spatial_path,report,{"design_file":str(location),
                                         "sha256":fingerprint(location),
                                         "building_count":design["building_count"],
                                         "access_verified":design["access_verified"]})
    units=report["work_units"]
    missing=[u["id"] for u in units if not (design_root/(u["id"]+".json")).is_file()]
    if missing:
        return state("URBAN_DESIGN","DESIGN_NEXT_WORK_UNIT_BEFORE_ART",
                     [missing[0],f"{len(missing)} of {len(units)} building plans missing"],
                     spatial_path,report)
    validate_all_unit_designs(plan,report,design_root,cfg,
                              allow_abstract=getattr(args,"_editorial_verified",False))
    if not report["generation_ready"]:
        blockers=report["blocking_gates"]
        nxt="VERIFY_SPATIAL_AND_ASSET_GATES"
        if blockers==["owner_art_authorized"]:
            nxt="REQUEST_EXPLICIT_ART_AUTHORIZATION"
        elif blockers==["source_bytes_verified"]:
            nxt="FETCH_AND_VERIFY_ORIGINAL_U02"
        return state("SPATIAL_VALIDATION",nxt,blockers,spatial_path,report)

    if zone["status"]=="PLANNING":
        urban_gate=acceptance.evaluate(
            getattr(args,"acceptance_ledger",None) or
                (zone_path.parent/"acceptance-ledger.json"),
            reference_file=args.reference,
            reference_sha256=cfg["reference"]["sha256"],
            reference_size=cfg["world_size_units"],
            require_urban=True,require_remote=True,expected_target=district)
        if urban_gate["status"]!="PASS":
            return state("INFRASTRUCTURE_ACCEPTANCE",
                         urban_gate["next_action"],urban_gate["blockers"],
                         spatial_path,report)
        return state("ART_AUTHORIZATION","ACTIVATE_GENERATION_FROM_ACCEPTED_GATES",
                     ["Record the stage-bound generation transition and verified work-unit IDs; no drawing approval is a substitute."],
                     spatial_path,report)
    required=None
    if getattr(args,"_editorial_verified",False):
        request=core.load(args.intent)
        if request["mode"]!="CREATE_REGION":
            if not args.editable_mask or not Path(args.editable_mask).is_file():
                raise core.Invalid("refinement requires materialized --editable-mask")
            with Image.open(args.editable_mask) as im:
                required=affected_unit_ids(report,im.convert("L"))
    bound=validate_work_unit_bindings(zone,report,plan=plan,required_units=required)
    pending=[x["id"] for x in zone["elements"] if x["status"]!="VERIFIED"]
    if pending:
        return state("ART_GENERATION","GENERATE_AND_VERIFY_NEXT_ATOMIC_ASSET",
                     [pending[0]],spatial_path,report)

    if zone["status"]=="PUBLISHED":
        return state("DONE","VERIFY_REMOTE_RELEASE_AND_READBACK",
                     [],spatial_path,report)
    if not args.execute:
        return state("COMPOSITION","COMPOSE_SAFE_CANDIDATE",
                     ["Run again with --execute, --reference, --assets and --out; pass --before if approved tiles exist."],
                     spatial_path,report)
    if not (args.reference and args.assets and args.out):
        raise core.Invalid("--execute requires --reference, --assets and --out")
    world=core.load(core.STATE)
    if world.get("last_approved_global_release") is not None and not args.before:
        raise core.Invalid("approved release exists: --before is mandatory to preserve its tiles")
    protection=urban.spatial_protection_mask(plan)
    out=Path(args.out); tiles=out/"tiles"
    core.audit_zone(zone,cfg,args.assets,strict=True)
    verify_unit_art_masks(plan,report,zone["elements"],args.assets,cfg)
    composition_contract=make_composition_contract(zone_path,spatial_path,design_root,zone,
                                       report,args.reference,args.assets,args.before)
    ledger_path=getattr(args,"acceptance_ledger",None) or (
        zone_path.parent/"acceptance-ledger.json")
    composition_contract["acceptance_evidence"]={
        "ledger_path":str(ledger_path),
        "ledger_sha256":fingerprint(ledger_path),
        "criteria_sha256":acceptance.criteria_contract()["sha256"],
        "reference_sha256":cfg["reference"]["sha256"],
        "accepted_stages":list(acceptance.STAGES)
    }
    edit_mask=None
    if getattr(args,"_editorial_verified",False):
        intent=core.load(args.intent)
        registration={
            "intent_path":str(Path(args.intent).resolve()),
            "intent_sha256":fingerprint(args.intent),
            "decisions_path":str(Path(args.decisions_file).resolve()),
            "decisions_sha256":fingerprint(args.decisions_file),
            "inventory_path":str(Path(args.inventory_file).resolve()),
            "inventory_sha256":fingerprint(args.inventory_file),
            "scope_index_path":str(Path(args.scope_index or ROOT/"scope-index.json").resolve()),
            "scope_index_sha256":fingerprint(args.scope_index or ROOT/"scope-index.json"),
            "research_path":str(Path(args.research_file).resolve()),
            "research_sha256":fingerprint(args.research_file),
            "capabilities_path":str(Path(args.capabilities).resolve()),
            "capabilities_sha256":fingerprint(args.capabilities)
        }
        composition_contract["execution_evidence"]=registration
        if intent["mode"]!="CREATE_REGION":
            if not args.editable_mask:
                raise core.Invalid(" refinement requires --editable-mask")
            with Image.open(args.editable_mask) as im:
                edit_mask=im.convert("L")
            contract.validate_edit_mask(edit_mask,intent["intervention"]["bounds"],protection)
            registration["edit_mask_sha256"]=fingerprint(args.editable_mask)
            registration["edit_mask_path"]=str(Path(args.editable_mask).resolve())
        if not args.image_receipts:
            raise core.Invalid(" native-image provenance receipts required")
        receipts=core.load(args.image_receipts)
        active=affected_unit_ids(report,edit_mask)
        verify_native_manifest(receipts,zone,report,cfg,args.assets,active_units=active,
                               reference_sha256=fingerprint(args.reference),
                               spatial_sha256=fingerprint(spatial_path))
        registration["image_receipts_path"]=str(Path(args.image_receipts).resolve())
        registration["image_receipts_sha256"]=fingerprint(args.image_receipts)
    manifest=core.composite([zone],cfg,args.reference,args.assets,tiles,
                            approved_before=args.before,protected_u02=protection,
                            edit_mask_u02=edit_mask,contract=composition_contract)
    comparison=out/"comparison.html"
    result=core.html_compare(args.before,tiles,args.reference,comparison,cfg)
    evidence={"tiles":len(manifest["tiles"]),"comparison":str(comparison),
              "comparison_bytes":result["bytes"],"manifest":str(tiles/"tiles.json"),
              "tiles_sha256":fingerprint(tiles/"tiles.json"),
              "before_sha256":fingerprint(out/"overview-before.png"),
              "after_sha256":fingerprint(out/"overview-after.png"),
              "image_receipts_sha256":fingerprint(args.image_receipts)}
    if getattr(args,"_editorial_verified",False):
        if not args.macro_review or not Path(args.macro_review).is_file():
            return state("GLOBAL_VISUAL_REVIEW","AGENT_INSPECT_COMPOSED_ATLAS",
                         ["Inspect real before/after overviews, tiles, unit interfaces and macro/micro coherence; record hash-bound global report."],
                         spatial_path,report,evidence)
        review=core.load(args.macro_review)
        evidence["global_visual_review"]=visual.validate_global_visual_review(
            review,tiles=tiles/"tiles.json",
            before_overview=out/"overview-before.png",
            after_overview=out/"overview-after.png",
            original_reference=args.reference,image_receipts=args.image_receipts)
    return state("CANDIDATE_READY_FOR_OWNER_REVIEW","SHOW_COMPLETE_BEFORE_AFTER",
                 ["Owner must explicitly approve candidate; GitHub/Drive readback and editorial gate remain mandatory."],
                 spatial_path,report,evidence)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("command",choices=["run"])
    target=p.add_mutually_exclusive_group(required=False)
    target.add_argument("--district")
    target.add_argument("--zone")
    p.add_argument("--spatial",help="approved candidate territorial/network manifest")
    p.add_argument("--design-root",help="Git-individual-building plans for all work units")
    p.add_argument("--design-unit",help="prepare one deterministic individual-building plan, before image generation")
    p.add_argument("--reference",help="actual original U02 PNG, verified by SHA")
    p.add_argument("--assets",help="locally retrieved SHA-verified artist assets")
    p.add_argument("--before",help="downloaded last approved tiles, never a candidate release")
    p.add_argument("--out",help="candidate output only; no canon write")
    p.add_argument("--execute",action="store_true",help="compose only if all planning and art gates pass")
    p.add_argument("--checkpoint",help="write deterministic resumable checkpoint JSON")
    p.add_argument("--intent",help="agent-resolved and canonical-indexed  request JSON")
    p.add_argument("--record-attempt",help="record one real candidate, then evaluate the same stage")
    p.add_argument("--topology-source",help="candidate spatial geometry/transport JSON; never an accepted stage")
    p.add_argument("--topology-classifications",help="agent-reviewed per-crossing observations")
    p.add_argument("--topology-out",help="candidate-only topology and diagnostic output directory")
    p.add_argument("--topology-prior",help="immutable accepted INF-01 geometry required for INF-02")
    p.add_argument("--acceptance-ledger",
                   help="hash-bound, self-reviewed infrastructure candidate rounds; defaults to zone ledger")
    p.add_argument("--scope-index",help="exact canonical subject/index snapshot")
    p.add_argument("--capabilities",help="host capabilities with actual execution receipts")
    p.add_argument("--research-file",help="external analogues including two independent domains")
    p.add_argument("--decisions-file",help="owner-signed proposal and decision register")
    p.add_argument("--inventory-file",help="full approved installation inventory")
    p.add_argument("--image-receipts",help="materialized native image receipts per work unit")
    p.add_argument("--editable-mask",help="owner-scoped U02 intervention mask for refinement")
    p.add_argument("--recipe-unit",help="prepare generator recipe for a single planned unit")
    p.add_argument("--audit-unit",help="audit native asset materialization and mask per unit")
    p.add_argument("--unit-receipt",help="one actual generated image receipt")
    p.add_argument("--unit-mask",help="local mask PNG at full atomic resolution")
    p.add_argument("--visual-review",help="hash-bound agent inspection of unit image/mask and face-neighbors")
    p.add_argument("--macro-review",help="agent inspection of real assembled tiles and before/after overviews")
    p.add_argument("--ledger",help="SHA-bound per-unit progress/repair ledger")
    p.add_argument("--start-unit",action="store_true",help="start one audit attempt in the ledger")
    p.add_argument("--strategy-id",help="new image-generation strategy for replan")
    p.add_argument("--replan-evidence",help="concrete evidence for image replanning")
    p.add_argument("--request-id",help="idempotent image attempt identifier")
    p.add_argument("--improvement-evidence",help="observable improvement since previous image failure")
    args=p.parse_args(argv)
    if args.execute and not args.intent:
        p.error("--execute requires --intent and verified gates")

    try:
        result=run(args)
        if args.checkpoint:
            controller.atomic_json(args.checkpoint,result)
        # PASS is reserved for verified criteria, not merely a successful
        # command that returned an incomplete checkpoint or a handoff.
        if (result.get("phase") == "INFRASTRUCTURE_ACCEPTANCE" and
                isinstance(result.get("audit"),dict) and
                result["audit"].get("status")=="FAIL"):
            outcome="FAIL"
        elif result.get("blockers") or result.get("phase") == "INFRASTRUCTURE_ACCEPTANCE":
            outcome="BLOCKED"
        elif result.get("phase") == "CANDIDATE_READY_FOR_OWNER_REVIEW":
            outcome="READY_FOR_OWNER_REVIEW"
        else:
            outcome="CHECKPOINT"
        print(json.dumps({"status":outcome, "next_action":result.get("next_action"),
                          "retryable":outcome == "FAIL" and result.get("next_action") not in
                            ("RESTORE_REQUIRED_HOST_TOOLS", "ASK_OWNER_ONE_DECISION"),
                          "result":result},ensure_ascii=False,indent=2))
        return 2 if outcome == "FAIL" else 0
    except (core.Invalid,urban.ContractError,contract.Blocked,
            topology.TopologyInvalid,KeyError,ValueError,OSError) as exc:
        print(json.dumps({"status":"FAIL","error":str(exc)},ensure_ascii=False),file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())

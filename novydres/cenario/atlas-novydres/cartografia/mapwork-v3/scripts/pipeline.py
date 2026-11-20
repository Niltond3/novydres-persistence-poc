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
import v33_contracts as v33
import v33_flow

ROOT=Path(__file__).resolve().parents[1]
SCHEMA="NOVYDRES_MAPWORK_V32_PIPELINE_CHECKPOINT_1"


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
        spatial=zone_path.parent/"global-spatial-v31.json"
        if not spatial.is_file():
            # An existing approved sketch is not a future reservation.
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


def check_canonical_pois(zone_path,plan):
    legacy=zone_path.parent/"spatial-plan.json"
    if legacy.is_file():
        source=core.load(legacy)
        required={p["id"] for p in source.get("pois",[])}
        found={p["id"] for p in plan["special_sites"]}
        actual_ids=[p["id"] for p in plan["special_sites"]]
        if len(actual_ids)!=len(set(actual_ids)) or found!=required:
            raise core.Invalid("approved POI inventory differs (omitted, duplicate or unauthorized): "+
                               ", ".join(sorted(required.symmetric_difference(found))))


def validate_work_unit_bindings(zone,report,plan=None):
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
    missing=expected.keys()-bound.keys()
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
                  plan.get("work_policy",{}).get("parceling")!="URBAN_BLOCKS_V33")
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


def verify_native_manifest(images,zone,report,cfg,assets):
    """Bind actual generated and reviewed image bytes to the exact composited lots."""
    core.fail(isinstance(images,dict) and
              images.get("schema")=="NOVYDRES_MAPWORK_V33_IMAGE_BATCH_1" and
              isinstance(images.get("images"),list),
              "V3.3 native-image batch missing or malformed")
    index={}
    for receipt in images["images"]:
        core.fail(isinstance(receipt,dict) and
                  receipt.get("work_unit_id") not in index and
                  isinstance(receipt.get("work_unit_id"),str),
                  "V3.3 duplicate or invalid native-image work unit")
        index[receipt["work_unit_id"]]=receipt
    units={u["id"]:u for u in report["work_units"]}
    core.fail(set(index)==set(units),
              "V3.3 native images must cover planned work units exactly once")
    bound={}
    for element in zone["elements"]:
        if element["kind"]=="lot":
            uid=element.get("work_unit_id")
            core.fail(uid not in bound and uid in units,
                      "V3.3 duplicate/unknown lot asset per unit")
            bound[uid]=element
    core.fail(set(bound)==set(units),
              "V3.3 every native image must correspond to one bound lot asset")
    for uid,unit in units.items():
        receipt=index[uid]
        bbox=unit["bbox"];scale=cfg["detail_pixels_per_unit"]
        v33.image_receipt(receipt,expected_size=[
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
        review=receipt.get("visual_review")
        core.fail(isinstance(review,dict) and review.get("by")=="AGENT" and
                  review.get("status")=="PASS" and
                  isinstance(review.get("evidence"),str) and
                  len(review["evidence"])>=12,
                  uid+": visual inspection receipt missing or failed")
    return len(units)


def make_composition_contract(zone_path,spatial_path,design_root,zone,report,
                              base,assets,before):
    """Content-addressed capability description; never just a boolean pass flag."""
    return {
        "schema":"NOVYDRES_MAPWORK_V32_COMPOSITION_CONTRACT_1",
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


def verify_composition_contract(contract,zones,cfg,base,assets,before,protected_u02):
    """Rebuild all authorization gates at use time, then verify input hash binding."""
    core.fail(contract.get("schema")=="NOVYDRES_MAPWORK_V32_COMPOSITION_CONTRACT_1",
              "invalid composition contract schema")
    core.fail(len(zones)==1 and cfg==core.load(core.CONFIG),
              "composition contract requires the current repository configuration and one zone")
    zone_path=Path(contract["zone_path"])
    spatial_path=Path(contract["spatial_path"])
    design_root=Path(contract["design_root"])
    core.fail(zone_path.is_file() and spatial_path.is_file(),
              "composition contract source files missing")
    core.fail(fingerprint(zone_path)==contract.get("zone_sha256") and
              fingerprint(spatial_path)==contract.get("spatial_sha256") and
              fingerprint(base)==contract.get("reference_sha256") and
              fingerprint(core.STATE)==contract.get("world_state_sha256"),
              "stale pipeline composition contract: source hash changed")
    zone=core.load(zone_path)
    plan=core.load(spatial_path)
    core.fail(zone==zones[0] and plan.get("zone",{}).get("id")==zone["id"] and
              plan.get("fixture_mode") is False and
              zone["status"] in ("GENERATING","VISUAL_REVIEW","OWNER_APPROVED"),
              "composition contract zone/plan authority mismatch")
    is_v33=bool(contract.get("v33"))
    if is_v33:
        receipt=contract["v33"]
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
                      "V3.3 composition authority drift: "+key)
        intent=core.load(receipt["intent_path"])
        index=core.load(receipt["scope_index_path"])
        core.fail(index["source_commit"]==intent["source_commit"],
                  "V3.3 source commit mismatch")
        v33.validate_intent(intent,index["targets"],index["world_bounds"])
        register=core.load(receipt["decisions_path"])
        approvals=v33.validate_proposals(register,region=zone["id"],commit=intent["source_commit"])
        core.fail(not approvals["pending"],"V3.3 has pending editorial decisions")
        inventory=core.load(receipt["inventory_path"])
        canon=set(index["targets"][zone["id"]].get("approved_element_ids",[]))
        core.fail(set(inventory.get("canonical_elements",[])).issubset(canon),
                  "V3.3 asserted unsupported existing elements")
        v33.validate_inventory(inventory["elements"],register,canonical_element_ids=canon)
        v33.validate_research(core.load(receipt["research_path"]))
        caps=v33.capability_preflight(core.load(receipt["capabilities_path"]))
        core.fail(not caps["missing"],"V3.3 required host capability not evidenced")
    core.audit_zone(zone,cfg,assets,strict=True,v33_verified=is_v33)
    check_canonical_pois(zone_path,plan)
    report=urban.plan_city(plan,cfg,reference_file=base,
                           neighbor_manifests=load_verified_neighbors(plan))
    if is_v33:
        report["gates"]["owner_art_authorized"]=True
    expected={u["id"] for u in report["work_units"]}
    core.fail(set(contract.get("design_sha256",{}))==expected,
              "composition contract incomplete work-unit design hashes")
    for uid in sorted(expected):
        path=design_root/(uid+".json")
        core.fail(path.is_file() and
                  fingerprint(path)==contract["design_sha256"][uid],
                  uid+": stale/missing work-unit design in composition contract")
    validate_all_unit_designs(plan,report,design_root,cfg,allow_abstract=is_v33)
    core.fail(report["generation_ready"] and
              (is_v33 or all(report["gates"].values())),
              "composition contract blocked by urban/art gates")
    bound=validate_work_unit_bindings(zone,report,plan=plan)
    verify_unit_art_masks(plan,report,zone["elements"],assets,cfg)
    core.fail(_asset_fingerprints(zone,assets)==contract.get("asset_sha256"),
              "composition contract asset hash or ownership mismatch")
    core.fail(contract.get("before_manifest_sha256")==(
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
    if is_v33:
        receipt=contract["v33"]
        if intent["mode"]!="CREATE_REGION":
            p=Path(receipt.get("edit_mask_path",""))
            core.fail(p.is_file() and fingerprint(p)==receipt.get("edit_mask_sha256"),
                      "V3.3 edit mask is missing or changed")
            with Image.open(p) as im:
                v33.validate_edit_mask(im.convert("L"),intent["intervention"]["bounds"],protection)
        images=core.load(receipt["image_receipts_path"])
        verify_native_manifest(images,zone,report,cfg,assets)


def run(args):
    if getattr(args,"intent",None) and not getattr(args,"v33_verified",False):
        return v33_flow.run(args,run)
    cfg=core.load(core.CONFIG)
    core.config_check(cfg)
    zone_path=resolve_zone(args.district,args.zone)
    if zone_path is None:
        return checkpoint(district=args.district,phase="BOOTSTRAP",
                          action="CREATE_ZONE_MANIFEST_FROM_CANON",
                          blockers=["Resolve district subject ID, canonical boundaries, neighbors and source SHA from GitHub master; do not invent geometry."])
    zone=core.load(zone_path)
    district=zone["id"]
    core.audit_zone(zone,cfg,strict=False,
                    v33_verified=getattr(args,"v33_verified",False))
    def state(phase,action,blockers=(),spatial_path=None,report=None,artifacts=None):
        return checkpoint(district=district,zone_path=zone_path,zone=zone,
                          phase=phase,action=action,blockers=blockers,
                          spatial_path=spatial_path,architectural_report=report,artifacts=artifacts)

    if zone["status"]=="PLANNING" and not getattr(args,"v33_verified",False):
        if not zone.get("research"):
            return state("RESEARCH","RESEARCH_ANALOGUES",
                         ["Record dated URLs and architecture/urbanism analogues before decisions."])
        open_questions=[x["id"] for x in zone["decisions"] if x["status"]=="OPEN"]
        if open_questions:
            return state("DECISIONS","ASK_OWNER_ONE_DECISION_AT_A_TIME",open_questions)
        if not zone["sketch_approved"]:
            return state("TECHNICAL_SKETCH","PRESENT_INTEGRAL_SKETCH_FOR_OWNER_APPROVAL",
                         ["Include global transport, water, urban blocks, buildings, POIs and neighboring zones."])

    if not zone["sketch_approved"] and not getattr(args,"v33_verified",False):
        return state("TECHNICAL_SKETCH","WAIT_EXPLICIT_SKETCH_APPROVAL")

    spatial_path=Path(args.spatial) if args.spatial else zone_path.parent/"global-spatial-v31.json"
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
    if getattr(args,"v33_verified",False):
        # V3.3 proposal register + exact installation inventory were validated
        # BEFORE calling this legacy spatial engine. The old blanket owner-art
        # approval is no longer an additional approval ceremony.
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
                              allow_abstract=getattr(args,"v33_verified",False))
    if not report["generation_ready"]:
        blockers=report["blocking_gates"]
        nxt="VERIFY_SPATIAL_AND_ASSET_GATES"
        if blockers==["owner_art_authorized"]:
            nxt="REQUEST_EXPLICIT_ART_AUTHORIZATION"
        elif blockers==["source_bytes_verified"]:
            nxt="FETCH_AND_VERIFY_ORIGINAL_U02"
        return state("SPATIAL_VALIDATION",nxt,blockers,spatial_path,report)

    if zone["status"]!="SKETCH_APPROVED":
        bound=validate_work_unit_bindings(zone,report,plan=plan)
    if zone["status"]=="SKETCH_APPROVED":
        return state("ART_AUTHORIZED","PROMOTE_ZONE_TO_GENERATING_WITH_AUDIT",
                     ["Spatial contract passed; create verified generation jobs only, not a release."],
                     spatial_path,report)
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
    core.audit_zone(zone,cfg,args.assets,strict=True,
                    v33_verified=getattr(args,"v33_verified",False))
    verify_unit_art_masks(plan,report,zone["elements"],args.assets,cfg)
    contract=make_composition_contract(zone_path,spatial_path,design_root,zone,
                                       report,args.reference,args.assets,args.before)
    edit_mask=None
    if getattr(args,"v33_verified",False):
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
        contract["v33"]=registration
        if intent["mode"]!="CREATE_REGION":
            if not args.editable_mask:
                raise core.Invalid("V3.3 refinement requires --editable-mask")
            with Image.open(args.editable_mask) as im:
                edit_mask=im.convert("L")
            v33.validate_edit_mask(edit_mask,intent["intervention"]["bounds"],protection)
            registration["edit_mask_sha256"]=fingerprint(args.editable_mask)
            registration["edit_mask_path"]=str(Path(args.editable_mask).resolve())
        if not args.image_receipts:
            raise core.Invalid("V3.3 native-image provenance receipts required")
        receipts=core.load(args.image_receipts)
        verify_native_manifest(receipts,zone,report,cfg,args.assets)
        registration["image_receipts_path"]=str(Path(args.image_receipts).resolve())
        registration["image_receipts_sha256"]=fingerprint(args.image_receipts)
    manifest=core.composite([zone],cfg,args.reference,args.assets,tiles,
                            approved_before=args.before,protected_u02=protection,
                            edit_mask_u02=edit_mask,contract=contract)
    comparison=out/"comparison.html"
    result=core.html_compare(args.before,tiles,args.reference,comparison,cfg)
    return state("CANDIDATE_READY_FOR_OWNER_REVIEW","SHOW_COMPLETE_BEFORE_AFTER",
                 ["Owner must explicitly approve candidate; GitHub/Drive readback and editorial gate remain mandatory."],
                 spatial_path,report,{"tiles":len(manifest["tiles"]),"comparison":str(comparison),
                                      "comparison_bytes":result["bytes"],"manifest":str(tiles/"tiles.json")})


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("command",choices=["run"])
    target=p.add_mutually_exclusive_group(required=False)
    target.add_argument("--district")
    target.add_argument("--zone")
    p.add_argument("--spatial",help="approved candidate territorial/network manifest")
    p.add_argument("--design-root",help="Git-versioned individual-building plans for all work units")
    p.add_argument("--design-unit",help="prepare one deterministic individual-building plan, before image generation")
    p.add_argument("--reference",help="actual original U02 PNG, verified by SHA")
    p.add_argument("--assets",help="locally retrieved SHA-verified artist assets")
    p.add_argument("--before",help="downloaded last approved tiles, never a candidate release")
    p.add_argument("--out",help="candidate output only; no canon write")
    p.add_argument("--execute",action="store_true",help="compose only if all planning and art gates pass")
    p.add_argument("--checkpoint",help="write deterministic resumable checkpoint JSON")
    p.add_argument("--intent",help="agent-resolved and canonical-indexed V3.3 request JSON")
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
    p.add_argument("--visual-review",help="separate agent-only aesthetic inspection receipt")
    p.add_argument("--ledger",help="SHA-bound per-unit progress/repair ledger")
    p.add_argument("--start-unit",action="store_true",help="start one audit attempt in the ledger")
    args=p.parse_args(argv)
    if args.execute and not args.intent:
        p.error("V3.3 composition requires --intent and owner decision/inventory receipts")
    if not args.intent and not (args.district or args.zone):
        p.error("legacy calls need --district/--zone; V3.3 calls need --intent")
    try:
        result=run(args)
        if args.checkpoint:
            core.save(args.checkpoint,result)
        print(json.dumps({"status":"PASS","result":result},ensure_ascii=False,indent=2))
        return 0
    except (core.Invalid,urban.ContractError,v33.Blocked,KeyError,ValueError,OSError) as exc:
        print(json.dumps({"status":"FAIL","error":str(exc)},ensure_ascii=False),file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())

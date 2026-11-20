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
            if zone["status"] in ("GENERATING","VISUAL_REVIEW","OWNER_APPROVED","PUBLISHED"):
                raise core.Invalid("active neighbor has no global spatial manifest: "+neighbor)
            continue
        other=core.load(spatial)
        if other.get("zone",{}).get("id")!=neighbor or other.get("fixture_mode") is not False:
            raise core.Invalid("invalid neighbor identity or fixture: "+neighbor)
        if other.get("source_sha256")!=plan["source_sha256"]:
            raise core.Invalid("neighbor U02 authority mismatch: "+neighbor)
        digest=lambda network: hashlib.sha256(json.dumps(network,sort_keys=True,
                    separators=(",",":")).encode("utf-8")).hexdigest()
        if digest(other["transport"])!=digest(plan["transport"]):
            raise core.Invalid("neighbor global transport differs: "+neighbor)
        peers[neighbor]={"seams":other["neighbor_seams"]}
    return peers


def check_canonical_pois(zone_path,plan):
    legacy=zone_path.parent/"spatial-plan.json"
    if legacy.is_file():
        source=core.load(legacy)
        required={p["id"] for p in source.get("pois",[])}
        found={p["id"] for p in plan["special_sites"]}
        if required and not required.issubset(found):
            raise core.Invalid("approved/planned POIs missing spatial sites: "+
                               ", ".join(sorted(required-found)))


def validate_work_unit_bindings(zone,report):
    """Every planned unit must own exactly one atomic lot asset."""
    expected={u["id"]:u for u in report["work_units"]}
    bound={}
    for e in zone["elements"]:
        uid=e.get("work_unit_id")
        if uid not in expected:
            raise core.Invalid(e["id"]+": absent or invalid work_unit_id")
        if e["kind"]=="lot":
            if uid in bound:
                raise core.Invalid(uid+": duplicate atomic lot asset")
            if e["core"]!=expected[uid]["bbox"]:
                raise core.Invalid(uid+": asset core differs from planned work unit")
            bound[uid]=e
    missing=expected.keys()-bound.keys()
    if missing:
        raise core.Invalid("planned work units lack bound art elements: "+", ".join(sorted(missing)[:6]))
    return bound


def verify_unit_art_masks(plan,report,elements,assets,cfg):
    """A lot's decoded mask may paint only its own editable work-unit cells."""
    from PIL import ImageChops, ImageDraw
    context=content.design_context(plan)
    w,h=context["w"],context["h"]
    scale=cfg["detail_pixels_per_unit"]
    for uid,e in elements.items():
        if e["status"]!="VERIFIED":
            continue
        x0,y0,x1,y1=e["envelope"]
        left,top=round(x0*scale),round(y0*scale)
        mask_file=Path(assets)/e["mask"]["path"]
        with Image.open(mask_file) as img:
            m=img.convert("L")
        allowed=Image.new("L",m.size,0)
        draw=ImageDraw.Draw(allowed)
        unit=next(u for u in report["work_units"] if u["id"]==uid)
        bx0,by0,bx1,by1=unit["bbox"]
        for y in range(by0,by1):
            for x in range(bx0,bx1):
                i=y*w+x
                if context["editable"][i] and context["labels"][i]==unit["block_label"]:
                    sx,sy=x*scale-left,y*scale-top
                    draw.rectangle([sx,sy,sx+scale-1,sy+scale-1],fill=255)
        if ImageChops.subtract(m,allowed).getbbox() is not None:
            raise core.Invalid(uid+": art mask paints outside its assigned editable cells")


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
    core.audit_zone(zone,cfg,assets,strict=True)
    check_canonical_pois(zone_path,plan)
    report=urban.plan_city(plan,cfg,reference_file=base,
                           neighbor_manifests=load_verified_neighbors(plan))
    core.fail(report["generation_ready"] and all(report["gates"].values()),
              "composition contract blocked by urban/art gates")
    expected={u["id"] for u in report["work_units"]}
    core.fail(set(contract.get("design_sha256",{}))==expected,
              "composition contract incomplete work-unit design hashes")
    ctx=content.design_context(plan)
    for uid in sorted(expected):
        path=design_root/(uid+".json")
        core.fail(path.is_file() and
                  fingerprint(path)==contract["design_sha256"][uid],
                  uid+": stale/missing work-unit design in composition contract")
        candidate=core.load(path)
        regenerated=content.design_unit(plan,report,uid,context=ctx)
        core.fail(candidate==regenerated and regenerated["access_verified"],
                  uid+": unverified detailed design at composition")
    bound=validate_work_unit_bindings(zone,report)
    verify_unit_art_masks(plan,report,bound,assets,cfg)
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


def run(args):
    cfg=core.load(core.CONFIG)
    core.config_check(cfg)
    zone_path=resolve_zone(args.district,args.zone)
    if zone_path is None:
        return checkpoint(district=args.district,phase="BOOTSTRAP",
                          action="CREATE_ZONE_MANIFEST_FROM_CANON",
                          blockers=["Resolve district subject ID, canonical boundaries, neighbors and source SHA from GitHub master; do not invent geometry."])
    zone=core.load(zone_path)
    district=zone["id"]
    core.audit_zone(zone,cfg,strict=False)
    def state(phase,action,blockers=(),spatial_path=None,report=None,artifacts=None):
        return checkpoint(district=district,zone_path=zone_path,zone=zone,
                          phase=phase,action=action,blockers=blockers,
                          spatial_path=spatial_path,architectural_report=report,artifacts=artifacts)

    if zone["status"]=="PLANNING":
        if not zone.get("research"):
            return state("RESEARCH","RESEARCH_ANALOGUES",
                         ["Record dated URLs and architecture/urbanism analogues before decisions."])
        open_questions=[x["id"] for x in zone["decisions"] if x["status"]=="OPEN"]
        if open_questions:
            return state("DECISIONS","ASK_OWNER_ONE_DECISION_AT_A_TIME",open_questions)
        if not zone["sketch_approved"]:
            return state("TECHNICAL_SKETCH","PRESENT_INTEGRAL_SKETCH_FOR_OWNER_APPROVAL",
                         ["Include global transport, water, urban blocks, buildings, POIs and neighboring zones."])

    if not zone["sketch_approved"]:
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
    context=content.design_context(plan)
    building_count=0
    for unit in units:
        item=core.load(design_root/(unit["id"]+".json"))
        expected=content.design_unit(plan,report,unit["id"],context=context)
        if item!=expected:
            raise core.Invalid(unit["id"]+": detailed building plan differs from validated urban geometry")
        if not expected["access_verified"]:
            raise core.Invalid(unit["id"]+": at least one building lacks ground street access")
        building_count+=expected["building_count"]
    report["urban_design"]={"work_units_verified":len(units),"buildings_placed":building_count,
                            "individual_footprints_verified":True,"all_access_paths_verified":True}
    if not report["generation_ready"]:
        blockers=report["blocking_gates"]
        nxt="VERIFY_SPATIAL_AND_ASSET_GATES"
        if blockers==["owner_art_authorized"]:
            nxt="REQUEST_EXPLICIT_ART_AUTHORIZATION"
        elif blockers==["source_bytes_verified"]:
            nxt="FETCH_AND_VERIFY_ORIGINAL_U02"
        return state("SPATIAL_VALIDATION",nxt,blockers,spatial_path,report)

    if zone["status"]!="SKETCH_APPROVED":
        bound=validate_work_unit_bindings(zone,report)
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
    core.audit_zone(zone,cfg,args.assets,strict=True)
    verify_unit_art_masks(plan,report,bound,args.assets,cfg)
    contract=make_composition_contract(zone_path,spatial_path,design_root,zone,
                                       report,args.reference,args.assets,args.before)
    manifest=core.composite([zone],cfg,args.reference,args.assets,tiles,
                            approved_before=args.before,protected_u02=protection,
                            contract=contract)
    comparison=out/"comparison.html"
    result=core.html_compare(args.before,tiles,args.reference,comparison,cfg)
    return state("CANDIDATE_READY_FOR_OWNER_REVIEW","SHOW_COMPLETE_BEFORE_AFTER",
                 ["Owner must explicitly approve candidate; GitHub/Drive readback and editorial gate remain mandatory."],
                 spatial_path,report,{"tiles":len(manifest["tiles"]),"comparison":str(comparison),
                                      "comparison_bytes":result["bytes"],"manifest":str(tiles/"tiles.json")})


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("command",choices=["run"])
    target=p.add_mutually_exclusive_group(required=True)
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
    args=p.parse_args(argv)
    try:
        result=run(args)
        if args.checkpoint:
            core.save(args.checkpoint,result)
        print(json.dumps({"status":"PASS","result":result},ensure_ascii=False,indent=2))
        return 0
    except (core.Invalid,urban.ContractError,KeyError,ValueError,OSError) as exc:
        print(json.dumps({"status":"FAIL","error":str(exc)},ensure_ascii=False),file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())

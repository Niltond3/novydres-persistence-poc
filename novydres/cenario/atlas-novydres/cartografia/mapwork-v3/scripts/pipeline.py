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
    report=urban.plan_city(plan,cfg,reference_file=args.reference)
    # Urban design is a mandatory deterministic phase, not an image-side suggestion.
    prerequisites=("source_and_global_topology","source_bytes_verified",
                   "territory_classification","urban_morphology",
                   "quadrants_derived_from_transport","work_unit_coverage",
                   "protected_network_coverage","neighbor_seams")
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
    manifest=core.composite([zone],cfg,args.reference,args.assets,tiles,
                            approved_before=args.before,protected_u02=protection)
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

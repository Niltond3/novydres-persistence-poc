#!/usr/bin/env python3
"""V3.3 agent orchestration layer of the SINGLE scripts/pipeline.py entrypoint.

This is a pure library. The host agent must genuinely perform web browsing,
editorial dialogue, GitHub readback and native image generation and write
versioned receipts. Missing capabilities are blockers, never simulated work.
"""
from __future__ import annotations

from pathlib import Path

import mapwork as core
import urban_architecture as urban
import urban_content as content
import v33_contracts as v33

ROOT=Path(__file__).resolve().parents[1]
CANON_CATALOG=ROOT.parents[3]/"catalogo.json"


def _load(path):
    return core.load(path) if path and Path(path).is_file() else None


def _state(phase, action, blockers, *, intent=None, audit=None, next_id=None):
    return {
        "schema":"NOVYDRES_MAPWORK_V33_PIPELINE_CHECKPOINT_1",
        "phase":phase,
        "next_action":action,
        "blockers":list(blockers),
        "target":intent["target"]["id"] if intent else None,
        "mode":intent["mode"] if intent else None,
        "request_sha256":v33.evidence_digest(intent) if intent else None,
        "audit":audit,
        "next_decision_id":next_id,
        "publication_authorized":False,
        "canonical_state_changed":False
    }


def run(args, v32_run):
    if not args.intent:
        return _state("INTENT", "AGENT_RESOLVE_AND_RECORD_INTENT",
                      ["Provide --intent JSON produced by semantic agent; scripts never guess place names"])
    intent = _load(args.intent)
    if intent is None:
        return _state("INTENT", "MATERIALIZE_INTENT",
                      ["Intent file absent; host agent must write and read it back"])
    index = _load(args.scope_index or ROOT/"scope-index.json")
    v33.require(isinstance(index,dict) and
                index.get("schema")=="NOVYDRES_MAPWORK_V33_SCOPE_INDEX_1",
                "canonical scope index missing")
    v33.require(index.get("source_commit")==intent.get("source_commit"),
                "canonical scope index and intent commit differ; rebootstrap master")
    if CANON_CATALOG.is_file():
        canonical_ids={s["id"] for s in core.load(CANON_CATALOG)["subjects"]}
        v33.require(all(v["subject_id"] in canonical_ids
                        for v in index["targets"].values()),
                    "scope index contains a noncanonical subject ID")
    scope = v33.validate_intent(intent,index["targets"],index["world_bounds"])
    target = scope["target"]
    capabilities = _load(args.capabilities)
    if not capabilities:
        return _state("CAPABILITY_CHECK", "PROVE_HOST_CAPABILITIES",
                      ["GitHub read/write, Web research, image tool, image materialization and mobile delivery require real host receipts"],
                      intent=intent)
    caps = v33.capability_preflight(capabilities)
    if caps["missing"]:
        return _state("BLOCKED_CAPABILITY", "RESTORE_REQUIRED_HOST_TOOLS",
                      caps["missing"], intent=intent, audit=caps)
    research = _load(args.research_file)
    if research is None:
        return _state("EXTERNAL_RESEARCH", "RESEARCH_REAL_WORLD_ANALOGUES",
                      ["At least two independent real-world domains; record observations, adaptations, dates, and URLs"],
                      intent=intent)
    citations = v33.validate_research(research)
    register = _load(args.decisions_file)
    if register is None:
        return _state("EDITORIAL_DECISIONS", "PROPOSE_AND_ASK_OWNER",
                      ["Propose all new elements from research and canon, then request one decision at a time"],
                      intent=intent, audit=citations)
    decisions = v33.validate_proposals(register,region=target,commit=intent["source_commit"])
    if decisions["pending"]:
        nxt=decisions["pending"][0]
        return _state("EDITORIAL_DECISIONS", "ASK_OWNER_ONE_DECISION",
                      [nxt], intent=intent, audit=decisions, next_id=nxt)
    inventory = _load(args.inventory_file)
    if inventory is None:
        return _state("INSTALLATION_INVENTORY", "RECONCILE_APPROVED_ELEMENTS",
                      ["Record exact installed IDs and identify previously canonical elements"],
                      intent=intent, audit=decisions)
    v33.require(isinstance(inventory,dict) and inventory.get("schema")==
                "NOVYDRES_MAPWORK_V33_INVENTORY_1" and
                inventory.get("region")==target and
                inventory.get("source_commit")==intent["source_commit"],
                "inventory authority mismatch")
    canon_ids=index["targets"][target].get("approved_element_ids",[])
    v33.require(set(inventory.get("canonical_elements",[])).issubset(set(canon_ids)),
                "inventory claims unsupported canonical existing elements")
    installation = v33.validate_inventory(inventory.get("elements",[]),register,
                                         canonical_element_ids=canon_ids)
    if intent["mode"]=="ADD_ELEMENT":
        v33.require(intent.get("element_id") in
                    {e["id"] for e in inventory.get("elements",[])},
                    "ADD_ELEMENT identity absent from permitted inventory")
    zone_path = v32_run.__globals__["resolve_zone"](target)
    if zone_path is None:
        return _state("SPATIAL_MODEL","BUILD_REGION_FROM_APPROVED_CANON",
                      ["No real zone geometry for "+target+"; preserve map, do not infer borders from U02 color"],
                      intent=intent,audit={"research":citations,"proposals":decisions,
                                          "inventory":installation})
    if args.recipe_unit or args.audit_unit:
        zone=core.load(zone_path)
        path=Path(args.spatial) if args.spatial else zone_path.parent/"global-spatial-v31.json"
        if not path.is_file():
            return _state("SPATIAL_MODEL","BUILD_AND_AUDIT_REAL_NETWORK",
                          ["global-spatial-v31.json absent; never generate from synthetic U02 fixtures"],
                          intent=intent)
        plan=core.load(path)
        cfg=core.load(core.CONFIG)
        core.config_check(cfg)
        v33.require(plan.get("zone",{}).get("id")==target and
                    plan.get("fixture_mode") is False,
                    "V3.3 atomic work requires real, matching spatial authority")
        if not args.reference or not Path(args.reference).is_file():
            return _state("REFERENCE_BYTES","MATERIALIZE_ORIGINAL_U02",
                          ["Original U02 PNG missing in local execution context"],
                          intent=intent)
        report=urban.plan_city(plan,cfg,reference_file=args.reference,
                               neighbor_manifests=v32_run.__globals__["load_verified_neighbors"](plan))
        required=("source_and_global_topology","source_bytes_verified",
                  "territory_classification","neighbor_seams",
                  "poi_sites_placed_and_accessible","ground_access_and_clearance")
        v33.require(all(report["gates"][key] for key in required),
                    "V3.3 spatial topology/access audits failed before image jobs")
        uid=args.recipe_unit or args.audit_unit
        unit=next((u for u in report["work_units"] if u["id"]==uid),None)
        v33.require(unit is not None,"requested work unit not in current spatial plan")
        if args.recipe_unit:
            design_root=Path(args.design_root) if args.design_root else zone_path.parent/"urban-design"
            design=design_root/(uid+".json")
            v33.require(design.is_file(),"detailed per-building urban unit file missing")
            expected=content.design_unit(plan,report,uid)
            actual=core.load(design)
            actual.pop("physical_routes",None)
            v33.require(actual==expected,
                        "recipe design differs from deterministic current spatial plan")
            v33.require(expected["access_verified"],
                        "unit building street accessibility audit failed")
            recipe=v33.make_generation_recipe(
                unit=unit,intent=intent,design_path=design,
                reference_path=args.reference,proposal_register=register,
                neighbor_digests={seam["id"]:report["transport_sha256"]
                                  for seam in plan["neighbor_seams"]},
                style={"projection":"TOP_DOWN_90",
                       "lighting":cfg["projection"]["lighting"],
                       "scale":cfg["detail_pixels_per_unit"],
                       "preserve_outside_mask":True})
            if not args.out:
                return _state("IMAGE_RECIPE","SPECIFY_LOCAL_RECIPE_DESTINATION",
                              ["--out required for versioned recipe write"],intent=intent)
            location=Path(args.out)/"recipes"/(uid+".json")
            core.save(location,recipe)
            return _state("IMAGE_RECIPE","GENERATE_WITH_CHATGPT_NATIVE_IMAGE",
                          ["Recipe saved. Generate image externally and materialize actual bytes before audit."],
                          intent=intent,audit={"recipe":str(location),
                                               "recipe_sha256":v33.digest(location)})
        receipt=core.load(args.unit_receipt) if args.unit_receipt and Path(args.unit_receipt).is_file() else None
        if not receipt:
            return _state("IMAGE_MATERIALIZATION","FETCH_NATIVE_IMAGE_BYTES",
                          ["Missing on-disk native image receipt for "+uid],intent=intent)
        if not args.unit_mask:
            return _state("IMAGE_AUDIT","MATERIALIZE_UNIT_MASK",
                          ["Image mask file absent for "+uid],intent=intent)
        audited=v33.audit_atomic_image(receipt,args.unit_mask,plan,report,uid,cfg)
        reviewed=core.load(args.visual_review) if args.visual_review and Path(args.visual_review).is_file() else None
        if not reviewed:
            return _state("IMAGE_VISUAL_REVIEW","AGENT_INSPECT_IMAGE",
                          ["Record lighting, geometry, roof, seams and visual continuity; technical audit is not aesthetic certification"],
                          intent=intent,audit=audited)
        v33.require(reviewed.get("by")=="AGENT","visual audit must be performed by the agent")
        if args.ledger:
            ledger=core.load(args.ledger) if Path(args.ledger).is_file() else {
                "schema":"NOVYDRES_MAPWORK_V33_UNIT_LEDGER_1","units":{}}
            if args.start_unit:
                v33.unit_transition(ledger,uid,event="START",input_sha256=
                                    v33.evidence_digest({"recipe":uid,"plan":report["transport_sha256"],
                                                         "reference":v33.digest(args.reference)}))
            input_hash=ledger.get("units",{}).get(uid,{}).get("input_sha256")
            v33.require(bool(input_hash),"unit ledger has no active attempt; start with --start-unit")
            record=v33.unit_transition(
                ledger,uid,event="AUDIT_PASS" if reviewed.get("status")=="PASS" else "AUDIT_FAIL",
                input_sha256=input_hash,receipt=audited if reviewed.get("status")=="PASS"
                else {"failure":reviewed.get("reason","visual audit failed")},
                visual_review=reviewed)
            core.save(args.ledger,ledger)
            return _state("IMAGE_AUDITED",
                          "NEXT_WORK_UNIT" if record["status"]=="VERIFIED" else "CORRECT_AND_RETEST",
                          [] if record["status"]=="VERIFIED" else [record["status"]],
                          intent=intent,audit=record)
        return _state("IMAGE_AUDITED",
                      "PERSIST_VERIFIED_UNIT_LEDGER" if reviewed.get("status")=="PASS"
                      else "CORRECT_AND_RETEST",
                      [] if reviewed.get("status")=="PASS" else ["visual inspection failed"],
                      intent=intent,audit={"technical":audited,"visual":reviewed})
    # Existing topology and renderer are reused, not forked. The old
    # SKETCH_APPROVED bit is NOT treated as owner approval of V3.3 art.
    args.v33_verified=True
    args.district=target
    args.zone=None
    result=v32_run(args)
    result["schema"]="NOVYDRES_MAPWORK_V33_PIPELINE_CHECKPOINT_1"
    result["intent_sha256"]=v33.evidence_digest(intent)
    result["research_sources"]=citations
    result["editorial_decisions"]=decisions
    result["installation_inventory"]=installation
    result["v33_authorization_verified"]=True
    result["publication_authorized"]=False
    result["canonical_state_changed"]=False
    return result

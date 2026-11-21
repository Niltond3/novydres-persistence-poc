#!/usr/bin/env python3
""" agent orchestration layer of the SINGLE scripts/pipeline.py entrypoint.

This is a pure library. The host agent must genuinely perform web browsing,
editorial dialogue, GitHub readback and native image generation and write
receipts. Missing capabilities are blockers, never simulated work.
"""
from __future__ import annotations

from pathlib import Path

import mapwork as core
import urban_architecture as urban
import urban_content as content
import contracts as contract
import visual
import acceptance as acceptance
import orchestration as controller

ROOT=Path(__file__).resolve().parents[1]
CANON_CATALOG=ROOT.parents[3]/"catalogo.json"


def _load(path):
    return core.load(path) if path and Path(path).is_file() else None


def _state(phase, action, blockers, *, intent=None, audit=None, next_id=None):
    return {
        "schema":"NOVYDRES_MAPWORK_PIPELINE_CHECKPOINT_1",
        "phase":phase,
        "next_action":action,
        "blockers":list(blockers),
        "target":intent["target"]["id"] if intent else None,
        "mode":intent["mode"] if intent else None,
        "request_sha256":contract.evidence_digest(intent) if intent else None,
        "audit":audit,
        "next_decision_id":next_id,
        "publication_authorized":False,
        "canonical_state_changed":False
    }


def run(args, core_run):
    if not getattr(args, "intent", None):
        return _state("INTENT", "AGENT_RESOLVE_AND_RECORD_INTENT",
                      ["Provide --intent JSON produced by semantic agent; scripts never guess place names"])
    intent = _load(args.intent)
    if intent is None:
        return _state("INTENT", "MATERIALIZE_INTENT",
                      ["Intent file absent; host agent must write and read it back"])
    index = _load(args.scope_index or ROOT/"scope-index.json")
    contract.require(isinstance(index,dict) and
                index.get("schema")=="NOVYDRES_MAPWORK_SCOPE_INDEX_1",
                "canonical scope index missing")
    contract.require(index.get("source_commit")==intent.get("source_commit"),
                "canonical scope index and intent commit differ; rebootstrap master")
    if CANON_CATALOG.is_file():
        canonical_ids={s["id"] for s in core.load(CANON_CATALOG)["subjects"]}
        contract.require(all(v["subject_id"] in canonical_ids
                        for v in index["targets"].values()),
                    "scope index contains a noncanonical subject ID")
    scope = contract.validate_intent(intent,index["targets"],index["world_bounds"])
    target = scope["target"]
    capabilities = _load(args.capabilities)
    if not capabilities:
        return _state("CAPABILITY_CHECK", "PROVE_HOST_CAPABILITIES",
                      ["GitHub read/write, research and user delivery require receipts; native PNGs are verified when generated"],
                      intent=intent)
    caps = contract.capability_preflight(capabilities,require_native=False)
    if caps["missing"]:
        return _state("BLOCKED_CAPABILITY", "RESTORE_REQUIRED_HOST_TOOLS",
                      caps["missing"], intent=intent, audit=caps)
    research = _load(args.research_file)
    if research is None:
        return _state("EXTERNAL_RESEARCH", "RESEARCH_REAL_WORLD_ANALOGUES",
                      ["At least two independent real-world domains; record observations, adaptations, dates, and URLs"],
                      intent=intent)
    citations = contract.validate_research(research)
    register = _load(args.decisions_file)
    if register is None:
        return _state("EDITORIAL_DECISIONS", "PROPOSE_AND_ASK_OWNER",
                      ["Propose all new elements from research and canon, then request one decision at a time"],
                      intent=intent, audit=citations)
    decisions = contract.validate_proposals(register,region=target,commit=intent["source_commit"])
    if decisions["pending"]:
        nxt=decisions["pending"][0]
        return _state("EDITORIAL_DECISIONS", "ASK_OWNER_ONE_DECISION",
                      [nxt], intent=intent, audit=decisions, next_id=nxt)
    inventory = _load(args.inventory_file)
    if inventory is None:
        return _state("INSTALLATION_INVENTORY", "RECONCILE_APPROVED_ELEMENTS",
                      ["Record exact installed IDs and identify previously canonical elements"],
                      intent=intent, audit=decisions)
    contract.require(isinstance(inventory,dict) and inventory.get("schema")==
                "NOVYDRES_MAPWORK_INVENTORY_1" and
                inventory.get("region")==target and
                inventory.get("source_commit")==intent["source_commit"],
                "inventory authority mismatch")
    canon_ids=index["targets"][target].get("approved_element_ids",[])
    contract.require(set(inventory.get("canonical_elements",[])).issubset(set(canon_ids)),
                "inventory claims unsupported canonical existing elements")
    installation = contract.validate_inventory(inventory.get("elements",[]),register,
                                         canonical_element_ids=canon_ids)
    if intent["mode"]=="ADD_ELEMENT":
        contract.require(intent.get("element_id") in
                    {e["id"] for e in inventory.get("elements",[])},
                    "ADD_ELEMENT identity absent from permitted inventory")
    zone_path = core_run.__globals__["resolve_zone"](target)
    if zone_path is None:
        return _state("SPATIAL_MODEL","BUILD_REGION_FROM_APPROVED_CANON",
                      ["No real zone geometry for "+target+"; preserve map, do not infer borders from U02 color"],
                      intent=intent,audit={"research":citations,"proposals":decisions,
                                          "inventory":installation})
    # Infrastructure acceptance is a mandatory  pre-lot gate.
    # Even a syntactically valid  spatial JSON cannot bypass actual
    # model-inspected U02 candidate rounds for roads, grade, rail, tram,
    # metro, network integration and exclusive territory.
    config=core.load(core.CONFIG)
    core.config_check(config)
    ledger_path=getattr(args,"acceptance_ledger",None) or (
        zone_path.parent/"acceptance-ledger.json")
    registered_attempt = None
    if getattr(args, "record_attempt", None):
        pre_gate=acceptance.evaluate(
            ledger_path, reference_file=getattr(args,"reference",None),
            reference_sha256=config["reference"]["sha256"],
            reference_size=[config["reference"]["width"],config["reference"]["height"]],
            require_urban=True, require_remote=True)
        if pre_gate["next_action"] in (
            "REPAIR_ACCEPTANCE_LEDGER", "INVALIDATE_AND_REAUDIT_STALE_EVIDENCE",
            "FIX_ACCEPTANCE_CONTRACT", "RESTORE_REFERENCE_AUTHORITY",
            "MATERIALIZE_ORIGINAL_REFERENCE", "RESTORE_ORIGINAL_REFERENCE"):
            return _state("INFRASTRUCTURE_ACCEPTANCE", pre_gate["next_action"],
                          pre_gate["blockers"],intent=intent,audit=pre_gate)
        spec = acceptance.criteria_contract()
        registered_attempt = controller.record_attempt(
            ledger_path, args.record_attempt, criteria_sha256=spec["sha256"],
            reference_sha256=config["reference"]["sha256"],
            schema=acceptance.SCHEMA, allowed_stages=acceptance.STAGES,
            active_stage=pre_gate["stage"])
    acceptance_gate=acceptance.evaluate(
        ledger_path,
        reference_file=getattr(args,"reference",None),
        reference_sha256=config["reference"]["sha256"],
        reference_size=[config["reference"]["width"],config["reference"]["height"]],
        require_remote=True,
        require_urban=bool(
            getattr(args,"record_attempt",None) or
            getattr(args,"recipe_unit",None) or
            getattr(args,"audit_unit",None) or
            getattr(args,"execute",False)))
    if acceptance_gate["status"] != "PASS":
        return _state(
            "INFRASTRUCTURE_ACCEPTANCE",acceptance_gate["next_action"],
            acceptance_gate["blockers"],intent=intent,
            audit={**acceptance_gate, "recorded_attempt": registered_attempt})

    if args.recipe_unit or args.audit_unit:
        zone=core.load(zone_path)
        path=Path(args.spatial) if args.spatial else zone_path.parent/"global-spatial.json"
        if not path.is_file():
            return _state("SPATIAL_MODEL","BUILD_AND_AUDIT_REAL_NETWORK",
                          ["global-spatial.json absent; never generate from synthetic U02 fixtures"],
                          intent=intent)
        plan=core.load(path)
        cfg=core.load(core.CONFIG)
        core.config_check(cfg)
        contract.require(plan.get("zone",{}).get("id")==target and
                    plan.get("fixture_mode") is False,
                    " atomic work requires real, matching spatial authority")
        if not args.reference or not Path(args.reference).is_file():
            return _state("REFERENCE_BYTES","MATERIALIZE_ORIGINAL_U02",
                          ["Original U02 PNG missing in local execution context"],
                          intent=intent)
        report=urban.plan_city(plan,cfg,reference_file=args.reference,
                               neighbor_manifests=core_run.__globals__["load_verified_neighbors"](plan))
        required=("source_and_global_topology","source_bytes_verified",
                  "territory_classification","neighbor_seams",
                  "pixel_masks_verified","poi_sites_placed_and_accessible",
                  "ground_access_and_clearance")
        contract.require(all(report["gates"][key] for key in required),
                    " spatial topology/access audits failed before image jobs")
        uid=args.recipe_unit or args.audit_unit
        unit=next((u for u in report["work_units"] if u["id"]==uid),None)
        contract.require(unit is not None,"requested work unit not in current spatial plan")
        if args.recipe_unit:
            design_root=Path(args.design_root) if args.design_root else zone_path.parent/"urban-design"
            design=design_root/(uid+".json")
            contract.require(design.is_file(),"detailed per-building urban unit file missing")
            expected=content.design_unit(plan,report,uid)
            actual=core.load(design)
            actual.pop("physical_routes",None)
            contract.require(actual==expected,
                        "recipe design differs from deterministic current spatial plan")
            contract.require(expected["access_verified"],
                        "unit building street accessibility audit failed")
            if not args.out:
                return _state("IMAGE_RECIPE","SPECIFY_LOCAL_RECIPE_DESTINATION",
                              ["--out required for recipe write"],intent=intent)
            owner_edit=None
            if intent["mode"]!="CREATE_REGION":
                if not args.editable_mask or not Path(args.editable_mask).is_file():
                    return _state("EDIT_MASK","MATERIALIZE_OWNER_APPROVED_EDIT_MASK",
                                  ["Owner edit mask required before preparing this refinement recipe"],
                                  intent=intent)
                from PIL import Image
                with Image.open(args.editable_mask) as im:
                    owner_edit=im.convert("L")
                contract.validate_edit_mask(owner_edit,intent["intervention"]["bounds"],
                                       urban.spatial_protection_mask(plan))
            mask=contract.plan_unit_mask(plan,report,uid,cfg,owner_edit_mask=owner_edit)
            if mask.getbbox() is None:
                return _state("IMAGE_RECIPE","SKIP_UNIT_OUTSIDE_EDIT_SCOPE",
                              [uid+" is unchanged; do not create a native image for it"],
                              intent=intent)
            mask_path=Path(args.out)/"masks"/(uid+".png")
            mask_path.parent.mkdir(parents=True,exist_ok=True)
            mask.save(mask_path)
            recipe=contract.make_generation_recipe(
                unit=unit,intent=intent,design_path=design,
                reference_path=args.reference,mask_file=mask_path,
                proposal_register=register,
                neighbor_digests={seam["id"]:report["transport_sha256"]
                                  for seam in plan["neighbor_seams"]},
                style={"projection":"TOP_DOWN_90",
                       "lighting":cfg["projection"]["lighting"],
                       "scale":cfg["detail_pixels_per_unit"],
                       "preserve_outside_mask":True})
            location=Path(args.out)/"recipes"/(uid+".json")
            core.save(location,recipe)
            return _state("IMAGE_RECIPE","GENERATE_WITH_CHATGPT_NATIVE_IMAGE",
                          ["Recipe saved. Generate image externally and materialize actual bytes before audit."],
                          intent=intent,audit={"recipe":str(location),
                                               "recipe_sha256":contract.digest(location),
                                               "mask_file":str(mask_path),
                                               "mask_sha256":contract.digest(mask_path)})
        receipt=core.load(args.unit_receipt) if args.unit_receipt and Path(args.unit_receipt).is_file() else None
        if not receipt:
            return _state("IMAGE_MATERIALIZATION","FETCH_NATIVE_IMAGE_BYTES",
                          ["Missing on-disk native image receipt for "+uid],intent=intent)
        if not args.unit_mask:
            return _state("IMAGE_AUDIT","MATERIALIZE_UNIT_MASK",
                          ["Image mask file absent for "+uid],intent=intent)
        audited=contract.audit_atomic_image(receipt,args.unit_mask,plan,report,uid,cfg)
        reviewed=core.load(args.visual_review) if args.visual_review and Path(args.visual_review).is_file() else None
        if not reviewed:
            return _state("IMAGE_VISUAL_REVIEW","AGENT_INSPECT_IMAGE",
                          ["Record lighting, geometry, roof, seams and visual continuity; technical audit is not aesthetic certification"],
                          intent=intent,audit=audited)
        if reviewed.get("status")=="PASS":
            peers=visual.neighbor_sides(report["work_units"],uid)
            batch=_load(args.image_receipts)
            receipts={r["work_unit_id"]:r for r in batch.get("images",[])} if batch else {}
            if batch:
                receipts.update({r["work_unit_id"]:r for r in batch.get("context_images",[])})
            if not set(peers).issubset(receipts):
                return _state("IMAGE_VISUAL_REVIEW","MATERIALIZE_NEIGHBOR_IMAGES_AND_INSPECT",
                              sorted(set(peers)-set(receipts)),intent=intent,audit=audited)
            visual.validate_unit_visual_review(
                reviewed,unit_id=uid,image_sha256=audited["image_sha256"],
                mask_sha256=audited["mask_sha256"],
                reference_sha256=contract.digest(args.reference),
                spatial_sha256=contract.digest(path),
                work_units=report["work_units"],neighbor_receipts=receipts)
        else:
            contract.require(reviewed.get("by")=="AGENT" and
                        reviewed.get("status")=="FAIL",
                        "failed visual review must be recorded by the agent")
        if args.ledger:
            ledger=core.load(args.ledger) if Path(args.ledger).is_file() else {
                "schema":"NOVYDRES_MAPWORK_UNIT_LEDGER_1","units":{}}
            plan_file=Path(args.design_root) if args.design_root else zone_path.parent/"urban-design"
            design_file=plan_file/(uid+".json")
            contract.require(design_file.is_file(),"unit ledger cannot omit detailed spatial design")
            fingerprints={
                "intent_sha256":contract.digest(args.intent),
                "scope_index_sha256":contract.digest(args.scope_index or ROOT/"scope-index.json"),
                "spatial_sha256":contract.digest(path),
                "design_sha256":contract.digest(design_file),
                "reference_sha256":contract.digest(args.reference),
                "decisions_sha256":contract.digest(args.decisions_file),
                "research_sha256":contract.digest(args.research_file),
                "inventory_sha256":contract.digest(args.inventory_file),
                "unit_mask_sha256":contract.digest(args.unit_mask),
                "work_unit_id":uid
            }
            input_hash=contract.evidence_digest(fingerprints)
            if args.start_unit:
                contract.unit_transition(ledger,uid,event="START",input_sha256=input_hash)
            contract.require(uid in ledger.get("units",{}),
                        "unit ledger has no active attempt; start with --start-unit")
            record=contract.unit_transition(
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
    # SKETCH_APPROVED bit is NOT treated as owner approval of  art.
    args.preflight_verified=True
    args.district=target
    args.zone=None
    result=core_run(args)
    result["schema"]="NOVYDRES_MAPWORK_PIPELINE_CHECKPOINT_1"
    result["intent_sha256"]=contract.evidence_digest(intent)
    result["research_sources"]=citations
    result["editorial_decisions"]=decisions
    result["installation_inventory"]=installation
    result["authorization_verified"]=True
    result["publication_authorized"]=False
    result["canonical_state_changed"]=False
    return result

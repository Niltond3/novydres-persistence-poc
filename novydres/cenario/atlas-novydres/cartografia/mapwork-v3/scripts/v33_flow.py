#!/usr/bin/env python3
"""V3.3 agent orchestration layer of the SINGLE scripts/pipeline.py entrypoint.

This is a pure library. The host agent must genuinely perform web browsing,
editorial dialogue, GitHub readback and native image generation and write
versioned receipts. Missing capabilities are blockers, never simulated work.
"""
from __future__ import annotations

from pathlib import Path

import mapwork as core
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
    installation = v33.validate_inventory(inventory.get("elements",[]),register,
                                         canonical_element_ids=inventory.get("canonical_elements",[]))
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
    # Existing topology and renderer are reused, not forked. The old
    # SKETCH_APPROVED bit is NOT treated as owner approval of V3.3 art.
    args.v33_verified=True
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

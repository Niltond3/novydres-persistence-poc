#!/usr/bin/env python3
"""D10 proposal validator. It validates documentary structure only; never writes narrative state."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator


BASE = Path(__file__).resolve().parent
REGISTRY_PATH = BASE / "D10_SCHEMA_REGISTRY_V001.json"
ROLE_ADAPTERS_PATH = BASE / "D10_ROLE_ADAPTERS_V001.json"
ENVELOPE_SCHEMA_PATH = BASE / "D10_PHASE_ENVELOPE_SCHEMA_V001.json"
TEST_CATALOG_PATH = BASE / "D10_ADVERSARIAL_TESTS_V001.json"
CONTRACT_PATH = BASE / "D01_CONTRACTS_V001.json"
EXPECTED_CONTRACT_BLOB = "22aa8bf6aa48156e9796bae42c912c630f70a736"
EXPECTED_BRANCH = "design/chr001-narrative-program-d01"
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
_TEST_SOURCE_ROOT: Path | None = None
_TEST_SOURCE_HEAD: str | None = None


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def git_output(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def load_registry() -> tuple[dict[str, Any], dict[str, Any]]:
    registry = load_json(REGISTRY_PATH)
    contract = load_json(CONTRACT_PATH)
    raw = CONTRACT_PATH.read_bytes()
    if git_blob_sha1(raw) != EXPECTED_CONTRACT_BLOB:
        raise ValueError("Frozen D01 contract bytes do not match the pinned Git blob.")
    if registry.get("source", {}).get("blob_sha") != EXPECTED_CONTRACT_BLOB:
        raise ValueError("D10 registry source pin does not match frozen D01.")
    if registry.get("source_schema") != contract:
        raise ValueError("D10 registry copy differs from the frozen D01 contract.")
    if contract.get("schema_status") != "PROPOSED_NON_OPERATIONAL":
        raise ValueError("D01 authority status changed; stop and reconcile before D10.")
    return registry, contract


def schema_for(contract: dict[str, Any], type_name: str) -> dict[str, Any]:
    if type_name not in contract.get("$defs", {}):
        raise ValueError(f"Unknown D01 schema type: {type_name}")
    return {
        "$schema": contract["$schema"],
        "$defs": contract["$defs"],
        "$ref": f"#/$defs/{type_name}",
    }


def schema_errors(data: Any, type_name: str, contract: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema_for(contract, type_name))
    return [e.message for e in validator.iter_errors(data)]


def _sample(schema: dict[str, Any], contract: dict[str, Any], depth: int = 0) -> Any:
    if depth > 40:
        raise ValueError("Schema fixture generation exceeded recursion limit.")
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/$defs/"):
            raise ValueError(f"Unsupported fixture $ref: {ref}")
        return _sample(contract["$defs"][ref.rsplit("/", 1)[1]], contract, depth + 1)
    if "const" in schema:
        return copy.deepcopy(schema["const"])
    if "enum" in schema:
        return copy.deepcopy(schema["enum"][0])
    for keyword in ("anyOf", "oneOf"):
        if keyword in schema:
            last_error = None
            for option in schema[keyword]:
                try:
                    candidate = _sample(option, contract, depth + 1)
                    if not list(Draft202012Validator(schema_for_fragment(option, contract)).iter_errors(candidate)):
                        return candidate
                except (KeyError, ValueError) as exc:
                    last_error = exc
            if last_error:
                raise last_error
    if "allOf" in schema:
        merged: dict[str, Any] = {}
        for option in schema["allOf"]:
            value = _sample(option, contract, depth + 1)
            if isinstance(value, dict):
                merged.update(value)
        return merged

    types = schema.get("type")
    if isinstance(types, list):
        types = next((t for t in types if t != "null"), types[0])
    if types == "object":
        result = {}
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            result[key] = _sample(properties.get(key, {}), contract, depth + 1)
        return result
    if types == "array":
        count = schema.get("minItems", 0)
        return [_sample(schema.get("items", {}), contract, depth + 1) for _ in range(count)]
    if types == "string":
        pattern = schema.get("pattern", "")
        if pattern == "^[0-9a-f]{40}$":
            return "a" * 40
        if "format" in schema and schema["format"] == "date-time":
            return "2026-11-09T00:00:00Z"
        return "x" * max(1, schema.get("minLength", 0))
    if types == "integer":
        return max(0, schema.get("minimum", 0))
    if types == "number":
        return max(0, schema.get("minimum", 0))
    if types == "boolean":
        return False
    if types == "null":
        return None
    if not schema:
        return None
    raise ValueError(f"Cannot build fixture from schema fragment: {schema}")


def schema_for_fragment(schema: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    if "$ref" in schema:
        return {"$schema": contract["$schema"], "$defs": contract["$defs"], "$ref": schema["$ref"]}
    return schema


def source(verification: str = "VERIFIED") -> dict[str, str]:
    return {
        "path": "test/fixture.json",
        "blob_sha": git_blob_sha1(b"NOVYDRES D10 synthetic source fixture\n"),
        "anchor": "synthetic D10 validation fixture",
        "verification": verification,
    }


def write_test_source(root: Path, relative_path: str, content: bytes) -> dict[str, str]:
    target = root / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    return {
        "path": relative_path,
        "blob_sha": git_blob_sha1(content),
        "anchor": "D10 synthetic authorization fixture",
        "verification": "VERIFIED",
    }


def verify_source_ref(
    ref: Any,
    source_root: Path | None,
    source_head: str | None,
    expected_source_head: str | None,
    require_verified: bool = False,
) -> tuple[list[str], bytes | None]:
    errors: list[str] = []
    if not isinstance(ref, dict):
        return ["source evidence must be an object"], None
    if source_root is None:
        return ["source root is required to verify evidence bytes"], None
    if not isinstance(source_head, str) or not SHA1_RE.fullmatch(source_head):
        return ["bundle must declare a verified Git source_head"], None
    if not isinstance(expected_source_head, str) or not SHA1_RE.fullmatch(expected_source_head):
        return ["an independently supplied expected source HEAD is required"], None
    if source_head != expected_source_head:
        return ["bundle source_head differs from the independently expected HEAD"], None
    relative = ref.get("path")
    if not isinstance(relative, str) or not relative or "\\" in relative:
        return ["source path must be a non-empty repository-relative POSIX path"], None
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        return ["source path escapes the verified repository root"], None
    root = source_root.resolve()
    try:
        resolved = (root / path).resolve(strict=True)
        if not resolved.is_relative_to(root):
            return ["source path escapes the verified repository root"], None
        raw = resolved.read_bytes()
        actual_head = git_output(root, "rev-parse", "HEAD")
        if actual_head != expected_source_head:
            return ["repository HEAD differs from the independently expected source HEAD"], None
        git_path = relative.replace("\\", "/")
        tracked_blob = git_output(root, "rev-parse", f"{expected_source_head}:{git_path}")
    except (OSError, RuntimeError):
        return [f"source path cannot be read from verified repository: {relative}"], None
    except subprocess.CalledProcessError:
        return [f"source path is not tracked at the expected Git HEAD: {relative}"], None
    expected = ref.get("blob_sha")
    actual = git_blob_sha1(raw)
    if not isinstance(expected, str) or not SHA1_RE.fullmatch(expected) or actual != expected:
        errors.append(f"source blob SHA does not match repository bytes: {relative}")
    if tracked_blob != expected:
        errors.append(f"source blob SHA does not match the expected Git HEAD tree: {relative}")
    if require_verified and ref.get("verification") != "VERIFIED":
        errors.append(f"source is not declared VERIFIED: {relative}")
    return errors, raw


def provenance() -> dict[str, Any]:
    return {
        "record_kind": "CANON_EVENT",
        "original_author": "NARRATOR",
        "fact_status": "CONFIRMED",
        "source_refs": [source()],
        "as_of_event_id": "E1",
    }


def actor(actor_id: str, knowledge_refs: list[str] | None = None, relationship_refs: list[str] | None = None) -> dict[str, Any]:
    return {
        "actor_id": actor_id,
        "actor_kind": "NPC",
        "as_of_event_id": "E1",
        "goals": [],
        "fears": [],
        "limits": [],
        "capabilities": [],
        "knowledge_refs": knowledge_refs or [],
        "relationship_refs": relationship_refs or [],
        "provenance": provenance(),
    }


def knowledge() -> dict[str, Any]:
    return {
        "knowledge_id": "K1",
        "knower_id": "A",
        "fact_ref": "F1",
        "as_of_event_id": "E1",
        "acquisition_ref": "ACQ1",
        "epistemic_status": "KNOWN",
        "provenance": provenance(),
    }


def relationship() -> dict[str, Any]:
    return {
        "edge_id": "R1",
        "from_id": "A",
        "to_id": "B",
        "relation_kind": "trust",
        "as_of_event_id": "E1",
        "epistemic_status": "CONFIRMED",
        "evidence_refs": [source()],
        "provenance": provenance(),
    }


def plot(plot_id: str = "P1", status: str = "ACTIVE") -> dict[str, Any]:
    return {
        "plot_id": plot_id,
        "scope": "MINOR",
        "status": status,
        "origin_event_refs": ["E1"],
        "dramatic_question": "Can the conflict be understood?",
        "why_matters": "The answer has a cost.",
        "pc_hook_noncoercive": "The character may decline involvement.",
        "actors": ["A"],
        "opposition": ["B"],
        "independent_pressure": "A deadline advances independently.",
        "clue_refs": [],
        "clock_refs": [],
        "outcomes": [],
        "closure_test": "Record outcome evidence and consequences.",
        "terminal_evidence_refs": ["EV1"] if status in {"RESOLVED", "FAILED", "ABANDONED_WITH_CONSEQUENCES", "RESOLVED_OFFSCREEN_WITH_EVIDENCE", "SUPERSEDED_WITH_PROVENANCE"} else [],
        "plot_links": [],
        "spoiler_class": "PLAYER_SAFE",
        "provenance": provenance(),
    }


def clue(critical: bool = True, routes: list[dict[str, str]] | None = None, lock: str = "LOCKED", lock_ref: str | None = "TL1") -> dict[str, Any]:
    if routes is None:
        routes = [
            {"route_id": "R1", "independent_mechanism": "witness testimony", "access_condition": "witness is contacted"},
            {"route_id": "R2", "independent_mechanism": "physical record", "access_condition": "record is inspected"},
        ]
    return {
        "clue_id": "C1",
        "fact_ref": "F1",
        "critical": critical,
        "discovery_routes": routes,
        "truth_lock_status": lock,
        "truth_lock_ref": lock_ref,
        "provenance": provenance(),
    }


def base_bundle(artifacts: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {
        "authority": "EDITORIAL_ONLY",
        "schema_status": "PROPOSED_NON_OPERATIONAL",
        "narrative_mutation": False,
        "mechanical_changes": [],
        "event_ids": ["E1"],
        "source_head": _TEST_SOURCE_HEAD,
        "acquisition_records": [],
        "decision_records": [],
        "evidence_records": [{"evidence_id": "EV1", "source": source()}],
        "player_decision_ids": [],
        "effective_gm_hidden_segregation": False,
        "artifacts": artifacts or [],
    }


def artifact(type_name: str, data: dict[str, Any], spoiler_class: str = "PLAYER_SAFE") -> dict[str, Any]:
    return {"type": type_name, "spoiler_class": spoiler_class, "data": data}


def _nested_spoiler_classes(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        classification = value.get("spoiler_class")
        if classification is not None:
            found.append(classification)
        for child in value.values():
            found.extend(_nested_spoiler_classes(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_nested_spoiler_classes(child))
    return found


def _nested_source_refs(value: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if {"path", "blob_sha", "anchor", "verification"}.issubset(value):
            found.append(value)
        else:
            for child in value.values():
                found.extend(_nested_source_refs(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_nested_source_refs(child))
    return found


def validate_bundle(
    bundle: dict[str, Any],
    contract: dict[str, Any],
    source_root: Path | None = None,
    expected_source_head: str | None = None,
) -> list[str]:
    source_root = source_root or _TEST_SOURCE_ROOT
    expected_source_head = expected_source_head or _TEST_SOURCE_HEAD
    errors: list[str] = []
    if bundle.get("authority") != "EDITORIAL_ONLY":
        errors.append("bundle authority must remain EDITORIAL_ONLY")
    if bundle.get("schema_status") != "PROPOSED_NON_OPERATIONAL":
        errors.append("D01 remains PROPOSED_NON_OPERATIONAL")
    if bundle.get("narrative_mutation") is not False:
        errors.append("narrative mutation is forbidden by D10")
    if bundle.get("mechanical_changes"):
        errors.append("D10 cannot grant or persist mechanical changes")

    known_events = set(bundle.get("event_ids", []))
    if len(bundle.get("event_ids", [])) != len(known_events):
        errors.append("event_ids must be unique and ordered as the authoritative checkpoint")
    source_head = bundle.get("source_head")
    if expected_source_head is None:
        errors.append("independently supplied expected source HEAD is required")
    elif source_head != expected_source_head:
        errors.append("bundle source_head differs from the independently expected HEAD")
    if source_root is not None:
        try:
            if git_output(source_root.resolve(), "rev-parse", "HEAD") != expected_source_head:
                errors.append("repository HEAD differs from the independently expected source HEAD")
        except (OSError, subprocess.CalledProcessError):
            errors.append("source root is not a readable Git repository")

    acquisition_records: dict[str, dict[str, Any]] = {}
    for position, record in enumerate(bundle.get("acquisition_records", [])):
        if not isinstance(record, dict):
            errors.append(f"acquisition_records[{position}] must be an object")
            continue
        required = ("acquisition_id", "knower_id", "event_id", "method", "evidence_id")
        if any(not isinstance(record.get(key), str) or not record.get(key) for key in required) or not isinstance(record.get("source"), dict):
            errors.append(f"acquisition_records[{position}] requires source-backed acquisition id, knower, event, method and evidence")
            continue
        source_errors, _ = verify_source_ref(record.get("source"), source_root, source_head, expected_source_head, require_verified=True)
        errors.extend(f"acquisition {record['acquisition_id']}: {message}" for message in source_errors)
        if record["acquisition_id"] in acquisition_records:
            errors.append(f"duplicate acquisition record id: {record['acquisition_id']}")
        acquisition_records[record["acquisition_id"]] = record

    decision_records: dict[str, dict[str, Any]] = {}
    for position, record in enumerate(bundle.get("decision_records", [])):
        if not isinstance(record, dict):
            errors.append(f"decision_records[{position}] must be an object")
            continue
        required = ("decision_id", "decision_maker", "decision_kind", "scope", "affected_refs", "event_id", "evidence_id", "source")
        if (any(key not in record for key in required) or record.get("decision_maker") != "PLAYER"
            or not isinstance(record.get("affected_refs"), list) or not record.get("affected_refs")
            or not isinstance(record.get("event_id"), str) or not record.get("event_id")
            or not isinstance(record.get("evidence_id"), str) or not record.get("evidence_id")
            or not isinstance(record.get("decision_kind"), str) or not record.get("decision_kind")
            or not isinstance(record.get("scope"), str) or not record.get("scope")):
            errors.append(f"decision_records[{position}] lacks explicit player decision scope and provenance")
            continue
        if not isinstance(record.get("decision_id"), str) or not record["decision_id"]:
            errors.append(f"decision_records[{position}] requires a decision_id")
            continue
        source_errors, _ = verify_source_ref(record.get("source"), source_root, source_head, expected_source_head, require_verified=True)
        errors.extend(f"decision {record['decision_id']}: {message}" for message in source_errors)
        if record["decision_id"] in decision_records:
            errors.append(f"duplicate player decision record id: {record['decision_id']}")
        decision_records[record["decision_id"]] = record
    evidence_ids: set[str] = set()
    evidence_records = bundle.get("evidence_records", [])
    for position, record in enumerate(evidence_records):
        if not isinstance(record, dict) or not isinstance(record.get("evidence_id"), str) or not record.get("evidence_id"):
            errors.append(f"evidence_records[{position}] requires a non-empty evidence_id")
            continue
        evidence_id = record["evidence_id"]
        if evidence_id in evidence_ids:
            errors.append(f"duplicate evidence record id: {evidence_id}")
        source_errors, _ = verify_source_ref(record.get("source"), source_root, source_head, expected_source_head, require_verified=True)
        errors.extend(f"evidence {evidence_id}: {message}" for message in source_errors)
        if not source_errors:
            evidence_ids.add(evidence_id)
    for ident, record in acquisition_records.items():
        actor_ids = {item.get("data", {}).get("actor_id") for item in bundle.get("artifacts", []) if isinstance(item, dict) and item.get("type") == "actor" and isinstance(item.get("data"), dict)}
        if record.get("knower_id") not in actor_ids:
            errors.append(f"acquisition {ident} has no matching actor record")
        if record.get("event_id") not in known_events:
            errors.append(f"acquisition {ident} event is outside the supplied checkpoint")
        if record.get("evidence_id") not in evidence_ids:
            errors.append(f"acquisition {ident} lacks verified evidence")
        if record.get("method") not in {"OBSERVED", "HEARD", "READ", "TOLD", "INFERRED", "SHARED", "OTHER"}:
            errors.append(f"acquisition {ident} method is not recognized")
    for ident, record in decision_records.items():
        if record.get("event_id") not in known_events or record.get("evidence_id") not in evidence_ids:
            errors.append(f"player decision {ident} lacks verified checkpoint or evidence")
    artifacts = bundle.get("artifacts", [])
    indexes: dict[str, dict[str, dict[str, Any]]] = {}
    id_fields = {
        "chronicle": "chronicle_id", "marco": "marco_id", "history_episode": "history_episode_id",
        "plot": "plot_id", "story": "story_id", "scene": "scene_id", "beat": "beat_id",
        "thread": "thread_id", "actor": "actor_id", "relationship": "edge_id", "clue": "clue_id",
        "clock": "clock_id", "knowledge": "knowledge_id", "ledger": "ledger_id", "retcon": "change_id",
    }
    for position, item in enumerate(artifacts):
        if not isinstance(item, dict) or not isinstance(item.get("data"), dict):
            errors.append(f"artifact[{position}] must contain typed object data")
            continue
        type_name = item.get("type")
        if type_name not in contract.get("$defs", {}):
            errors.append(f"artifact[{position}] has unknown schema type")
            continue
        if item.get("spoiler_class") not in {"PLAYER_SAFE", "GM_HIDDEN"}:
            errors.append(f"artifact[{position}] has invalid spoiler classification")
        nested_classes = _nested_spoiler_classes(item["data"])
        if any(label not in {"PLAYER_SAFE", "GM_HIDDEN"} for label in nested_classes):
            errors.append(f"artifact[{position}] contains an invalid nested spoiler classification")
        effective_class = "GM_HIDDEN" if "GM_HIDDEN" in nested_classes else "PLAYER_SAFE"
        if nested_classes and item.get("spoiler_class") != effective_class:
            errors.append(f"artifact[{position}] envelope spoiler classification differs from nested data")
        if item.get("spoiler_class") == "GM_HIDDEN" or effective_class == "GM_HIDDEN":
            errors.append("D10 refuses all GM_HIDDEN payloads until effective segregation is independently verified outside this adapter")
        for message in schema_errors(item["data"], type_name, contract):
            errors.append(f"{type_name}: {message}")
        for source_position, source_ref in enumerate(_nested_source_refs(item["data"])):
            source_errors, _ = verify_source_ref(source_ref, source_root, source_head, expected_source_head)
            errors.extend(f"{type_name} source[{source_position}]: {message}" for message in source_errors)
        id_field = id_fields.get(type_name)
        if id_field and isinstance(item["data"].get(id_field), str):
            ident = item["data"][id_field]
            if ident in indexes.setdefault(type_name, {}):
                errors.append(f"duplicate {type_name} id: {ident}")
            indexes[type_name][ident] = item["data"]

    actors = indexes.get("actor", {})
    knowledge_items = indexes.get("knowledge", {})
    relationships = indexes.get("relationship", {})
    chronicles = indexes.get("chronicle", {})
    marcos = indexes.get("marco", {})
    histories = indexes.get("history_episode", {})
    plots = indexes.get("plot", {})
    stories = indexes.get("story", {})
    scenes = indexes.get("scene", {})
    beats = indexes.get("beat", {})
    threads = indexes.get("thread", {})
    clues = indexes.get("clue", {})
    clocks = indexes.get("clock", {})
    ledgers = indexes.get("ledger", {})
    known_ids = {ident for group in indexes.values() for ident in group}

    for ident, item in chronicles.items():
        if any(ref not in marcos for ref in item.get("marco_ids", [])):
            errors.append(f"chronicle {ident} references an unresolved Marco")
        if any(ref not in plots for ref in item.get("central_plot_ids", [])):
            errors.append(f"chronicle {ident} references an unresolved plot")
    for ident, item in marcos.items():
        if item.get("chronicle_id") not in chronicles:
            errors.append(f"Marco {ident} references an unresolved chronicle")
    for ident, item in histories.items():
        if item.get("marco_id") not in marcos:
            errors.append(f"history episode {ident} references an unresolved Marco")
        if item.get("outcome_event_ref") not in known_events:
            errors.append(f"history episode {ident} outcome is outside the supplied checkpoint")

    for ident, item in actors.items():
        if item.get("as_of_event_id") not in known_events:
            errors.append(f"actor {ident} references an event outside the supplied checkpoint")
        for ref in item.get("knowledge_refs", []):
            record = knowledge_items.get(ref)
            if record is None:
                errors.append(f"actor {ident} has unresolved knowledge ref {ref}")
            elif record.get("knower_id") != ident:
                errors.append(f"knowledge {ref} belongs to {record.get('knower_id')}, not actor {ident}")
        for ref in item.get("relationship_refs", []):
            edge = relationships.get(ref)
            if edge is None:
                errors.append(f"actor {ident} has unresolved directed relationship ref {ref}")
            elif ident not in {edge.get("from_id"), edge.get("to_id")}:
                errors.append(f"relationship {ref} does not include actor {ident}")

    for ident, item in knowledge_items.items():
        if item.get("knower_id") not in actors:
            errors.append(f"knowledge {ident} has no corresponding actor record")
        if item.get("as_of_event_id") not in known_events:
            errors.append(f"knowledge {ident} is outside the supplied event checkpoint")
        acquisition = acquisition_records.get(item.get("acquisition_ref"))
        if acquisition is None:
            errors.append(f"knowledge {ident} lacks a verified acquisition record")
        else:
            if acquisition.get("knower_id") != item.get("knower_id"):
                errors.append(f"knowledge {ident} acquisition is recorded for another knower")
            if acquisition.get("event_id") not in known_events:
                errors.append(f"knowledge {ident} acquisition event is outside the supplied checkpoint")
            if acquisition.get("evidence_id") not in evidence_ids:
                errors.append(f"knowledge {ident} acquisition lacks verified evidence")
            if acquisition.get("method") not in {"OBSERVED", "HEARD", "READ", "TOLD", "INFERRED", "SHARED", "OTHER"}:
                errors.append(f"knowledge {ident} acquisition method is not recognized")
            try:
                if list(bundle.get("event_ids", [])).index(acquisition.get("event_id")) > list(bundle.get("event_ids", [])).index(item.get("as_of_event_id")):
                    errors.append(f"knowledge {ident} predates its acquisition event")
            except ValueError:
                pass

    for ident, edge in relationships.items():
        if edge.get("from_id") not in actors or edge.get("to_id") not in actors:
            errors.append(f"relationship {ident} has an unresolved endpoint")
        if edge.get("as_of_event_id") not in known_events:
            errors.append(f"relationship {ident} is outside the supplied event checkpoint")

    terminal_plot_states = {"RESOLVED", "FAILED", "ABANDONED_WITH_CONSEQUENCES", "RESOLVED_OFFSCREEN_WITH_EVIDENCE", "SUPERSEDED_WITH_PROVENANCE"}
    for ident, item in plots.items():
        if any(ref not in known_events for ref in item.get("origin_event_refs", [])):
            errors.append(f"plot {ident} origin event is outside the supplied checkpoint")
        for actor_ref in [*item.get("actors", []), *item.get("opposition", [])]:
            if actor_ref not in actors:
                errors.append(f"plot {ident} references unresolved actor {actor_ref}")
        if any(ref not in clues for ref in item.get("clue_refs", [])):
            errors.append(f"plot {ident} references unresolved clue")
        if any(ref not in clocks for ref in item.get("clock_refs", [])):
            errors.append(f"plot {ident} references unresolved clock")
        if item.get("status") in terminal_plot_states:
            refs = item.get("terminal_evidence_refs", [])
            if not refs or any(ref not in evidence_ids for ref in refs):
                errors.append(f"terminal plot {ident} requires verified terminal evidence")
        for link in item.get("plot_links", []):
            if link.get("kind") == "CAUSAL":
                if link.get("target_id") not in plots:
                    errors.append(f"causal link from {ident} points to an unresolved plot")
                if not link.get("sources"):
                    errors.append(f"causal link from {ident} requires verified source evidence")
                if any(s.get("verification") != "VERIFIED" for s in link.get("sources", []) if isinstance(s, dict)):
                    errors.append(f"causal link from {ident} requires verified source evidence")

    for item in artifacts:
        if not isinstance(item, dict) or not isinstance(item.get("data"), dict):
            continue
        data = item["data"]
        if item.get("type") == "clue" and data.get("critical") is True:
            routes = data.get("discovery_routes", [])
            mechanisms = {route.get("independent_mechanism") for route in routes}
            if len(routes) < 2 or len(mechanisms) < 2:
                errors.append(f"critical clue {data.get('clue_id')} needs two independent discovery mechanisms")
            status = data.get("truth_lock_status")
            if status not in {"LOCKED", "NOT_APPLICABLE", "REVISED_WITH_APPROVAL"}:
                errors.append(f"critical clue {data.get('clue_id')} cannot be used before truth lock")
            if status == "LOCKED" and not data.get("truth_lock_ref"):
                errors.append(f"critical clue {data.get('clue_id')} has a placeholder truth lock")
        if item.get("type") == "story":
            if data.get("marco_id") not in indexes.get("marco", {}):
                errors.append(f"story {data.get('story_id')} references an unresolved Marco")
            if any(ref not in plots for ref in data.get("plot_ids", [])):
                errors.append(f"story {data.get('story_id')} references an unresolved plot")
            if str(data.get("state", "")).startswith("CLOSED_") and not data.get("closure_routes"):
                errors.append(f"closed story {data.get('story_id')} lacks a closure route")
        if item.get("type") == "scene":
            if data.get("story_id") not in stories:
                errors.append(f"scene {data.get('scene_id')} references an unresolved story")
            if data.get("state") == "CLOSED" and data.get("scene_id") not in set(bundle.get("scene_close_evidence_ids", [])):
                errors.append(f"closed scene {data.get('scene_id')} lacks close evidence")
        if item.get("type") == "beat" and data.get("scene_id") not in scenes:
            errors.append(f"beat {data.get('beat_id')} references an unresolved scene")
        if item.get("type") == "thread" and data.get("plot_id") not in (None, *plots.keys()):
            errors.append(f"thread {data.get('thread_id')} references an unresolved plot")
        if item.get("type") == "thread":
            owner = data.get("owner_id")
            if owner is not None and owner not in actors:
                errors.append(f"thread {data.get('thread_id')} references an unresolved owner")
            if data.get("origin_event_ref") not in known_events:
                errors.append(f"thread {data.get('thread_id')} origin is outside the supplied checkpoint")
        if item.get("type") == "clock":
            if data.get("actor_id") not in actors:
                errors.append(f"clock {data.get('clock_id')} references an unresolved actor")
            if data.get("current", 0) > data.get("maximum", 0):
                errors.append(f"clock {data.get('clock_id')} exceeds its maximum")
            if any(ref not in known_events for ref in data.get("event_evidence_refs", [])):
                errors.append(f"clock {data.get('clock_id')} has tick evidence outside the supplied checkpoint")
        if item.get("type") == "ledger":
            if data.get("chronicle_id") not in chronicles:
                errors.append(f"ledger {data.get('ledger_id')} references an unresolved chronicle")
            if any(ref not in known_events for ref in data.get("event_refs", [])):
                errors.append(f"ledger {data.get('ledger_id')} contains an event outside the supplied checkpoint")
            for field, target in (("actor_state_refs", actors), ("plot_state_refs", plots), ("open_thread_refs", threads)):
                if any(ref not in target for ref in data.get(field, [])):
                    errors.append(f"ledger {data.get('ledger_id')} contains unresolved {field}")
        if item.get("type") == "retcon":
            if data.get("status") in {"PLAYER_APPROVED", "APPLIED_VERSIONED"}:
                decision = data.get("approval_decision_id")
                record = decision_records.get(decision)
                if (data.get("approval_required") is not True or not record or record.get("decision_kind") != "RETCON_APPROVAL"
                    or record.get("scope") != "EXACT_RETCON" or set(data.get("affected_refs", [])) != set(record.get("affected_refs", []))
                    or record.get("event_id") not in known_events or record.get("evidence_id") not in evidence_ids):
                    errors.append(f"retcon {data.get('change_id')} lacks express player approval evidence")

    return errors


def adapt_for_role(
    bundle: dict[str, Any],
    role: str,
    contract: dict[str, Any],
    source_root: Path | None,
    expected_source_head: str | None = None,
) -> dict[str, Any]:
    allowed_roles = {"PLAYER", "NARRATOR", "DRAMATURGO", "AUDITOR", "ORCHESTRATOR"}
    if role not in allowed_roles:
        return {"status": "DENY", "route": None, "payload": [], "reasons": ["unknown role"]}
    validation_errors = validate_bundle(bundle, contract, source_root, expected_source_head)
    if validation_errors:
        return {"status": "HOLD", "route": "DRAMATURGO", "payload": [], "reasons": validation_errors}
    hidden = [
        a for a in bundle.get("artifacts", [])
        if a.get("spoiler_class") == "GM_HIDDEN" or "GM_HIDDEN" in _nested_spoiler_classes(a.get("data"))
    ]
    if hidden:
        return {"status": "HOLD", "route": "DRAMATURGO", "payload": [], "reasons": ["D10 refuses GM_HIDDEN until effective segregation is independently verified outside this adapter"]}
    if bundle.get("emergency") is True:
        return {"status": "HOLD", "route": "DRAMATURGO", "payload": [], "reasons": ["emergency requires Dramaturgo review"]}
    if role == "NARRATOR":
        return {
            "status": "HOLD",
            "route": "DRAMATURGO",
            "payload": [],
            "reasons": ["D10 adapters are PROPOSED_NON_OPERATIONAL; documentary flags cannot grant NARRATOR_PERMISSION"],
        }
    safe = [
        a for a in bundle.get("artifacts", [])
        if a.get("spoiler_class") == "PLAYER_SAFE" and "GM_HIDDEN" not in _nested_spoiler_classes(a.get("data"))
    ]
    if role in {"PLAYER", "AUDITOR", "ORCHESTRATOR"}:
        payload = safe
    else:
        payload = safe
    return {"status": "ALLOW_READ_ONLY", "route": None, "payload": copy.deepcopy(payload), "reasons": []}


def validate_publication(record: dict[str, Any]) -> list[str]:
    errors = []
    if record.get("target_branch") != EXPECTED_BRANCH:
        errors.append("publication target must be the authorized documentary branch")
    if record.get("force_push") is not False:
        errors.append("force push is prohibited")
    if not SHA1_RE.fullmatch(str(record.get("commit", ""))) or not SHA1_RE.fullmatch(str(record.get("parent", ""))) or not SHA1_RE.fullmatch(str(record.get("tree", ""))):
        errors.append("commit, parent and tree must be verified 40-character SHAs")
    if record.get("master_unchanged") is not True:
        errors.append("master must remain unchanged")
    for field in ("input_head", "remote_head_before", "remote_head_after"):
        if not SHA1_RE.fullmatch(str(record.get(field, ""))):
            errors.append(f"{field} must be a verified 40-character SHA")
    if record.get("remote_head_before") != record.get("input_head"):
        errors.append("remote documentary HEAD changed before publication")
    if record.get("parent") != record.get("input_head"):
        errors.append("published commit parent must match the verified input HEAD")
    if record.get("remote_head_after") != record.get("commit"):
        errors.append("remote readback HEAD must match the published commit")
    if record.get("working_tree_clean_before") is not True or record.get("new_artifacts_only") is not True or record.get("frozen_paths_unchanged") is not True or record.get("secret_scan_clear") is not True:
        errors.append("publication scope and preflight checks are incomplete")
    readback = record.get("readback", {})
    if readback.get("commit_matches") is not True or readback.get("tree_matches") is not True or readback.get("all_blobs_match") is not True or readback.get("all_contents_match") is not True:
        errors.append("complete remote readback of commit, tree, blobs and contents is required")
    return errors


def validate_phase_envelope(envelope: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors = [e.message for e in Draft202012Validator(schema).iter_errors(envelope)]
    validation = envelope.get("validation", {})
    if validation.get("passed", 0) > validation.get("total", 0):
        errors.append("passed checks cannot exceed total checks")
    if validation.get("status") == "PASS" and validation.get("passed") != validation.get("total"):
        errors.append("a PASS validation requires every catalogued check to pass")
    publication = envelope.get("publication", {})
    successful_gate = envelope.get("gate") in {"PASS", "PASS_WITH_UNKNOWN"}
    transitioning = envelope.get("next_phase") is not None
    final_release = envelope.get("phase") == "D12" and successful_gate
    if successful_gate or transitioning or final_release:
        if validation.get("status") != "PASS" or validation.get("passed") != validation.get("total"):
            errors.append("successful gate, phase transition and D12 release require every validation check to pass")
        if any(envelope.get("audit", {}).get(role) not in {"PASS", "PASS_WITH_UNKNOWN"} for role in ("technical", "literary")):
            errors.append("successful gate, phase transition and D12 release require completed technical and literary review")
        if publication.get("branch") != EXPECTED_BRANCH:
            errors.append("successful gate, phase transition and D12 release must read back the authorized documentary branch")
        if publication.get("readback_verified") is not True or publication.get("status") != "READBACK_VERIFIED":
            errors.append("successful gate, phase transition and D12 release require READBACK_VERIFIED publication status")
        publication_errors = validate_publication(envelope.get("publication_record", {}))
        errors.extend(f"publication record: {message}" for message in publication_errors)
    if final_release:
        if envelope.get("pending_player_approvals"):
            errors.append("D12 cannot release while player approvals remain pending")
        prior_gates = envelope.get("prior_phase_gates", {})
        required_prior_phases = {f"D{number:02d}" for number in range(1, 12)}
        if not isinstance(prior_gates, dict) or set(prior_gates) != required_prior_phases or any(status not in {"PASS", "PASS_WITH_UNKNOWN"} for status in prior_gates.values()):
            errors.append("D12 release requires approved gates for every phase D01 through D11")

    for artifact_record in envelope.get("artifacts", []):
        path = artifact_record.get("path", "")
        if artifact_record.get("spoiler_class") != "PLAYER_SAFE":
            errors.append("documentary phase envelope cannot publish GM_HIDDEN artifacts")
        if not isinstance(path, str) or not path.startswith("novydres/runtime/narrative-architecture/program/deliverables/") or ".." in Path(path).parts:
            errors.append("phase envelope artifact path must stay inside authorized documentary deliverables")
    if envelope.get("next_phase") is not None and publication.get("readback_verified") is not True:
        errors.append("phase transition requires publication readback")
    if envelope.get("next_phase") is not None and publication.get("status") != "READBACK_VERIFIED":
        errors.append("phase transition requires READBACK_VERIFIED publication status")
    if envelope.get("next_phase") is not None and envelope.get("gate") not in {"PASS", "PASS_WITH_UNKNOWN"}:
        errors.append("phase transition requires an approved documentary gate")
    if envelope.get("next_phase") is not None:
        phase = envelope.get("phase")
        expected_next = {f"D{n:02d}": f"D{n + 1:02d}" for n in range(5, 12)}.get(phase)
        if envelope.get("next_phase") != expected_next:
            errors.append("phase transition must advance exactly one step from D05 through D12")
        if envelope.get("next_phase") == "D12" and phase != "D11":
            errors.append("only D11 may transition to D12")
    if envelope.get("narrator_ready") is not False:
        errors.append("D10 envelope cannot grant narrator readiness")
    return errors


def run_tests(registry: dict[str, Any], contract: dict[str, Any], roles: dict[str, Any], envelope_schema: dict[str, Any], test_catalog: dict[str, Any]) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []

    def check(test_id: str, fn: Callable[[], None]) -> None:
        try:
            fn()
            results.append({"id": test_id, "result": "PASS"})
        except Exception as exc:  # each adversarial case must produce explicit evidence
            results.append({"id": test_id, "result": "FAIL", "detail": str(exc)})

    def require(condition: bool, message: str) -> None:
        if not condition:
            raise AssertionError(message)

    def test_registry() -> None:
        require(registry.get("registry_status") == "PROPOSED_NON_OPERATIONAL", "registry authority changed")
        require(set(registry.get("type_map", {})) == set(contract.get("$defs", {})), "type map does not cover exact D01 definitions")
        Draft202012Validator.check_schema(contract)

    check("T-D10-001-registry-pin-and-coverage", test_registry)
    check("T-D10-002-phase-envelope-schema", lambda: Draft202012Validator.check_schema(envelope_schema))
    for index, (type_name, definition) in enumerate(contract["$defs"].items(), start=1):
        def schema_valid(name: str = type_name) -> None:
            Draft202012Validator.check_schema(schema_for(contract, name))
        check(f"T-D10-{index + 2:03d}-schema-{type_name}", schema_valid)

        def valid_sample(name: str = type_name, schema: dict[str, Any] = definition) -> None:
            sample = _sample(schema, contract)
            errors = schema_errors(sample, name, contract)
            require(not errors, f"generated sample invalid: {errors}")
        check(f"T-D10-{index + 23:03d}-positive-{type_name}", valid_sample)

        def missing_required(name: str = type_name, schema: dict[str, Any] = definition) -> None:
            required = schema.get("required", [])
            require(bool(required), "definition has no required fields")
            sample = _sample(schema, contract)
            sample.pop(required[0], None)
            require(bool(schema_errors(sample, name, contract)), "missing required field was accepted")
        check(f"T-D10-{index + 44:03d}-negative-required-{type_name}", missing_required)

        if definition.get("additionalProperties") is False:
            def reject_extra(name: str = type_name, schema: dict[str, Any] = definition) -> None:
                sample = _sample(schema, contract)
                sample["__unexpected_D10_test_field__"] = True
                require(bool(schema_errors(sample, name, contract)), "unknown property was accepted")
            check(f"T-D10-{index + 65:03d}-negative-extra-{type_name}", reject_extra)

        enum_props = [key for key, value in definition.get("properties", {}).items() if isinstance(value, dict) and "enum" in value]
        if enum_props:
            key = enum_props[0]
            def reject_enum(name: str = type_name, prop: str = key, schema: dict[str, Any] = definition) -> None:
                sample = _sample(schema, contract)
                sample[prop] = "__NOT_A_CONTRACT_ENUM__"
                require(bool(schema_errors(sample, name, contract)), "invalid enum value was accepted")
            check(f"T-D10-{index + 86:03d}-negative-enum-{type_name}", reject_enum)

    sample = base_bundle([artifact("actor", actor("A", ["K1"], ["R1"])), artifact("actor", actor("B")), artifact("knowledge", knowledge()), artifact("relationship", relationship())])
    sample["acquisition_records"] = [{"acquisition_id":"ACQ1","knower_id":"A","event_id":"E1","method":"OBSERVED","evidence_id":"EV1","source":source()}]
    check("T-D10-110-semantic-valid-acquired-knowledge", lambda: require(not validate_bundle(sample, contract), str(validate_bundle(sample, contract))))

    bad = copy.deepcopy(sample)
    bad["artifacts"][0]["data"]["knowledge_refs"] = ["MISSING"]
    check("T-D10-111-negative-unknown-knowledge-ref", lambda: require(any("unresolved knowledge" in e for e in validate_bundle(bad, contract)), "unknown knowledge ref accepted"))

    bad = copy.deepcopy(sample)
    bad["acquisition_records"] = []
    check("T-D10-112-negative-unacquired-npc-knowledge", lambda: require(any("acquisition record" in e for e in validate_bundle(bad, contract)), "knowledge without acquisition accepted"))

    bad = copy.deepcopy(sample)
    bad["event_ids"] = []
    check("T-D10-113-negative-knowledge-after-checkpoint", lambda: require(any("outside the supplied" in e for e in validate_bundle(bad, contract)), "future/out-of-checkpoint knowledge accepted"))

    check("T-D10-114-directed-relationship-not-mirrored", lambda: require(len([a for a in sample["artifacts"] if a["type"] == "relationship"]) == 1 and not validate_bundle(sample, contract), "directional edge was mirrored or rejected"))

    causal = base_bundle([artifact("actor", actor("A")), artifact("actor", actor("B")), artifact("plot", plot("P1")), artifact("plot", plot("P2"))])
    causal["artifacts"][2]["data"]["plot_links"] = [{"target_id": "P2", "kind": "CAUSAL", "sources": [source()]}]
    check("T-D10-115-verified-causal-link", lambda: require(not validate_bundle(causal, contract), str(validate_bundle(causal, contract))))

    bad = copy.deepcopy(causal)
    bad["artifacts"][2]["data"]["plot_links"][0]["sources"] = [source("UNVERIFIED")]
    check("T-D10-116-negative-unproven-causality", lambda: require(any("verified source evidence" in e for e in validate_bundle(bad, contract)), "unverified causal link accepted"))

    bad = copy.deepcopy(causal)
    bad["artifacts"][2]["data"]["plot_links"][0]["target_id"] = "P404"
    check("T-D10-117-negative-dangling-causal-target", lambda: require(any("unresolved plot" in e for e in validate_bundle(bad, contract)), "dangling causal target accepted"))

    check("T-D10-118-critical-clue-two-routes-and-lock", lambda: require(not validate_bundle(base_bundle([artifact("clue", clue())]), contract), str(validate_bundle(base_bundle([artifact("clue", clue())]), contract))))
    check("T-D10-119-negative-critical-clue-one-route", lambda: require(any("two independent" in e for e in validate_bundle(base_bundle([artifact("clue", clue(routes=clue()["discovery_routes"][:1]))]), contract)), "single critical clue route accepted"))
    check("T-D10-120-negative-critical-clue-placeholder-lock", lambda: require(any("placeholder truth lock" in e for e in validate_bundle(base_bundle([artifact("clue", clue(lock_ref=None))]), contract)), "empty truth-lock placeholder accepted"))
    check("T-D10-121-negative-critical-clue-undecided-lock", lambda: require(any("before truth lock" in e for e in validate_bundle(base_bundle([artifact("clue", clue(lock="UNDECIDED", lock_ref=None))]), contract)), "unlocked critical clue accepted"))

    check("T-D10-122-terminal-plot-evidence", lambda: require(not validate_bundle(base_bundle([artifact("actor", actor("A")), artifact("actor", actor("B")), artifact("plot", plot(status="RESOLVED"))]), contract), "terminal plot with evidence rejected"))
    bad = base_bundle([artifact("actor", actor("A")), artifact("actor", actor("B")), artifact("plot", plot(status="RESOLVED"))])
    bad["evidence_records"] = []
    bad["evidence_ids"] = ["EV1"]
    check("T-D10-123-negative-terminal-plot-without-evidence", lambda: require(any("terminal evidence" in e for e in validate_bundle(bad, contract)), "terminal plot without evidence accepted"))

    check("T-D10-124-pending-retcon-no-fabricated-approval", lambda: require(not validate_bundle(base_bundle([artifact("retcon", {"change_id":"RC1","kind":"RETCON_SOFT","affected_refs":["E1"],"before_claim":"x","after_proposal":"y","evidence":[],"downstream_impacts":[],"alternatives":["keep existing history"],"approval_required":True,"approval_decision_id":None,"status":"PENDING_PLAYER_APPROVAL"})]), contract), "pending retcon should remain a valid pending proposal"))
    applied = {"change_id":"RC2","kind":"RETCON_HARD","affected_refs":["E1"],"before_claim":"x","after_proposal":"y","evidence":[],"downstream_impacts":[],"alternatives":[],"approval_required":True,"approval_decision_id":"APP1","status":"APPLIED_VERSIONED"}
    invented_approval = base_bundle([artifact("retcon", applied)])
    invented_approval["player_decision_ids"] = ["APP1"]
    check("T-D10-125-negative-retcon-without-player-decision", lambda: require(any("express player approval" in e for e in validate_bundle(invented_approval, contract)), "caller-supplied decision ID accepted without a verified record"))
    approved_bundle = base_bundle([artifact("retcon", applied)])
    approved_bundle["decision_records"] = [{
        "decision_id":"APP1", "decision_maker":"PLAYER", "decision_kind":"RETCON_APPROVAL",
        "scope":"EXACT_RETCON", "affected_refs":["E1"], "event_id":"E1", "evidence_id":"EV1", "source":source()
    }]
    check("T-D10-126-approved-retcon-decision-reference", lambda: require(not validate_bundle(approved_bundle, contract), str(validate_bundle(approved_bundle, contract))))

    check("T-D10-127-no-mechanical-grants", lambda: require(any("mechanical changes" in e for e in validate_bundle({**base_bundle(), "mechanical_changes":[{"xp":1}]}, contract)), "mechanical mutation accepted"))
    check("T-D10-128-no-narrative-mutation", lambda: require(any("narrative mutation" in e for e in validate_bundle({**base_bundle(), "narrative_mutation":True}, contract)), "narrative mutation accepted"))
    check("T-D10-129-no-gm-hidden-without-segregation", lambda: require(any("GM_HIDDEN" in e for e in validate_bundle(base_bundle([artifact("actor", actor("A"), "GM_HIDDEN")]), contract)), "unsegregated hidden artifact accepted"))

    player_bundle = base_bundle([artifact("actor", actor("A")), artifact("actor", actor("B"), "GM_HIDDEN")])
    player_bundle["effective_gm_hidden_segregation"] = True
    check("T-D10-130-player-view-filters-hidden", lambda: require(adapt_for_role(player_bundle, "PLAYER", contract, _TEST_SOURCE_ROOT)["status"] == "HOLD", "hidden content was not held before player projection"))
    check("T-D10-131-hidden-content-holds-unsegregated-delivery", lambda: require(adapt_for_role({**player_bundle, "effective_gm_hidden_segregation":False}, "DRAMATURGO", contract, _TEST_SOURCE_ROOT)["status"] == "HOLD", "unsegregated hidden material was delivered"))
    check("T-D10-132-emergency-routes-to-dramaturgo", lambda: require(adapt_for_role({**base_bundle(), "emergency":True}, "NARRATOR", contract, _TEST_SOURCE_ROOT).get("route") == "DRAMATURGO", "emergency did not route to Dramaturgo"))
    narrator = adapt_for_role(base_bundle(), "NARRATOR", contract, _TEST_SOURCE_ROOT)
    check("T-D10-133-proposed-contract-blocks-narrator", lambda: require(narrator["status"] == "HOLD" and not narrator["payload"], "proposed D01 contract allowed narrator content"))
    complete_but_no_scene = {**base_bundle(), "documentary_release_status":"APPROVED","schema_status":"APPROVED_CONGELADO","all_required_gates":"PASS","semantic_validation_passed":True,"scene_ready":False,"narrator_permission":True,"operational_readback_verified":True}
    check("T-D10-134-scene-ready-separate-gate", lambda: require(adapt_for_role(complete_but_no_scene, "NARRATOR", contract, _TEST_SOURCE_ROOT)["status"] == "HOLD", "NARRATOR_PERMISSION bypassed SCENE_READY"))
    complete_but_no_permission = {**base_bundle(), "documentary_release_status":"APPROVED","schema_status":"APPROVED_CONGELADO","all_required_gates":"PASS","semantic_validation_passed":True,"scene_ready":True,"narrator_permission":False,"operational_readback_verified":True,"artifacts":[artifact("scene", {"scene_id":"S1","state":"READY"})]}
    check("T-D10-135-narrator-permission-separate-gate", lambda: require(adapt_for_role(complete_but_no_permission, "NARRATOR", contract, _TEST_SOURCE_ROOT)["status"] == "HOLD", "SCENE_READY bypassed NARRATOR_PERMISSION"))
    bad_role = adapt_for_role(base_bundle(), "UNREGISTERED", contract, _TEST_SOURCE_ROOT)
    check("T-D10-136-negative-unknown-role", lambda: require(bad_role["status"] == "DENY" and not bad_role["payload"], "unknown role was accepted"))

    good_publication = {"target_branch":EXPECTED_BRANCH,"force_push":False,"commit":"1"*40,"parent":"2"*40,"tree":"3"*40,"input_head":"2"*40,"remote_head_before":"2"*40,"remote_head_after":"1"*40,"working_tree_clean_before":True,"new_artifacts_only":True,"frozen_paths_unchanged":True,"secret_scan_clear":True,"master_unchanged":True,"readback":{"commit_matches":True,"tree_matches":True,"all_blobs_match":True,"all_contents_match":True}}
    check("T-D10-137-publication-readback-complete", lambda: require(not validate_publication(good_publication), str(validate_publication(good_publication))))
    check("T-D10-138-negative-master-target", lambda: require(any("documentary branch" in e for e in validate_publication({**good_publication,"target_branch":"master"})), "master target accepted"))
    check("T-D10-139-negative-force-push", lambda: require(any("force push" in e for e in validate_publication({**good_publication,"force_push":True})), "force push accepted"))
    check("T-D10-140-negative-missing-readback", lambda: require(any("readback" in e for e in validate_publication({**good_publication,"readback":{}})), "incomplete readback accepted"))
    check("T-D10-141-negative-master-mutation", lambda: require(any("master" in e for e in validate_publication({**good_publication,"master_unchanged":False})), "master mutation accepted"))
    check("T-D10-142-negative-invalid-commit-sha", lambda: require(any("40-character SHAs" in e for e in validate_publication({**good_publication,"commit":"not-a-sha"})), "invalid commit hash accepted"))
    chronicle_data = _sample(contract["$defs"]["chronicle"], contract)
    chronicle_data.update({"chronicle_id":"CH1", "marco_ids":["M1"], "spoiler_class":"PLAYER_SAFE"})
    marco_data = _sample(contract["$defs"]["marco"], contract)
    marco_data.update({"marco_id":"M1", "chronicle_id":"CH1"})
    story_data = _sample(contract["$defs"]["story"], contract)
    story_data.update({"story_id":"ST1", "marco_id":"M1", "state":"DRAFT"})
    scene_data = _sample(contract["$defs"]["scene"], contract)
    scene_data.update({"scene_id":"S1", "story_id":"ST1", "state":"READY"})
    ready_bundle = {**base_bundle([artifact("chronicle", chronicle_data), artifact("marco", marco_data), artifact("story", story_data), artifact("scene", scene_data)]), "documentary_release_status":"APPROVED","all_required_gates":"PASS","semantic_validation_passed":True,"scene_ready":True,"narrator_permission":True,"operational_readback_verified":True}
    def proposal_blocks_ready_scene() -> None:
        errors = validate_bundle(ready_bundle, contract)
        require(not errors, str(errors))
        require(adapt_for_role(ready_bundle, "NARRATOR", contract, _TEST_SOURCE_ROOT)["status"] == "HOLD", "proposal-only adapter admitted a ready scene")
    check("T-D10-143-exactly-one-ready-scene", proposal_blocks_ready_scene)
    two_scenes = {**ready_bundle,"artifacts":[artifact("scene", {"scene_id":"S1","state":"READY"}),artifact("scene", {"scene_id":"S2","state":"READY"})]}
    check("T-D10-144-negative-multiple-ready-scenes", lambda: require(adapt_for_role(two_scenes, "NARRATOR", contract, _TEST_SOURCE_ROOT)["status"] == "HOLD", "multiple scenes bypassed one-scene handoff limit"))
    unvalidated = {**ready_bundle,"semantic_validation_passed":False}
    check("T-D10-145-negative-unvalidated-narrator-content", lambda: require(adapt_for_role(unvalidated, "NARRATOR", contract, _TEST_SOURCE_ROOT)["status"] == "HOLD", "unvalidated content reached Narrator"))
    check("T-D10-146-negative-branch-divergence", lambda: require(any("HEAD changed" in e for e in validate_publication({**good_publication,"remote_head_before":"4"*40})), "concurrent branch advance accepted"))
    check("T-D10-147-negative-parent-mismatch", lambda: require(any("parent" in e for e in validate_publication({**good_publication,"parent":"5"*40})), "non-fast-forward publication accepted"))
    check("T-D10-148-negative-incomplete-scope-preflight", lambda: require(any("preflight checks" in e for e in validate_publication({**good_publication,"secret_scan_clear":False})), "incomplete publication preflight accepted"))

    phase_envelope = {"program_id":"NOVYDRES_CHR001_NARRATIVE_ARCHITECTURE","phase":"D10","gate":"PASS_WITH_UNKNOWN","authority":"EDITORIAL_ONLY","schema_status":"PROPOSED_NON_OPERATIONAL","operational_mutation":False,"artifacts":[],"validation":{"status":"PASS","passed":4,"total":4},"audit":{"technical":"PASS","literary":"PASS_WITH_UNKNOWN"},"publication":{"status":"READBACK_VERIFIED","branch":EXPECTED_BRANCH,"readback_verified":True},"publication_record":good_publication,"pending_player_approvals":[],"next_phase":"D11","narrator_ready":False}
    check("T-D10-149-envelope-preserves-pass-with-unknown", lambda: require(not validate_phase_envelope(phase_envelope, envelope_schema), str(validate_phase_envelope(phase_envelope, envelope_schema))))
    check("T-D10-150-negative-envelope-transition-before-readback", lambda: require(any("readback" in e for e in validate_phase_envelope({**phase_envelope,"publication":{"status":"PUSHED","branch":EXPECTED_BRANCH,"readback_verified":False}}, envelope_schema)), "phase advanced before readback"))
    check("T-D10-151-negative-envelope-cannot-grant-narrator", lambda: require(bool(validate_phase_envelope({**phase_envelope,"narrator_ready":True}, envelope_schema)), "documentary envelope granted narrator readiness"))
    check("T-D10-152-negative-envelope-check-counts", lambda: require(any("exceed" in e for e in validate_phase_envelope({**phase_envelope,"validation":{"status":"PASS","passed":149,"total":148}}, envelope_schema)), "invalid check counts accepted"))
    check("T-D10-155-negative-envelope-premature-audit", lambda: require(any("completed technical and literary" in e for e in validate_phase_envelope({**phase_envelope,"audit":{"technical":"PENDING","literary":"PASS"}}, envelope_schema)), "phase advanced without complete review"))

    hidden_chronicle = _sample(contract["$defs"]["chronicle"], contract)
    hidden_chronicle.update({"chronicle_id":"H1", "spoiler_class":"GM_HIDDEN"})
    mismarked_hidden = base_bundle([artifact("chronicle", hidden_chronicle, "PLAYER_SAFE")])
    check("T-D10-157-negative-nested-hidden-envelope-mismatch", lambda: require(any("envelope spoiler classification differs" in e for e in validate_bundle(mismarked_hidden, contract)), "nested GM_HIDDEN content passed as PLAYER_SAFE"))

    nested_hidden = base_bundle([artifact("chronicle", hidden_chronicle, "GM_HIDDEN")])
    check("T-D10-158-negative-nested-hidden-without-segregation", lambda: require(any("GM_HIDDEN" in e for e in validate_bundle(nested_hidden, contract)), "nested GM_HIDDEN content passed without segregation"))
    nested_hidden["effective_gm_hidden_segregation"] = True
    check("T-D10-159-player-adapter-filters-nested-hidden", lambda: require(adapt_for_role(nested_hidden, "PLAYER", contract, _TEST_SOURCE_ROOT)["status"] == "HOLD", "nested hidden content was not held before player projection"))

    bad = copy.deepcopy(causal)
    bad["artifacts"][2]["data"]["plot_links"][0]["sources"] = [{**source(), "path":"test/missing.json", "blob_sha":"b" * 40}]
    check("T-D10-160-negative-causal-source-not-in-checkpoint", lambda: require(any("source path cannot be read" in e or "source path is not tracked" in e or "blob SHA does not match" in e for e in validate_bundle(bad, contract)), "causal source with nonexistent path and invented SHA accepted"))

    bad = base_bundle([artifact("actor", actor("A")), artifact("actor", actor("B")), artifact("plot", plot(status="RESOLVED"))])
    bad["evidence_ids"] = ["EV1"]
    bad["evidence_records"] = []
    check("T-D10-161-negative-terminal-id-without-source-record", lambda: require(any("terminal evidence" in e for e in validate_bundle(bad, contract)), "caller-supplied terminal evidence ID accepted without a source record"))

    check("T-D10-162-negative-envelope-nonsequential-phase", lambda: require(bool(validate_phase_envelope({**phase_envelope,"next_phase":"D12"}, envelope_schema)), "D10 skipped directly to D12"))
    bad_branch_envelope = {**phase_envelope,"publication":{"status":"READBACK_VERIFIED","branch":"master","readback_verified":True},"publication_record":{**good_publication,"target_branch":"master"}}
    check("T-D10-163-negative-envelope-master-branch", lambda: require(any("documentary branch" in e or "authorized documentary branch" in e for e in validate_phase_envelope(bad_branch_envelope, envelope_schema)), "master was accepted as a phase publication branch"))
    bad_readback_envelope = {**phase_envelope,"publication_record":{**good_publication,"readback":{"commit_matches":True,"tree_matches":True,"all_blobs_match":False,"all_contents_match":True}}}
    check("T-D10-164-negative-envelope-incomplete-readback", lambda: require(any("readback" in e for e in validate_phase_envelope(bad_readback_envelope, envelope_schema)), "phase advanced with incomplete artifact readback"))

    untracked_ref = write_test_source(_TEST_SOURCE_ROOT, "test/untracked.json", b"untracked source\n")
    check("T-D10-165-negative-untracked-source", lambda: require(any("not tracked at the expected Git HEAD" in e for e in verify_source_ref(untracked_ref, _TEST_SOURCE_ROOT, _TEST_SOURCE_HEAD, _TEST_SOURCE_HEAD, True)[0]), "untracked working-tree file accepted as evidence"))

    outside = _TEST_SOURCE_ROOT.parent / f"{_TEST_SOURCE_ROOT.name}-outside.json"
    outside.write_bytes(b"outside repository\n")
    escape_link = _TEST_SOURCE_ROOT / "test" / "escape.json"
    escape_link.symlink_to(outside)
    escape_ref = {"path":"test/escape.json","blob_sha":git_blob_sha1(outside.read_bytes()),"anchor":"escape test","verification":"VERIFIED"}
    def reject_symlink_escape() -> None:
        try:
            errs = verify_source_ref(escape_ref, _TEST_SOURCE_ROOT, _TEST_SOURCE_HEAD, _TEST_SOURCE_HEAD, True)[0]
            require(any("escapes the verified repository root" in e for e in errs), "symlink escape accepted")
        finally:
            escape_link.unlink(missing_ok=True)
            outside.unlink(missing_ok=True)
    check("T-D10-166-negative-symlink-source-escape", reject_symlink_escape)

    check("T-D10-167-negative-unexpected-source-head", lambda: require(any("independently expected HEAD" in e for e in validate_bundle({**base_bundle(),"source_head":"f"*40}, contract, _TEST_SOURCE_ROOT, _TEST_SOURCE_HEAD)), "bundle-supplied source HEAD overrode external expected HEAD"))
    traversal_ref = {"path":"../outside.json","blob_sha":"a"*40,"anchor":"traversal test","verification":"VERIFIED"}
    check("T-D10-168-negative-source-path-traversal", lambda: require(any("escapes the verified repository root" in e for e in verify_source_ref(traversal_ref, _TEST_SOURCE_ROOT, _TEST_SOURCE_HEAD, _TEST_SOURCE_HEAD, True)[0]), "path traversal source accepted"))

    fake_hidden = base_bundle([artifact("actor", actor("A"), "GM_HIDDEN")])
    fake_hidden["effective_gm_hidden_segregation"] = True
    check("T-D10-169-negative-caller-asserted-segregation", lambda: require(adapt_for_role(fake_hidden, "DRAMATURGO", contract, _TEST_SOURCE_ROOT)["status"] == "HOLD", "caller boolean released hidden payload"))

    failed_validation_envelope = {**phase_envelope,"validation":{"status":"FAIL","passed":0,"total":1}}
    check("T-D10-170-negative-success-envelope-with-failed-validation", lambda: require(any("every validation check" in e for e in validate_phase_envelope(failed_validation_envelope, envelope_schema)), "successful gate advanced with failed validation"))

    hidden_envelope = {**phase_envelope,"artifacts":[{"path":"novydres/runtime/narrative-architecture/program/deliverables/secret.json","blob_sha":"a"*40,"spoiler_class":"GM_HIDDEN"}]}
    check("T-D10-171-negative-envelope-GM-hidden-artifact", lambda: require(bool(validate_phase_envelope(hidden_envelope, envelope_schema)), "phase envelope published GM_HIDDEN artifact"))

    invalid_d12 = {**phase_envelope,"phase":"D12","next_phase":None,"publication":{"status":"PUSHED","branch":"master","readback_verified":False},"publication_record":{**good_publication,"target_branch":"master","force_push":True,"parent":"9"*40,"remote_head_after":"8"*40,"working_tree_clean_before":False}}
    check("T-D10-172-negative-D12-release-without-valid-readback", lambda: require(any("readback" in e or "publication" in e for e in validate_phase_envelope(invalid_d12, envelope_schema)), "D12 release bypassed publication validation"))

    valid_prior_gates = {f"D{number:02d}":"PASS_WITH_UNKNOWN" for number in range(1, 12)}
    valid_d12 = {**phase_envelope,"phase":"D12","next_phase":None,"prior_phase_gates":valid_prior_gates}
    check("T-D10-173-positive-D12-final-publication-record", lambda: require(not validate_phase_envelope(valid_d12, envelope_schema), str(validate_phase_envelope(valid_d12, envelope_schema))))

    pending_approval_d12 = {**valid_d12,"pending_player_approvals":["PLAYER_DECISION_REQUIRED"]}
    check("T-D10-177-negative-D12-pending-player-approval", lambda: require(any("player approvals remain pending" in e for e in validate_phase_envelope(pending_approval_d12, envelope_schema)), "D12 released with unresolved player approval"))

    incomplete_prior_gates = {**valid_d12,"prior_phase_gates":{**valid_prior_gates,"D10":"FAIL"}}
    missing_prior_gates = {key:value for key,value in valid_d12.items() if key != "prior_phase_gates"}
    check("T-D10-178-negative-D12-missing-or-failed-prior-gates", lambda: require(any("prior_phase_gates" in e for e in validate_phase_envelope(missing_prior_gates, envelope_schema)) and any("approved gates for every phase" in e for e in validate_phase_envelope(incomplete_prior_gates, envelope_schema)), "D12 released without all prior phase gates"))

    late_acquisition = base_bundle([artifact("actor", actor("A", ["K1"])), artifact("knowledge", knowledge())])
    late_acquisition["event_ids"] = ["E1", "E2"]
    late_acquisition["acquisition_records"] = [{"acquisition_id":"ACQ1","knower_id":"A","event_id":"E2","method":"OBSERVED","evidence_id":"EV1","source":source()}]
    check("T-D10-174-negative-knowledge-before-acquisition", lambda: require(any("predates its acquisition" in e for e in validate_bundle(late_acquisition, contract)), "knowledge predating acquisition was accepted"))

    wrong_scope = base_bundle([artifact("retcon", applied)])
    wrong_scope["decision_records"] = [{"decision_id":"APP1","decision_maker":"PLAYER","decision_kind":"RETCON_APPROVAL","scope":"GENERAL","affected_refs":["E1"],"event_id":"E1","evidence_id":"EV1","source":source()}]
    check("T-D10-175-negative-retcon-decision-wrong-scope", lambda: require(any("express player approval" in e for e in validate_bundle(wrong_scope, contract)), "general decision was accepted as exact retcon approval"))

    missing_acquisition_source = base_bundle([artifact("actor", actor("A", ["K1"])), artifact("knowledge", knowledge())])
    missing_acquisition_source["acquisition_records"] = [{"acquisition_id":"ACQ1","knower_id":"A","event_id":"E1","method":"OBSERVED","evidence_id":"EV1"}]
    check("T-D10-176-negative-acquisition-without-source", lambda: require(any("source-backed acquisition" in e for e in validate_bundle(missing_acquisition_source, contract)), "caller-authored acquisition record without Git source accepted"))

    check("T-D10-153-role-contract-requires-semantic-validation", lambda: require("semantic_validation_passed_for_exact_payload" in roles.get("roles",{}).get("NARRATOR",{}).get("preconditions",[]), "role contract omits semantic prevalidation"))
    check("T-D10-154-runner-test-ids-unique", lambda: require(len({item["id"] for item in results}) == len(results), "test catalog IDs are duplicated"))

    def catalog_alignment() -> None:
        catalog_ids = [item.get("id") for item in test_catalog.get("test_cases", [])]
        actual_ids = [item["id"] for item in results]
        candidate_id = "T-D10-156-catalog-matches-runner"
        require(catalog_ids == actual_ids + [candidate_id], "catalog IDs/order do not exactly match executable assertions")
    check("T-D10-156-catalog-matches-runner", catalog_alignment)

    return results


def initialize_test_repository(root: Path) -> str:
    fixture_path = root / "test" / "fixture.json"
    fixture_path.parent.mkdir(parents=True, exist_ok=True)
    fixture_path.write_bytes(b"NOVYDRES D10 synthetic source fixture\n")
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "D10 Test"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "d10-test@example.invalid"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["git", "-C", str(root), "add", "test/fixture.json"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "D10 synthetic test fixture"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return git_output(root, "rev-parse", "HEAD")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="run executable schema and adversarial checks")
    parser.add_argument("--expected-gate", choices=["PASS", "PASS_WITH_UNKNOWN", "FAIL"])
    parser.add_argument("--bundle", type=Path, help="validate one D01 artifact bundle")
    parser.add_argument("--repo-root", type=Path, help="repository root used to resolve and verify source blobs")
    parser.add_argument("--expected-source-head", help="independently verified Git HEAD for every source reference")
    parser.add_argument("--role", choices=["PLAYER", "NARRATOR", "DRAMATURGO", "AUDITOR", "ORCHESTRATOR"], help="apply a proposed role projection to the validated bundle")
    args = parser.parse_args()
    try:
        registry, contract = load_registry()
        roles = load_json(ROLE_ADAPTERS_PATH)
        envelope_schema = load_json(ENVELOPE_SCHEMA_PATH)
        test_catalog = load_json(TEST_CATALOG_PATH)
    except Exception as exc:
        print(f"D10 bootstrap FAIL: {exc}", file=sys.stderr)
        return 2
    if args.self_test:
        global _TEST_SOURCE_ROOT, _TEST_SOURCE_HEAD
        with tempfile.TemporaryDirectory(prefix="novydres-d10-tests-") as temp_root:
            _TEST_SOURCE_ROOT = Path(temp_root)
            _TEST_SOURCE_HEAD = initialize_test_repository(_TEST_SOURCE_ROOT)
            results = run_tests(registry, contract, roles, envelope_schema, test_catalog)
        _TEST_SOURCE_ROOT = None
        _TEST_SOURCE_HEAD = None
        for item in results:
            suffix = f" — {item['detail']}" if item["result"] == "FAIL" else ""
            print(f"{item['id']}: {item['result']}{suffix}")
        failed = sum(item["result"] != "PASS" for item in results)
        gate = "FAIL" if failed else "PASS_WITH_UNKNOWN"  # D01 remains an unapproved proposal.
        print(f"RESULT {len(results)-failed}/{len(results)}; gate={gate}")
        if args.expected_gate and args.expected_gate != gate:
            print(f"EXPECTED_GATE_MISMATCH expected={args.expected_gate} actual={gate}", file=sys.stderr)
            return 1
        return 1 if failed else 0
    if args.bundle:
        if not args.repo_root or not args.expected_source_head or not SHA1_RE.fullmatch(args.expected_source_head):
            print("D10 validation FAIL: --repo-root and an independently verified --expected-source-head are required.", file=sys.stderr)
            return 2
        try:
            bundle = load_json(args.bundle)
        except Exception as exc:
            print(f"D10 validation FAIL: cannot load bundle: {exc}", file=sys.stderr)
            return 2
        errors = validate_bundle(bundle, contract, args.repo_root, args.expected_source_head)
        if errors:
            print(json.dumps({"status":"FAIL","errors":errors},ensure_ascii=False,indent=2))
            return 1
        if args.role:
            adapted = adapt_for_role(bundle, args.role, contract, args.repo_root, args.expected_source_head)
            print(json.dumps(adapted,ensure_ascii=False,indent=2))
            return 0 if adapted["status"] in {"ALLOW_READ_ONLY", "HOLD"} else 1
        print(json.dumps({"status":"PASS","artifact_count":len(bundle.get("artifacts",[]))},ensure_ascii=False))
        return 0
    parser.error("choose --self-test or --bundle")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

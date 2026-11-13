"""Novydres Web-first Chronicle Core v0.2 — deterministic stateless operations.
The *single* Drive document is the authoritative serialised store. This code has
no Google credentials or network access. The ChatGPT tool relay performs I/O.
"""
from __future__ import annotations
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import secrets
from typing import Any

VERSION = "0.2.0"
SCHEMA = "NOVYDRES_WEBFIRST_STORE_V1"
GENESIS = "0" * 64
SOURCE_FACTS = {"PLAYER_DECLARATION", "NPC_ACTION", "WORLD_EVENT", "MECHANICAL_RESULT", "CORRECTION", "CHARACTER_IMPORT", "SYSTEM"}
NONFACT = {"PLAYER_INTENT", "NPC_CLAIM", "GM_PLAN", "GM_PROPOSAL"}
VISIBILITIES = {"PLAYER_PUBLIC", "PC_KNOWN", "GM_HIDDEN", "SYSTEM_AUDIT"}
PC_VOLUNTARY = {"PLAYER_DECLARATION", "CHARACTER_IMPORT"}
PC_PROTECTED = {"pc.location", "pc.action", "pc.speech", "pc.choice", "pc.xp.available", "pc.willpower.current"}
OPTIONAL = {"pc.xp.available", "pc.willpower.current"}
V5_RULES = {"V5_BASIC_POOL", "V5_BASIC_ROUSE"}

class ValidationError(ValueError):
    pass

def canonical(v: Any) -> str:
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def sha(v: Any) -> str:
    return hashlib.sha256(canonical(v).encode("utf-8")).hexdigest()

def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def create_store() -> dict:
    return {"schema": SCHEMA, "engine_version": VERSION,
            "chronicle_id": None, "phase": "PREPARATION", "session_id": None,
            "initial_state": {}, "state": {}, "events": [], "rolls": [],
            "last_hash": GENESIS, "last_seq": 0, "last_roll_seq": 0, "last_roll_hash": GENESIS}

def _expect(ok: bool, message: str):
    if not ok: raise ValidationError(message)

def _event_digest(prev_hash: str, unsigned_event: dict) -> str:
    return sha({"prev_hash": prev_hash, "event": unsigned_event})

def validate_store(store: dict) -> dict:
    _expect(isinstance(store, dict) and store.get("schema") == SCHEMA, "Invalid store schema")
    _expect(store.get("chronicle_id") is None or isinstance(store["chronicle_id"], str), "Invalid chronicle")
    _expect(isinstance(store.get("events"), list) and isinstance(store.get("rolls"), list), "Missing ledgers")
    _expect(isinstance(store.get("initial_state"), dict) and isinstance(store.get("state"), dict), "Missing state")
    _expect(store["initial_state"] == {} or store.get("chronicle_id"), "Initial character state requires a chronicle")
    state = deepcopy(store["initial_state"])
    prev = GENESIS
    ids = set()
    for i, e in enumerate(store["events"], 1):
        _expect(isinstance(e, dict), "Event not object")
        _expect(e.get("seq") == i and e.get("id") == f"EVT-{i:06d}", "Event sequence mismatch")
        _expect(e.get("kind") in SOURCE_FACTS | NONFACT, "Bad event kind")
        _expect(e.get("prev_hash") == prev, "Event chain broken")
        _expect(e.get("id") not in ids, "Duplicate event")
        ids.add(e["id"])
        _expect(isinstance(e.get("deltas"), list), "Missing event deltas")
        if e["kind"] in NONFACT:
            _expect(not e["deltas"], "Plan/intent/claim cannot change actual state")
        if e["kind"] in PC_VOLUNTARY:
            _expect(e.get("declaration", "") and e.get("text") == e["declaration"], "PC action not literal")
        if e.get("kind") == "CORRECTION":
            _expect(e.get("target_id") in ids and e["target_id"] != e["id"], "Correction requires prior event")
            _expect(e.get("player_approval"), "Correction requires player approval")
        for ref in e.get("causal_refs", []):
            _expect(ref in ids and ref != e["id"], "Causal reference absent")
        unsigned = {k:v for k,v in e.items() if k not in ("prev_hash", "hash")}
        _expect(e.get("hash") == _event_digest(prev, unsigned), "Event digest mismatch")
        for delta in e["deltas"]:
            _expect(isinstance(delta, dict) and isinstance(delta.get("field"), str), "Bad delta")
            field = delta["field"]
            _expect(state.get(field) == delta.get("before"), "State before mismatch")
            state[field] = delta.get("after")
        prev = e["hash"]
    _expect(store["state"] == state, "Materialized state != events")
    _expect(store.get("last_hash") == prev, "Last hash incorrect")
    _expect(store.get("last_seq") == len(store["events"]), "Sequence incorrect")
    all_roll_ids = set()
    roll_prev = GENESIS
    for i,r in enumerate(store["rolls"], 1):
        _expect(r.get("id") == f"ROLL-{i:06d}", "Roll sequence mismatch")
        _expect(r["id"] not in all_roll_ids, "Duplicate roll")
        all_roll_ids.add(r["id"])
        _expect(r.get("event_id") in ids, "Roll without committed event")
        _expect(r.get("prev_hash") == roll_prev, "Roll chain broken")
        raw_roll = {k:v for k,v in r.items() if k not in ("prev_hash", "hash")}
        _expect(r.get("hash") == _event_digest(roll_prev, raw_roll), "Roll digest mismatch")
        roll_prev = r["hash"]
        if r.get("rule_ref") == "V5_BASIC_POOL":
            computed=score_pool(r["normal"],r["hunger"],r["difficulty"])
            _expect(computed == r.get("computed"), "Roll outcome tampered")
        elif r.get("rule_ref") == "V5_BASIC_ROUSE":
            _expect(r.get("die") in range(1,11) and r.get("success") == (r["die"] >= 6), "Rouse outcome tampered")
        else:
            raise ValidationError("Unrecognized rule ref")
    _expect(store.get("last_roll_seq") == len(store["rolls"]), "Roll count incorrect")
    _expect(store.get("last_roll_hash") == roll_prev, "Last roll hash incorrect")
    return {"ok": True, "events":len(ids), "rolls":len(all_roll_ids),
            "last_event":f"EVT-{len(ids):06d}" if ids else None,
            "last_roll":f"ROLL-{len(all_roll_ids):06d}" if all_roll_ids else None,
            "last_hash": prev, "phase":store["phase"], "state":deepcopy(state)}

def score_pool(normal: list[int], hunger: list[int], difficulty: int) -> dict:
    _expect(type(difficulty) == int and 0 <= difficulty <= 20, "Difficulty must be 0..20")
    _expect(isinstance(normal, list) and isinstance(hunger, list), "Dice arrays required")
    _expect(0 < len(normal)+len(hunger) <= 50 and len(hunger) <= 5, "Invalid pool")
    _expect(all(type(v)==int and 1<=v<=10 for v in normal+hunger), "Invalid die")
    nums=normal+hunger
    pairs=sum(v==10 for v in nums)//2
    successes=sum(v>=6 for v in nums)+pairs*2
    passed=successes>=difficulty
    return {"successes":successes,"critical_pairs":pairs,"critical":pairs>0,
            "messy_critical":pairs>0 and 10 in hunger,
            "bestial_failure":not passed and 1 in hunger,
            "passed":passed,"margin":successes-difficulty}

def _normalize_deltas(store: dict, cmd: dict) -> list:
    deltas=cmd.get("deltas",[])
    _expect(isinstance(deltas,list), "deltas must be list")
    seen=set()
    for d in deltas:
        _expect(isinstance(d,dict) and set(d)=={"field","before","after","reason"}, "Bad delta shape")
        _expect(isinstance(d["field"],str) and d["field"], "Invalid field")
        _expect(d["field"] not in seen, "Repeated field update")
        seen.add(d["field"])
        _expect(d["before"]==store["state"].get(d["field"]), "Stale state before")
        _expect(isinstance(d["reason"],str) and d["reason"], "Delta requires cause")
        if d["field"] in OPTIONAL:
            _expect(cmd.get("player_approval") is not None, "Optional spend must be explicitly authorized")
        if d["field"] in PC_PROTECTED and cmd["kind"] not in ("PLAYER_DECLARATION", "CHARACTER_IMPORT", "CORRECTION"):
            _expect(cmd.get("rule_ref") is not None and cmd.get("causal_refs"), "PC protected state requires evidence")
        if d["field"] == "pc.hunger":
            _expect(cmd.get("rule_ref") is not None and bool(cmd.get("causal_refs")), "Hunger change requires rule and causal event")
            _expect(type(d["after"])==int and 0<=d["after"]<=5, "Hunger range")
        if d["field"] == "pc.willpower.current":
            _expect(type(d["after"])==int and 0<=d["after"]<=20, "Willpower range")
        if d["field"] == "pc.xp.available":
            _expect(type(d["after"])==int and d["after"]>=0, "Negative XP")
    return deltas

def append_event(store: dict, cmd:dict) -> dict:
    validate_store(store)
    _expect(isinstance(cmd, dict), "Bad command")
    kind=cmd.get("kind")
    _expect(kind in SOURCE_FACTS|NONFACT, "Invalid event kind")
    _expect(cmd.get("canon_change") is not True, "Scenario canon is immutable")
    _expect(isinstance(cmd.get("text"),str) and cmd["text"].strip(), "Missing text")
    _expect(cmd.get("visibility","PLAYER_PUBLIC") in VISIBILITIES, "Bad visibility")
    actor=cmd.get("actor")
    _expect(isinstance(actor,str) and bool(actor.strip()), "Missing actor")
    if actor == "pc":
        _expect(kind=="PLAYER_DECLARATION" or kind=="CHARACTER_IMPORT", "GM cannot declare PC voluntary action")
    if kind=="PLAYER_DECLARATION":
        _expect(actor=="pc" and cmd.get("declaration")==cmd["text"], "PC event must quote the player's actual message")
        _expect(cmd.get("declaration_ref"), "PC event requires source message reference")
        _expect(cmd.get("declaration_class") in {"ATTEMPT","ACTION","SPEECH","CHOICE"}, "Missing declaration class")
    if kind=="CHARACTER_IMPORT":
        _expect(actor=="pc" and cmd.get("player_approval"), "Import requires explicit player approval")
        _expect(cmd.get("declaration")==cmd["text"] and cmd.get("declaration_ref"), "Import requires quoted approval")
    if kind=="CORRECTION":
        _expect(cmd.get("target_id") in {e["id"] for e in store["events"]}, "Correction target absent")
        _expect(cmd.get("player_approval"), "Correction requires explicit approval")
    refs=cmd.get("causal_refs",[])
    _expect(isinstance(refs,list) and all(r in {e["id"] for e in store["events"]} for r in refs), "Causality references unverified")
    deltas=_normalize_deltas(store,cmd)
    if kind in NONFACT: _expect(not deltas, "Plans and claims cannot mutate factual state")
    if kind == "PLAYER_DECLARATION" and cmd.get("declaration_class")=="ATTEMPT":
        _expect(not deltas, "Attempt cannot itself resolve an action or update location")
    if kind=="NPC_ACTION" and cmd.get("knowledge_used"):
        known=set(store["state"].get("knowledge."+actor,[]))
        _expect(all(k in known for k in cmd["knowledge_used"]), "NPC uses unverified knowledge")
    if cmd.get("rule_ref") is not None:
        _expect(isinstance(cmd["rule_ref"],str) and cmd["rule_ref"],"rule_ref must be nonempty")
    event={"seq":len(store["events"])+1,"id":f"EVT-{len(store['events'])+1:06d}",
           "kind":kind,"actor":actor,"text":cmd["text"],
           "declaration":cmd.get("declaration"),"declaration_ref":cmd.get("declaration_ref"),
           "declaration_class":cmd.get("declaration_class"),"player_approval":cmd.get("player_approval"),
           "causal_refs":refs,"deltas":deltas,"rule_ref":cmd.get("rule_ref"),
           "visibility":cmd.get("visibility","PLAYER_PUBLIC"),"knowledge_used":cmd.get("knowledge_used",[]),
           "target_id":cmd.get("target_id"),"diegetic_time":cmd.get("diegetic_time"),
           "location":cmd.get("location"),"source":cmd.get("source"),"timestamp_utc":cmd.get("timestamp_utc",utcnow()),
           "prev_hash":store["last_hash"]}
    unsigned={k:v for k,v in event.items() if k not in ("prev_hash","hash")}
    event["hash"]=_event_digest(event["prev_hash"],unsigned)
    updated=deepcopy(store)
    updated["events"].append(event)
    updated["last_seq"]=event["seq"]
    updated["last_hash"]=event["hash"]
    for d in deltas: updated["state"][d["field"]]=d["after"]
    validate_store(updated)
    return updated

def prepare_pool(pool:int,hunger:int,difficulty:int,rule_ref="V5_BASIC_POOL") -> dict:
    _expect(type(pool)==int and 1<=pool<=50,"Pool 1..50")
    _expect(type(hunger)==int and 0<=hunger<=min(5,pool),"Hunger count invalid")
    _expect(type(difficulty)==int and 0<=difficulty<=20,"Difficulty invalid")
    _expect(rule_ref=="V5_BASIC_POOL", "Only V5_BASIC_POOL implemented")
    return {"pool":pool,"hunger":hunger,"difficulty":difficulty,"rule_ref":rule_ref}

def apply_pool_roll(store:dict, spec:dict, *, source_event_id:str, rng=None) -> dict:
    validate_store(store)
    prepare_pool(spec["pool"],spec["hunger"],spec["difficulty"],spec.get("rule_ref", "V5_BASIC_POOL"))
    _expect(source_event_id in {e["id"] for e in store["events"]}, "Roll requires committed source action")
    plan=store["events"][-1]
    _expect(plan["id"]==source_event_id and plan["kind"]=="SYSTEM" and plan["rule_ref"]=="V5_BASIC_POOL", "Roll requires latest committed preparation event")
    _expect(plan["source"] == {"roll_spec":prepare_pool(spec["pool"],spec["hunger"],spec["difficulty"],spec.get("rule_ref", "V5_BASIC_POOL"))}, "Dice specification differs from committed preparation")
    _expect(not any(r["source_event_id"]==source_event_id for r in store["rolls"]), "Source event already rolled")
    rnd=rng if rng is not None else secrets.SystemRandom()
    normal=[rnd.randrange(1,11) for _ in range(spec["pool"]-spec["hunger"])]
    hunger=[rnd.randrange(1,11) for _ in range(spec["hunger"])]
    computed=score_pool(normal,hunger,spec["difficulty"])
    return _commit_roll(store, {"rule_ref":"V5_BASIC_POOL","source_event_id":source_event_id,
                                "normal":normal,"hunger":hunger,"difficulty":spec["difficulty"],
                                "computed":computed,"engine_version":VERSION})

def apply_rouse(store:dict, *, source_event_id:str, rng=None) -> dict:
    validate_store(store)
    _expect(source_event_id in {e["id"] for e in store["events"]},"Rouse requires source event")
    plan=store["events"][-1]
    _expect(plan["id"]==source_event_id and plan["kind"]=="SYSTEM" and plan["rule_ref"]=="V5_BASIC_ROUSE", "Rouse requires latest committed preparation event")
    _expect(plan["source"] == {"roll_spec":{"rule_ref":"V5_BASIC_ROUSE"}}, "Rouse preparation invalid")
    _expect(not any(r["source_event_id"]==source_event_id for r in store["rolls"]), "Source event already rolled")
    rnd=rng if rng is not None else secrets.SystemRandom()
    die=rnd.randrange(1,11)
    return _commit_roll(store,{"rule_ref":"V5_BASIC_ROUSE","source_event_id":source_event_id,
                              "die":die,"success":die>=6,"engine_version":VERSION})

def _commit_roll(store:dict, roll:dict) -> dict:
    """Record roll and mechanical outcome in one serialised Drive-store mutation.
    For Rouse: hunger effect is NOT applied until verified as separate mechanical delta.
    """
    updated=deepcopy(store)
    roll["id"]=f"ROLL-{len(updated['rolls'])+1:06d}"
    roll["event_id"]=updated["events"][-1]["id"]
    roll["timestamp_utc"]=utcnow()
    roll["prev_hash"]=updated["last_roll_hash"]
    roll["hash"]=_event_digest(roll["prev_hash"],{k:v for k,v in roll.items() if k not in ("prev_hash", "hash")})
    updated["rolls"].append(roll)
    updated["last_roll_seq"]=len(updated["rolls"])
    updated["last_roll_hash"]=roll["hash"]
    validate_store(updated)
    return updated

def serialize_store(store:dict)->str:
    validate_store(store)
    return canonical(store)

def parse_store(text:str)->dict:
    _expect(isinstance(text,str),"Store must be text")
    store=json.loads(text.strip())
    validate_store(store)
    return store

def plan_drive_replace(old_text:str,new_store:dict)->dict:
    """Connector-neutral CAS instructions; the ChatGPT relay must fetch revisionId.
    Requires single read/written DOC with exactly one JSON text body.
    """
    old=parse_store(old_text)
    _expect(new_store.get("last_seq",0)>=old["last_seq"],"Cannot shorten event ledger")
    _expect(new_store.get("last_roll_seq",0)>=old["last_roll_seq"],"Cannot shorten roll ledger")
    _expect(new_store["events"][:old["last_seq"]]==old["events"],"Historical event mutated")
    _expect(new_store["rolls"][:old["last_roll_seq"]]==old["rolls"],"Historical roll mutated")
    _expect(new_store.get("chronicle_id")==old.get("chronicle_id") and new_store.get("initial_state")==old.get("initial_state"), "Unauthorized meta/initial-state rewrite")
    validate_store(new_store)
    return {"containsText":{"text":canonical(old),"matchCase":True},"replaceText":canonical(new_store)}

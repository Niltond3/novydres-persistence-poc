"""Deterministic *library* for classified corridor intersections.

Never derives road grade, graph connectivity or editorial authority from pixels.
Called only by scripts/pipeline.py; does not promote infrastructure acceptance.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
from pathlib import Path

from jsonschema import Draft202012Validator

EPS = 1e-7
RELATIONS = {"at_grade", "grade_separated", "no_connection"}


class TopologyInvalid(ValueError):
    pass


def require(ok, reason):
    if not ok:
        raise TopologyInvalid(reason)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"),
                        ensure_ascii=False).encode("utf-8")).hexdigest()


def close(a, b):
    return math.dist(a, b) <= EPS


def xy(p):
    return (isinstance(p, list) and len(p) == 2 and
            all(type(v) in (int, float) and math.isfinite(v) for v in p))


def _cross(v, w):
    return v[0]*w[1]-v[1]*w[0]


def _intersect(a, b, c, d):
    v = (b[0]-a[0], b[1]-a[1])
    w = (d[0]-c[0], d[1]-c[1])
    den = _cross(v, w)
    q = (c[0]-a[0], c[1]-a[1])
    if abs(den) <= EPS:
        if abs(_cross(q, v)) > EPS:
            return None
        axis = 0 if abs(v[0]) >= abs(v[1]) else 1
        overlap = min(max(a[axis], b[axis]), max(c[axis], d[axis])) - max(
            min(a[axis], b[axis]), min(c[axis], d[axis]))
        return "OVERLAP" if overlap > EPS else None
    t = _cross(q, w)/den
    u = _cross(q, v)/den
    if -EPS <= t <= 1+EPS and -EPS <= u <= 1+EPS:
        # exact segment intersection, no near-miss snapping
        return [a[0]+min(1, max(0, t))*v[0], a[1]+min(1, max(0, t))*v[1]]
    return None


def _key(a, b, point):
    return tuple(sorted((a, b))) + tuple(round(v, 8) for v in point)


def _level(edge, model):
    if model == "urban" and edge.get("class") == "ramp":
        return None  # changing-grade ramp requires independent surveyed subdivision
    return edge.get("level")


def _model(data):
    if data.get("schema") == "NOVYDRES_MAPWORK_INFRA_GEOMETRY":
        return "infra", "network"
    if data.get("schema") == "NOVYDRES_MAPWORK_TERRITORY_NETWORK":
        return "urban", "transport"
    raise TopologyInvalid("unsupported spatial candidate schema")


def _observations(network, model):
    edges = network.get("edges")
    nodes = network.get("nodes")
    require(isinstance(edges, list) and isinstance(nodes, list),
            "network nodes/edges absent")
    byedge = {}
    bynode = {}
    for node in nodes:
        require(isinstance(node, dict) and isinstance(node.get("id"), str) and
                node["id"] not in bynode and xy(node.get("point")) and
                type(node.get("level")) is int, "invalid node coordinates/level/identity")
        bynode[node["id"]] = node
    for edge in edges:
        require(isinstance(edge, dict) and isinstance(edge.get("id"), str) and
                edge["id"] not in byedge and isinstance(edge.get("points"), list) and
                len(edge["points"]) >= 2 and all(xy(p) for p in edge["points"]) and
                edge.get("from") in bynode and edge.get("to") in bynode and
                edge["from"] != edge["to"], "invalid source edge")
        pts = edge["points"]
        require(all(math.dist(a, b) > EPS for a, b in zip(pts, pts[1:])),
                "degenerate source edge")
        require(close(pts[0], bynode[edge["from"]]["point"]) and
                close(pts[-1], bynode[edge["to"]]["point"]),
                "source edge endpoints mismatch")
        require((_level(edge, model) is None and model=="urban" and edge.get("class")=="ramp" and
                 type(edge.get("level_from")) is int and type(edge.get("level_to")) is int) or
                type(_level(edge, model)) is int,
                "source edge level missing")
        byedge[edge["id"]] = edge
    # One event per exact point/pair; a pair can have multiple independent events.
    events = {}
    ids = sorted(byedge)
    for i, ia in enumerate(ids):
        a = byedge[ia]
        for ib in ids[i+1:]:
            b = byedge[ib]
            for x, y in zip(a["points"], a["points"][1:]):
                for z, w in zip(b["points"], b["points"][1:]):
                    pt = _intersect(x, y, z, w)
                    if pt is None:
                        continue
                    if pt == "OVERLAP":
                        # A tram may explicitly share a road carriageway.
                        shared = ((a.get("mode")=="road" or a.get("class") in
                                   ("street","collector","avenue","arterial","expressway","service")) and
                                  (b.get("mode")=="tram" or b.get("class")=="tram") and
                                   b.get("shared_with_road") is True) or (
                                  (b.get("mode")=="road" or b.get("class") in
                                   ("street","collector","avenue","arterial","expressway","service")) and
                                  (a.get("mode")=="tram" or a.get("class")=="tram") and
                                   a.get("shared_with_road") is True)
                        if shared:
                            continue
                        key = (ia, ib, "OVERLAP")
                        events[key] = {"corridors": [ia, ib], "point": None,
                                       "reason": "COLLINEAR_OVERLAP"}
                        continue
                    common = {a["from"], a["to"]} & {b["from"], b["to"]}
                    # Already incident in the source graph: no new semantic claim.
                    if any(close(pt, bynode[n]["point"]) for n in common):
                        continue
                    key = _key(ia, ib, pt)
                    events[key] = {"corridors": [ia, ib], "point": pt,
                                   "reason": "CLASSIFICATION_REQUIRED"}
    return events, byedge, bynode


def _check_record(record, event, byedge, model, reference_sha):
    ids = event["corridors"]
    pt = event["point"]
    require(isinstance(record.get("id"),str) and bool(record["id"].strip()),
            "classification requires a stable identity")
    require(record.get("status") == "RESOLVED" and record.get("relation") in RELATIONS,
            "unresolved crossing cannot authorize geometry")
    require(record.get("corridors") == ids and xy(record.get("point")) and
            close(record["point"], pt), "crossing classification mismatches geometry")
    visual = record.get("visual")
    require(isinstance(visual, dict) and visual.get("inspected_by") == "AGENT" and
            visual.get("reference_sha256") == reference_sha and
            isinstance(visual.get("observation"), str) and
            len(visual["observation"].strip()) >= 24 and
            isinstance(visual.get("bbox"), list) and len(visual["bbox"]) == 4 and
            all(type(v) in (int, float) and math.isfinite(v) for v in visual["bbox"]) and
            visual["bbox"][0] <= pt[0] <= visual["bbox"][2] and
            visual["bbox"][1] <= pt[1] <= visual["bbox"][3],
            "crossing requires U02-bound agent visual observation and crop")
    require(isinstance(record.get("geometry_observation"), str) and
            len(record["geometry_observation"].strip()) >= 16,
            "crossing requires geometric observation")
    levels = {eid: _level(byedge[eid], model) for eid in ids}
    require(all(type(v) is int for v in levels.values()),
            "crossing on changing-grade ramp needs surveyed level; no inference")
    require(record.get("levels") == levels,
            "grade may not be invented or altered by classification")
    relation = record["relation"]
    require((levels[ids[0]] == levels[ids[1]]) == (relation != "grade_separated"),
            "classified relation contradicts actual levels")
    if relation == "no_connection" and levels[ids[0]] == levels[ids[1]]:
        require(isinstance(record.get("barrier_evidence"), str) and
                len(record["barrier_evidence"].strip()) >= 12,
                "same-level nonconnection requires physical barrier evidence")
    editorial = record.get("editorial")
    require(isinstance(editorial, dict) and type(editorial.get("new_element")) is bool,
            "explicit existing/new element editorial status required")
    authority = (isinstance(editorial.get("decision_id"), str) and
                 bool(editorial["decision_id"].strip()) and
                 isinstance(editorial.get("evidence"), str) and
                 len(editorial["evidence"].strip()) >= 12 and
                 editorial.get("status") == "APPROVED")
    special = (relation == "at_grade" and any(
        byedge[eid].get("mode") in ("rail", "metro") or
        byedge[eid].get("class") in ("rail_main", "rail_freight", "rail_siding", "metro") or
        byedge[eid].get("protected_structure_id") for eid in ids))
    require(not (editorial["new_element"] or special) or authority,
            "new/protected/rail at-grade element lacks explicit owner decision")
    return authority


def _distance_along(edge, pt):
    distance = 0.0
    matches = []
    pts = edge["points"]
    for a, b in zip(pts, pts[1:]):
        length = math.dist(a, b)
        t = ((pt[0]-a[0])*(b[0]-a[0]) +
             (pt[1]-a[1])*(b[1]-a[1]))/(length*length)
        t = max(0.0, min(1.0, t))
        projection = [a[0]+t*(b[0]-a[0]), a[1]+t*(b[1]-a[1])]
        if close(projection, pt):
            matches.append(distance+t*length)
        distance += length
    require(bool(matches), "classified point absent from source centerline")
    require(len(set(round(v, 7) for v in matches)) == 1,
            "self-overlap/ambiguous chainage cannot be auto-segmented")
    return matches[0]


def _segment(edge, cuts, node_for, original_nodes):
    """Split on arclength, retaining all original intermediate vertices."""
    pts = edge["points"]
    length = 0.0
    vertices = [(0.0, pts[0])]
    for a, b in zip(pts, pts[1:]):
        length += math.dist(a, b)
        vertices.append((length, b))
    entries = [(0.0, edge["from"], pts[0]), (length, edge["to"], pts[-1])]
    for point, node_id in cuts:
        dist = _distance_along(edge, point)
        if dist <= EPS or length-dist <= EPS:
            continue
        require(all(abs(dist-item[0]) > EPS or item[1] == node_id for item in entries),
                "conflicting junction identities on one source polyline")
        entries.append((dist, node_id, point))
    entries.sort(key=lambda item: item[0])
    parts = []
    for i, (start, a, start_pt) in enumerate(entries[:-1]):
        end, b, end_pt = entries[i+1]
        require(end-start > EPS and a != b, "degenerate split segment")
        middle = [p for dist, p in vertices if start+EPS < dist < end-EPS]
        line = [list(start_pt)] + [list(p) for p in middle] + [list(end_pt)]
        require(all(math.dist(p, q) > EPS for p, q in zip(line, line[1:])),
                "duplicate consecutive vertices in split")
        item = copy.deepcopy(edge)
        item["id"] = edge["id"] if len(entries) == 2 else edge["id"]+"~"+str(i+1).zfill(3)
        item["from"], item["to"], item["points"] = a, b, line
        if len(entries) != 2:
            item["source_edge_id"] = edge["id"]
        parts.append(item)
    rebuilt = [p for part in parts for p in part["points"][:-1]] + [parts[-1]["points"][-1]]
    # Split additions must be collinear points on the original polyline.
    assert close(rebuilt[0], pts[0]) and close(rebuilt[-1], pts[-1])
    return parts


def reconcile(data, classifications, *, protected_edges=(), protected_nodes=()):
    """Return (candidate, diagnostic), never an acceptance PASS.

    UNRESOLVED/missing entries are individually reported and cannot be promoted.
    The original graph is embedded for deterministic readback/idempotence.
    """
    model, key = _model(data)
    require(isinstance(classifications, dict) and
            classifications.get("schema") == "NOVYDRES_MAPWORK_TOPOLOGY_CLASSIFICATIONS",
            "semantic classification contract missing")
    schema=json.loads((Path(__file__).resolve().parents[1]/
                      "schemas/topology-classifications.schema.json").read_text(encoding="utf-8"))
    errors=list(Draft202012Validator(schema).iter_errors(classifications))
    require(not errors,"semantic classification schema: "+("; ".join(e.message for e in errors[:3])))
    reference_sha = data.get("source_sha256")
    require(classifications.get("reference_sha256") == reference_sha,
            "classifications refer to another U02")
    network = data[key]
    if "topology_source" in network:
        original = network["topology_source"]
        stripped = {k:v for k,v in original.items() if k not in ("topology_source", "topology_audit")}
        raw={**data,key:stripped}
        if model=="urban":
            raw["neighbor_seams"]=network.get("topology_source_seams",data.get("neighbor_seams",[]))
        expected, report = reconcile(raw, classifications,
                                     protected_edges=protected_edges,protected_nodes=protected_nodes)
        require({k:v for k,v in network.items() if k not in ("topology_source","topology_audit")} ==
                {k:v for k,v in expected[key].items() if k not in ("topology_source","topology_audit")},
                "reconciled graph drifted from immutable source")
        require(network.get("topology_audit") == expected[key].get("topology_audit"),
                "topology audit digest/diagnostics altered")
        if model=="urban":
            require(data.get("neighbor_seams",[])==expected.get("neighbor_seams",[]),
                    "neighbor connector was modified after reconciliation")
        return copy.deepcopy(data), report
    require(classifications.get("network_sha256") == digest(network),
            "source network changed; stale crossing classification")
    events, edges, nodes = _observations(network, model)
    provided = classifications.get("crossings")
    require(isinstance(provided, list), "semantic crossing list required")
    records = {}
    for rec in provided:
        require(isinstance(rec, dict) and isinstance(rec.get("corridors"), list) and
                len(rec["corridors"]) == 2 and all(isinstance(v,str) for v in rec["corridors"]) and
                xy(rec.get("point")), "invalid classification key")
        ident = _key(*rec["corridors"], rec["point"])
        require(ident not in records and ident in events, "duplicate/stale crossing classification")
        records[ident] = rec
    resolved = {}
    pending = []
    for ident, event in sorted(events.items(), key=lambda item: str(item[0])):
        if event["reason"] == "COLLINEAR_OVERLAP":
            pending.append({**event, "id":str(ident), "reason":"COLLINEAR_OVERLAP"})
            continue
        record = records.get(ident)
        if record is None or record.get("status") == "UNRESOLVED":
            pending.append({**event, "id":str(ident),
                            "reason":"CLASSIFICATION_REQUIRED" if record is None else
                                     record.get("reason","INSUFFICIENT_VISUAL_EVIDENCE")})
            continue
        authority = _check_record(record, event, edges, model, reference_sha)
        resolved[ident] = (event, record, authority)
    protected = set(protected_edges)
    fixed_nodes = set(protected_nodes)
    require(protected <= set(edges), "protected geometry identifier unknown")
    require(fixed_nodes <= set(nodes), "protected node identifier unknown")
    cuts = {eid:[] for eid in edges}
    additions = {}
    rewrites = {}
    # For each coordinate/level, use the same node ONLY when authorized as a
    # connection. Coincident disconnected crossing nodes remain independent.
    connected = {}
    for ident, (event, record, auth) in resolved.items():
        if record["relation"] != "at_grade":
            continue
        pt = event["point"]
        k = (round(pt[0],8), round(pt[1],8), record["levels"][event["corridors"][0]])
        entry=connected.setdefault(k, {"ids":set(),"point":pt})
        entry["ids"].update(event["corridors"])
    for k, entry in list(connected.items()):
        ids=entry["ids"]
        pt=entry["point"]
        # At the same XY, a path through A-B and A-C implies B-C; no
        # unreviewed transitive connection is permitted.
        for i, ea in enumerate(sorted(ids)):
            for eb in sorted(ids)[i+1:]:
                ident = _key(ea,eb,pt)
                pre_shared={edges[ea]["from"],edges[ea]["to"]} & {
                    edges[eb]["from"],edges[eb]["to"]}
                already_connected=any(close(nodes[n]["point"],pt) for n in pre_shared)
                require(already_connected or (ident in resolved and
                        resolved[ident][1]["relation"]=="at_grade"),
                        "unreviewed transitive junction at "+str(pt))
        endpoint_ids = sorted({nid for eid in ids for nid in
            (edges[eid]["from"],edges[eid]["to"]) if close(nodes[nid]["point"],pt)})
        winner = endpoint_ids[0] if endpoint_ids else "TJ-"+digest([sorted(ids),pt])[:14]
        if endpoint_ids:
            pt=nodes[winner]["point"]
        if not endpoint_ids:
            additions[winner] = {"id":winner,"point":pt,"level":k[2]}
            if model == "urban":
                additions[winner]["kind"] = "rail_crossing" if any(
                    edges[eid].get("class","").startswith("rail") for eid in ids) and any(
                    edges[eid].get("class") in ("street","collector","avenue","arterial",
                        "expressway","ramp","service") for eid in ids) else "intersection"
        elif len(endpoint_ids)>1:
            for nid in endpoint_ids[1:]:
                require(nodes[nid]["level"] == k[2],
                        "cannot join different-level coincident nodes")
                require(nid not in fixed_nodes,
                        "previously accepted node cannot be merged or removed")
                rewrites[nid] = winner
        connected[k] = (ids, winner, pt)
    # Do not turn non-connected pair into a junction through a shared
    # canonical node selected by another crossing at the same location.
    for ident, (event, record, auth) in resolved.items():
        if record["relation"] == "at_grade":
            continue
        ids = event["corridors"]
        if any(set(ids) <= participants for participants, winner, p in connected.values()):
            raise TopologyInvalid("disconnected classification conflicts with connected junction")
    for ident, (event, record, auth) in resolved.items():
        pt = event["point"]
        for eid in event["corridors"]:
            if record["relation"] == "at_grade":
                k=(round(pt[0],8),round(pt[1],8),record["levels"][eid])
                node_id=connected[k][1]
                pt=connected[k][2]
            else:
                edge=edges[eid]
                existing = [nid for nid in (edge["from"],edge["to"])
                            if close(nodes[nid]["point"], pt)]
                node_id = (rewrites.get(existing[0], existing[0]) if existing else
                           "TP-"+digest([eid,pt])[:14])
                if not existing:
                    additions[node_id]={"id":node_id,"point":pt,"level":record["levels"][eid]}
                    if model=="urban":
                        additions[node_id]["kind"]="intersection"
            if eid in protected and _distance_along(edges[eid],pt)>EPS and (
                _distance_along(edges[eid],pt) <
                sum(math.dist(a,b) for a,b in zip(edges[eid]["points"],edges[eid]["points"][1:]))-EPS):
                raise TopologyInvalid("protected/approved centerline may not be segmented: "+eid)
            cuts[eid].append((pt,node_id))
    updated_nodes = copy.deepcopy(nodes)
    for orphan, winner in rewrites.items():
        updated_nodes.pop(orphan)
    updated_nodes.update(additions)
    changed_edges = copy.deepcopy(edges)
    for edge in changed_edges.values():
        before=(edge["from"],edge["to"])
        edge["from"] = rewrites.get(edge["from"],edge["from"])
        edge["to"] = rewrites.get(edge["to"],edge["to"])
        require(edge["id"] not in protected or before==(edge["from"],edge["to"]),
                "protected/approved graph edge endpoint may not be rewritten")
    parts = {}
    for eid in sorted(edges):
        parts[eid] = _segment(changed_edges[eid],cuts[eid],None,updated_nodes)
    all_edges = [e for eid in sorted(parts) for e in parts[eid]]
    require(len({e["id"] for e in all_edges}) == len(all_edges),"duplicate resulting segment ID")
    require(all(e["from"] != e["to"] for e in all_edges),"degenerate resulting graph edge")
    signatures=set()
    for e in all_edges:
        line=tuple(tuple(v) for v in e["points"])
        mode=e.get("mode",e.get("class"))
        signature=(mode,e.get("level",e.get("level_from")),min(line,tuple(reversed(line))))
        require(signature not in signatures,"duplicate co-located segment of same mode/level")
        signatures.add(signature)
    result_crossings = []
    seen = set()
    for ident,(event,rec,auth) in resolved.items():
        a,b = event["corridors"]; pt=event["point"]
        aa=[e for e in parts[a] if close(pt,e["points"][0]) or close(pt,e["points"][-1])]
        bb=[e for e in parts[b] if close(pt,e["points"][0]) or close(pt,e["points"][-1])]
        require(aa and bb, "split did not preserve crossing locus")
        for left in aa:
            for right in bb:
                pair = tuple(sorted((left["id"],right["id"])))
                require(pair not in seen, "multiple crossing loci per segment pair")
                seen.add(pair)
                if model == "infra":
                    item={"a":pair[0],"b":pair[1],"kind":rec["relation"],
                          "point":pt,"classification_id":rec["id"]}
                    if rec["relation"]=="at_grade":
                        node=({left["from"],left["to"]} & {right["from"],right["to"]})
                        require(len(node)==1,"classified at-grade junction not incident")
                        item["authorized_junction_id"]=next(iter(node))
                        if auth:
                            item["authority"] = {k:rec["editorial"][k] for k in
                                                  ("status","decision_id","evidence")}
                    if rec["relation"]=="no_connection":
                        item["barrier_evidence"]=rec.get("barrier_evidence")
                else:
                    item={"id":rec["id"]+"-"+digest(pair)[:8],
                          "edge_a":pair[0],"edge_b":pair[1],
                          "kind":rec["relation"],"point":pt,
                          "classification_id":rec["id"]}
                    if rec["relation"]=="at_grade":
                        node=({left["from"],left["to"]} & {right["from"],right["to"]})
                        require(len(node)==1,"classified at-grade junction not incident")
                        item["junction_id"]=next(iter(node))
                        if auth:
                            item["authority"] = {k:rec["editorial"][k] for k in
                                                  ("status","decision_id","evidence")}
                    if rec["relation"]=="no_connection":
                        item["barrier_evidence"]=rec.get("barrier_evidence")
                result_crossings.append(item)
    # Preserve pre-existing declared at-grade relationships on source shared
    # nodes, but never silently carry a now-invalid stale crossing reference.
    for prior in network.get("crossings",[]):
        a,b=(prior.get("a"),prior.get("b")) if model=="infra" else (
            prior.get("edge_a"),prior.get("edge_b"))
        consumed={tuple(x["corridors"]) for x,_,_ in resolved.values()}
        if a in parts and b in parts and len(parts[a])==len(parts[b])==1 and (
            tuple(sorted((a,b))) not in consumed):
            if not any((x.get("a",x.get("edge_a")),x.get("b",x.get("edge_b")))==(a,b)
                       for x in result_crossings):
                result_crossings.append(copy.deepcopy(prior))
    out_network={k:copy.deepcopy(v) for k,v in network.items()
                 if k not in ("nodes","edges","crossings")}
    out_network.update(nodes=[updated_nodes[i] for i in sorted(updated_nodes)],
                       edges=all_edges,crossings=sorted(result_crossings,
                           key=lambda x:(x.get("a",x.get("edge_a")),
                                         x.get("b",x.get("edge_b")),str(x.get("point")))))
    report={"status":"BLOCKED" if pending else "RECONCILED_NOT_ACCEPTED",
            "observed_crossings":len(events),"resolved_crossings":len(resolved),
            "unresolved_crossings":pending,
            "source_edge_count":len(edges),"result_edge_count":len(all_edges),
            "created_nodes":len(additions),"source_network_sha256":digest(network),
            "classification_sha256":digest(classifications)}
    out_network["topology_source"]=copy.deepcopy(network)
    if model=="urban":
        out_network["topology_source_seams"]=copy.deepcopy(data.get("neighbor_seams",[]))
    out_network["topology_audit"]={"status":report["status"],
                                   "source_network_sha256":report["source_network_sha256"],
                                   "classification_sha256":report["classification_sha256"],
                                   "result_network_sha256":digest(out_network)}
    result=copy.deepcopy(data)
    result[key]=out_network
    if model=="urban":
        for seam in result.get("neighbor_seams",[]):
            source_id=seam.get("network_edge_id")
            if source_id not in parts:
                continue
            candidates=[]
            for piece in parts[source_id]:
                try:
                    _distance_along(piece,seam["point"])
                except (TopologyInvalid,KeyError,TypeError):
                    continue
                candidates.append(piece)
            require(len(candidates)==1,
                    "neighbor connector must resolve to exactly one segmented edge")
            seam["network_edge_id"]=candidates[0]["id"]
            if seam.get("network_node_id") in rewrites:
                seam["network_node_id"]=rewrites[seam["network_node_id"]]
    return result, report


def reconcile_file(source, classification_file, output, *, expected_reference_sha=None,
                   original_reference=None, prior_accepted=None):
    """Materialize a *candidate*, never mutate source, U02, ledger or canon."""
    import os
    source = Path(source)
    classification_file = Path(classification_file)
    data=json.loads(source.read_text(encoding="utf-8"))
    classification=json.loads(classification_file.read_text(encoding="utf-8"))
    if expected_reference_sha is not None:
        require(data.get("source_sha256")==expected_reference_sha,
                "candidate not bound to required original U02")
    if data.get("fixture_mode") is not True:
        require(original_reference is not None and Path(original_reference).is_file() and
                hashlib.sha256(Path(original_reference).read_bytes()).hexdigest() ==
                data.get("source_sha256"), "original U02 bytes missing or changed")
    protected_edges=set(classification.get("protected_edge_ids",[]))
    protected_nodes=set()
    prior=None
    if data.get("stage")=="INF-02" and data.get("fixture_mode") is not True:
        require(prior_accepted is not None, "INF-02 requires accepted INF-01 geometry")
    if prior_accepted is not None:
        path=Path(prior_accepted)
        require(path.is_file(),"accepted previous geometry missing")
        prior=json.loads(path.read_text(encoding="utf-8"))
        require(prior.get("stage")=="INF-01" and data.get("stage")=="INF-02" and
                prior.get("source_sha256")==data.get("source_sha256") and
                data.get("previous_stage_sha256")==
                hashlib.sha256(path.read_bytes()).hexdigest(),
                "previous accepted INF-01 bytes/stage mismatch")
        prev=prior.get("network",{})
        current=data.get("network",{})
        old_edges={e["id"]:e for e in prev.get("edges",[])}
        new_edges={e["id"]:e for e in current.get("edges",[])}
        old_nodes={n["id"]:n for n in prev.get("nodes",[])}
        new_nodes={n["id"]:n for n in current.get("nodes",[])}
        require(all(eid in new_edges and new_edges[eid]==e for eid,e in old_edges.items()) and
                all(nid in new_nodes and new_nodes[nid]==n for nid,n in old_nodes.items()) and
                prior.get("zone_mask")==data.get("zone_mask"),
                "previous accepted network/zone mask cannot be changed")
        protected_edges.update(old_edges)
        protected_nodes.update(old_nodes)
    reconciled, report=reconcile(data,classification,
        protected_edges=protected_edges,protected_nodes=protected_nodes)
    destination=Path(output)
    destination.mkdir(parents=True,exist_ok=True)
    target=destination/"topology-candidate.json"
    diagnostic=destination/"topology-diagnostic.json"
    for path,value in ((target,reconciled),(diagnostic,report)):
        temporary=path.with_name(path.name+".tmp")
        temporary.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        os.replace(temporary,path)
    report["candidate_path"]=str(target)
    report["candidate_sha256"]=hashlib.sha256(target.read_bytes()).hexdigest()
    report["diagnostic_path"]=str(diagnostic)
    return report

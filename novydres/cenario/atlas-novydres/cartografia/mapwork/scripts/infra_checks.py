"""Deterministic spatial audit used by  acceptance, independent of model prose.

Stage requirements and accepted modals are read from the binding Markdown's
machine-readable profile, not another agent instruction source. An incomplete
spatial model MUST NOT become geometry PASS through four text assertions.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from PIL import Image

EPS=1e-7
MODES={"road", "rail", "tram", "metro", "water"}
CLASSES=("urban", "industrial", "natural", "water", "protected")


class InfraInvalid(ValueError):
    pass


def demand(value, message):
    if not value:
        raise InfraInvalid(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _safe_file(value, root):
    demand(isinstance(value, dict), "spatial binary evidence descriptor missing")
    loc=value.get("path")
    demand(isinstance(loc,str) and loc and "\\" not in loc,"binary evidence path invalid")
    p=Path(loc)
    demand(not p.is_absolute() and ".." not in p.parts,"binary evidence escaped candidate directory")
    file=(root/p).resolve()
    demand(file.is_relative_to(root.resolve()) and file.is_file(),"spatial binary bytes missing")
    demand(len(str(value.get("sha256","")))==64 and sha(file)==value["sha256"],
           "spatial mask SHA mismatch")
    return file


def _point(v,w,h):
    return (isinstance(v,list) and len(v)==2 and
            all(isinstance(x,(int,float)) and not isinstance(x,bool) and
                math.isfinite(x) for x in v) and
            0<=v[0]<=w and 0<=v[1]<=h)


def _segments(edge):
    pts=edge["points"]
    return zip(pts, pts[1:])


def _cross(a,b,c,d):
    return (b[0]-a[0])*(d[1]-c[1])-(b[1]-a[1])*(d[0]-c[0])


def _intersection(a,b,c,d):
    den=_cross(a,b,c,d)
    if abs(den)<EPS:
        # Collinear overlap MUST be explicit; mere same shared endpoint is fine.
        if abs(_cross(a,b,a,c))>EPS: return False
        axis=0 if abs(b[0]-a[0])>=abs(b[1]-a[1]) else 1
        overlap=min(max(a[axis],b[axis]),max(c[axis],d[axis]))-max(min(a[axis],b[axis]),min(c[axis],d[axis]))
        return "OVERLAP" if overlap>EPS else False
    t=_cross(a,c,c,d)/den
    u=_cross(a,c,a,b)/den
    return -EPS<=t<=1+EPS and -EPS<=u<=1+EPS


def _intersection_xy(a,b,c,d):
    denominator=_cross(a,b,c,d)
    if abs(denominator)<EPS:
        return None
    t=_cross(a,c,c,d)/denominator
    return (a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1]))


def _same_point(a,b):
    return math.dist(a,b)<=EPS


def _authority(c):
    value=c.get("authority")
    return (isinstance(value,dict) and value.get("status")=="APPROVED" and
            isinstance(value.get("decision_id"),str) and bool(value["decision_id"].strip()) and
            isinstance(value.get("evidence"),str) and len(value["evidence"].strip())>=12)


def _as_binary(item,root,dimensions):
    p=_safe_file(item,root)
    with Image.open(p) as image:
        demand(image.format=="PNG" and image.size==dimensions,
               "spatial mask PNG dimensions do not match original U02")
        im=image.convert("L")
        data=im.tobytes()
    demand(set(data).issubset({0,255}),"spatial mask must be exactly binary")
    return data


def validate(geometry_file, *, source_sha, dimensions, profile, prior=None):
    """Recompute geometry on actual candidate bytes; no trust in asserted metrics."""
    path=Path(geometry_file)
    data=json.loads(path.read_text(encoding="utf-8"))
    demand(isinstance(data,dict) and data.get("schema")=="NOVYDRES_MAPWORK_INFRA_GEOMETRY",
           "strict spatial geometry schema absent")
    stage=data.get("stage")
    demand(stage in profile["stage_modes"],"unknown infrastructure stage")
    demand(data.get("source_sha256")==source_sha,"spatial base source SHA mismatch")
    demand(data.get("reference_size")==list(dimensions),"spatial reference size mismatch")
    root=path.parent
    mask=_as_binary(data.get("zone_mask"),root,tuple(dimensions))
    area=sum(p==255 for p in mask)
    demand(area>0,"target zone mask empty")
    network=data.get("network",{})
    nodes=network.get("nodes")
    edges=network.get("edges")
    crossings=network.get("crossings")
    demand(isinstance(nodes,list) and isinstance(edges,list) and isinstance(crossings,list),
           "global network nodes/edges/crossings required")
    demand(bool(nodes) and bool(edges),"global network geometry empty")
    w,h=dimensions
    nd={}
    for n in nodes:
        demand(isinstance(n,dict) and isinstance(n.get("id"),str) and n["id"] not in nd and
               _point(n.get("point"),w,h) and type(n.get("level")) is int,
               "invalid/duplicate network node, coordinate or grade")
        nd[n["id"]]=n
    byid={}
    for edge in edges:
        demand(isinstance(edge,dict) and isinstance(edge.get("id"),str) and edge["id"] not in byid,
               "duplicate/invalid network edge")
        a=edge.get("from"); b=edge.get("to"); level=edge.get("level")
        pts=edge.get("points")
        demand(edge.get("mode") in MODES and a in nd and b in nd and a!=b and
               type(level) is int and isinstance(edge.get("width_units"),(int,float)) and
               math.isfinite(edge["width_units"]) and edge["width_units"]>0 and
               isinstance(pts,list) and len(pts)>=2 and all(_point(pt,w,h) for pt in pts),
               "invalid mode, width, grade or corridor geometry")
        demand(nd[a]["point"]==pts[0] and nd[b]["point"]==pts[-1] and
               nd[a]["level"]==level and nd[b]["level"]==level,
               "edge endpoints and node levels disconnected")
        demand(all(math.dist(x,y)>EPS for x,y in zip(pts,pts[1:])),
               "zero-length road/rail/tram/metro segment")
        byid[edge["id"]]=edge
    required=set(profile["stage_modes"][stage])
    modes={e["mode"] for e in edges}
    demand(required.issubset(modes),"missing required stage modal geometry: "+str(sorted(required-modes)))
    cx={}
    for c in crossings:
        demand(isinstance(c,dict) and c.get("a") in byid and c.get("b") in byid and
               c["a"]!=c["b"] and c.get("kind") in
               ("at_grade","grade_separated","no_connection"),
               "invalid explicit crossing")
        pair=tuple(sorted((c["a"],c["b"])))
        demand(pair not in cx,"duplicate crossing relation")
        first,second=byid[c["a"]],byid[c["b"]]
        shared={first["from"],first["to"]} & {second["from"],second["to"]}
        if c["kind"]=="at_grade":
            junction=c.get("authorized_junction_id")
            demand(isinstance(junction,str) and junction in nd,
                   "at-grade junction must identify an existing node")
            demand(junction in shared,
                   "at-grade junction edges must be split at the actual shared node")
            demand(first["level"]==second["level"]==nd[junction]["level"],
                   "at-grade junction level mismatch")
            demand(_same_point(nd[junction]["point"],first["points"][0]) or
                   _same_point(nd[junction]["point"],first["points"][-1]),
                   "junction not incident to first segment")
            demand(_same_point(nd[junction]["point"],second["points"][0]) or
                   _same_point(nd[junction]["point"],second["points"][-1]),
                   "junction not incident to second segment")
        else:
            demand(not shared,"non-connected crossing cannot share a graph node")
        if c["kind"]=="grade_separated":
            demand(first["level"]!=second["level"],
                   "claimed flyover/tunnel has identical levels")
        if c["kind"]=="no_connection" and first["level"]==second["level"]:
            demand(isinstance(c.get("barrier_evidence"),str) and
                   len(c["barrier_evidence"].strip())>=12,
                   "same-level nonconnection needs physical separation evidence")
        if (c["kind"]=="at_grade" and
            (first["mode"] in ("rail","metro") or second["mode"] in ("rail","metro")
             or first.get("protected_structure_id") or second.get("protected_structure_id"))):
            demand(_authority(c),
                   "rail/metro/protected at-grade junction requires specific owner authority")
        cx[pair]=c
    detected=0
    observed_pairs=set()
    all_edges=list(byid.values())
    for i,edge in enumerate(all_edges):
        for peer in all_edges[i+1:]:
            intersection_points=[]
            for a,b in _segments(edge):
                for c,d in _segments(peer):
                    result=_intersection(a,b,c,d)
                    if result=="OVERLAP":
                        raise InfraInvalid("two corridors overlap without separate authorized lane/track geometry")
                    if result:
                        xy=_intersection_xy(a,b,c,d)
                        if xy is not None:
                            intersection_points.append(xy)
            if not intersection_points:
                continue
            detected+=1
            pair=tuple(sorted((edge["id"],peer["id"])))
            observed_pairs.add(pair)
            shared={edge["from"],edge["to"]} & {peer["from"],peer["to"]}
            relation=cx.get(pair)
            if shared:
                demand(edge["level"]==peer["level"],"shared node crosses different levels")
                for xy in intersection_points:
                    demand(any(_same_point(xy,nd[node]["point"]) for node in shared),
                           "unsplit extra intersection away from shared graph node")
                if relation is not None:
                    demand(relation["kind"]=="at_grade",
                           "same graph node falsely declared disconnected")
            else:
                demand(relation is not None,
                       "untyped crossing/proximity is not a connection: "+str(pair))
                demand(relation["kind"]!="at_grade",
                       "at-grade connection without real split incident node: "+str(pair))
                if relation["kind"]=="grade_separated":
                    demand(edge["level"]!=peer["level"],
                           "grade-separated geometry has identical levels")
    demand(set(cx).issubset(observed_pairs),
           "declared crossing does not intersect actual geometry")
    # Fail-closed cumulative model: preceding stage geometry is a required parent.
    if prior is not None:
        previous=json.loads(Path(prior).read_text(encoding="utf-8"))
        demand(data.get("previous_stage_sha256")==sha(prior),"stale previous stage geometry SHA")
        demand(previous.get("zone_mask")==data.get("zone_mask"),
               "target territory mask changed after preceding acceptance")
        old={e["id"]:e for e in previous["network"]["edges"]}
        demand(all(eid in byid and byid[eid]==edge for eid,edge in old.items()),
               "previously accepted modal geometry was modified or removed")
        oldnodes={e["id"]:e for e in previous["network"]["nodes"]}
        demand(all(nid in nd and nd[nid]==n for nid,n in oldnodes.items()),
               "previously approved network node moved")
        oldcross={tuple(sorted((e["a"],e["b"]))):e for e in previous["network"]["crossings"]}
        demand(all(k in cx and cx[k]==v for k,v in oldcross.items()),
               "previously approved crossing was changed")
    territory_pixels=None
    if stage in profile.get("coverage_stages",[]):
        classes=data.get("territory",{}).get("class_masks",{})
        demand(isinstance(classes,dict) and set(classes)==set(profile["territory_classes"]),
               "five exclusive territory classes required")
        layers=[_as_binary(classes[key],root,tuple(dimensions)) for key in profile["territory_classes"]]
        count=0
        for i,z in enumerate(mask):
            covered=sum(layer[i]==255 for layer in layers)
            demand(covered==(1 if z==255 else 0),
                   "territory unclassified, overlapping or outside approved boundary")
            count+=covered
        territory_pixels=count
    protected=data.get("protected_mask")
    if protected:
        px=_as_binary(protected,root,tuple(dimensions))
        demand(all(not(v and not z) for v,z in zip(px,mask)),
               "protected pixels escape approved zone")
    return {"status":"PASS","stage":stage,"geometry_sha256":sha(path),
            "zone_pixels":area,"road_edges":sum(e["mode"]=="road" for e in edges),
            "modals":sorted(modes),"node_count":len(nd),"edge_count":len(edges),
            "crossings_detected":detected,"crossing_relations":len(cx),
            "territory_pixels":territory_pixels,
            "previous_stage_sha256":sha(prior) if prior else None}

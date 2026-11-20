#!/usr/bin/env python3
"""Mapwork V3.1: topology-first urban planning, separate from artistic rendering.

The urban LOT is a topological city block/quadrant bounded by at-grade transport
and other physical barriers. A WORK UNIT is an atomic masked generation job
inside the lot. Buildings, factories and POIs are occupants, never the lot ID.

Pillow rasterization is intentionally on the approved U02 reference grid only.
No physical metres or demographic counts are inferred from those pixels.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw
from jsonschema import Draft202012Validator


class ContractError(ValueError):
    pass


ROAD_CLASSES = {"street", "collector", "avenue", "arterial", "expressway", "ramp", "service"}
RAIL_CLASSES = {"rail_main", "rail_freight", "rail_siding"}
TRAM_CLASSES = {"tram"}
WATER_CLASSES = {"river", "canal"}
UNDERGROUND_CLASSES = {"metro", "heat_pipe", "gas_pipe", "utility_duct"}
UTILITY_CLASSES = UNDERGROUND_CLASSES | {"aqueduct"}
EDGE_CLASSES = ROAD_CLASSES | RAIL_CLASSES | TRAM_CLASSES | WATER_CLASSES | UTILITY_CLASSES
JUNCTION_CLASSES = {"intersection", "roundabout", "interchange", "rail_crossing", "tram_junction", "tram_stop", "terminal", "portal", "rail_station", "freight_terminal", "overpass", "underpass", "metro_station", "utility_hub", "aqueduct_gate", "heat_exchange", "gas_terminal"}
CROSSING_CLASSES = {"at_grade", "grade_separated"}
LANDUSE_CLASSES = {"urban", "industrial", "natural", "water", "protected"}
MORPH_CLASSES = {"historic", "worker", "industrial", "technical", "mixed", "waterfront"}
SCHEMA = "NOVYDRES_MAPWORK_V31_TERRITORY_NETWORK_1"


def require(test, reason):
    if not test:
        raise ContractError(reason)


def finite_xy(p):
    return isinstance(p, list) and len(p) == 2 and all(
        isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
        for v in p
    )


def point_close(a, b, tol=0.05):
    return math.hypot(a[0]-b[0], a[1]-b[1]) <= tol


def seg_cross(a, b, c, d):
    """Non-collinear 2D segment intersection; collinear overlap is handled by co-location policy."""
    v=(b[0]-a[0],b[1]-a[1])
    w=(d[0]-c[0],d[1]-c[1])
    det=v[0]*w[1]-v[1]*w[0]
    if abs(det) < 1e-9:
        return None
    diff=(c[0]-a[0],c[1]-a[1])
    t=(diff[0]*w[1]-diff[1]*w[0])/det
    u=(diff[0]*v[1]-diff[1]*v[0])/det
    if -1e-8<=t<=1+1e-8 and -1e-8<=u<=1+1e-8:
        return [a[0]+t*v[0], a[1]+t*v[1]]
    return None


def collinear_overlap(a,b,c,d):
    """Return a representative interior point of a positive-length same-line overlap."""
    dx,dy=b[0]-a[0],b[1]-a[1]
    def cross(p): return dx*(p[1]-a[1])-dy*(p[0]-a[0])
    if abs(cross(c))>1e-8 or abs(cross(d))>1e-8:
        return None
    axis=0 if abs(dx)>=abs(dy) else 1
    start=max(min(a[axis],b[axis]),min(c[axis],d[axis]))
    end=min(max(a[axis],b[axis]),max(c[axis],d[axis]))
    if end-start<=1e-8:
        return None
    t=((start+end)/2-a[axis])/(b[axis]-a[axis])
    return [a[0]+t*dx,a[1]+t*dy]


def _edge_level(edge, at_start=False):
    return edge["level_from"] if at_start and edge["class"]=="ramp" else (
        edge["level_to"] if edge["class"]=="ramp" else edge["level"])


def _validate_nodes_edges(transport, width, height):
    nodes=transport.get("nodes",[])
    edges=transport.get("edges",[])
    require(bool(nodes) and bool(edges),"transport nodes/edges required")
    node_ids={x.get("id") for x in nodes}
    edge_ids={x.get("id") for x in edges}
    require(len(node_ids)==len(nodes) and None not in node_ids,"duplicate/missing transport nodes")
    require(len(edge_ids)==len(edges) and None not in edge_ids,"duplicate/missing transport edges")
    bynode={n["id"]:n for n in nodes}
    incid=collections.Counter()
    for n in nodes:
        p=n.get("point")
        require(finite_xy(p) and 0<=p[0]<=width and 0<=p[1]<=height,
                f"{n['id']}: invalid node position")
        require(n.get("kind") in JUNCTION_CLASSES, f"{n['id']}: invalid junction type")
        require(isinstance(n.get("level"),int),f"{n['id']}: node level required")
    for e in edges:
        label=e["id"]
        require(e.get("class") in EDGE_CLASSES,f"{label}: unknown transport class")
        require(e.get("from") in bynode and e.get("to") in bynode and e["from"]!=e["to"],
                f"{label}: broken transport endpoints")
        pts=e.get("points")
        require(isinstance(pts,list) and len(pts)>=2 and all(finite_xy(p) for p in pts),
                f"{label}: invalid polyline")
        require(all(0<=p[0]<=width and 0<=p[1]<=height for p in pts),f"{label}: line outside reference")
        require(all(not point_close(pts[i],pts[i+1]) for i in range(len(pts)-1)),
                f"{label}: zero length segment")
        require(point_close(pts[0],bynode[e["from"]]["point"]) and
                point_close(pts[-1],bynode[e["to"]]["point"]),
                f"{label}: polyline must terminate at declared nodes")
        require(e.get("owner")=="GLOBAL_NETWORK",f"{label}: network must be globally owned")
        require(isinstance(e.get("width_units"),(int,float)) and 0<e["width_units"]<=12,
                f"{label}: invalid physical corridor width")
        require(type(e.get("separates_blocks")) is bool,
                f"{label}: explicit lot barrier semantics required")
        if e["class"]=="ramp":
            require(isinstance(e.get("level_from"),int) and isinstance(e.get("level_to"),int)
                    and e["level_from"]!=e["level_to"],f"{label}: ramp must connect two levels")
            require(e["separates_blocks"] is False,
                    f"{label}: grade-changing ramp must not split surface blocks")
            from_level,to_level=e["level_from"],e["level_to"]
        else:
            require(isinstance(e.get("level"),int),f"{label}: structure level required")
            from_level=to_level=e["level"]
        require(bynode[e["from"]]["level"]==from_level and
                bynode[e["to"]]["level"]==to_level,
                f"{label}: node and edge levels mismatch")
        if e["class"] in TRAM_CLASSES:
            require(e["separates_blocks"] is False,
                    f"{label}: tram tracks do not create independent road quadrants")
            require(e.get("shared_with_road") is True or e.get("reserved_right_of_way") is True,
                    f"{label}: tram must declare shared or reserved corridor")
        if to_level!=0 or from_level!=0:
            if e["class"]!="ramp":
                require(e.get("structure") in {"viaduct","overpass","elevated_rail","tunnel","underpass"},
                        f"{label}: non-surface infrastructure must identify physical structure")
            require(e["separates_blocks"] is False or (from_level==to_level==0),
                    f"{label}: elevated route cannot cut ground-level blocks")
        if e["class"] in WATER_CLASSES:
            require(e["separates_blocks"] is True,f"{label}: river/canal is a physical boundary")
        if e["class"] in UNDERGROUND_CLASSES:
            require(from_level<0 and to_level<0 and
                    e.get("structure") in {"tunnel","underpass"},
                    f"{label}: underground network requires negative level and tunnel")
            require(e["separates_blocks"] is False,
                    f"{label}: subsurface networks cannot split ground city blocks")
        if e["class"]=="aqueduct":
            require(e["separates_blocks"] is False,
                    f"{label}: utility aqueduct cannot independently subdivide lots")
        incid[e["from"]]+=1;incid[e["to"]]+=1
    incident=collections.defaultdict(list)
    for e in edges:
        incident[e["from"]].append(e)
        incident[e["to"]].append(e)
    for n in nodes:
        touching=incident[n["id"]]
        has_rail=any(e["class"] in RAIL_CLASSES for e in touching)
        has_road=any(e["class"] in ROAD_CLASSES for e in touching)
        if has_rail and has_road:
            require(n["kind"]=="rail_crossing",
                    f"{n['id']}: at-grade road/rail connection requires declared rail crossing")
        if n["kind"]=="roundabout":
            require(incid[n["id"]]>=3,f"{n['id']}: roundabout requires at least 3 branches")
            ring=n.get("ring_geometry")
            require(isinstance(ring,list) and len(ring)>=4 and all(finite_xy(p) for p in ring),
                    f"{n['id']}: roundabout requires a physical ring polygon")
        if n["kind"]=="interchange":
            require(incid[n["id"]]>=2,f"{n['id']}: empty interchange")
            require(any(e["class"]=="ramp" for e in touching),
                    f"{n['id']}: interchange requires a grade-changing ramp")
    return bynode,{e["id"]:e for e in edges}


def validate_transport(transport, width, height):
    """Check infrastructure hierarchy, at-grade junctions and grade separations.

    All geometric crossings must be declared, unless two edges meet at their
    shared endpoint node or a tram shares the exact carriageway corridor.
    """
    bynode,byedge=_validate_nodes_edges(transport,width,height)
    crossings=transport.get("crossings",[])
    seen=set()
    for x in crossings:
        pair=frozenset([x.get("edge_a"),x.get("edge_b")])
        require(len(pair)==2 and pair<=set(byedge),f"invalid crossing edge pair {x.get('id')}")
        require(pair not in seen,f"duplicate crossing pair {x.get('id')}")
        seen.add(pair)
        require(x.get("kind") in CROSSING_CLASSES,f"{x.get('id')}: invalid crossing kind")
        require(finite_xy(x.get("point")),f"{x.get('id')}: invalid crossing coordinate")
        a,b=byedge[x["edge_a"]],byedge[x["edge_b"]]
        if x["kind"]=="grade_separated":
            require(a.get("level",a.get("level_from"))!=b.get("level",b.get("level_from")),
                    f"{x['id']}: grade separation requires distinct levels")
        else:
            require(a.get("level",a.get("level_from"))==b.get("level",b.get("level_from")),
                    f"{x['id']}: at-grade crossing must share level")
            require(x.get("junction_id") in bynode,f"{x['id']}: at-grade junction must have a node")
            require(point_close(x["point"],bynode[x["junction_id"]]["point"]),
                    f"{x['id']}: crossing does not align junction")
            require(x["junction_id"] in (a["from"],a["to"]) and
                    x["junction_id"] in (b["from"],b["to"]),
                    f"{x['id']}: at-grade crossing must split both edge geometries at junction")
    # Spatial hash to avoid checking every network segment against every other.
    bucket=16
    cells=collections.defaultdict(list)
    segments=[]
    for e in byedge.values():
        for i in range(len(e["points"])-1):
            a,b=e["points"][i:i+2]
            idx=len(segments);segments.append((e,a,b))
            x0=int(math.floor(min(a[0],b[0])/bucket))
            x1=int(math.floor(max(a[0],b[0])/bucket))
            y0=int(math.floor(min(a[1],b[1])/bucket))
            y1=int(math.floor(max(a[1],b[1])/bucket))
            for tx in range(x0,x1+1):
                for ty in range(y0,y1+1):
                    cells[(tx,ty)].append(idx)
    pairs=set()
    for ids in cells.values():
        for i in range(len(ids)):
            for j in range(i+1,len(ids)):
                if ids[i]!=ids[j]:
                    pairs.add((min(ids[i],ids[j]),max(ids[i],ids[j])))
    actual=collections.defaultdict(list)
    for ia,ib in pairs:
        a,pa,qa=segments[ia];b,pb,qb=segments[ib]
        if a["id"]==b["id"]:
            continue
        pt=seg_cross(pa,qa,pb,qb)
        underground_grade=(a["class"] in UNDERGROUND_CLASSES or
                           b["class"] in UNDERGROUND_CLASSES)
        different_grade=a.get("level",a.get("level_from"))!=b.get("level",b.get("level_from"))
        if underground_grade and different_grade:
            continue
        if pt is None:
            overlap=collinear_overlap(pa,qa,pb,qb)
            if overlap is None:
                continue
            same_corridor=(a["class"] in ROAD_CLASSES and b["class"] in TRAM_CLASSES and
                           b.get("shared_with_road") is True) or (
                           b["class"] in ROAD_CLASSES and a["class"] in TRAM_CLASSES and
                           a.get("shared_with_road") is True)
            require(same_corridor,
                    f"undeclared collinear transport overlap {a['id']}/{b['id']}: {overlap}")
            continue
        # Shared endpoint is legal only when the edges share the actual node.
        endpoints={a["from"],a["to"]}&{b["from"],b["to"]}
        if any(point_close(pt,bynode[n]["point"]) for n in endpoints):
            continue
        pair=frozenset((a["id"],b["id"]))
        actual[pair].append(pt)
    listed={frozenset([x["edge_a"],x["edge_b"]]):x for x in crossings}
    for pair,points in actual.items():
        edges=list(pair)
        a,b=byedge[edges[0]],byedge[edges[1]]
        # Shared-running tram and road are expected to be collinear; a true
        # transverse crossing still requires an explicit junction.
        desc=listed.get(pair)
        require(desc is not None,f"undeclared transport crossing {edges}: {points[0]}")
        require(any(point_close(desc["point"],pt,0.5) for pt in points),
                f"{desc['id']}: declared crossing does not match segment geometry")
        if desc["kind"]=="at_grade":
            require(bynode[desc["junction_id"]]["level"]==a.get("level",a.get("level_from")),
                    f"{desc['id']}: junction level mismatch")
    return {
        "nodes":len(bynode),"edges":len(byedge),
        "declared_crossings":len(crossings),"detected_nonnode_crossings":len(actual),
        "roads":sum(e["class"] in ROAD_CLASSES for e in byedge.values()),
        "rails":sum(e["class"] in RAIL_CLASSES for e in byedge.values()),
        "trams":sum(e["class"] in TRAM_CLASSES for e in byedge.values()),
        "waterways":sum(e["class"] in WATER_CLASSES for e in byedge.values()),
        "metro":sum(e["class"]=="metro" for e in byedge.values()),
        "utilities":sum(e["class"] in UTILITY_CLASSES and e["class"]!="metro" for e in byedge.values()),
        "junctions":dict(collections.Counter(n["kind"] for n in bynode.values()))
    }


def _polygon_mask(shape, polygon, holes=None):
    """Classify territory with interior voids, e.g. rivers through urban blocks."""
    im=Image.new("L",shape,0)
    draw=ImageDraw.Draw(im)
    draw.polygon([tuple(p) for p in polygon],fill=1)
    for hole in holes or []:
        require(len(hole)>=3 and all(finite_xy(p) for p in hole),
                "invalid territory hole")
        draw.polygon([tuple(p) for p in hole],fill=0)
    return im


def _line_mask(shape, transport, selector):
    im=Image.new("L",shape,0);d=ImageDraw.Draw(im)
    for e in transport["edges"]:
        if not selector(e):
            continue
        width=max(1,round(e["width_units"]))
        pts=[tuple(p) for p in e["points"]]
        d.line(pts,fill=1,width=width,joint="curve")
    return im


def classify_territory(plan):
    w,h=plan["grid"]["width"],plan["grid"]["height"]
    shape=(w,h)
    zone=_polygon_mask(shape,plan["zone"]["polygon"]).tobytes()
    area=bytearray(w*h)
    labels=bytearray(w*h)
    categories={x:i+1 for i,x in enumerate(sorted(LANDUSE_CLASSES))}
    ownership=collections.defaultdict(int)
    for x in plan["territory"]:
        typ=x.get("class")
        require(typ in LANDUSE_CLASSES,f"{x.get('id')}: invalid landuse class")
        bit=_polygon_mask(shape,x["polygon"],x.get("holes",[])).tobytes()
        for i,p in enumerate(bit):
            if not p:
                continue
            require(zone[i],f"{x['id']}: class polygon extends outside zone")
            require(not labels[i],f"{x['id']}: overlapping primary landuse polygons")
            labels[i]=categories[typ]
            ownership[typ]+=1
    missing=sum(1 for i,p in enumerate(zone) if p and not labels[i])
    require(missing==0,f"territorial coverage incomplete: {missing} unclassified reference pixels")
    return zone,labels,categories,dict(ownership)


def spatial_protection_mask(plan):
    """Exact U02-grid protected cells; caller must first pass plan_city with real source."""
    w,h=plan["grid"]["width"],plan["grid"]["height"]
    zone,classes,names,_=classify_territory(plan)
    corridors=_line_mask((w,h),plan["transport"],lambda e:
                         e["class"] not in UNDERGROUND_CLASSES or
                         e.get("surface_easement") is True).tobytes()
    protected_categories={names["water"],names["natural"],names["protected"]}
    mask=bytes(255 if zone[i] and
               (classes[i] in protected_categories or corridors[i]) else 0
               for i in range(w*h))
    return Image.frombytes("L",(w,h),mask)


def _street_access(width, height, labels, editable, road):
    """Trace at-grade routes along the setbacks of parcels within one city block."""
    parents, distance = {}, {}
    queue = collections.deque()
    for i, allowed in enumerate(editable):
        if not allowed:
            continue
        x, y = i % width, i // width
        neighbors = ([i - 1] if x else []) + ([i + 1] if x < width - 1 else [])
        neighbors += ([i - width] if y else []) + ([i + width] if y < height - 1 else [])
        if any(road[j] for j in neighbors):
            parents[i] = None
            distance[i] = 0
            queue.append(i)
    while queue:
        i = queue.popleft()
        x, y = i % width, i // width
        neighbors = ([i - 1] if x else []) + ([i + 1] if x < width - 1 else [])
        neighbors += ([i - width] if y else []) + ([i + width] if y < height - 1 else [])
        for j in neighbors:
            if editable[j] and labels[j] == labels[i] and j not in parents:
                parents[j] = i
                distance[j] = distance[i] + 1
                queue.append(j)
    return parents, distance


def _validate_special_sites(plan, width, height, labels, blocks, editable, distance):
    """POIs must occupy a real buildable parcel with a surveyed entrance and path."""
    sites = plan["special_sites"]
    require(isinstance(sites, list), "explicit special_sites inventory required")
    ids, cells, verified = set(), set(), []
    byblock = {b["id"]: i + 1 for i, b in enumerate(blocks)}
    for s in sites:
        sid = s["id"]
        require(sid not in ids, f"{sid}: duplicate POI")
        ids.add(sid)
        block = byblock.get(s["block_id"])
        require(block is not None, f"{sid}: POI references absent city block")
        point, entrance, box = s["point"], s["entrance"], s["footprint"]
        require(finite_xy(point) and finite_xy(entrance), f"{sid}: POI location/entrance required")
        require(isinstance(box, list) and len(box) == 4 and
                all(isinstance(v, (int, float)) and math.isfinite(v) for v in box) and
                box[0] < box[2] and box[1] < box[3], f"{sid}: invalid footprint")
        x, y = int(point[0]), int(point[1])
        require(0 <= x < width and 0 <= y < height and
                x < point[0] < x + 1 and y < point[1] < y + 1,
                f"{sid}: POI point must be inside a parcel")
        i = y * width + x
        require(i not in cells and labels[i] == block and editable[i],
                f"{sid}: POI parcel collides or is not editable within its block")
        cells.add(i)
        require(x < box[0] < box[2] < x + 1 and y < box[1] < box[3] < y + 1,
                f"{sid}: POI footprint must preserve parcel perimeter clearance")
        require(box[0] <= entrance[0] <= box[2] and box[1] <= entrance[1] <= box[3],
                f"{sid}: entrance outside footprint")
        require(i in distance, f"{sid}: no at-grade street path")
        cls = next(key for key, value in
                   {name: idx + 1 for idx, name in enumerate(sorted(LANDUSE_CLASSES))}.items()
                   if value == plan["_site_class_ids"][i])
        clearance = plan["morphology"][cls]["access_clearance_units"]
        require(2 * min(box[0] - x, y + 1 - box[3], box[1] - y, x + 1 - box[2]) >= clearance - 1e-8,
                f"{sid}: insufficient POI access corridor width")
        verified.append({"id": sid, "block_id": s["block_id"], "point": point,
                         "entrance": entrance, "footprint": box, "road_access_steps": distance[i]})
    return verified


def _morphology_rules(plan, class_counts):
    rules=plan.get("morphology",{})
    for cls in ("urban","industrial"):
        if class_counts.get(cls,0)==0:
            continue
        r=rules.get(cls)
        require(isinstance(r,dict),f"missing morphology for {cls}")
        require(r.get("typology") in MORPH_CLASSES,f"{cls}: missing/invalid architectural typology")
        require(isinstance(r.get("occupation_target"),(int,float)) and
                0<r["occupation_target"]<=1,f"{cls}: occupation target must be (0,1]")
        band=r.get("building_floors")
        require(isinstance(band,list) and len(band)==2 and
                all(isinstance(n,int) and n>=1 for n in band) and band[0]<=band[1],
                f"{cls}: invalid building-height band")
        mixes=r.get("use_mix")
        require(isinstance(mixes,dict) and len(mixes)>=1 and
                all(isinstance(v,(int,float)) and v>=0 for v in mixes.values()) and
                abs(sum(mixes.values())-1)<=1e-6,f"{cls}: use mix must sum to one")
        required=r.get("access_clearance_units")
        require(isinstance(required,(int,float)) and not isinstance(required,bool) and
                math.isfinite(required) and 0<required<1,
                f"{cls}: explicit at-grade access clearance in U02 units required")
        require(r.get("access_mode") in ("pedestrian","vehicle"),
                f"{cls}: pedestrian/vehicle access mode required")
        gap=1-math.sqrt(r["occupation_target"])
        require(gap+1e-8>=required,
                f"{cls}: occupation leaves less clearance than the required access corridor")


def _label_blocks(width,height,eligible,dividers,category_map):
    """A lot is a ground-level street-bounded connected region, NOT a rectangle."""
    occupied=bytearray(eligible)
    for i,v in enumerate(dividers):
        if v:
            occupied[i]=0
    labels=[0]*(width*height)
    blocks=[]
    for start,allowed in enumerate(occupied):
        if not allowed or labels[start]:
            continue
        bid=len(blocks)+1
        q=collections.deque([start])
        labels[start]=bid
        x0,y0=start%width,start//width
        minx=maxx=x0;miny=maxy=y0
        counts=collections.Counter()
        pixels=0
        while q:
            k=q.popleft()
            x,y=k%width,k//width
            pixels+=1;counts[category_map[k]]+=1
            minx=min(minx,x);maxx=max(maxx,x);miny=min(miny,y);maxy=max(maxy,y)
            neighbors=[]
            if x>0:neighbors.append(k-1)
            if x<width-1:neighbors.append(k+1)
            if y>0:neighbors.append(k-width)
            if y<height-1:neighbors.append(k+width)
            for nxt in neighbors:
                if occupied[nxt] and not labels[nxt]:
                    labels[nxt]=bid
                    q.append(nxt)
        blocks.append({
            "id":f"BLK-{miny:04d}-{minx:04d}",
            "bbox":[minx,miny,maxx+1,maxy+1],
            "pixels":pixels,
            "kind":"STREET_BOUNDED_QUADRANT",
            "landuse_counts":dict(counts)
        })
    return labels,blocks


def derive_work_units(width,height,labels,allowed,max_units,scale):
    """Partition ALL eligible pixels exactly once into bounded work-unit masks."""
    labels_n=len(labels)
    require(labels_n==width*height,"invalid block label image")
    require(isinstance(max_units,int) and 1<=max_units<=32,"work-unit size must be between 1 and 32 reference pixels")
    tasks={}
    covered=bytearray(width*height)
    for i,block in enumerate(labels):
        if block==0 or not allowed[i]:
            continue
        x=i%width;y=i//width
        key=(block,x//max_units,y//max_units)
        if key not in tasks:
            tasks[key]={
                "id":f"WU-{block:05d}-{key[2]:04d}-{key[1]:04d}",
                "block_label":block,
                "bbox":[x,y,x+1,y+1],
                "pixels":0
            }
        t=tasks[key];t["pixels"]+=1
        box=t["bbox"]
        box[0]=min(box[0],x);box[1]=min(box[1],y)
        box[2]=max(box[2],x+1);box[3]=max(box[3],y+1)
        require(covered[i]==0,"duplicate pixel assignment to work unit")
        covered[i]=1
    require(all((not x) or covered[i] for i,x in enumerate(allowed)),
            "eligible area is not completely assigned to work units")
    result=sorted(tasks.values(),key=lambda x:x["id"])
    for t in result:
        w=t["bbox"][2]-t["bbox"][0];h=t["bbox"][3]-t["bbox"][1]
        require(w<=max_units and h<=max_units,"oversized atomic work unit")
        t["max_render_width_px"]=w*scale
        t["max_render_height_px"]=h*scale
        t["status"]="PENDING"
    return result,sum(covered)


def plan_city(plan, cfg, *, reference_file=None, neighbor_manifests=None):
    """Fully materialize contracts for a declared synthetic/real spatial manifest."""
    require(plan.get("schema")==SCHEMA,"architecture schema mismatch")
    schema_path=Path(__file__).resolve().parents[1]/"schemas"/"urban_architecture_v31.schema.json"
    schema=json.loads(schema_path.read_text(encoding="utf-8"))
    errors=list(Draft202012Validator(schema).iter_errors(plan))
    require(not errors,"V3.1 schema: "+("; ".join(e.message for e in errors[:3])))
    require(plan.get("source_sha256")==cfg["reference"]["sha256"] or
            (plan.get("fixture_mode") is True and plan.get("source_sha256")=="SYNTHETIC"),
            "source U02 binding mismatch")
    w=plan["grid"]["width"];h=plan["grid"]["height"]
    require(isinstance(w,int) and isinstance(h,int) and 8<=w<=10000 and 8<=h<=10000,
            "invalid reference grid")
    require(plan.get("zone",{}).get("id") and len(plan["zone"].get("polygon",[]))>=3,
            "zone requires a polygon")
    require(all(finite_xy(x) for x in plan["zone"]["polygon"]),
            "zone contains invalid polygon vertex")
    require(0<=min(x[0] for x in plan["zone"]["polygon"]) and
            max(x[0] for x in plan["zone"]["polygon"])<=w and
            0<=min(x[1] for x in plan["zone"]["polygon"]) and
            max(x[1] for x in plan["zone"]["polygon"])<=h,
            "zone outside reference")
    transport_stats=validate_transport(plan["transport"],w,h)
    zone,classes,names,class_counts=classify_territory(plan)
    _morphology_rules(plan,class_counts)
    source_verified=False
    if reference_file is not None:
        ref=Path(reference_file)
        if ref.is_file():
            digest=hashlib.sha256(ref.read_bytes()).hexdigest()
            with Image.open(ref) as pic:
                dims=pic.size
            source_verified=(digest==cfg["reference"]["sha256"] and dims==(w,h)
                             and plan.get("fixture_mode") is not True)
        require(source_verified,"actual U02 source file failed SHA or dimensions")
    eligible_classes={names["urban"],names["industrial"]}
    eligible=bytearray(1 if zone[i] and classes[i] in eligible_classes else 0 for i in range(w*h))
    # The surface of streets at ground level defines the *quadrant* perimeter.
    divider=_line_mask((w,h),plan["transport"],lambda e:
        e["separates_blocks"] and e.get("level",e.get("level_from",0))==0).tobytes()
    # Elevated rail/roads/viaducts are preserved as a second overlay, but they
    # do not connect ground roads or falsely split lots at an overpass.
    all_rails_roads=_line_mask((w,h),plan["transport"],lambda e:
        e["class"] not in UNDERGROUND_CLASSES or
        e.get("surface_easement") is True).tobytes()
    landuse_protected={names["water"],names["natural"],names["protected"]}
    protected=bytearray(1 if (zone[i] and (classes[i] in landuse_protected or
                                           all_rails_roads[i])) else 0 for i in range(w*h))
    labels,blocks=_label_blocks(w,h,eligible,divider,classes)
    eligible_edit=bytearray(1 if (eligible[i] and not protected[i]) else 0 for i in range(w*h))
    require(all(not eligible_edit[i] or labels[i]>0 for i in range(w*h)),
            "editable pixel missing a road-bounded block")
    roads=_line_mask((w,h),plan["transport"],lambda e:
                     e["class"] in ROAD_CLASSES and e.get("level",e.get("level_from",0))==0).tobytes()
    _,distance=_street_access(w,h,labels,eligible_edit,roads)
    unreachable=sum(bool(allowed) and i not in distance for i,allowed in enumerate(eligible_edit))
    require(unreachable==0,f"{unreachable} parcels lack at-grade street access")
    # Local scratch mapping only; never added to the persisted spatial manifest.
    site_plan=dict(plan,_site_class_ids=classes)
    verified_sites=_validate_special_sites(site_plan,w,h,labels,blocks,eligible_edit,distance)
    tasksize=plan.get("work_policy",{}).get("max_units")
    tasks,pixels=derive_work_units(w,h,labels,eligible_edit,tasksize,cfg["detail_pixels_per_unit"])
    budget=plan["work_policy"].get("max_work_units")
    require(isinstance(budget,int) and budget>0,"work-unit budget missing")
    require(len(tasks)<=budget,
            f"planned {len(tasks)} work units exceeds budget {budget}; split into batches")
    need=sum(eligible_edit)
    require(need==pixels,"eligible coverage not exactly 100 percent")
    batchsize=plan["work_policy"].get("batch_size",min(12,budget))
    require(isinstance(batchsize,int) and 1<=batchsize<=budget,
            "invalid incremental generation batch size")
    batches=[
        {"id":f"BATCH-{k//batchsize+1:04d}",
         "work_unit_ids":[t["id"] for t in tasks[k:k+batchsize]],
         "status":"PENDING_UNAUTHORIZED"}
        for k in range(0,len(tasks),batchsize)
    ]
    flattened=[unit for batch in batches for unit in batch["work_unit_ids"]]
    require(len(flattened)==len(tasks) and
            len(set(flattened))==len(tasks),"incomplete or duplicate incremental queue")
    total=sum(zone)
    classified=sum(class_counts.values())
    require(total==classified,"territory classification must cover exact polygon")
    declared_seams=plan.get("neighbor_seams",[])
    require(isinstance(declared_seams,list),"neighbor seam list required")
    require(len({s["id"] for s in declared_seams})==len(declared_seams),
            "duplicate shared connector identifiers")
    counterparts=neighbor_manifests if neighbor_manifests is not None else {}
    transport_digest=hashlib.sha256(
        json.dumps(plan["transport"],sort_keys=True,separators=(",",":")).encode("utf-8")
    ).hexdigest()
    seams_verified=bool(declared_seams)
    matched_seams=0
    reserved_seams=0
    for seam in declared_seams:
        require(seam.get("from_zone")==plan["zone"]["id"] and
                seam.get("to_zone") and seam.get("id") and finite_xy(seam.get("point")),
                "malformed bilateral seam contract")
        peer=counterparts.get(seam["to_zone"])
        mate=next((x for x in peer.get("seams",[]) if x.get("id")==seam["id"]),None) if peer is not None else None
        expected=("kind","width_units","profile")
        good=bool(mate) and mate.get("from_zone")==seam["to_zone"] and mate.get("to_zone")==seam["from_zone"]
        good=good and all(mate.get(k)==seam.get(k) for k in expected)
        good=good and point_close(mate.get("point",[float("inf"),float("inf")]),seam["point"],0.01)
        if peer is not None:
            require(bool(good),f"{seam['id']}: existing neighbor seam differs or is missing from global authority")
            matched_seams+=1
        else:
            reservation=(seam.get("reservation_status")=="APPROVED_SCOPED" and
                         seam.get("authority_sha256")==transport_digest)
            reserved_seams+=int(reservation)
            seams_verified=seams_verified and reservation
    receipt=plan.get("work_policy",{}).get("mask_receipt",{})
    masks_verified=(
        isinstance(receipt,dict) and
        receipt.get("editable_sha256")==hashlib.sha256(eligible_edit).hexdigest() and
        receipt.get("protected_sha256")==hashlib.sha256(protected).hexdigest() and
        receipt.get("work_unit_count")==len(tasks) and
        receipt.get("source_sha256")==cfg["reference"]["sha256"] and
        source_verified
    )
    owner_approval=plan.get("owner_art_approval",{})
    owner_auth=(
        plan.get("owner_art_authorized") is True and
        isinstance(owner_approval,dict) and
        owner_approval.get("decision")=="APPROVED" and
        isinstance(owner_approval.get("evidence"),str) and
        len(owner_approval["evidence"])>=8
    )
    required_gates={
        "source_and_global_topology":True,
        "source_bytes_verified":source_verified,
        "territory_classification":True,
        "urban_morphology":True,
        "quadrants_derived_from_transport":True,
        "work_unit_coverage":True,
        "protected_network_coverage":True,
        "neighbor_seams":seams_verified,
        "pixel_masks_verified":masks_verified,
        "owner_art_authorized":owner_auth,
        "poi_sites_placed_and_accessible":len(verified_sites)==len(plan["special_sites"]),
        "ground_access_and_clearance":unreachable==0
    }
    ready=all(required_gates.values()) and plan.get("fixture_mode") is False
    # No claim that a synthetic fixture provides real city evidence.
    blocked=[k for k,v in required_gates.items() if not v]
    block_programs=[]
    reverse={v:k for k,v in names.items()}
    for b in blocks:
        counts={reverse[k]:v for k,v in b["landuse_counts"].items()}
        typ=max(counts,key=counts.get)
        profile=plan["morphology"][typ]
        block_programs.append({
            "block_id":b["id"],"quadrant_bbox":b["bbox"],"area_pixels":b["pixels"],
            "urban_program":typ,"typology":profile["typology"],
            "occupation_target":profile["occupation_target"],
            "building_floor_band":profile["building_floors"],
            "use_mix":profile["use_mix"],
            "poi_sites":[site["id"] for site in verified_sites
                         if site["block_id"]==b["id"]],
            "buildings_generated":0
        })
    return {
        "schema":"NOVYDRES_MAPWORK_V31_AUDIT_REPORT_1",
        "zone":plan["zone"]["id"],
        "fixture":plan.get("fixture_mode") is True,
        "transport":transport_stats,
        "territory":{"total_pixels":total,"classified_pixels":classified,
                     "coverage_pct":100,"by_landuse":class_counts},
        "geometry":{"urban_lots":len(blocks),"editable_pixels":need,
                    "work_units":len(tasks),"assigned_pixels":pixels,
                    "eligible_coverage_pct":100 if need else 0,
                    "lot_semantics":"ROAD_BOUNDED_QUADRANT",
                    "work_unit_semantics":"ATOMIC_GENERATION_WINDOW"},
        "blocks":blocks,
        "block_programs":block_programs,
        "poi_sites":verified_sites,
        "access":{"connected_parcels":len(distance),"unreachable_parcels":unreachable,
                  "semantics":"ABSTRACT_U02_CORRIDOR_NOT_METRIC_VEHICLE_CERTIFICATION"},
        "work_units":tasks,
        "generation_queue":{
            "batches":batches,
            "batch_size":batchsize,
            "total_work_units":len(tasks),
            "all_work_units_queued_once":True,
            "generation_authorized":False
        },
        "gates":required_gates,
        "generation_ready":ready,
        "blocking_gates":blocked,
        "seam_status":{"matched":matched_seams,"reserved":reserved_seams,
                       "declared":len(declared_seams),
                       "pending_peer_verification":reserved_seams>0},
        "transport_sha256":transport_digest,
        "mask_fingerprints":{
            "editable_sha256":hashlib.sha256(eligible_edit).hexdigest(),
            "protected_sha256":hashlib.sha256(protected).hexdigest()
        },
        "status":"GENERATION_READY" if ready else "STRUCTURE_VALID_NOT_GENERATION_READY"
    }


def audit_legacy_kingswell_coverage(sketch, detail, width, height):
    """Quantify incomplete 14-window LEGACY planning against approved real outline.

    This is deliberately not building-density coverage: the polygon also
    includes streets, water and terrain. Never infer that missing windows
    correspond one-for-one to missing buildings.
    """
    zone=_polygon_mask((width,height),sketch["raion_polygon_candidate_px"]).tobytes()
    m=Image.new("L",(width,height),0);p=ImageDraw.Draw(m)
    for item in detail["lots"]:
        x0,y0,x1,y1=item["core"]
        require(x0<x1 and y0<y1,"invalid legacy macro-window")
        p.rectangle((int(x0),int(y0),int(x1)-1,int(y1)-1),fill=1)
    painted=m.tobytes()
    total=sum(zone)
    covered=sum(1 for a,b in zip(zone,painted) if a and b)
    require(total>0,"empty Kingswell polygon")
    return {"polygon_pixels":total,"legacy_window_pixels":covered,
            "window_coverage_pct":round(covered*100/total,2),
            "unwindowed_pixels":total-covered,
            "full_generation_area_coverage_proven":False,
            "area_basis":"all Kingswell polygon including water/streets/terrain",
            "legacy_windows_are_city_lots":False}


def verify_no_protected_edits(original, modified, protected_indices):
    """Byte-level change guard: images must be identical at every protected pixel."""
    require(original.size==modified.size,"before/after dimensions differ")
    a=original.convert("RGBA").tobytes();b=modified.convert("RGBA").tobytes()
    for i in protected_indices:
        j=i*4
        require(a[j:j+4]==b[j:j+4],f"protected pixel changed: {i}")
    return True


def cli():
    raise SystemExit("urban_architecture.py is internal only; use scripts/pipeline.py run")


if __name__=="__main__":
    cli()

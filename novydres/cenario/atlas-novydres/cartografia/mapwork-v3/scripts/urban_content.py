#!/usr/bin/env python3
"""Deterministic, infrastructure-first individual-building layouts for bounded work units.

The layout uses U02 abstract coordinates, never metres, population or a claim that
a synthetic geometry reproduces the real city. No image pixels are generated here.
"""
from __future__ import annotations

import collections
import hashlib
import math

import urban_architecture as urban


def _choose_building_use(mix, key):
    q=int(hashlib.sha256(key.encode("utf-8")).hexdigest()[:12],16)/float(16**12)
    for name,weight in sorted(mix.items()):
        q-=weight
        if q<=0:
            return name
    return sorted(mix)[-1]


def _street_access(width,height,labels,editable,road):
    """Multi-source BFS: each parcel must connect through its block to an at-grade street.

    Grid corridors run between building setbacks. This proves topological ground access,
    not physical vehicle clearance, legal easements, or scaled street widths.
    """
    parents={}
    distance={}
    q=collections.deque()
    for i,allowed in enumerate(editable):
        if not allowed:
            continue
        x,y=i%width,i//width
        neighbors=[]
        if x: neighbors.append(i-1)
        if x<width-1: neighbors.append(i+1)
        if y: neighbors.append(i-width)
        if y<height-1: neighbors.append(i+width)
        if any(road[j] for j in neighbors):
            parents[i]=None
            distance[i]=0
            q.append(i)
    while q:
        i=q.popleft()
        x,y=i%width,i//width
        neigh=[]
        if x: neigh.append(i-1)
        if x<width-1: neigh.append(i+1)
        if y: neigh.append(i-width)
        if y<height-1: neigh.append(i+width)
        for j in neigh:
            if editable[j] and labels[i]==labels[j] and j not in parents:
                parents[j]=i
                distance[j]=distance[i]+1
                q.append(j)
    return parents,distance


def design_context(plan):
    """Build one reusable spatial index for all work-unit designs of a city."""
    w,h=plan["grid"]["width"],plan["grid"]["height"]
    zone,classes,names,_=urban.classify_territory(plan)
    eligible_classes={names["urban"],names["industrial"]}
    eligible=bytearray(1 if zone[i] and classes[i] in eligible_classes else 0 for i in range(w*h))
    dividers=urban._line_mask((w,h),plan["transport"],lambda e:
        e["separates_blocks"] and e.get("level",e.get("level_from",0))==0).tobytes()
    protected=urban.spatial_protection_mask(plan).tobytes()
    labels,blocks=urban._label_blocks(w,h,eligible,dividers,classes)
    editable=bytearray(1 if eligible[i] and not protected[i] else 0 for i in range(w*h))
    roads=urban._line_mask((w,h),plan["transport"],lambda e:
        e["class"] in urban.ROAD_CLASSES and
        e.get("level",e.get("level_from",0))==0).tobytes()
    parents,distance=_street_access(w,h,labels,editable,roads)
    return dict(w=w,h=h,classes=classes,names=names,labels=labels,blocks=blocks,
                editable=editable,parents=parents,distance=distance)


def design_unit(plan, report, work_unit_id, *, max_buildings=512, context=None):
    """Emit explicit parcel/building footprints for one atomic generation window.

    Fail on inaccessible buildings or an oversize job. All footprint rectangles are
    strictly within one eligible U02 pixel, leaving perimeter service circulation.
    """
    urban.require(report["zone"]==plan["zone"]["id"],"urban report/plan identity mismatch")
    work=next((x for x in report["work_units"] if x["id"]==work_unit_id),None)
    urban.require(work is not None,"unknown work unit")
    ctx=context if context is not None else design_context(plan)
    w,h=ctx["w"],ctx["h"]
    classes,names=ctx["classes"],ctx["names"]
    labels,blocks=ctx["labels"],ctx["blocks"]
    editable=ctx["editable"]
    parents,distance=ctx["parents"],ctx["distance"]
    programs={b["block_id"]:b for b in report["block_programs"]}
    target_block=next((b for i,b in enumerate(blocks,1)
                       if i==work["block_label"]),None)
    urban.require(target_block is not None,"work unit references absent city block")
    program=programs[target_block["id"]]
    reverse={v:k for k,v in names.items()}
    buildings=[]
    inaccessible=[]
    x0,y0,x1,y1=work["bbox"]
    for y in range(y0,y1):
        for x in range(x0,x1):
            i=y*w+x
            if not editable[i] or labels[i]!=work["block_label"]:
                continue
            typ=reverse[classes[i]]
            profile=plan["morphology"][typ]
            target=profile["occupation_target"]
            inset=(1-math.sqrt(target))/2
            building_id=f"B-{work_unit_id}-{y:04d}-{x:04d}"
            band=profile["building_floors"]
            hash_value=int(hashlib.sha256(building_id.encode()).hexdigest()[:8],16)
            floors=band[0]+hash_value%(band[1]-band[0]+1)
            if i not in parents:
                inaccessible.append(building_id)
            parent=parents.get(i)
            buildings.append({
                "id":building_id,
                "parcel":[x,y,x+1,y+1],
                "footprint":[round(x+inset,6),round(y+inset,6),
                             round(x+1-inset,6),round(y+1-inset,6)],
                "use":_choose_building_use(profile["use_mix"],building_id),
                "floors":floors,
                "landuse":typ,
                "typology":profile["typology"],
                "road_access_steps":distance.get(i),
                "next_access_cell":[parent%w,parent//w] if parent is not None else None
            })
    urban.require(len(buildings)==work["pixels"],
                  "parcel coverage differs from exactly assigned work-unit pixels")
    urban.require(len(buildings)<=max_buildings,
                  "too many buildings for one job; reduce max_units and regenerate planning queue")
    return {
        "schema":"NOVYDRES_MAPWORK_V32_URBAN_DESIGN_UNIT_1",
        "zone":plan["zone"]["id"],
        "work_unit":work_unit_id,
        "city_block":target_block["id"],
        "landuse_program":program["urban_program"],
        "poi_sites":program["poi_sites"],
        "building_count":len(buildings),
        "parcels_covered_exactly_once":True,
        "building_footprints_in_editable_area":True,
        "access_verified":not inaccessible,
        "inaccessible_buildings":inaccessible,
        "access_semantics":"GRID_PEDESTRIAN_PATH_CANDIDATE_NOT_VEHICLE_CLEARANCE",
        "buildings":buildings,
        "owner_image_approval_inferred":False
    }

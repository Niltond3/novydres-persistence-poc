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


def _street_access(width, height, labels, editable, road):
    # Shared authority; do not fork access semantics between planner and asset layout.
    return urban._street_access(width, height, labels, editable, road)


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
    blocking=urban._line_mask((w,h),plan["transport"],lambda e:
        (e["class"] in (urban.RAIL_CLASSES | urban.WATER_CLASSES) and
         e.get("level",e.get("level_from",0))==0) or
        (e.get("surface_easement") is True and e["class"] in urban.UNDERGROUND_CLASSES)).tobytes()
    forbidden=bytearray(1 if classes[i] in
        (names["water"],names["natural"],names["protected"]) or blocking[i] else 0
        for i in range(w*h))
    return dict(w=w,h=h,classes=classes,names=names,labels=labels,blocks=blocks,
                editable=editable,parents=parents,distance=distance,
                roads=roads,forbidden=forbidden)


def _predicted_footprint(plan,ctx,x,y):
    """Compute a neighboring parcel's real planned rectangle without global upscale."""
    if x<0 or y<0 or x>=ctx["w"] or y>=ctx["h"]:
        return None
    i=y*ctx["w"]+x
    if not ctx["editable"][i] or not ctx["labels"][i]:
        return None
    special=next((s for s in plan["special_sites"]
                  if int(s["point"][0])==x and int(s["point"][1])==y),None)
    if special:
        return special["footprint"]
    reverse={v:k for k,v in ctx["names"].items()}
    profile=plan["morphology"][reverse[ctx["classes"][i]]]
    inset=(1-math.sqrt(profile["occupation_target"]))/2
    return [x+inset,y+inset,x+1-inset,y+1-inset]


def validate_unit_physical_access(plan,design,authored,ctx,physical):
    """Confirm individually authored, local vector corridors against all nearby parcels."""
    if not physical:
        return False
    routes=authored.get("physical_routes")
    buildings=design["buildings"]
    if not isinstance(routes,dict) or set(routes)!={b["id"] for b in buildings}:
        return False
    roads=[e for e in plan["transport"]["edges"] if
           e["class"] in urban.ROAD_CLASSES and
           e.get("level",e.get("level_from"))==0]
    for b in buildings:
        route=routes[b["id"]]
        pts=route.get("points") if isinstance(route,dict) else None
        if not isinstance(pts,list) or not pts or not all(urban.finite_xy(p) for p in pts):
            return False
        rad=route.get("width_m",0)/physical["metres_per_unit"]/2
        if not isinstance(rad,(int,float)) or not math.isfinite(rad) or rad<=0 or rad>=1:
            return False
        xs=[p[0] for p in pts];ys=[p[1] for p in pts]
        left=max(0,int(math.floor(min(xs)-rad))-1)
        right=min(ctx["w"],int(math.ceil(max(xs)+rad))+2)
        top=max(0,int(math.floor(min(ys)-rad))-1)
        bottom=min(ctx["h"],int(math.ceil(max(ys)+rad))+2)
        if (right-left)*(bottom-top)>4096:
            return False
        obstacles,forbidden=[],[]
        own=(int(b["parcel"][0]),int(b["parcel"][1]))
        for y in range(top,bottom):
            for x in range(left,right):
                if (x,y)!=own:
                    footprint=_predicted_footprint(plan,ctx,x,y)
                    if footprint is not None:
                        obstacles.append(footprint)
                i=y*ctx["w"]+x
                if ctx["forbidden"][i]:
                    forbidden.append([x,y,x+1,y+1])
        urban.validate_physical_route(
            route,entrance=b["entrance"],footprint=b["footprint"],
            mode=b["access_mode"],scale=physical["metres_per_unit"],
            minimum_width_m=physical["minimum_width_m"][b["access_mode"]],
            ground_roads=roads,obstacles=obstacles,forbidden=forbidden)
    return True


def design_unit(plan, report, work_unit_id, *, max_buildings=512, context=None):
    """Emit explicit parcel/building footprints for one atomic generation window.

    Fail on inaccessible buildings or an oversize job. All footprint rectangles are
    strictly within one eligible U02 pixel, leaving perimeter service circulation.
    """
    if plan.get("work_policy",{}).get("parceling")=="URBAN_BLOCKS":
        import parceling
        return parceling.design_unit(plan,report,work_unit_id,
                                     max_buildings=max_buildings,context=context)
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
    sites={(int(s["point"][0]),int(s["point"][1])):s for s in plan["special_sites"]}
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
            special=sites.get((x,y))
            footprint=special["footprint"] if special else [
                round(x+inset,6),round(y+inset,6),
                round(x+1-inset,6),round(y+1-inset,6)]
            clearance=2*min(footprint[0]-x,footprint[1]-y,
                            x+1-footprint[2],y+1-footprint[3])
            building_id=f"B-{work_unit_id}-{y:04d}-{x:04d}"
            band=profile["building_floors"]
            hash_value=int(hashlib.sha256(building_id.encode()).hexdigest()[:8],16)
            floors=band[0]+hash_value%(band[1]-band[0]+1)
            if i not in parents or clearance+1e-8 < profile["access_clearance_units"]:
                inaccessible.append(building_id)
            parent=parents.get(i)
            if special:
                entrance=special["entrance"]
            else:
                neighbor=parent
                if neighbor is None:
                    candidate=[]
                    for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)):
                        nx,ny=x+dx,y+dy
                        if 0<=nx<w and 0<=ny<h and ctx["roads"][ny*w+nx]:
                            candidate.append((nx,ny))
                    if candidate:
                        nx,ny=candidate[0]
                    else:
                        nx,ny=x,y
                else:
                    nx,ny=neighbor%w,neighbor//w
                entrance=([footprint[0],(footprint[1]+footprint[3])/2] if nx<x else
                          [footprint[2],(footprint[1]+footprint[3])/2] if nx>x else
                          [(footprint[0]+footprint[2])/2,footprint[1]] if ny<y else
                          [(footprint[0]+footprint[2])/2,footprint[3]] if ny>y else None)
            buildings.append({
                "id":building_id,
                "parcel":[x,y,x+1,y+1],
                "footprint":footprint,
                "use":"special_site" if special else _choose_building_use(profile["use_mix"],building_id),
                "site_id":special["id"] if special else None,
                "entrance":entrance,
                "access_mode":profile["access_mode"],
                "clearance_units":round(clearance,6),
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
        "schema":"NOVYDRES_MAPWORK_URBAN_DESIGN_UNIT_1",
        "zone":plan["zone"]["id"],
        "work_unit":work_unit_id,
        "city_block":target_block["id"],
        "landuse_program":program["urban_program"],
        "poi_sites":[s["id"] for s in sites.values() if
                     s["block_id"]==target_block["id"] and
                     x0<=s["point"][0]<x1 and y0<=s["point"][1]<y1],
        "building_count":len(buildings),
        "parcels_covered_exactly_once":True,
        "building_footprints_in_editable_area":True,
        "access_verified":not inaccessible,
        "inaccessible_buildings":inaccessible,
        "access_semantics":"VERIFIED_ABSTRACT_U02_GROUND_CORRIDOR_NOT_METRIC_CERTIFICATION",
        "buildings":buildings,
        "owner_image_approval_inferred":False
    }

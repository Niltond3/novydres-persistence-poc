#!/usr/bin/env python3
"""Deterministic  urban block parceling on the abstract U02 grid.

Not a metric cadastral survey. A parcel can span multiple U02 cells; building
footprints and polygons need not be one square per pixel. All parcels stay
within the same road-bounded block, land-use class and atomic work unit.
"""
from __future__ import annotations

import hashlib
import math

import urban_architecture as urban


def _key(label):
    return int(hashlib.sha256(label.encode("utf-8")).hexdigest()[:12], 16)


def _round(v):
    return round(v, 6)


def polygon_for_box(box, form):
    x0,y0,x1,y1=box
    dx,dy=x1-x0,y1-y0
    if form=="L_SHAPE":
        return [[x0,y0],[x1,y0],[x1,y0+dy*.43],
                [x0+dx*.55,y0+dy*.43],[x0+dx*.55,y1],[x0,y1]]
    if form=="U_SHAPE":
        return [[x0,y0],[x1,y0],[x1,y1],[x0+dx*.70,y1],
                [x0+dx*.70,y0+dy*.50],[x0+dx*.30,y0+dy*.50],
                [x0+dx*.30,y1],[x0,y1]]
    return [[x0,y0],[x1,y0],[x1,y1],[x0,y1]]


def design_unit(plan, report, work_unit_id, *, max_buildings=512, context=None):
    import urban_content as old

    urban.require(report["zone"]==plan["zone"]["id"],
                  " urban report/plan identity mismatch")
    unit=next((u for u in report["work_units"] if u["id"]==work_unit_id),None)
    urban.require(unit is not None, " work unit unknown")
    ctx=context if context is not None else old.design_context(plan)
    w,h=ctx["w"],ctx["h"]
    x0,y0,x1,y1=unit["bbox"]
    eligible={
        (x,y) for y in range(y0,y1) for x in range(x0,x1)
        if ctx["editable"][y*w+x] and
        ctx["labels"][y*w+x]==unit["block_label"]
    }
    areas={
        s["point"][0]:s for s in []  # no inferred new canonical sites
    }
    special={(int(s["point"][0]),int(s["point"][1])):s
             for s in plan["special_sites"]}
    used=set()
    buildings=[]
    inaccessible=[]
    reverse={v:k for k,v in ctx["names"].items()}
    target_block=ctx["blocks"][unit["block_label"]-1]
    program=next(b for b in report["block_programs"]
                 if b["block_id"]==target_block["id"])
    for x,y in sorted(eligible,key=lambda p:(p[1],p[0])):
        if (x,y) in used:
            continue
        i=y*w+x
        typ=reverse[ctx["classes"][i]]
        profile=plan["morphology"][typ]
        seed=_key(f"{unit['id']}:{x}:{y}")
        # Preference, not an artificial minimum density: no block crossing,
        # no new road, no absorption of a protected/special adjacent cell.
        choices=([(2,2),(2,1),(1,2),(1,1)] if seed%3==0 else
                 [(1,2),(2,1),(2,2),(1,1)] if seed%3==1 else
                 [(2,1),(2,2),(1,2),(1,1)])
        if (x,y) in special:
            choices=[(1,1)]
        width=height=1
        for dx,dy in choices:
            group={(xx,yy) for yy in range(y,y+dy) for xx in range(x,x+dx)}
            if (group <= (eligible-used) and
                all((xx,yy) not in special and
                    ctx["classes"][yy*w+xx]==ctx["classes"][i]
                    for xx,yy in group) if (x,y) not in special else (dx,dy)==(1,1)):
                width,height=dx,dy
                break
        cells={(xx,yy) for yy in range(y,y+height)
               for xx in range(x,x+width)}
        urban.require(cells <= (eligible-used),
                      " parcel intersects another owner or protected area")
        used.update(cells)
        parcel=[x,y,x+width,y+height]
        special_site=special.get((x,y))
        target=profile["occupation_target"]
        inset=(1-math.sqrt(target))/2
        # Inset is proportional to parcel dimensions, but always leaves
        # a circulation margin. No inference of actual metres is made.
        footprint=(list(special_site["footprint"]) if special_site else
                   [_round(x+inset),_round(y+inset),
                    _round(x+width-inset),_round(y+height-inset)])
        urban.require(0<=footprint[0]-x and 0<=footprint[1]-y and
                      footprint[2]<=x+width and footprint[3]<=y+height,
                      " footprint exceeds parcel")
        selected=min(cells,key=lambda cell:ctx["distance"].get(cell[1]*w+cell[0],10**12))
        first=selected[1]*w+selected[0]
        parent=ctx["parents"].get(first)
        pcoord=(parent%w,parent//w) if parent is not None else None
        if pcoord is not None and pcoord in cells:
            # Follow the deterministic access-tree until leaving the parcel.
            probe=parent
            for _ in range(len(cells)+1):
                if probe is None or (probe%w,probe//w) not in cells:
                    break
                probe=ctx["parents"].get(probe)
            if probe is not None:
                pcoord=(probe%w,probe//w)
        if special_site:
            entrance=special_site["entrance"]
        elif pcoord is None:
            entrance=None
        else:
            nx,ny=pcoord
            # Door is always on the perimeter rectangle, not in the yard.
            entrance=(
                [footprint[0],(footprint[1]+footprint[3])/2] if nx<x else
                [footprint[2],(footprint[1]+footprint[3])/2] if nx>=x+width else
                [(footprint[0]+footprint[2])/2,footprint[1]] if ny<y else
                [(footprint[0]+footprint[2])/2,footprint[3]] if ny>=y+height else None
            )
        bid=f"B-{unit['id']}-{y:04d}-{x:04d}"
        clearance=2*min(footprint[0]-x,footprint[1]-y,
                        x+width-footprint[2],y+height-footprint[3])
        reachable=parent is not None and entrance is not None and (
            clearance+1e-8>=profile["access_clearance_units"])
        if not reachable:
            inaccessible.append(bid)
        floors=profile["building_floors"]
        form=("RECTANGLE" if special_site else
              ("L_SHAPE","U_SHAPE","RECTANGLE","RECTANGLE")[seed%4]
              if len(cells)>1 else "RECTANGLE")
        poly=polygon_for_box(footprint,form)
        yard=(None if special_site else [x,y,x+width,y+height])
        buildings.append({
            "id":bid,"parcel":parcel,
            "parcel_cells":[[xx,yy] for xx,yy in sorted(cells)],
            "parcel_polygon":polygon_for_box(parcel,"RECTANGLE"),
            "footprint":footprint,
            "footprint_polygon":[[_round(px),_round(py)] for px,py in poly],
            "mass_form":form,
            "courtyard_type":"SEMI_PRIVATE" if form=="U_SHAPE" else
                              "SERVICE_YARD" if form=="L_SHAPE" else "NONE",
            "service_yard":yard,
            "use":"special_site" if special_site else
                  old._choose_building_use(profile["use_mix"],bid),
            "site_id":special_site["id"] if special_site else None,
            "entrance":entrance,"access_mode":profile["access_mode"],
            "clearance_units":_round(clearance),
            "floors":floors[0]+seed%(floors[1]-floors[0]+1),
            "landuse":typ,"typology":profile["typology"],
            "road_access_steps":ctx["distance"].get(first),
            "next_access_cell":list(pcoord) if pcoord is not None else None
        })
    urban.require(used==eligible," parcel coverage not exactly 100 percent")
    urban.require(len(buildings)<=max_buildings,
                  " work unit exceeds atomic building budget")
    return {
        "schema":"NOVYDRES_MAPWORK_URBAN_DESIGN_UNIT",
        "zone":plan["zone"]["id"],"work_unit":work_unit_id,
        "city_block":target_block["id"],
        "landuse_program":program["urban_program"],
        "poi_sites":[s["id"] for s in special.values()
                     if s["block_id"]==target_block["id"]
                     and x0<=s["point"][0]<x1 and y0<=s["point"][1]<y1],
        "building_count":len(buildings),
        "assigned_u02_cells":len(used),
        "parcels_covered_exactly_once":True,
        "building_footprints_in_editable_area":True,
        "access_verified":not inaccessible,
        "inaccessible_buildings":inaccessible,
        "access_semantics":"VERIFIED_ABSTRACT_U02_NO_METRIC_CERTIFICATION",
        "physical_scale_certified":False,
        "buildings":buildings,
        "owner_image_approval_inferred":False
    }

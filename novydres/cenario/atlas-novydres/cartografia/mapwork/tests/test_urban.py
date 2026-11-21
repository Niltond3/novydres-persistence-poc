"""consolidated block-parcel planner tests; synthetic grid is never real city canon."""
import copy
import sys
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import mapwork as core
import urban_architecture as urban
import urban_content


def _setup():
    plan=core.load(ROOT/"fixtures"/"topology-synthetic.json")
    plan["work_policy"]["parceling"]="URBAN_BLOCKS"
    report=urban.plan_city(plan,core.load(ROOT/"config.json"))
    return plan,report


def test_urban_parcels_cover_blocks_exactly_once_and_show_variety():
    plan,report=_setup()
    found=False
    for work in report["work_units"]:
        design=urban_content.design_unit(plan,report,work["id"])
        cells=[tuple(v) for b in design["buildings"] for v in b["parcel_cells"]]
        assert len(cells)==len(set(cells))==work["pixels"]
        assert design["assigned_u02_cells"]==work["pixels"]
        assert design["building_count"]<=work["pixels"]
        assert design["parcels_covered_exactly_once"]
        assert all(len(b["footprint_polygon"])>=4 for b in design["buildings"])
        assert all(b["road_access_steps"] is not None or not design["access_verified"]
                   for b in design["buildings"])
        found|=any(len(b["parcel_cells"])>1 for b in design["buildings"])
    assert found, "synthetic sample ought to exercise at least one multi-cell parcel"


def test_urban_is_deterministic_and_inherits_site_identity():
    plan,report=_setup()
    uid=report["work_units"][0]["id"]
    one=urban_content.design_unit(plan,report,uid)
    two=urban_content.design_unit(copy.deepcopy(plan),copy.deepcopy(report),uid)
    assert one==two
    assert one["physical_scale_certified"] is False
    assert one["schema"]=="NOVYDRES_MAPWORK_URBAN_DESIGN_UNIT"

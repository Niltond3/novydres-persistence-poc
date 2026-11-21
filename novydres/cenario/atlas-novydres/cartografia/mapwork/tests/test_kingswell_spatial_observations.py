"""consolidated Kingswell candidate U02 vectors: regression guards, not an art-ready schema."""
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / 'zones' / 'cidade-velha' / 'spatial-observations.json'
SHA_U02 = '9d55965f45181e3b943552e32df0e8ad41b63c8974ffd6e670f447ffd36eb9a0'
SHA_SKETCH = '180f3a01ad40983b6ade2217cb488c7b591fa45d'

def point_dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def proper_cross(a, b, c, d):
    def cross(u, v): return u[0]*v[1]-u[1]*v[0]
    v=(b[0]-a[0], b[1]-a[1]); w=(d[0]-c[0], d[1]-c[1]); z=(c[0]-a[0], c[1]-a[1])
    den=cross(v, w)
    if abs(den)<1.e-10: return False
    t=cross(z,w)/den; u=cross(z,v)/den
    return -1.e-9<=t<=1+1.e-9 and -1.e-9<=u<=1+1.e-9

def line_intersects(a,b):
    return any(proper_cross(a[i],a[i+1],b[j],b[j+1]) for i in range(len(a)-1) for j in range(len(b)-1))

def assert_guards(o):
    assert o['schema']=='NOVYDRES_MAPWORK_U02_SPATIAL_OBSERVATIONS'
    assert o['reference']['sha256']==SHA_U02
    assert [o['reference']['width'],o['reference']['height']]==[1448,1086]
    assert o['source']['sketch_blob_sha']==SHA_SKETCH
    assert o['status']=='PARTIAL_RASTER_BACKED_VECTOR_TRACING_NOT_GLOBAL_SPATIAL'
    assert o['validation']['generation_ready'] is False
    assert o['validation']['spatial_network_topology_certified'] is False
    assert o['validation']['neighbor_seams_verified'] is False
    assert o['validation']['landuse_100_percent_classified'] is False
    metro=o['other_modes']['metro']
    assert metro['owner_approved_option']=='A' and metro['core_exclusion']=='KW-HIST'
    assert metro['alignment'] is None and not metro['stations'] and not metro['portals'] and not metro['bilateral_joins']
    assert not o['other_modes']['rail']['new_geometry_authorized']
    bridges=o['historical_bridge_sites']
    assert [b['id'] for b in bridges]==['KW-B01','KW-B02','KW-B03']
    roads=o['observed_major_road_corridors']
    assert len(roads)>=20 and len(roads)==len({r['id'] for r in roads})
    byid={r['id']:r for r in roads}
    w,h=o['reference']['width'],o['reference']['height']
    for r in roads:
        pts=r['points_px']
        assert len(pts)>=2 and all(0<=x<w and 0<=y<=h for x,y in pts)
        assert r['level']=='UNVERIFIED_FOR_GRADE'
        assert r['geometry_status']=='TRACED_ON_U02_NOT_NETWORK_CERTIFIED'
    approaches={'KW-B01':('KW-R-08','KW-R-09'), 'KW-B02':('KW-R-03','KW-R-10'), 'KW-B03':('KW-R-12','KW-R-11')}
    river=o['hydrography'][0]['points_px']
    for b in bridges:
        assert line_intersects(b['approved_sketch_span_px'],river)
        for endpoint,road in zip(b['approved_sketch_span_px'],approaches[b['id']]):
            pts=byid[road]['points_px']
            assert min(point_dist(endpoint,pts[0]),point_dist(endpoint,pts[-1]))<=2.5
    junctions=o.get('intersection_candidates',[])
    assert len(junctions)==o['validation']['provisional_road_road_intersections']==24
    assert all(j['grade']=='UNRESOLVED' and j['graph_connectivity']=='NOT_ASSERTED' for j in junctions)
    crossings=o.get('additional_road_river_intersections',[])
    assert len(crossings)==4 and all(c['is_new_bridge'] is False for c in crossings)
    assert len(o['poi_sketch_anchors'])==5
    assert all(not p['footprint_surveyed'] and not p['site_access_verified'] for p in o['poi_sketch_anchors'])

class TestU02SpatialObservations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(OBS.read_text(encoding='utf-8'))

    def test_positive_guards(self): assert_guards(self.data)

    def test_negative_source_sha(self):
        bad=copy.deepcopy(self.data);bad['reference']['sha256']='0'*64
        with self.assertRaises(AssertionError): assert_guards(bad)

    def test_negative_fourth_historical_bridge(self):
        bad=copy.deepcopy(self.data)
        bad['historical_bridge_sites'].append(dict(bad['historical_bridge_sites'][0],id='KW-B04'))
        with self.assertRaises(AssertionError): assert_guards(bad)

    def test_negative_invented_metro(self):
        bad=copy.deepcopy(self.data);bad['other_modes']['metro']['alignment']=[[600,800],[670,900]]
        with self.assertRaises(AssertionError): assert_guards(bad)

    def test_negative_grade_falsification(self):
        bad=copy.deepcopy(self.data);bad['observed_major_road_corridors'][0]['level']=0
        with self.assertRaises(AssertionError): assert_guards(bad)

    def test_negative_displaced_bridge(self):
        bad=copy.deepcopy(self.data)
        bad['historical_bridge_sites'][0]['approved_sketch_span_px']=[[950,900],[970,910]]
        with self.assertRaises(AssertionError): assert_guards(bad)

    def test_negative_ready_flag(self):
        bad=copy.deepcopy(self.data);bad['validation']['generation_ready']=True
        with self.assertRaises(AssertionError): assert_guards(bad)

    def test_negative_invented_poi_access(self):
        bad=copy.deepcopy(self.data);bad['poi_sketch_anchors'][0]['site_access_verified']=True
        with self.assertRaises(AssertionError): assert_guards(bad)

    def test_optional_real_u02_sha(self):
        path=os.environ.get('NOVYDRES_U02_PATH')
        if not path:self.skipTest('U02 private bytes not supplied to this executor')
        with open(path,'rb') as f: actual=hashlib.file_digest(f,'sha256').hexdigest()
        self.assertEqual(actual,SHA_U02)

if __name__=='__main__': unittest.main()

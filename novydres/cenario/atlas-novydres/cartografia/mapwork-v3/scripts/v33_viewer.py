#!/usr/bin/env python3
"""Offline/mobile tile-on-demand comparison; full U02 atlas stays integral.

No base64 tile atlas, no 92k x 69k monolithic bitmap, no server/GitHub access.
The comparison is a portable directory (and optional zip), containing only
necessary high-resolution tile files plus a low-resolution global overview.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from urllib.parse import quote

from PIL import Image


def _safe_tile(name):
    path = Path(name)
    if path.is_absolute() or len(path.parts) != 1 or path.suffix != ".png" or ".." in path.parts:
        raise ValueError("unsafe viewer tile filename")
    return path.name


def _copy_tile(source, target, entry):
    name = _safe_tile(entry["filename"])
    src = Path(source) / name
    if not src.is_file():
        raise ValueError("tile is absent: " + name)
    target.mkdir(parents=True, exist_ok=True)
    dst = target / name
    if src.resolve() != dst.resolve():
        shutil.copy2(src, dst)
    return name


def build_comparison(before, after, reference, output, cfg, *, zip_bundle=False):
    """Produce self-contained mobile comparison folder, not a single embedded HTML."""
    import mapwork as core

    core.source_check(reference, cfg)
    after_root = Path(after)
    prior_root = Path(before) if before else None
    new_manifest = core.load(after_root / "tiles.json")
    core.verify_tiles(new_manifest, after_root, cfg, inherited_root=prior_root)
    old_manifest = core.load(prior_root / "tiles.json") if prior_root else None
    if old_manifest:
        core.verify_tiles(old_manifest, prior_root, cfg)
    root = Path(output).parent
    root.mkdir(parents=True, exist_ok=True)
    tile_root = root / "viewer-assets"
    tile_root.mkdir(parents=True, exist_ok=True)
    ref_dst = tile_root / "reference.png"
    if Path(reference).resolve() != ref_dst.resolve():
        shutil.copy2(reference, ref_dst)
    s, tile = cfg["detail_pixels_per_unit"], cfg["tile_size_px"]
    before_entries = {}
    if old_manifest:
        for entry in old_manifest.get("inherited_tiles", []) + old_manifest["tiles"]:
            before_entries[(entry["x"], entry["y"])] = entry
    after_entries = dict(before_entries)
    for entry in new_manifest.get("inherited_tiles", []):
        after_entries[(entry["x"], entry["y"])] = entry
    for entry in new_manifest["tiles"]:
        after_entries[(entry["x"], entry["y"])] = entry
    prior_copied, after_copied = {}, {}

    def transfer(entries, subdir):
        payload = []
        target = tile_root / subdir
        for coords, entry in sorted(entries.items()):
            # Inherited entries require bytes from the previously approved release.
            from_new = entry in new_manifest["tiles"]
            folder = after_root if from_new else prior_root
            if folder is None:
                raise ValueError("inherited tile has no approved source")
            name = _copy_tile(folder, target, entry)
            payload.append({"x": coords[0], "y": coords[1],
                            "width": entry["width"], "height": entry["height"],
                            "src": "viewer-assets/" + subdir + "/" + quote(name)})
        return payload

    prior = transfer(before_entries, "before") if before_entries else []
    candidate = transfer(after_entries, "after")
    data = {"base": "viewer-assets/reference.png", "before": prior,
            "after": candidate, "s": s, "tile": tile,
            "w": cfg["world_size_units"][0], "h": cfg["world_size_units"][1]}

    def overview(entries, target):
        with Image.open(reference) as img:
            canvas = img.convert("RGBA")
        for item in entries:
            coords = (item["x"], item["y"])
            p = root / item["src"]
            with Image.open(p) as tile_img:
                tiny = tile_img.convert("RGBA").resize(
                    (max(1, round(item["width"] / s)),
                     max(1, round(item["height"] / s))), Image.Resampling.LANCZOS)
            canvas.alpha_composite(tiny, (coords[0] * tile // s,
                                          coords[1] * tile // s))
        canvas.convert("RGB").save(root / target, optimize=True)

    overview(prior, "overview-before.png")
    overview(candidate, "overview-after.png")
    template = r"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>Novydres — ANTES / DEPOIS</title>
<style>
:root{color-scheme:dark}body{background:#111920;color:#eee;font:14px system-ui;margin:8px}
header{display:flex;flex-wrap:wrap;gap:8px;align-items:center}button{background:#25384b;color:white;border:1px solid #7c90a1;border-radius:7px;padding:8px 12px}
.views{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px}
.frame{border:1px solid #627184;border-radius:8px;overflow:hidden}canvas{width:100%;height:70vh;background:#23303a;display:block;touch-action:none}
h3{font-size:13px;margin:9px 0}small{opacity:.75}@media(max-width:700px){.views{grid-template-columns:1fr}canvas{height:35vh}}
</style></head><body>
<header><strong>Novydres • atlas integral</strong><button id="plus">Zoom +</button>
<button id="minus">Zoom −</button><button id="reset">Ver tudo</button>
<small>Arraste, use pinça ou roda do mouse. Visualização sincronizada, tiles sob demanda.</small></header>
<div class="views"><section><h3>ANTES — aprovado</h3><div class="frame"><canvas id="before"></canvas></div></section>
<section><h3>DEPOIS — candidato (não canônico)</h3><div class="frame"><canvas id="after"></canvas></div></section></div>
<script>
const D=__DATA__, views=[document.getElementById('before'),document.getElementById('after')];
const pools=[D.before,D.after], cache=new Map(), pending=new Set(), MAX_CACHE=96;
let zoom=1,dx=0,dy=0,active=new Map(),pinch=null;
const overviews=[new Image(),new Image()];overviews[0].src='overview-before.png';overviews[1].src='overview-after.png';overviews.forEach(im=>im.onload=draw);
function getImage(src){
  if(cache.has(src)){const i=cache.get(src);cache.delete(src);cache.set(src,i);return i;}
  if(pending.has(src))return null;
  const im=new Image();pending.add(src);im.onload=()=>{pending.delete(src);cache.set(src,im);
    if(cache.size>MAX_CACHE)cache.delete(cache.keys().next().value);draw()};
  im.onerror=()=>{pending.delete(src);console.error('Tile indisponível:',src)};
  im.src=src;return null;
}
function fit(c){return Math.min(c.clientWidth/D.w,c.clientHeight/D.h)}
function viewport(c){let k=fit(c)*zoom;return {k,x:(c.clientWidth-D.w*k)/2+dx,y:(c.clientHeight-D.h*k)/2+dy}}
function draw(){
  views.forEach((c,idx)=>{
    const pixelRatio=Math.min(devicePixelRatio||1,3),v=viewport(c);
    c.width=Math.round(c.clientWidth*pixelRatio);c.height=Math.round(c.clientHeight*pixelRatio);
    const g=c.getContext('2d');g.setTransform(pixelRatio,0,0,pixelRatio,0,0);
    g.clearRect(0,0,c.clientWidth,c.clientHeight);
    if(overviews[idx].complete&&overviews[idx].naturalWidth)g.drawImage(overviews[idx],v.x,v.y,D.w*v.k,D.h*v.k);
    for(const t of pools[idx]){
      const x=v.x+(t.x*D.tile/D.s)*v.k,y=v.y+(t.y*D.tile/D.s)*v.k;
      const w=(t.width/D.s)*v.k,h=(t.height/D.s)*v.k;
      if(x+w<0||y+h<0||x>c.clientWidth||y>c.clientHeight)continue;
      // Global overview is already accurate at small zoom: avoid loading
      // dozens of full-resolution images until actual detail is visible.
      if(v.k*D.s<.75)continue;
      const im=getImage(t.src);if(im&&im.complete)g.drawImage(im,x,y,w,h);
    }
  });
}
function scale(factor){zoom=Math.max(1,Math.min(D.s*6,zoom*factor));draw()}
document.getElementById('plus').onclick=()=>scale(1.6);
document.getElementById('minus').onclick=()=>scale(1/1.6);
document.getElementById('reset').onclick=()=>{zoom=1;dx=dy=0;draw()};
for(const c of views){
 c.addEventListener('pointerdown',e=>{c.setPointerCapture(e.pointerId);active.set(e.pointerId,[e.clientX,e.clientY]);});
 c.addEventListener('pointermove',e=>{
   if(!active.has(e.pointerId))return;
   const old=active.get(e.pointerId);active.set(e.pointerId,[e.clientX,e.clientY]);
   if(active.size===1){dx+=e.clientX-old[0];dy+=e.clientY-old[1];draw()}
   else if(active.size===2){
     const [a,b]=[...active.values()],d=Math.hypot(a[0]-b[0],a[1]-b[1]);
     if(pinch)scale(d/pinch);pinch=d;
   }
 });
 for(const event of ['pointerup','pointercancel','lostpointercapture'])
   c.addEventListener(event,e=>{active.delete(e.pointerId);pinch=null});
 c.addEventListener('wheel',e=>{e.preventDefault();scale(e.deltaY<0?1.2:1/1.2)},{passive:false});
}
addEventListener('resize',draw);draw();
</script></body></html>"""
    html = template.replace("__DATA__", json.dumps(data, separators=(",", ":")))
    Path(output).write_text(html, encoding="utf-8")
    bundle = None
    if zip_bundle:
        bundle = shutil.make_archive(str(root / "novydres-comparison"), "zip", root,
                                     base_dir=".")
    return {"path": str(output), "before_tiles": len(prior),
            "after_tiles": len(candidate), "bytes": Path(output).stat().st_size,
            "before_overview": str(root / "overview-before.png"),
            "after_overview": str(root / "overview-after.png"), "bundle": bundle}

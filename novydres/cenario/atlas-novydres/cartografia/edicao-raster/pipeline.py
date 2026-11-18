#!/usr/bin/env python3
"""Pipeline de máscaras de Novydres. Requer Pillow. Nunca sobrescreve o mapa-mestre."""
import argparse
import base64
import io
import json
from pathlib import Path
from PIL import Image, ImageDraw

def load_image(path):
    return Image.open(path).convert('RGB')

def mask_from_spec(spec, size):
    if list(size) != spec['base']['size']:
        raise ValueError('Resolução incompatível com a imagem-base')
    result = Image.new('L', size, 0)
    draw = ImageDraw.Draw(result)
    for polygon in spec['polygons']:
        draw.polygon([tuple(x) for x in polygon], fill=255)
    for polygon in spec.get('protected_holes', []):
        draw.polygon([tuple(x) for x in polygon], fill=0)
    return result

def preview(base, mask, destination):
    art = base.convert('RGBA')
    tint = Image.new('RGBA', art.size, (15, 190, 183, 0))
    tint.putalpha(mask.point(lambda v: 95 if v else 0))
    Image.alpha_composite(art, tint).convert('RGB').save(destination)

def compose(base, proposed, mask, destination):
    if not (base.size == proposed.size == mask.size):
        raise ValueError('As imagens e a máscara devem ter dimensões iguais')
    out = Image.composite(proposed, base, mask.point(lambda v: 255 if v else 0))
    if not verify(base, out, mask)['external_unchanged']:
        raise RuntimeError('Pixels externos à máscara foram alterados')
    out.save(destination)
    return out

def verify(base, result, mask):
    if not (base.size == result.size == mask.size):
        raise ValueError('Dimensões diferentes')
    a, b = base.tobytes(), result.tobytes()
    m = mask.tobytes()
    outside, inside, edited = 0, 0, 0
    for j, v in enumerate(m):
        changed = a[3*j:3*j+3] != b[3*j:3*j+3]
        if v == 0 and changed: outside += 1
        if v and changed: inside += 1
        if changed: edited += 1
    return dict(external_unchanged=(outside == 0), outside_changes=outside,
                inside_changes=inside, total_changes=edited, mask_pixels=sum(bool(v) for v in m))

def uri(image, crop=None):
    if crop: image = image.crop(crop)
    temp = io.BytesIO()
    image.save(temp, 'WEBP', quality=82, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(temp.getvalue()).decode('ascii')

def comparator(before, after, dest, bbox=None):
    if before.size != after.size: raise ValueError('Antes/depois com dimensões diferentes')
    if bbox is None: bbox = (0, 0, *before.size)
    sources = [uri(before), uri(after), uri(before, bbox), uri(after, bbox)]
    markup = '''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Novydres — comparação</title><style>
*{box-sizing:border-box}body{font:15px system-ui;background:#101923;color:#ecf5ff;margin:0;padding:12px}main{max-width:1250px;margin:auto}button{background:#263e52;color:white;border:1px solid #8e9ca6;border-radius:7px;padding:10px;margin:2px;cursor:pointer}button[aria-pressed=true]{background:#edc57a;color:#17232b}.compare{position:relative;overflow:hidden;touch-action:pan-y;user-select:none;cursor:ew-resize}.compare img,.panes img{width:100%;display:block;height:auto}.top{position:absolute;inset:0;clip-path:inset(0 50% 0 0)}.line{position:absolute;top:0;bottom:0;left:50%;width:2px;background:white;pointer-events:none}.panes{display:none;grid-template-columns:1fr 1fr;gap:12px}.panes figure{margin:0;min-width:0}.panes figcaption{margin:5px 0}input{width:85%;accent-color:#edc57a}.lbl{display:flex;justify-content:space-between}p{color:#b6c3d0;font-size:13px}@media(max-width:700px){.panes{grid-template-columns:1fr}button{font-size:13px}}
</style></head><body><main><h2>Novydres — Antes / Depois</h2><p>Mapa integral por padrão. Imagens incorporadas; sem serviços externos.</p><nav><button id="full" aria-pressed="true">Mapa completo</button><button id="detail" aria-pressed="false">Detalhe</button><button id="slide" aria-pressed="true">Deslizar</button><button id="side" aria-pressed="false">Lado a lado</button></nav>
<section id="overlay"><div class="lbl"><b>DEPOIS ◀</b><b>▶ ANTES</b></div><div class="compare" id="frame"><img id="before" src="__A__" alt="Antes"><img class="top" id="after" src="__B__" alt="Depois"><div class="line" id="line"></div></div><label for="mix">Divisão</label><input id="mix" type="range" min="0" max="100" value="50"></section>
<section id="panes" class="panes"><figure><figcaption>ANTES</figcaption><img id="paneA" src="__A__" alt="Antes integral"></figure><figure><figcaption>DEPOIS</figcaption><img id="paneB" src="__B__" alt="Depois integral"></figure></section>
<p>Imagens de comparação em WebP para abertura offline; preservação pixel a pixel é verificada nos arquivos PNG.</p></main><script>
const $=s=>document.querySelector(s),data={full:[$('#before').src,$('#after').src],detail:['__C__','__D__']};let view='full',mode='slide';
function selected(k){for(const id of ['full','detail'])$('#'+id).setAttribute('aria-pressed',id===k)}
function setView(k){view=k;selected(k);$('#before').src=$('#paneA').src=data[k][0];$('#after').src=$('#paneB').src=data[k][1]}
function setMode(k){mode=k;$('#overlay').style.display=k==='slide'?'block':'none';$('#panes').style.display=k==='side'?'grid':'none';$('#slide').setAttribute('aria-pressed',k==='slide');$('#side').setAttribute('aria-pressed',k==='side')}
function move(v){v=Math.max(0,Math.min(100,Number(v)));$('#mix').value=v;$('#after').style.clipPath='inset(0 '+(100-v)+'% 0 0)';$('#line').style.left=v+'%'}
$('#full').onclick=()=>setView('full');$('#detail').onclick=()=>setView('detail');$('#slide').onclick=()=>setMode('slide');$('#side').onclick=()=>setMode('side');$('#mix').oninput=e=>move(e.target.value);
const frame=$('#frame');let pointer=null;function position(e){const r=frame.getBoundingClientRect();move(Math.round(100*(e.clientX-r.left)/r.width))};frame.onpointerdown=e=>{pointer=e.pointerId;frame.setPointerCapture(pointer);position(e)};frame.onpointermove=e=>{if(pointer===e.pointerId)position(e)};frame.onpointerup=frame.onpointercancel=()=>{pointer=null};setView('full');setMode('slide');move(50);
</script></body></html>'''
    for key, value in zip(('__A__','__B__','__C__','__D__'),sources):
        markup=markup.replace(key,value)
    Path(dest).write_text(markup,encoding='utf-8')

def main():
    ap=argparse.ArgumentParser(description='Novydres: máscaras, composição, verificação e comparador')
    sub=ap.add_subparsers(dest='action',required=True)
    for name in ('mask','compose','verify','compare'):
        cmd=sub.add_parser(name)
        cmd.add_argument('--base',required=True)
        if name=='mask':cmd.add_argument('--spec',required=True)
        if name=='compose':cmd.add_argument('--candidate',required=True)
        if name in ('compose','verify'):cmd.add_argument('--mask',required=True)
        if name in ('verify','compare'):cmd.add_argument('--after',required=True)
        if name=='compare':cmd.add_argument('--mask',required=False)
        if name!='verify':cmd.add_argument('--out',required=True)
    args=ap.parse_args()
    base=load_image(args.base)
    if args.action=='mask':
        spec=json.loads(Path(args.spec).read_text()); mask=mask_from_spec(spec,base.size)
        mask.save(args.out);preview(base,mask,Path(args.out).with_name('preview_'+Path(args.out).name))
        print(json.dumps(dict(mask_pixels=sum(bool(x) for x in mask.tobytes()),path=args.out)))
    elif args.action=='compose':
        mask=Image.open(args.mask).convert('L');result=compose(base,load_image(args.candidate),mask,args.out)
        print(json.dumps(verify(base,result,mask)))
    elif args.action=='verify':
        print(json.dumps(verify(base,load_image(args.after),Image.open(args.mask).convert('L'))))
    elif args.action=='compare':
        bbox=None
        if args.mask:
            bbox=Image.open(args.mask).convert('L').getbbox()
            if bbox:
                pad=20;bbox=(max(0,bbox[0]-pad),max(0,bbox[1]-pad),min(base.width,bbox[2]+pad),min(base.height,bbox[3]+pad))
        comparator(base,load_image(args.after),args.out,bbox)
        print(json.dumps(dict(output=args.out,bytes=Path(args.out).stat().st_size)))

if __name__=='__main__':main()

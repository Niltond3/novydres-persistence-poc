#!/usr/bin/env python3
"""T03/U03 — estudo arquitetônico raster conservador sobre U02 imutável.

Gerado por pixel com ROI de trabalho explicitamente NÃO cadastrais e sem mover
nenhuma feição. Executar apenas com U02 aprovada e o inventário V3 originais.
"""
import argparse, json, hashlib, random, io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, cv2

W,H=1448,1086
SOURCE_SHA='9d55965f45181e3b943552e32df0e8ad41b63c8974ffd6e670f447ffd36eb9a0'
# As formas abaixo são ROIs de APARÊNCIA sobre os núcleos urbanizados da U02,
# não alteram nem interpretam os limites canônicos GEO e não são máscaras aprovadas.
CORES={
'New London':('#80929b','#d6cfbf','#b4a78f'),
'Dunwich':('#719eaa','#b2d2c6','#4c8e96'),
'Bukovie':('#8c8a94','#b1a69e','#b8a076'),
'Alexandria':('#9299a0','#d2c4ac','#aca28f'),
'Vasyl Bay':('#8b96a0','#c2bfbe','#b1a89e'),
'Crisol':('#657380','#afb9c3','#5c6975'),
'Levi':('#8799a9','#aebecb','#9ea8b9'),
'Sulfok':('#6c6a69','#9b7a6d','#815e50'),
'Kingswell':('#666c75','#90858a','#695c64'),
'Drevnigrad':('#7f7b82','#9e817f','#745c58'),
}
ROIS={
'New London':[(177,115),(244,113),(313,125),(386,140),(441,170),(415,201),(348,226),(272,218),(203,243),(173,220)],
'Dunwich':[(445,123),(530,120),(604,151),(685,149),(761,149),(831,157),(967,186),(952,221),(852,222),(745,229),(647,210),(549,208),(481,197)],
'Bukovie':[(1024,139),(1100,111),(1214,111),(1335,113),(1424,155),(1447,212),(1380,250),(1279,259),(1160,251),(1077,227),(1000,190)],
'Alexandria':[(228,413),(290,378),(373,390),(458,383),(519,422),(528,500),(475,550),(354,578),(255,541),(219,477)],
'Vasyl Bay':[(560,414),(624,401),(711,403),(775,422),(796,467),(767,530),(705,554),(608,547),(555,505)],
'Crisol':[(826,452),(869,443),(935,454),(951,483),(927,522),(871,534),(820,508)],
'Levi':[(1102,373),(1170,363),(1256,373),(1353,368),(1430,389),(1448,442),(1429,526),(1411,599),(1324,637),(1202,615),(1130,554)],
'Sulfok':[(189,742),(275,681),(378,677),(485,703),(546,732),(557,821),(516,911),(437,960),(296,977),(197,958)],
'Kingswell':[(560,716),(617,690),(739,697),(829,702),(952,731),(999,766),(1007,878),(972,946),(864,983),(720,1008),(585,960)],
'Drevnigrad':[(1086,744),(1177,711),(1329,744),(1410,749),(1448,818),(1434,951),(1369,1009),(1229,1018),(1110,973),(1061,866)],
}
# ROIs deliberadamente afastadas de infraestrutura principal, costas e POIs,
# com refino técnico por análise de textura do raster aprovado.
PALETTE={k:tuple(tuple(int(c[i:i+2],16) for i in (1,3,5)) for c in arr) for k,arr in CORES.items()}

def read_img(path):
 b=Path(path).read_bytes(); sha=hashlib.sha256(b).hexdigest()
 if sha!=SOURCE_SHA: raise ValueError('U02 fonte errada: '+sha)
 im=Image.open(io.BytesIO(b)).convert('RGB')
 if im.size!=(W,H):raise ValueError('Dimensao invalida')
 return im

def build_masks(src,inventory):
 arr=np.asarray(src).astype(np.float32)
 lum=cv2.cvtColor(arr.astype('uint8'),cv2.COLOR_RGB2GRAY).astype(np.float32)
 # Excluir água, gelo, relevo e vias: textura local e cores de telhado.
 sigma=np.sqrt(np.maximum(cv2.blur(lum**2,(7,7))-cv2.blur(lum,(7,7))**2,0))
 saturation=arr.max(2)-arr.min(2)
 # Densidade de detalhe urbano e luminosidade média de material construído.
 urban=(lum>47)&(lum<161)&(sigma>14)&(sigma<59)&(saturation<83)
 # Excluir canal principal, Expresso ferroviário a oeste e o eixo principal.
 protect=np.zeros((H,W),np.uint8)
 protect[:,:181]=1  # corredores ferroviários e estação norte/sul, sem deslocamentos
 # Proteção conservadora das amostras de POI (coordenadas antigas não registram lote exato)
 # Nesta fase não construímos/recaracterizamos individualmente os 34 POIs.
 for poi in inventory.get('pois',[]):
  pt=poi.get('candidate_point_px')
  if not pt or poi.get('number')==33:continue
  cx,cy=map(int,pt);cv2.circle(protect,(cx,cy),15,1,-1)
 # Manual: protegem-se as cabeceiras das ligações das ilhas, da estação e dos terminais
 for a,b,t in [((498,503),(583,503),10),((772,503),(832,503),10),((642,547),(642,675),10),((332,561),(337,688),10),((935,511),(934,640),10)]:
  cv2.line(protect,a,b,1,t)
 masks={}
 for name,poly in ROIS.items():
  m=np.zeros((H,W),np.uint8)
  cv2.fillPoly(m,[np.array(poly,np.int32)],1)
  masks[name]=(m.astype(bool)&urban&(protect==0)).astype(np.uint8)
 return masks,protect,urban

def apply(img, masks):
 base=np.asarray(img).astype(np.float32)
 out=base.copy()
 total=0
 # Color grade por materiais e microrrelevo de cobertura já existente:
 # sem recortar novas vias, sem acrescentar água, sem apagar edifícios.
 for zone,m in masks.items():
  rng=np.random.default_rng(int(hashlib.sha256(zone.encode()).hexdigest()[:8],16))
  col=np.array(PALETTE[zone][0],dtype=np.float32)
  detail=np.array(PALETTE[zone][1],dtype=np.float32)
  # ganho de cor discreto, sem globalizar o bairro nem criar manchas homogêneas
  y,x=np.indices(m.shape)
  noise=cv2.GaussianBlur(rng.normal(0,1,m.shape).astype('float32'),(0,0),sigmaX=2.2)
  noise=noise/(noise.std()+1e-6)
  v=np.clip(0.11+0.037*noise,0.045,0.19)[...,None]
  target=0.80*col+0.20*detail
  mask=m.astype(bool)
  out[mask]=np.clip(base[mask]*(1-v[mask])+target*v[mask],0,255)
  total+=int(mask.sum())
 return Image.fromarray(np.uint8(out.round()),'RGB'),total

def detail_roofs(src, initial, masks):
 # Desenhar microdetalhes apenas SOBRE telhados candidatos e com alfa muito baixo.
 # A intenção não é mapear os POIs, nem desenhar cada edifício do município.
 out=initial.convert('RGBA')
 lay=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(lay,'RGBA')
 counts={}
 for name,m in masks.items():
  rng=random.Random(int(hashlib.sha256(name.encode()).hexdigest()[:8],16))
  ys,xs=np.where(m>0)
  if len(xs)<500: counts[name]=0;continue
  n={"New London":325,"Dunwich":245,"Bukovie":320,"Alexandria":320,"Vasyl Bay":285,"Crisol":55,"Levi":330,"Sulfok":440,"Kingswell":480,"Drevnigrad":380}[name]
  # Amostragem distante e irregular. Cada traço deve ficar dentro de máscara de telhado.
  used=np.zeros((H,W),np.uint8);placed=0
  edge=Image.new('L',(W,H));edge.putdata([0]*(W*H)) if False else None
  for _ in range(n*45):
   if placed>=n:break
   idx=rng.randrange(len(xs));x=int(xs[idx]);y=int(ys[idx]);
   w=rng.randint(2,5);h=rng.randint(2,5)
   if x<181 or x+w>=W or y+h>=H:continue
   region=m[max(0,y-2):y+h+2,max(0,x-2):x+w+2]
   if region.shape!=(h+4,w+4) or region.mean()<0.72:continue
   if used[max(0,y-7):y+8,max(0,x-7):x+8].any():continue
   c0,c1,c2=PALETTE[name]
   # apenas pixels/arestas internas da região editável de cobertura
   if name in ('New London','Alexandria','Levi'):
    d.rectangle([x,y,x+w,y+h],outline=(*c1,64),width=1)
    if rng.random()<0.4:d.line([(x+1,y+1),(x+w-1,y+1)],fill=(*c2,56),width=1)
   elif name=='Vasyl Bay':
    if rng.random()<0.30:d.ellipse([x,y,x+w,y+h],outline=(*c1,87),width=1)
    else:d.rectangle([x,y,x+w,y+h],outline=(*c1,61),width=1)
   elif name=='Dunwich':
    if rng.random()<0.21:d.ellipse([x,y,x+w,y+h],outline=(*c1,86),width=1)
    else:d.line([(x,y+2),(x+w,y+2)],fill=(*c2,52),width=1)
   elif name=='Bukovie':
    d.rectangle([x,y,x+w,y+h],outline=(*c1,62),width=1)
    if rng.random()<0.7:d.point((x+w//2,y+h//2),fill=(*c2,95))
   elif name=='Crisol':
    d.rectangle([x,y,x+w,y+h],outline=(*c0,64),width=1)
   elif name=='Sulfok':
    d.line([(x,y),(x+w,y+2)],fill=(*c2,82),width=1)
    d.line([(x,y+2),(x+w,y+4)],fill=(*c1,52),width=1)
   elif name=='Kingswell':
    d.line([(x,y),(x+w//2,y+2),(x+w,y)],fill=(*c1,72),width=1)
    if rng.random()<0.55:d.line([(x,y+3),(x+w,y+3)],fill=(*c2,47),width=1)
   elif name=='Drevnigrad':
    d.line([(x,y+2),(x+w//2,y),(x+w,y+2)],fill=(*c1,79),width=1)
    d.line([(x,y+3),(x+w,y+4)],fill=(*c2,49),width=1)
   used[max(0,y-6):y+7,max(0,x-6):x+7]=1;placed+=1
  counts[name]=placed
 # Garantir máscara morfológica exata: nenhum traço solto fora de pixels de telhados
 combined=np.maximum.reduce(list(masks.values())).astype(np.uint8)*255
 alpha=np.asarray(lay.getchannel('A'))
 la=np.array(lay);la[:,:,3]=np.minimum(alpha,combined)
 new_layer=Image.fromarray(la,'RGBA')
 composed=Image.alpha_composite(out,new_layer).convert('RGB')
 return composed,counts

def main():
 p=argparse.ArgumentParser();p.add_argument('--base',default='T03_U02_aprovada.png');p.add_argument('--inventory',default='inventario_espacial_novydres_v3_aprovado.json');p.add_argument('--out',default='T03_U03_candidata.png');args=p.parse_args()
 orig=read_img(args.base)
 inv=json.loads(Path(args.inventory).read_text())
 masks,protect,urban=build_masks(orig,inv)
 first,touched=apply(orig,masks)
 result,counts=detail_roofs(orig,first,masks)
 result.save(args.out,optimize=True)
 a=np.asarray(orig);b=np.asarray(result)
 diff=np.any(a!=b,axis=2)
 allowed=np.maximum.reduce(list(masks.values())).astype(bool)
 outside=int(np.logical_and(diff,~allowed).sum())
 if outside:raise AssertionError('Outside work ROI changes: '+str(outside))
 meta={'schema':'NOVYDRES_T03_U03_VISUAL_CANDIDATE_V1','status':'CANDIDATE_AWAITING_OWNER_APPROVAL','source_u02_sha256':SOURCE_SHA,'result_sha256':hashlib.sha256(Path(args.out).read_bytes()).hexdigest(), 'resolution':[W,H], 'source_immutable':True,'changed_pixels':int(diff.sum()),'changed_outside_protective_rois':outside,'architectural_detail_counts':counts,'active_roof_pixel_masks':{k:int(v.sum()) for k,v in masks.items()},'regional_swap':{'former_Vasyl_Bay':'New London','former_New_London':'Vasyl Bay'},'poi34':'New London, physical station unchanged','poi21':'identity preserved; position unapproved','poi35':'retired','boundary_status':'VISUAL_SEARCH_ROIS_NOT_ADMINISTRATIVE_BOUNDARIES','canon_changed':False,'conflicts':['GEO-013.1: Sulfok versus U03 New London POI34','Inventário V3 coordenadas oriundas de raster anterior; contornos não transferidos como SIG','Arquitetura em estudo, ROI e marcação de telhados não são máscaras aprovadas'],'validation':['png_sha256_reference','same_dimensions_and_perspective','bitwise_protected_pixels','no_new_labels','noncanonical_zonal_mapping']}
 Path('T03_U03_verificacao.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False))
 # strict layout full-comparison, each panel exact full size; small header separate from imagery
 pal=Image.new('RGB',(W*2+48,H+92),(14,22,31)); pal.paste(orig,(16,65));pal.paste(result,(W+32,65))
 dt=ImageDraw.Draw(pal);dt.text((16,25),'ANTES — T03/U02 APROVADA',fill=(238,239,236));dt.text((W+32,25),'DEPOIS — T03/U03 CANDIDATA',fill=(238,239,236))
 pal.save('T03_U03_antes_depois.png',optimize=True)
 # graphic of changes only; technical, not approval artifact
 diffimg=np.asarray(orig).copy();diffimg[diff]=(np.array([239,164,104])*.65+diffimg[diff]*.35).astype('uint8')
 Image.fromarray(diffimg).save('T03_U03_areas_alteradas.png')
 print(json.dumps(meta,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
#!/usr/bin/env python3
"""Reconstrói byte a byte o PNG M02 V3 aprovado a partir da M01 V2 e patch Git.

Uso (na raiz do checkout):
  python novydres/cenario/atlas-novydres/cartografia/edicao-raster/reconstruct_m02_v3.py --out M02-V3.png

Dependência: Pillow. O script não sobrescreve arquivos e verifica SHA-256 e máscara.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw

BASE_SHA = 'bb5c4a03bf65240e250e49504e6d281b6dc0b864eab16aa6a44e9b623cd26963'
MASK_PIXEL_SHA = '1f6bfdde213b9dee4aa837e3f8c1dbb85e17a3110ec5efdb19162aac9c7f1a9c'
PATCH_SHA = 'e09e8189350ba63da129e267f88792758a0483220be759f7532a3fbef74a0476'
OUTPUT_SHA = 'c118a0560e4adcaaede454b524d43bc3a4a94474dc01cfd17ceaea2963318e0b'
EXPECTED_SIZE = (1448, 1086)
EXPECTED_MASK_PIXELS = 29469
PATCH_BOX = (700, 975, 1042, 1086)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build(base_path: Path, spec_path: Path, patch_path: Path, out: Path) -> None:
    if out.exists():
        raise FileExistsError(f'Não sobrescrever arquivo existente: {out}')
    if sha256(base_path.read_bytes()) != BASE_SHA:
        raise ValueError('M01 V2 não corresponde ao SHA-256 aprovado')
    if sha256(patch_path.read_bytes()) != PATCH_SHA:
        raise ValueError('Patch Git não corresponde ao SHA-256 aprovado')

    spec = json.loads(spec_path.read_text(encoding='utf-8'))
    if (spec.get('id') != 'M02' or spec.get('mask_sha256') !=
            '45203d53388c961cb1a81e593e29313b031a7b6a6f5110cb1e8a0a82230576d8'):
        raise ValueError('Especificação da máscara M02 V3 inesperada')
    if spec.get('approved') is not True and spec.get('mask_approved') is not True:
        raise ValueError('Máscara M02 V3 não aprovada')

    base = Image.open(base_path).convert('RGB')
    if base.size != EXPECTED_SIZE:
        raise ValueError('Dimensão da base incorreta')
    mask = Image.new('L', EXPECTED_SIZE, 0)
    pen = ImageDraw.Draw(mask)
    for polygon in spec['polygons']:
        pen.polygon([tuple(point) for point in polygon], fill=255)
    for hole in spec.get('protected_holes', []):
        pen.polygon([tuple(point) for point in hole], fill=0)
    if (sha256(mask.tobytes()) != MASK_PIXEL_SHA or
            sum(bool(value) for value in mask.tobytes()) != EXPECTED_MASK_PIXELS):
        raise ValueError('Geometria binária da máscara divergente')

    patch = Image.open(patch_path).convert('RGB')
    x0, y0, x1, y1 = PATCH_BOX
    if patch.size != (x1-x0, y1-y0):
        raise ValueError('Tamanho do patch inesperado')
    region = base.crop(PATCH_BOX)
    region.paste(patch, (0, 0), mask.crop(PATCH_BOX))
    base.paste(region, (x0, y0))

    stream = io.BytesIO()
    base.save(stream, format='PNG')
    final_bytes = stream.getvalue()
    if sha256(final_bytes) != OUTPUT_SHA:
        raise ValueError('PNG reconstruído não coincide com a versão aprovada')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(final_bytes)
    print(f'OK: {out} ({len(final_bytes)} bytes; SHA-256 {OUTPUT_SHA})')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--base', type=Path, help='PNG M01 V2 aprovado (SHA verificado)')
    parser.add_argument('--spec', type=Path, help='M02.json, para teste')
    parser.add_argument('--patch', type=Path, help='patch.webp, para teste')
    args = parser.parse_args()
    folder = Path(__file__).resolve().parent
    spec = args.spec or folder / 'masks' / 'M02.json'
    patch = args.patch or folder / 'assets' / 'm02_v3_approved' / 'patch.webp'
    if args.base:
        build(args.base, spec, patch, args.out)
    else:
        from reconstruct_assets import reconstruct
        with TemporaryDirectory() as td:
            original = reconstruct('m01_v2', Path(td) / 'M01-V2.png')
            build(original, spec, patch, args.out)

if __name__ == '__main__':
    main()

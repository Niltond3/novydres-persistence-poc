#!/usr/bin/env python3
"""Valida e opcionalmente exporta a referência visual canônica de Novydres.
Os pixels exportados são idênticos ao PNG aprovado; os bytes PNG podem diferir.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
DEFAULT_RECORD = ROOT / "visual-canon.json"

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify(record_file: Path, out: Path | None = None) -> dict:
    spec = json.loads(record_file.read_text(encoding="utf-8"))
    image_ref = spec["git_lossless_source"]
    image = ROOT / Path(image_ref["path"]).relative_to(ROOT.parent.parent.parent.parent) if False else ROOT / "assets/visual_canon_gothic_punk_v1.webp"
    raw = image.read_bytes()
    if sha256(raw) != image_ref["sha256"]:
        raise ValueError("WebP Git: SHA-256 divergente")
    rgb = Image.open(image).convert("RGB")
    if list(rgb.size) != spec["original_illustration"]["dimensions"]:
        raise ValueError("Dimensões divergentes")
    pixel_hash = sha256(rgb.tobytes())
    if pixel_hash != spec["original_illustration"]["raw_rgb_pixel_sha256"]:
        raise ValueError("Pixels RGB divergentes")
    if out is not None:
        if out.exists():
            raise FileExistsError("Não sobrescrever artefato existente: " + str(out))
        rgb.save(out)
        verify_out = Image.open(out).convert("RGB")
        if sha256(verify_out.tobytes()) != pixel_hash:
            out.unlink(missing_ok=True)
            raise ValueError("Arquivo PNG exportado não corresponde aos pixels aprovados")
    return {"status": "PASS", "source_webp_sha256": sha256(raw), "size": list(rgb.size), "rgb_pixel_sha256": pixel_hash, "output": str(out) if out else None}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", type=Path, default=DEFAULT_RECORD)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    print(json.dumps(verify(args.record,args.out),ensure_ascii=False,indent=2))

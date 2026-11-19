#!/usr/bin/env python3
"""Restitui, sem perdas, a coleção T02/U01-V2/U02 aprovada de Novydres.

Requisitos: Python 3, binário `zstd` no PATH. Não faz edição de arte.
Uso: python reconstruct_topdown.py --out ./restaurado
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import shutil
import subprocess
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

def check(data: bytes, expected: str, kind: str) -> None:
    got = hashlib.sha256(data).hexdigest()
    if got != expected:
        raise ValueError(f"{kind}: SHA256 divergente: {got} != {expected}")


def restore(manifest_path: Path, output_dir: Path) -> None:
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    if not shutil.which('zstd'):
        raise RuntimeError('Comando zstd não encontrado. Instale zstd.')
    parts = []
    for row in manifest['parts']:
        path = HERE / 'parts' / row['name']
        content = path.read_bytes()
        if len(content) != row['size_bytes']:
            raise ValueError(f"Tamanho incorreto: {path}")
        check(content, row['sha256'], row['name'])
        parts.append(content)
    packed = b''.join(parts)
    assert len(packed) == manifest['archive']['bytes']
    check(packed, manifest['archive']['sha256'], 'arquivo comprimido completo')
    proc = subprocess.run(['zstd', '-q', '--decompress', '--stdout'], input=packed, stdout=subprocess.PIPE, check=True)
    with tarfile.open(fileobj=io.BytesIO(proc.stdout), mode='r:') as tar:
        lookup = {f['archive_path']: f for f in manifest['files']}
        members = [m for m in tar.getmembers() if m.isfile()]
        if set(m.name for m in members) != set(lookup):
            raise ValueError('Conteúdo do TAR diverge do manifesto')
        for member in members:
            expected = lookup[member.name]
            content = tar.extractfile(member).read()
            if len(content) != expected['size_bytes']:
                raise ValueError(f"Tamanho incorreto: {member.name}")
            check(content, expected['sha256'], member.name)
            destination = (output_dir / member.name).resolve()
            if not destination.is_relative_to(output_dir):
                raise ValueError(f"Caminho inválido: {member.name}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                raise FileExistsError(f"Recusado sobrescrever: {destination}")
            destination.write_bytes(content)
    print(f"RESTORED_OK: {len(lookup)} arquivos, todos conferidos por SHA256")

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--manifest', default=HERE/'topdown_assets_manifest.json', type=Path)
    args=parser.parse_args()
    restore(args.manifest,args.out)
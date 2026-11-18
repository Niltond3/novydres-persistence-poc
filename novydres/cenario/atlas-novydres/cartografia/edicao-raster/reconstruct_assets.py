#!/usr/bin/env python3
"""Reconstruct the exact PNG binaries versioned in GitHub as byte-for-byte parts.

Usage: python reconstruct_assets.py --asset master_v1 [--out target.png]
       python reconstruct_assets.py --asset m01_v2 [--out target.png]
Requires only Python stdlib. Never overwrites an existing file.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def reconstruct(asset_id: str, out: Path | None = None) -> Path:
    assets = Path(__file__).resolve().parent / 'assets'
    spec = json.loads((assets / 'parts.json').read_text(encoding='utf-8'))[asset_id]
    output = out or (assets / spec['source'])
    if output.exists():
        raise FileExistsError(f'File already exists; refusing overwrite: {output}')
    output.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    total = 0
    with output.open('wb') as dest:
        for item in spec['parts']:
            source = assets / asset_id / item['filename']
            chunk = source.read_bytes()
            if len(chunk) != item['size_bytes'] or git_blob_sha(chunk) != item['git_sha1']:
                raise RuntimeError(f'Git chunk invalid: {source}')
            dest.write(chunk)
            digest.update(chunk)
            total += len(chunk)
    if total != spec['size_bytes'] or digest.hexdigest() != spec['sha256']:
        output.unlink(missing_ok=True)
        raise RuntimeError('Reconstructed file SHA-256 mismatch; output removed')
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--asset', choices=['master_v1','m01_v2'], required=True)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = reconstruct(args.asset, args.out)
    print(f'OK: {result} ({result.stat().st_size} bytes)')
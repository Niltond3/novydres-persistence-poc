#!/usr/bin/env python3
"""Restaura exatamente o raster candidato T03/U03 dos fragmentos ASCII Git."""
import argparse,base64,hashlib
from pathlib import Path
SHA256='3fae4c251e09651994c4da43e8f61967193b655abf39f983eabccff2c7ad96b1'
N=8

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 root=Path(__file__).resolve().parent
 joined=''.join((root/'parts'/f'part-{i:03}.b64').read_text('ascii') for i in range(N))
 body=base64.b64decode(joined,validate=True)
 actual=hashlib.sha256(body).hexdigest()
 if actual!=SHA256: raise ValueError(f'Divergência SHA256: {actual}')
 if a.out.exists():raise FileExistsError(a.out)
 a.out.parent.mkdir(parents=True,exist_ok=True)
 a.out.write_bytes(body)
 print(f'RESTORED_OK U03: {len(body)} bytes SHA256 {actual}')
if __name__=='__main__':main()
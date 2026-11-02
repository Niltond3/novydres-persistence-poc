# MasterMap original binary bytes — migration archive

The ten `part_NNN.bin` blobs are consecutive, byte-identical chunks of the original Library `MasterMap.png`, not alternate images. Reconstruct only after cloning the repository:

```sh
cat part_*.bin > MasterMap.png
sha256sum MasterMap.png
```

The expected SHA-256 is `b0a78213ce7d57ea9249f9525f1ff07a058b49861dc2b2771fe660970874179a` and exact size is `3793941` bytes. Refer to `MANIFEST.json` for original Library provenance and each chunk's Git SHA. `MasterMap.png` is recorded as a candidate reference, not an authorized frozen source. Do not alter originals or infer editorial promotion.

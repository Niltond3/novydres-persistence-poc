# Binary transfer feasibility / 2026-11-02

Original asset tested: Arranha-céu monumental em gravura marrom-avermelhada.png (reported Library ID libfile_34219b1b60e88191a96cc05f6d216923, original size 2,380,605 bytes).
Files.read in image_file mode returned an image_asset_pointer/rendition, not original PNG bytes or original checksum.
Files.materialize(raw_file) for the resolved file_0000000059388211adc631f7cc89a150 returned: This Project file does not have an authorized raw-byte materialization path.
GitHub create_blob supports base64 but cannot be used here without authenticated source raw bytes. Reencoding/renditions are NOT faithful original copies.
Result: 0 binaries copied. 19 binaries referenced by the historical 2026-09-28 inventory are PENDING_BINARY_TRANSFER. Canon-approved POI images remain on original Library; no replacement files generated.
Potential future bridge: obtain authorized original raw file bytes or a connector action which returns base64 of the original, upload Git blob and verify size/checksum against source. Do not use image previews as originals.

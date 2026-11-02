# Inline context POC V1.1

Derived from the completed **synthetic** load-001 at seq030; it is a test fork, not an actual continuation or migration of CHR-001.

LIVE.json stores scene.context_packet plus character, unresolved threads and buffer. HISTORY_INDEX.json has NO active_scene and is not updated merely because a scene changes. Historical provenance still points to POC test fixtures. SCENE_CONTEXT.md is deliberately NOT present in this run: it is a disposable/export-only projection.

Test fixture steps 031–033 change scene twice. Each transition should write only LIVE.json with one update_file and one fetch_file readback; recovery of archived evidence may require extra reads, which must be reported separately.

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE if (HERE / "D06_SOURCE_RECONCILIATION_V001.json").exists() else HERE.parent
checks = []


def check(ok, label):
    checks.append((label, bool(ok)))
    if not ok:
        raise AssertionError(label)


def git_blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


candidate_dir = WORK / "source-candidates"
if not candidate_dir.exists():
    candidate_dir = WORK
episode_path = candidate_dir / "M3.01_v006.source.txt"
state_path = candidate_dir / "state_v044.source.txt"
rec_path = WORK / "D06_SOURCE_RECONCILIATION_V001.json"
episode = episode_path.read_text(encoding="utf-8")
state = state_path.read_text(encoding="utf-8")
rec = json.loads(rec_path.read_text(encoding="utf-8"))

check(git_blob_sha(episode_path) == "8b72355fb8242b4d35994bc76ced8af1811b85cf", "episode candidate blob SHA")
check(git_blob_sha(state_path) == "6dad4e47da3eeb9f59380e895eeebf15894ab785", "state candidate blob SHA")
check("PARENT_BLOB_SHA: 42fb8a8fe2b4b32f6d560f420c5b18710b0e011f" in episode, "episode parent v005 recorded")
check("antes de 1970" in episode[:1200], "M3.01 candidate retimed before 1970")
check("Bartolomeu permanece mortal em todas as cenas" in episode[:1200], "mortal through all M3.01 scenes")
check("nenhum Abraço é registrado em M3.01" in episode[:1200], "no Embrace inside M3.01")
check("Data civil exata, datas individuais e espaçamento permanecem UNKNOWN." in episode[:1200], "exact diegetic dates remain unknown")
check("CHR001-M301-C05-22-20261109-001" in state, "state checkpoint event matches cycle")
check("M3.01 C01-C05 closed; C06 not started" in state, "state checkpoint recovered from open sources")
check("Bartholomeu Krauser remains mortal; no Abraço has occurred." in state, "state preserves current mortal/no-Embrace checkpoint")
check("state_v043.source.txt | BLOB_SHA: 46612796f44c9b75cbd7ab43854dcec33283804a" in state, "state v043 mismatch source and hash retained")
check("not silently relabeled" in state, "old content is not silently relabeled")
check("NON_OPERATIONAL; NOT PROMOTED" in state, "state candidate is explicitly non-operational")
check(rec["design_branch"]["head_read"] == "3101f183c456a3cf0f188dd2a70ca50e3290092f", "branch source HEAD captured")
check(rec["master"]["head_read"] == "735fe5d52e2761c4d492fe873a4b6bbcce17654a", "master source HEAD captured")
check(rec["master"]["modified_by_this_run"] is False, "master unchanged by reconciliation")
manifest = next(x for x in rec["sources"] if x["path"] == "novydres/MANIFEST_V47.json")
check(manifest["blob_sha"] == "6d00581981b406ec30bd0138928248965b083cc7", "current manifest source captured")
check("points to CYCLE_V0033" in rec["pointer_reconciliation"]["current_authority"], "current cursor points at cycle 33")
check(rec["gate_disposition"]["operational_gate"] == "BLOCKED_CONFLICT because master cycle/source refs were not updated and source candidates are non-operational", "operational gate remains blocked")
check(rec["gate_disposition"]["secret_truth"] == "BLOCKED_EXTERNAL_DEPENDENCY; no effective ACL and no open variant; no secret file/content was accessed", "hidden-truth dependency remains blocked")
check(rec["gate_disposition"]["scene_ready"] == "NOT_VERIFIED", "scene readiness not inferred")
check(rec["gate_disposition"]["narrator_permission"] == "NOT_GRANTED", "Narrator permission not inferred")

result = {
    "validator": "D06_SOURCE_VALIDATE_V001.py",
    "status": "PASS",
    "checks_passed": len(checks),
    "checks_total": len(checks),
    "checks": [{"id": f"SRC-{i:02d}", "label": label, "result": "PASS" if passed else "FAIL"} for i, (label, passed) in enumerate(checks, 1)],
    "validator_blob_sha": git_blob_sha(Path(__file__)),
    "inputs": {
        "episode_path": "novydres/runtime/narrative-architecture/program/deliverables/source-candidates/M3.01_v006.source.txt",
        "episode_blob_sha": git_blob_sha(episode_path),
        "state_path": "novydres/runtime/narrative-architecture/program/deliverables/source-candidates/state_v044.source.txt",
        "state_blob_sha": git_blob_sha(state_path),
        "reconciliation_path": "novydres/runtime/narrative-architecture/program/deliverables/D06_SOURCE_RECONCILIATION_V001.json",
        "reconciliation_blob_sha": git_blob_sha(rec_path),
    },
}
result_path = WORK / "D06_SOURCE_VALIDATE_V001_RESULT.json"
result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"PASS: {len(checks)}/{len(checks)} D06 source assertions")
print(f"result: {result_path}")

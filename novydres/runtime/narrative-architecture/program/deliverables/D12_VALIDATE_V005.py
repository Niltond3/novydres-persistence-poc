import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
checks = []


def git_blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def check(ok, label):
    checks.append((label, bool(ok)))
    if not ok:
        raise AssertionError(label)


def load(name):
    path = BASE / name
    check(path.is_file(), f"file exists: {name}")
    return json.loads(path.read_text(encoding="utf-8"))


episode = (BASE / "source-candidates/M3.01_v006.source.txt").read_text(encoding="utf-8")
state = (BASE / "source-candidates/state_v044.source.txt").read_text(encoding="utf-8")
rec = load("D06_SOURCE_RECONCILIATION_V001.json")
bible = load("D06_CHRONICLE_BIBLE_V005.json")
routes = load("D06_TRANSFORMATION_PATHS_V005.json")
queue = load("D06_PLAYER_APPROVAL_QUEUE_V005.json")
a06 = load("AUDIT_D06_V005.json")
h06 = load("HANDOFF_D06_V005.json")
src_result = load("D06_SOURCE_VALIDATE_V001_RESULT.json")
a12 = load("AUDIT_D12_V005.json")
h12 = load("HANDOFF_D12_V005.json")
release = load("D12_RELEASE_CANDIDATE_V005.json")

check(git_blob_sha(BASE / "source-candidates/M3.01_v006.source.txt") == "8b72355fb8242b4d35994bc76ced8af1811b85cf", "M3.01 v006 blob")
check(git_blob_sha(BASE / "source-candidates/state_v044.source.txt") == "6dad4e47da3eeb9f59380e895eeebf15894ab785", "state v044 blob")
check(src_result["status"] == "PASS" and src_result["checks_passed"] == 22 and src_result["checks_total"] == 22, "direct source validator result")
check(src_result["validator_blob_sha"] == git_blob_sha(BASE / "D06_SOURCE_VALIDATE_V001.py"), "direct source validator hash")
check(src_result["inputs"]["reconciliation_blob_sha"] == git_blob_sha(BASE / "D06_SOURCE_RECONCILIATION_V001.json"), "source validator bound to reconciliation blob")
check("antes de 1970" in episode[:1200], "M3.01 before 1970")
check("Bartolomeu permanece mortal em todas as cenas" in episode[:1200], "mortal throughout M3.01")
check("nenhum Abraço é registrado em M3.01" in episode[:1200], "no Embrace in M3.01")
check("Data civil exata, datas individuais e espaçamento permanecem UNKNOWN." in episode[:1200], "exact dates remain unknown")
check("late 1970s" not in episode and "fim dos anos 1970" not in episode, "prior late-1970s labels removed from candidate")
check("STATE v019 / M2.03" in state and "STATE v041" in state, "old state provenance is explicitly described")
check("not silently relabeled" in state and "NON_OPERATIONAL" in state, "state candidate does not reinterpret or promote v043")
check(rec["design_branch"]["head_read"] == "3101f183c456a3cf0f188dd2a70ca50e3290092f", "documentary input head")
check(rec["master"]["head_read"] == "735fe5d52e2761c4d492fe873a4b6bbcce17654a", "master input head")
check(rec["master"]["modified_by_this_run"] is False, "master remains unmodified")
check("points to CYCLE_V0033" in rec["pointer_reconciliation"]["current_authority"], "MANIFEST_V47 cursor reconciled to CYCLE_V0033")
check("historical metadata" in rec["pointer_reconciliation"]["historical_reference"], "embedded MANIFEST_V46 remains historical")
check(rec["gate_disposition"]["operational_gate"].startswith("BLOCKED_CONFLICT"), "operational conflict stays blocked")
check(rec["gate_disposition"]["secret_truth"].startswith("BLOCKED_EXTERNAL_DEPENDENCY"), "secret dependency stays blocked")
check(rec["gate_disposition"]["scene_ready"] == "NOT_VERIFIED", "SCENE_READY not inferred")
check(rec["gate_disposition"]["narrator_permission"] == "NOT_GRANTED", "Narrator permission not inferred")
decision = next(x for x in queue["decisions"] if x["id"] == "APPROVAL-D06-001")
check(decision["actual_event"] == "NOT_ESTABLISHED", "forced Embrace target is not an occurred event")
check("1970-12-25" in decision["selected_target"], "forced Embrace cutoff retained")
check("AUTHORIAL_TARGET_RECONCILED_IN_NON_OPERATIONAL_CANDIDATES" == decision["status"], "authorial target only applied to candidates")
check(bible["gate"] == "PASS_WITH_UNKNOWN", "D06 documentary gate")
check(bible["operational_target_gate"] == "BLOCKED_CONFLICT", "D06 operational target gate")
check("NOT_REPEATED_FOR_V005" == a06["independent_review"]["status"], "no new independent review claimed")
check(a06["validation"]["checks_passed"] == 22 and a06["validation"]["checks_total"] == 22, "D06 validation count recorded")
check(h06["publication_readback"]["status"] == "PASS_INITIAL_PUBLICATION_READBACK", "D06 initial package readback passed")
check(h06["publication_readback"]["commit_sha"] == "22cb6dd34d5b62709fc70912504dc59dd421931a" and h06["publication_readback"]["published_package_files_read_back"] == 16, "D06 initial readback binds commit A and all 16 files")
check(a12["status"] == "BLOCKED_CONFLICT" and a12["documentary_gate"] == "PASS_WITH_UNKNOWN", "D12 documentary and operational gates separated")
check(a12["gates"]["secret_truth"] == "BLOCKED_EXTERNAL_DEPENDENCY", "D12 secret gate")
check(a12["gates"]["SCENE_READY"] == "NOT_VERIFIED", "D12 scene gate")
check(a12["gates"]["NARRATOR_PERMISSION"] == "NOT_GRANTED", "D12 Narrator gate")
check(a12["gates"]["promotion"] == "NOT_PERFORMED", "D12 promotion not performed")
check(a12["previous_validation"]["validator"] == "D12_VALIDATE_V004.py" and a12["previous_validation"]["checks"] == "62/62", "V004 validator run retained")
check(h12["status"] == "BLOCKED_CONFLICT", "D12 handoff remains blocked operationally")
check(h12["next_phase"] == "Dramaturge planning only", "next step scoped to Dramaturge planning")
check(h12["publication_readback"]["status"] == "PASS_INITIAL_PUBLICATION_READBACK" and h12["publication_readback"]["commit_sha"] == "22cb6dd34d5b62709fc70912504dc59dd421931a" and h12["publication_readback"]["files"] == 16, "D12 initial readback binds commit A and all 16 files")
check(a12["publication_readback"]["status"] == "PASS_INITIAL_PUBLICATION_READBACK" and release["publication_readback"]["status"] == "PASS_INITIAL_PUBLICATION_READBACK", "audit and release record initial readback")
check(release["status"] == "BLOCKED_CONFLICT", "release candidate remains blocked")
check(release["documentary_gate"] == "PASS_WITH_UNKNOWN", "release documentary gate")
check(release["authorizations"]["promotion_performed"] is False and release["authorizations"]["master_write"] is False, "no promotion or master write")
check(release["authorizations"]["scene_execution"] is False and release["authorizations"]["narrator_permission"] is False, "no scene or Narrator authorization")
check(release["d07_activation"] is False, "D07 not activated")

prompt = (BASE / "DRAMATURGO_CONTINUITY_PROMPT_V001.md").read_text(encoding="utf-8")
for token, label in [
    ("8b72355fb8242b4d35994bc76ced8af1811b85cf", "prompt cites episode candidate hash"),
    ("6dad4e47da3eeb9f59380e895eeebf15894ab785", "prompt cites state candidate hash"),
    ("MANIFEST_V47", "prompt identifies current manifest"),
    ("antes de 1970", "prompt enforces M3.01 date boundary"),
    ("consentimento", "prompt preserves forced nature of Embrace"),
    ("Sistema Circulatório", "prompt retains authored network direction"),
    ("aproximadamente sete ou oito Gangrel", "prompt retains player confrontation concept"),
    ("Não escreva prosa de cena", "prompt excludes scene writing"),
    ("não inicie ciclo de Narrador", "prompt excludes Narrator cycle"),
    ("Não acesse", "prompt prohibits secret access"),
    ("SCENE_READY", "prompt distinguishes scene readiness"),
    ("NARRATOR_PERMISSION", "prompt distinguishes Narrator permission"),
]:
    check(token in prompt, label)

expected = {
    "source-candidates/M3.01_v006.source.txt", "source-candidates/state_v044.source.txt",
    "D06_SOURCE_RECONCILIATION_V001.json", "D06_CHRONICLE_BIBLE_V005.json",
    "D06_TRANSFORMATION_PATHS_V005.json", "D06_PLAYER_APPROVAL_QUEUE_V005.json",
    "AUDIT_D06_V005.json", "HANDOFF_D06_V005.json",
    "D06_SOURCE_VALIDATE_V001.py", "D06_SOURCE_VALIDATE_V001_RESULT.json",
    "AUDIT_D12_V005.json", "HANDOFF_D12_V005.json",
    "D12_RELEASE_CANDIDATE_V005.json", "D12_VALIDATE_V005.py",
    "D12_VALIDATE_V005_RESULT.json", "DRAMATURGO_CONTINUITY_PROMPT_V001.md",
}
check(set(release["outputs"]) == expected, "D12 release inventory exactly matches 16 deliverables")

result = {
    "validator": "D12_VALIDATE_V005.py",
    "status": "PASS",
    "checks_passed": len(checks),
    "checks_total": len(checks),
    "checks": [{"id": f"D12-{i:02d}", "label": label, "result": "PASS" if passed else "FAIL"} for i, (label, passed) in enumerate(checks, 1)],
    "validator_blob_sha": git_blob_sha(Path(__file__)),
    "documentary_input_head": rec["design_branch"]["head_read"],
    "master_input_head": rec["master"]["head_read"],
    "candidate_blobs": {
        "episode": git_blob_sha(BASE / "source-candidates/M3.01_v006.source.txt"),
        "state": git_blob_sha(BASE / "source-candidates/state_v044.source.txt"),
    },
}
(BASE / "D12_VALIDATE_V005_RESULT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"PASS: {len(checks)}/{len(checks)} D12 V005 assertions")
print(f"result: {BASE / 'D12_VALIDATE_V005_RESULT.json'}")

"""Reference-bound native-image edit handoff for the one Mapwork pipeline.

No model call is made by Python. The ChatGPT Web host must actually attach
both verified images to its native edit operation and supply a receipt. The
host is responsible for the truth of that tool-call attestation; this module
verifies the material bytes and all internal bindings, not unseen model I/O.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

REQUEST_SCHEMA = "NOVYDRES_MAPWORK_NATIVE_EDIT_REQUEST"
HANDOFF_SCHEMA = "NOVYDRES_MAPWORK_NATIVE_EDIT_HANDOFF"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_digest(value):
    return digest(json.dumps(value, sort_keys=True, ensure_ascii=False,
                             separators=(",", ":")).encode("utf-8"))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def png(path, *, kind):
    f = Path(path)
    require(f.is_file(), kind + " input bytes missing")
    payload = f.read_bytes()
    with Image.open(f) as im:
        require(im.format == "PNG", kind + " must be PNG")
        size = list(im.size)
        im.verify()
    return {"sha256": digest(payload), "size": size}


def edit_request(*, reference_sha256, mask_sha256, goal, scope, job_id):
    """Deterministic instruction, not an image or a provider dispatch."""
    require(scope in ("SYNTHETIC", "CANONICAL") and isinstance(job_id, str)
            and bool(job_id.strip()), "native edit scope/job missing")
    for name, sha in (("reference", reference_sha256), ("mask", mask_sha256)):
        require(isinstance(sha, str) and len(sha) == 64 and
                all(c in "0123456789abcdef" for c in sha), name + " SHA-256 invalid")
    require(isinstance(goal, str) and len(goal.strip()) >= 20,
            "concrete native image edit goal required")
    prompt = ("EDITAR A IMAGEM FORNECIDA COMO REFERÊNCIA VISUAL. "
              "Use a máscara fornecida para delimitar exclusivamente os pixels editáveis. "
              "Preserve a composição e os pixels fora da máscara. "
              "Objetivo visual: " + goal.strip() + ". "
              "SAÍDA: somente a imagem cartográfica editada, sem legendas, relatórios, "
              "tabelas, painéis, banners, infográficos, títulos ou marcas de aprovação. "
              "Não inventar elementos fora do objetivo autorizado.")
    return {"schema": REQUEST_SCHEMA, "scope": scope, "job_id": job_id,
            "mode": "EDIT_WITH_REFERENCE", "reference_sha256": reference_sha256,
            "mask_sha256": mask_sha256, "prompt": prompt,
            "prompt_sha256": digest(prompt.encode("utf-8")),
            "required_input_roles": ["reference-image", "edit-mask"]}


def verify_handoff(handoff, *, request, output_sha256, expected_operation_id=None):
    """Fail closed on missing reference, mask, dispatch binding or independent GET.

    A host tool invocation cannot be cryptographically authenticated by Python;
    the explicit dispatch receipt must come from the connected host, never from
    an unverified model-generated success paragraph.
    """
    require(isinstance(handoff, dict) and handoff.get("schema") == HANDOFF_SCHEMA,
            "native edit handoff missing")
    require(isinstance(request, dict) and request.get("schema") == REQUEST_SCHEMA,
            "native edit request missing")
    require(request.get("mode") == "EDIT_WITH_REFERENCE" and
            request.get("scope") in ("CANONICAL", "SYNTHETIC") and
            request.get("required_input_roles") == ["reference-image", "edit-mask"] and
            isinstance(request.get("prompt"), str) and
            request.get("prompt_sha256") == digest(request["prompt"].encode("utf-8")) and
            "sem legendas, relatórios" in request["prompt"].lower(),
            "native generation request has no reference-edit-only prompt")
    require(handoff.get("request_sha256") == json_digest(request),
            "native edit request fingerprint mismatch")
    if expected_operation_id is not None:
        require(handoff.get("operation_id") == expected_operation_id,
                "native edit operation_id mismatch")
    inputs = handoff.get("inputs")
    require(isinstance(inputs, dict) and set(inputs) == {"reference-image", "edit-mask"},
            "native edit needs both reference-image and edit-mask attachments")
    identities = {}
    for role, sha_key in (("reference-image", "reference_sha256"),
                          ("edit-mask", "mask_sha256")):
        item = inputs[role]
        require(isinstance(item, dict) and item.get("provider") == "drive"
                and isinstance(item.get("remote_id"), str) and item["remote_id"],
                role + " Drive identity missing")
        source, get = Path(item.get("path", "")), Path(item.get("readback_path", ""))
        require(source.is_file() and get.is_file() and source.resolve() != get.resolve(),
                role + " independent Drive GET missing")
        expected = request[sha_key]
        require(digest(source.read_bytes()) == expected and
                get.read_bytes() == source.read_bytes() and item.get("sha256") == expected,
                role + " input differs from verified provider bytes")
        identities[role] = png(source, kind=role)
    require(identities["reference-image"]["size"] == identities["edit-mask"]["size"],
            "native edit mask and reference dimensions differ")
    dispatch = handoff.get("dispatch")
    require(isinstance(dispatch, dict) and
            dispatch.get("provider") == "CHATGPT_NATIVE_IMAGE" and
            dispatch.get("mode") == "EDIT_WITH_REFERENCE" and
            isinstance(dispatch.get("generation_id"), str) and dispatch["generation_id"] and
            dispatch.get("prompt_sha256") == request["prompt_sha256"] and
            dispatch.get("request_sha256") == json_digest(request) and
            dispatch.get("attached_inputs") == {
                role: {"remote_id": inputs[role]["remote_id"],
                       "sha256": request[sha_key]}
                for role, sha_key in (("reference-image", "reference_sha256"),
                                      ("edit-mask", "mask_sha256"))},
            "native generator dispatch has no matching visual input attachments")
    output = handoff.get("output")
    require(isinstance(output, dict) and output.get("provider") == "drive" and
            isinstance(output.get("remote_id"), str) and output["remote_id"] and
            output.get("sha256") == output_sha256 and
            dispatch.get("result_sha256") == output_sha256,
            "native generated image receipt/output mismatch")
    target, recovered = Path(output.get("path", "")), Path(output.get("readback_path", ""))
    require(target.is_file() and recovered.is_file() and
            target.resolve() != recovered.resolve() and
            target.read_bytes() == recovered.read_bytes() and
            digest(target.read_bytes()) == output_sha256,
            "native generated image Drive readback mismatch")
    png(target, kind="generated image")
    require(output_sha256 != request["reference_sha256"] and
            output_sha256 != request["mask_sha256"],
            "native image generation reused input bytes")
    return {"status": "VERIFIED_INPUT_BINDINGS", "request_sha256": json_digest(request),
            "reference_sha256": request["reference_sha256"],
            "mask_sha256": request["mask_sha256"],
            "image_sha256": output_sha256, "generation_id": dispatch["generation_id"]}

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
    # Visual instructions only. Protocol identifiers and SHA values stay in
    # the request envelope and must never be pasted into the image prompt.
    visual_goal = goal.strip().rstrip(".")
    require(not any(word in visual_goal.lower() for word in (
        "sha256", "operation_id", "journal", "dispatch", "receipt", "github",
        "google drive", "status: pass", "edit_op")), "operational metadata in visual goal")
    prompt = ("Edite exatamente a imagem anexada. Altere somente " +
              visual_goal + ". Mantenha todo o resto idêntico. "
              "Não crie nova composição. Não adicione texto, legendas, "
              "painéis, diagramas ou infográficos. Saída: apenas a imagem editada.")
    return {"schema": REQUEST_SCHEMA, "scope": scope, "job_id": job_id,
            "mode": "EDIT_WITH_REFERENCE", "reference_sha256": reference_sha256,
            "mask_sha256": mask_sha256, "prompt": prompt,
            "prompt_sha256": digest(prompt.encode("utf-8")),
            "required_input_roles": ["reference-image", "edit-mask"]}


def verify_handoff(handoff, *, request, output_sha256, expected_operation_id=None):
    """Fail closed on missing reference, mask, dispatch binding or independent GET.

    A host tool invocation cannot be cryptographically authenticated by Python;
    the explicit dispatch and attachment observation must come from the connected host, never from
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
            "não adicione texto" in request["prompt"].lower(),
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
            dispatch.get("request_sha256") == json_digest(request),
            "native generator invocation identity or prompt differs")
    # The Web UI does not expose an API-style inputs[] or edit_op receipt.
    # These are independently recovered bytes plus an explicit HOST account of
    # visual inputs actually displayed in the native invocation. Never infer
    # attachment just from Drive IDs, hashes or a textual prompt.
    evidence = handoff.get("visual_input_evidence")
    require(isinstance(evidence, dict) and
            evidence.get("source") == "CHATGPT_WEB_NATIVE_TOOL" and
            evidence.get("generation_id") == dispatch["generation_id"] and
            isinstance(evidence.get("observation"), str) and
            len(evidence["observation"].strip()) >= 30,
            "real visual attachment observation missing")
    attached = evidence.get("inputs")
    require(isinstance(attached, dict) and set(attached) ==
            {"reference-image", "edit-mask"}, "reference and mask visual attachments missing")
    seen = set()
    for role, sha_key in (("reference-image", "reference_sha256"),
                          ("edit-mask", "mask_sha256")):
        item = attached[role]
        require(isinstance(item, dict) and
                isinstance(item.get("visual_file_id"), str) and
                item["visual_file_id"].startswith("file_") and
                item["visual_file_id"] == inputs[role].get("visual_file_id") and
                item["visual_file_id"] not in seen and
                item.get("sha256") == request[sha_key],
                "native tool lacks observed " + role + " visual attachment")
        seen.add(item["visual_file_id"])
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
    return {"status": "VERIFIED_INPUT_BYTES_AND_HOST_VISUAL_ATTESTATION", "request_sha256": json_digest(request),
            "reference_sha256": request["reference_sha256"],
            "mask_sha256": request["mask_sha256"],
            "image_sha256": output_sha256, "generation_id": dispatch["generation_id"]}


# Strict raster composition is independent of the model's ability to obey
# a mask. Never treat a plausible-looking visual match as pixel preservation.
def _pair(reference_path, mask_path):
    from PIL import Image
    with Image.open(reference_path) as src, Image.open(mask_path) as raw_mask:
        require(src.format == "PNG" and raw_mask.format == "PNG",
                "reference and mask must be material PNG files")
        source = src.convert("RGBA").copy()
        require(raw_mask.size == source.size, "reference/mask pixel geometry mismatch")
        coverage = raw_mask.convert("L").point(lambda v: 255 if v else 0)
    require(coverage.getbbox() is not None, "empty authorized edit mask")
    return source, coverage


def prepare_local_edit(reference_path, mask_path, output_dir, *, context_px=64):
    """Derive a native-edit crop WITH context, preserving original coordinates.

    The crop mask remains binary and tied to the full-frame authorized mask.
    Context is supplied for visual understanding, NEVER for write permission.
    """
    require(type(context_px) is int and 0 <= context_px <= 2048,
            "invalid visual context padding")
    reference, mask = _pair(reference_path, mask_path)
    x0, y0, x1, y1 = mask.getbbox()
    bbox = (max(0, x0-context_px), max(0, y0-context_px),
            min(reference.width, x1+context_px),
            min(reference.height, y1+context_px))
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    reference_crop = directory / "reference-crop.png"
    mask_crop = directory / "mask-crop.png"
    reference.crop(bbox).save(reference_crop)
    mask.crop(bbox).save(mask_crop)
    return {"bbox": list(bbox), "reference_crop_path": str(reference_crop),
            "mask_crop_path": str(mask_crop),
            "reference_crop_sha256": digest(reference_crop.read_bytes()),
            "mask_crop_sha256": digest(mask_crop.read_bytes()),
            "reference_sha256": digest(Path(reference_path).read_bytes()),
            "mask_sha256": digest(Path(mask_path).read_bytes()),
            "full_size": list(reference.size),
            "allowed_pixels": sum(1 for v in mask.getdata() if v),
            "context_not_editable": True}


def _changed_any_channel(diff):
    # Pillow RGBA.getbbox() defaults to alpha_only=True. Pixel RGB edits with
    # unchanged opacity would otherwise be incorrectly reported as identical.
    return any(band.getbbox() is not None for band in diff.split())


def compose_masked(reference_path, mask_path, candidate_path, output_path, *,
                   crop_bbox=None, protected_mask_path=None):
    """Apply only authorized pixels. Resize and fuzzy alignment are forbidden.

    A native result must be exactly aligned to either the original frame or
    the recorded reference crop; if its aspect/resolution changed, fail closed.
    """
    from PIL import Image, ImageChops
    original, allowed = _pair(reference_path, mask_path)
    if protected_mask_path is not None:
        with Image.open(protected_mask_path) as protected:
            require(protected.size == original.size, "protected geometry mismatch")
            locked = protected.convert("L").point(lambda v: 255 if v else 0)
        require(ImageChops.multiply(allowed, locked).getbbox() is None,
                "edit mask intersects previously protected/approved pixels")
    with Image.open(candidate_path) as proposed:
        require(proposed.format == "PNG", "native candidate must be PNG")
        edited = proposed.convert("RGBA").copy()
    if crop_bbox is None:
        require(edited.size == original.size, "unaligned native result: full size differs")
        aligned = edited
    else:
        require(isinstance(crop_bbox, (list, tuple)) and len(crop_bbox) == 4
                and all(type(v) is int for v in crop_bbox),
                "invalid crop coordinate contract")
        x0,y0,x1,y1 = crop_bbox
        require(0 <= x0 < x1 <= original.width and
                0 <= y0 < y1 <= original.height,
                "crop escapes original reference")
        require(edited.size == (x1-x0, y1-y0),
                "unaligned native crop: exact geometry required")
        require(allowed.crop((x0,y0,x1,y1)).getbbox() is not None,
                "crop does not contain editable pixels")
        # All allowed pixels must fall within the selected crop.
        outside = allowed.copy()
        from PIL import ImageDraw
        ImageDraw.Draw(outside).rectangle((x0,y0,x1-1,y1-1),fill=0)
        require(outside.getbbox() is None, "crop excludes authorized pixels")
        aligned = original.copy()
        aligned.paste(edited, (x0,y0))
    composed = Image.composite(aligned, original, allowed)
    outside_differences = ImageChops.difference(composed, original)
    outside_differences.paste((0,0,0,0), mask=allowed)
    require(not _changed_any_channel(outside_differences), "outside-mask regression")
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    composed.save(output, format="PNG")
    # Re-open the persisted PNG, not merely the in-memory compositor result.
    with Image.open(output) as saved:
        check = ImageChops.difference(saved.convert("RGBA"), original)
    check.paste((0,0,0,0), mask=allowed)
    require(not _changed_any_channel(check), "persisted PNG changed protected pixels")
    return {"schema": "NOVYDRES_MAPWORK_MASKED_COMPOSITION",
            "reference_sha256": digest(Path(reference_path).read_bytes()),
            "mask_sha256": digest(Path(mask_path).read_bytes()),
            "native_candidate_sha256": digest(Path(candidate_path).read_bytes()),
            "composed_sha256": digest(output.read_bytes()),
            "composed_path": str(output), "size": list(original.size),
            "outside_mask_changed_pixels": 0,
            "alignment": "EXACT_CROP" if crop_bbox is not None else "EXACT_FRAME",
            "semantic_status": "REQUIRES_AGENT_VISUAL_REVIEW"}


def localized_repair_mask(authorized_mask_path, defects, output_path, *,
                          protected_mask_path=None):
    """Create an exact, minimal approved-mask intersection for concrete defects.

    Defect rectangles must be agent-inspected coordinates in full-frame pixels.
    They are NOT permission to edit protected geometry or unseen neighbors.
    """
    from PIL import Image, ImageDraw, ImageChops
    with Image.open(authorized_mask_path) as im:
        authorized = im.convert("L").point(lambda x: 255 if x else 0)
    require(isinstance(defects, list) and bool(defects), "specific defects required")
    selection = Image.new("L", authorized.size, 0)
    brush = ImageDraw.Draw(selection)
    ids = []
    for defect in defects:
        require(isinstance(defect, dict) and defect.get("severity") in
                ("LOW", "MEDIUM", "HIGH", "CRITICAL") and
                isinstance(defect.get("observation"), str) and
                len(defect["observation"].strip()) >= 12, "uninspected defect")
        box = defect.get("bbox")
        require(isinstance(box, list) and len(box) == 4 and
                all(type(v) is int for v in box), "defect bbox missing")
        x0,y0,x1,y1 = box
        require(0 <= x0 < x1 <= authorized.width and
                0 <= y0 < y1 <= authorized.height, "defect outside image")
        require(isinstance(defect.get("id"), str) and
                defect["id"] not in ids, "defect needs unique id")
        ids.append(defect["id"])
        brush.rectangle((x0,y0,x1-1,y1-1), fill=255)
    if protected_mask_path:
        with Image.open(protected_mask_path) as im:
            require(im.size == authorized.size, "protected mask shape differs")
            locked = im.convert("L").point(lambda x: 255 if x else 0)
        require(ImageChops.multiply(selection, locked).getbbox() is None,
                "defect intersects protected or previously approved region")
    local = ImageChops.multiply(selection, authorized)
    require(local.getbbox() is not None, "defects have no authorized writable pixels")
    # Reject partial overlaps that would silently hide a protected location.
    require(ImageChops.subtract(selection, authorized).getbbox() is None,
            "defect extends beyond authorized edit mask")
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    local.save(path, format="PNG")
    return {"path": str(path), "sha256": digest(path.read_bytes()),
            "bbox": list(local.getbbox()), "defect_ids": ids,
            "requires_agent_review": True}


def verify_composed(reference_path, mask_path, candidate_path, composed_path, *,
                    crop_bbox=None, protected_mask_path=None):
    """Independently recompute masked pixels from material source/candidate.

    No semantic claim is inferred. A matching hash alone cannot establish
    geometry, grade separation, readability or seam continuity.
    """
    from PIL import Image, ImageChops
    from tempfile import TemporaryDirectory
    with TemporaryDirectory(prefix="mapwork-recomposition-") as folder:
        expected = Path(folder) / "expected.png"
        composition = compose_masked(reference_path, mask_path, candidate_path,
                                     expected, crop_bbox=crop_bbox,
                                     protected_mask_path=protected_mask_path)
        with Image.open(expected) as reference_composed, Image.open(composed_path) as actual:
            require(actual.format == "PNG" and
                    actual.size == reference_composed.size,
                    "composed Drive image encoding or dimensions invalid")
            diff = ImageChops.difference(
                reference_composed.convert("RGBA"), actual.convert("RGBA"))
            require(not _changed_any_channel(diff),
                    "composed Drive pixels differ from authorized deterministic result")
    with Image.open(reference_path) as ref, Image.open(composed_path) as after:
        before_pixels=ref.convert("RGBA")
        after_pixels=after.convert("RGBA")
        require(before_pixels.size == after_pixels.size,
                "composed image differs from original size")
        changed=sum(a != b for a,b in zip(before_pixels.getdata(), after_pixels.getdata()))
    require(changed > 0, "native edit candidate changed no authorized pixels")
    composition["composed_sha256"] = digest(Path(composed_path).read_bytes())
    composition["composed_path"] = str(Path(composed_path))
    composition["changed_pixels"] = changed
    return composition

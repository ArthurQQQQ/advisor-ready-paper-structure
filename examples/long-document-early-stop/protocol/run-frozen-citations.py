#!/usr/bin/env python3
"""Run the frozen citation protocol on separately prepared validation streams."""

import argparse
from copy import deepcopy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys


MANIFEST_NAME = "freeze-manifest.json"
REVISION = "fdc9d8214fbab5dd782958601db4d678e6934a54"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_snapshot(directory, manifest):
    files = manifest["files"]
    if not files or Path(__file__).name not in files:
        raise ValueError("The freeze manifest must include the runner.")
    for relative, expected in files.items():
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts or digest(directory / path) != expected:
            raise ValueError(f"Frozen source differs: {relative}")


def load_protocol(snapshot, manifest):
    verify_snapshot(snapshot, manifest)
    sys.path.insert(0, str(snapshot))
    protocol = runpy.run_path(str(snapshot / "run-openrouter-citations-v5c.py"))
    for name in ("revised", "workflow", "v2", "v3", "v4", "inputs",
                 "original_inputs", "conflicts", "conflicts_v3"):
        source = Path(protocol[name].__file__).resolve()
        if source.parent != snapshot or source.name not in manifest["files"]:
            raise ValueError(f"Frozen dependency was loaded from outside the snapshot: {name}")
    for module in list(sys.modules.values()):
        filename = getattr(module, "__file__", None)
        if filename and Path(filename).resolve().parent == snapshot:
            if Path(filename).name not in manifest["files"]:
                raise ValueError(f"Imported source is absent from freeze: {filename}")
    return protocol


def complete_frozen(protocol, token, name, prompt, schema, evidence):
    """Apply the effective final-run aspect schema without changing prompts."""
    adjusted = deepcopy(schema)
    limits = {}
    if "aspects" in adjusted.get("properties", {}):
        adjusted["properties"].pop("gap")
        adjusted["required"] = list(adjusted["properties"])
        for field in ("aspects", "paragraph_ids"):
            adjusted["properties"][field]["maxItems"] = 8
            limits[field] = 8
    value, metadata = protocol["complete"](token, name, prompt, adjusted, evidence)
    if limits:
        metadata["recovery_array_limits"] = limits
        metadata["recovery_optional_gap_removed"] = True
        value["gap"] = "" if value["aspects"] else "No documented aspects were supplied."
    return value, metadata


def validate_inputs(directory, workflow):
    questions = load_json(directory / "questions.json")
    audit = load_json(directory / "stream-audit.json")
    expected_dataset = {
        "name": "allenai/qasper", "config": "qasper", "split": "validation", "revision": REVISION,
    }
    if audit["dataset"] != expected_dataset or audit["step"] != 256:
        raise ValueError("Expected pinned validation data and the shared 256-token grid.")
    if not isinstance(questions, list) or not questions:
        raise ValueError("No development questions supplied.")
    documents = {}
    for document in audit["documents"]:
        row = document["row"]
        if type(row) is not int or row < 0 or row in documents:
            raise ValueError("Malformed or duplicate document row.")
        documents[row] = document
    identifiers = set()
    positions = set()
    paths = {}
    for question in questions:
        row, qid, order = question["row"], question["qid"], question["question_order"]
        if (type(row) is not int or row not in documents or not isinstance(qid, str) or
                not qid or qid in identifiers or type(order) is not int or order < 1 or
                (row, order) in positions or not isinstance(question["question"], str) or
                not question["question"].strip()):
            raise ValueError("Malformed or duplicate development question.")
        if question["paper_id"] != documents[row]["paper_id"]:
            raise ValueError(f"Question and stream refer to different papers at row {row}.")
        identifiers.add(qid)
        positions.add((row, order))
        path = directory / f"{row}.checkpoints.jsonl"
        count = sum(1 for _ in workflow.iter_prefixes(path, question, documents[row], 256))
        if count != documents[row]["checkpoint_count"]:
            raise ValueError(f"Wrong checkpoint count at row {row}.")
        paths[row] = path
    if set(paths) != set(documents):
        raise ValueError("Unused documents in the stream audit.")
    return audit, questions, documents, paths


def run(directory, output, token, snapshot):
    manifest_path = snapshot / MANIFEST_NAME
    manifest = load_json(manifest_path)
    protocol = load_protocol(snapshot, manifest)
    workflow = protocol["workflow"]
    audit, questions, documents, paths = validate_inputs(directory, workflow)
    transport = protocol["V1"]
    actual_settings = {
        "endpoint": transport["ENDPOINT"],
        "model": transport["MODEL"],
        "provider": transport["PROVIDER"],
        "seed": transport["SEED"],
        "temperature": 0,
        "max_output_tokens": protocol["MAX_OUTPUT_TOKENS"],
        "step": 256,
    }
    for field, expected in manifest["settings"].items():
        if field in actual_settings and expected != actual_settings[field]:
            raise ValueError(f"Runtime setting differs from freeze: {field}")
    inputs = [directory / "questions.json", directory / "stream-audit.json", *paths.values()]
    config = {
        "dataset": audit["dataset"],
        "mode": "openrouter",
        "citation_protocol": manifest["protocol"],
        "freeze_manifest_sha256": digest(manifest_path),
        "frozen_settings": manifest["settings"],
        **actual_settings,
        "aspect_schema": {
            "gap_field_removed": True,
            "array_max_items": {"aspects": 8, "paragraph_ids": 8},
        },
        "inputs_sha256": {path.name: digest(path) for path in inputs},
    }
    write_json = transport["write_json"]
    output.mkdir(parents=True, exist_ok=True)
    with (output / ".lock").open("a", encoding="utf-8") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        progress_path, final_path = output / "progress.json", output / "model-run.json"
        if final_path.exists():
            raise ValueError("A completed run already exists in this output directory.")
        if progress_path.exists():
            progress = load_json(progress_path)
            if progress["config"] != config:
                raise ValueError("Frozen protocol or input data changed since the saved run.")
            if set(progress["checks"]) - {question["qid"] for question in questions}:
                raise ValueError("Saved progress contains unrelated questions.")
        else:
            progress = {"config": config, "checks": {}}
            write_json(progress_path, progress)
        final = {**config, "checkpoint_count": 0, "questions": []}
        for question in questions:
            row, qid = question["row"], question["qid"]
            document = documents[row]
            checks = progress["checks"].setdefault(qid, [])
            for index, prefix in enumerate(workflow.iter_prefixes(paths[row], question, document, 256)):
                if index < len(checks):
                    saved = checks[index]
                    if (saved["body_tokens"], saved["eof"]) != (prefix.body_tokens, prefix.eof):
                        raise ValueError(f"Saved progress differs at {qid}, {prefix.body_tokens}.")
                    continue

                def complete(key, name, prompt, schema, evidence):
                    return complete_frozen(protocol, key, name, prompt, schema, evidence)

                try:
                    record = protocol["revised"].evaluate(prefix, token, complete)
                except (RuntimeError, ValueError, KeyError, TypeError) as error:
                    raise RuntimeError(
                        f"Row {row}/{question['question_order']}, {prefix.body_tokens} tokens: {error}"
                    ) from None
                checks.append(record)
                write_json(progress_path, progress)
                print(f"row={row}/{question['question_order']} tokens={prefix.body_tokens} {record['verdict']}",
                      flush=True)
            if len(checks) != document["checkpoint_count"]:
                raise ValueError(f"Wrong saved checkpoint count at {qid}.")
            final["questions"].append({**question, "checks": checks})
            final["checkpoint_count"] += len(checks)
        verify_snapshot(snapshot, manifest)
        if digest(manifest_path) != config["freeze_manifest_sha256"]:
            raise ValueError("Freeze manifest changed while running.")
        if any(digest(path) != config["inputs_sha256"][path.name] for path in inputs):
            raise ValueError("Input data changed while running.")
        write_json(final_path, final)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Prepared development stream directory")
    parser.add_argument("output", type=Path, help="New run output directory")
    args = parser.parse_args()
    token = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not token:
        parser.error("OPENROUTER_API_KEY is missing in the execution environment.")
    try:
        run(args.directory.resolve(), args.output.resolve(), token, Path(__file__).resolve().parent)
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(1, f"Run stopped: {error}\n")


if __name__ == "__main__":
    main()

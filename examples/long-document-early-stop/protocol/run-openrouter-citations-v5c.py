#!/usr/bin/env python3
"""Run the revised citation gate over the pinned QASPER development streams."""

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys

import citation_conflict_v3 as conflicts_v3
import citation_conflict_v4 as conflicts
import citation_openrouter_v2 as v2
import citation_openrouter_v3 as v3
import citation_openrouter_v4 as v4
import citation_openrouter_v5c as revised
import citation_inputs_v5c as inputs
import citation_inputs_v5 as original_inputs
import citation_workflow as workflow


V1_PATH = Path(__file__).with_name("run-openrouter-citations.py")
V1 = runpy.run_path(str(V1_PATH))
CHECKPOINT_COUNT = sum(value[2] for value in V1["QUESTIONS"].values())
MAX_OUTPUT_TOKENS = 1536


def complete(token, name, prompt, schema, evidence):
    """Use the pinned transport with the same output cap in every stage."""
    original_complete = V1["complete"]
    transport_globals = original_complete.__globals__
    original_open = transport_globals["urlopen"]

    def open_with_output_cap(request, *args, **kwargs):
        if request.full_url != V1["ENDPOINT"]:
            raise ValueError("Unexpected model API endpoint.")
        payload = json.loads(request.data)
        if payload["model"] != V1["MODEL"] or payload["max_tokens"] != 700:
            raise ValueError("Unexpected model transport settings.")
        payload["max_tokens"] = MAX_OUTPUT_TOKENS
        request.data = json.dumps(payload).encode("utf-8")
        return original_open(request, *args, **kwargs)

    # The driver executes model requests sequentially in this process.
    transport_globals["urlopen"] = open_with_output_cap
    try:
        value, metadata = original_complete(token, name, prompt, schema, evidence)
    finally:
        transport_globals["urlopen"] = original_open
    metadata["max_output_tokens"] = MAX_OUTPUT_TOKENS
    return value, metadata


def run(directory, output, token):
    audit, questions, documents, paths = V1["validate_input"](directory)
    files = [
        Path(__file__), V1_PATH, Path(revised.__file__), Path(conflicts.__file__),
        Path(v2.__file__), Path(v3.__file__), Path(v4.__file__), Path(inputs.__file__),
        Path(original_inputs.__file__),
        Path(conflicts_v3.__file__), Path(workflow.__file__),
        directory / "questions.json", directory / "stream-audit.json", *paths,
    ]
    step = audit["step"]
    config = {
        "dataset": audit["dataset"],
        "step": step,
        "mode": "openrouter",
        "citation_protocol": "v5c",
        "endpoint": V1["ENDPOINT"],
        "model": V1["MODEL"],
        "provider": V1["PROVIDER"],
        "seed": V1["SEED"],
        "temperature": 0,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "inputs_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files},
    }
    write_json = V1["write_json"]
    output.mkdir(parents=True, exist_ok=True)
    with (output / ".lock").open("a", encoding="utf-8") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        run_file = output / "model-run.json"
        progress_file = output / "progress.json"
        if run_file.exists():
            raise ValueError(f"A completed run already exists in {output}.")
        if progress_file.exists():
            progress = workflow.load_json(progress_file)
            if progress["config"] != config:
                raise ValueError("Inputs or configuration changed since the interrupted run.")
        else:
            progress = {"config": config, "checks": {}}
            write_json(progress_file, progress)

        result = {**config, "checkpoint_count": 0, "questions": []}
        for question, path in zip(questions, paths):
            row = question["row"]
            doc = documents[row]
            checks = progress["checks"].setdefault(question["qid"], [])
            for index, prefix in enumerate(workflow.iter_prefixes(path, question, doc, step)):
                if index < len(checks):
                    saved = checks[index]
                    if (prefix.body_tokens, prefix.eof) != (saved["body_tokens"], saved["eof"]):
                        raise ValueError(f"Saved checkpoint does not match development row {row}.")
                    continue
                try:
                    record = revised.evaluate(prefix, token, complete)
                except (RuntimeError, ValueError, KeyError, TypeError) as exc:
                    raise RuntimeError(f"Row {row}, {prefix.body_tokens} tokens: {exc}") from None
                checks.append(record)
                write_json(progress_file, progress)
                print(f"row={row} tokens={prefix.body_tokens} {record['verdict']}", flush=True)

            if len(checks) != doc["checkpoint_count"]:
                raise ValueError(f"Unexpected number of saved checkpoints for development row {row}.")
            result["questions"].append({**question, "checks": checks})
            result["checkpoint_count"] += len(checks)

        if result["checkpoint_count"] != CHECKPOINT_COUNT:
            raise ValueError(f"Expected all {CHECKPOINT_COUNT} development checkpoints.")
        write_json(run_file, result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Pinned citation-dev-v1 input directory")
    parser.add_argument("output", type=Path, help="Separate directory for the revised model trajectory")
    args = parser.parse_args()
    token = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not token:
        parser.error("OPENROUTER_API_KEY is missing in the execution environment.")
    try:
        run(args.directory, args.output, token)
    except (ValueError, RuntimeError, OSError) as exc:
        print(f"Run stopped: {exc}", file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()

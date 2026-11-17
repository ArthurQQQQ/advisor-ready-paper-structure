#!/usr/bin/env python3
"""Render an offline research workspace from the saved Codex brief."""

import argparse
import json
import os
from pathlib import Path
import re
from tempfile import NamedTemporaryFile
from urllib.parse import urlsplit


TEMPLATE = Path(__file__).resolve().parents[1] / "assets" / "research-workspace.html"
STATE_BLOCK = re.compile(
    r'(<script id="research-state" type="application/json">\n).*?(\n</script>)',
    re.DOTALL,
)


def load_state(path):
    state = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(state, dict):
        raise ValueError("Research state must be a JSON object.")
    if state.get("status") not in ("discussing", "confirmed", "ready"):
        raise ValueError("Use the discussing, confirmed, or ready status.")
    for field in ("id", "idea", "topic", "metric", "controls", "failure", "openQuestion", "outline"):
        value = state.setdefault(field, "")
        if not isinstance(value, str):
            raise ValueError(f"{field} must be a string.")
    if state["status"] != "discussing" and not state["topic"].strip():
        raise ValueError("A confirmed brief must name its topic.")
    if state["status"] == "ready" and not state["outline"].strip():
        raise ValueError("A ready brief must include the Quick Paper Markdown.")

    baselines = state.setdefault("baselines", [])
    if not isinstance(baselines, list):
        raise ValueError("baselines must be an array.")
    for index, baseline in enumerate(baselines, 1):
        if not isinstance(baseline, dict):
            raise ValueError(f"Baseline {index} must be an object.")
        for field in ("name", "role", "match", "notes"):
            if not isinstance(baseline.setdefault(field, ""), str):
                raise ValueError(f"Baseline {index} {field} must be a string.")
        source = baseline.get("source") or ""
        if not isinstance(source, str):
            raise ValueError(f"Baseline {index} source must be a URL or empty.")
        parsed = urlsplit(source)
        if source and (parsed.scheme not in ("http", "https") or not parsed.netloc):
            raise ValueError(f"Baseline {index} source must use HTTP or HTTPS.")
        baseline["source"] = source
    return state


def render(state, output):
    payload = json.dumps(state, ensure_ascii=False, indent=2).replace("<", r"\u003c")
    template = TEMPLATE.read_text(encoding="utf-8")
    html, matches = STATE_BLOCK.subn(lambda match: match[1] + payload + match[2], template)
    if matches != 1:
        raise ValueError("The workspace template must contain exactly one research-state block.")

    temporary = None
    try:
        with NamedTemporaryFile("w", encoding="utf-8", dir=output.parent, delete=False) as file:
            temporary = Path(file.name)
            file.write(html)
        os.replace(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path, help="Research brief JSON")
    parser.add_argument("output", type=Path, help="Rendered standalone HTML")
    args = parser.parse_args()
    try:
        output = args.output.resolve()
        if output in (args.state.resolve(), TEMPLATE):
            raise ValueError("Use a separate output file for the rendered workspace.")
        render(load_state(args.state), output)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    print(output)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Embed an original PDF and its offline viewer in a paper review."""

import argparse
import base64
import hashlib
import io
import os
from pathlib import Path
import tarfile
import tempfile
from urllib.request import urlopen


PDFJS_VERSION = "6.4.299"
PDFJS_ARCHIVE_URL = f"https://registry.npmjs.org/pdfjs-dist/-/pdfjs-dist-{PDFJS_VERSION}.tgz"
PDFJS_INTEGRITY = (
    "AVl138zALtfaAPvADulE0PZThbYzCBS79nL4pOSL/6Sm/"
    "4AH5A21BD9VHt97OlCuzJuCpmeZtAtkinisF4Vb1g=="
)
MARKER = "<!-- EMBEDDED_PDF -->"
ASSETS = Path(__file__).resolve().parents[1] / "assets"


def read_pdfjs(archive_path):
    if archive_path is None:
        with urlopen(PDFJS_ARCHIVE_URL, timeout=30) as response:
            archive_bytes = response.read()
    else:
        archive_bytes = archive_path.read_bytes()

    digest = base64.b64encode(hashlib.sha512(archive_bytes).digest()).decode("ascii")
    if digest != PDFJS_INTEGRITY:
        raise ValueError(f"PDF.js archive does not match the pinned {PDFJS_VERSION} SHA-512")

    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as archive:
        return (
            read_member(archive, "package/build/pdf.min.mjs"),
            read_member(archive, "package/build/pdf.worker.min.mjs"),
            read_member(archive, "package/LICENSE").decode("utf-8"),
        )


def read_member(archive, name):
    member = archive.getmember(name)
    if not member.isfile():
        raise ValueError(f"Expected a regular file in the PDF.js archive: {name}")
    with archive.extractfile(member) as stream:
        return stream.read()


def script_block(script_type, element_id, content):
    if "</script" in content.lower():
        raise ValueError(f"Embedded script content contains a closing script tag: {element_id}")
    return f'<script type="{script_type}" id="{element_id}">\n{content}\n</script>'


def make_bundle(html, pdf_bytes, pdfjs_archive):
    if html.count(MARKER) != 1:
        raise ValueError(f"The input HTML must contain exactly one {MARKER} marker")

    viewer = "\n\n".join(
        (ASSETS / filename).read_text(encoding="utf-8")
        for filename in ("pdf-text-match.js", "pdf-panel.js")
    )
    main, worker, license_text = read_pdfjs(pdfjs_archive)
    scripts = [
        script_block("text/plain", "pdfjs-license", license_text),
        *(
            script_block("application/octet-stream", element_id, base64.b64encode(data).decode("ascii"))
            for element_id, data in (
                ("pdf-original-data", pdf_bytes),
                ("pdfjs-main-data", main),
                ("pdfjs-worker-data", worker),
            )
        ),
        script_block("text/javascript", "pdf-review-viewer", viewer),
    ]
    return html.replace(MARKER, "\n".join(scripts))


def write_private(output, contents):
    # NamedTemporaryFile creates the file with mode 0600 before any bytes are written.
    staged_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n",
            dir=output.parent, prefix=f".{output.name}.", delete=False,
        ) as staged:
            staged_path = Path(staged.name)
            staged.write(contents)
        os.replace(staged_path, output)
    finally:
        if staged_path is not None:
            staged_path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Review HTML with an EMBEDDED_PDF marker")
    parser.add_argument("pdf", type=Path, help="Original manuscript PDF to embed")
    parser.add_argument("output", type=Path, help="Standalone review HTML to write")
    parser.add_argument("--pdfjs-archive", type=Path, help="Pinned PDF.js archive for offline bundling")
    args = parser.parse_args()

    try:
        if args.output.resolve() == args.pdf.resolve() or (
            args.output.exists() and args.output.samefile(args.pdf)
        ):
            raise ValueError("The output path must differ from the original PDF path")
        html = args.html.read_text(encoding="utf-8")
        contents = make_bundle(html, args.pdf.read_bytes(), args.pdfjs_archive)
        write_private(args.output, contents)
    except (KeyError, OSError, ValueError, tarfile.TarError) as error:
        parser.exit(1, f"{parser.prog}: {error}\n")


if __name__ == "__main__":
    main()

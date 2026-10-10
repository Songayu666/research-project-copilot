#!/usr/bin/env python3
"""Validate common research-project-copilot deliverable invariants."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PLACEHOLDERS = ("lorem", "待补充", "placeholder", "todo")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    root = args.output_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        print(f"ERROR: output directory does not exist: {root}")
        return 2

    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        for token in PLACEHOLDERS:
            if token in text:
                warnings.append(f"placeholder-like text '{token}': {path.relative_to(root)}")

    manifest = root / "imagegen-manifest.json"
    slides_dir = root / "slides"
    if slides_dir.is_dir():
        slides = sorted(slides_dir.glob("*.png")) + sorted(slides_dir.glob("*.jpg"))
        if not slides:
            errors.append("slides directory exists but contains no PNG/JPG files")
        if manifest.exists():
            try:
                records = json.loads(manifest.read_text(encoding="utf-8"))
                if len(records) != len(slides):
                    errors.append(f"manifest has {len(records)} records but slides has {len(slides)} images")
                for record in records:
                    for key in ("slide", "prompt_file", "generated_source", "copied_to", "backend"):
                        if not record.get(key):
                            errors.append(f"manifest record missing '{key}': {record}")
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"invalid imagegen-manifest.json: {exc}")
        else:
            warnings.append("slides directory exists without imagegen-manifest.json")

        try:
            from PIL import Image

            for path in slides:
                with Image.open(path) as image:
                    ratio = image.width / image.height
                    if abs(ratio - 16 / 9) > 0.03:
                        errors.append(f"slide is not 16:9: {path.name} ({image.width}x{image.height})")
                    sample = image.convert("RGB").resize((32, 18))
                    corners = [sample.getpixel((0, 0)), sample.getpixel((31, 0)), sample.getpixel((0, 17)), sample.getpixel((31, 17))]
                    if sum(min(pixel) >= 235 for pixel in corners) < 3:
                        warnings.append(f"slide may not use a white background: {path.name}")
        except ImportError:
            warnings.append("Pillow is unavailable; skipped image dimension/background checks")

    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"ERROR: {item}")
    if errors:
        return 1
    print(f"OK: deliverables validated at {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

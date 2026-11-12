#!/usr/bin/env python3
"""Process staged catalog images from upload_content into catalog/catalog."""
from __future__ import annotations

import io
import json
import os
import sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = ROOT / "upload_content"
DEST_ROOT = ROOT / "catalog" / "catalog"
FOLDERS = ("gallery", "tyby", "sosat", "soft", "sosattyby", "kavar", "me5da")
SOURCE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
TARGET_BYTES = 100_000
MAX_BYTES = 150_000
MAX_DIMENSION = 1000


def encode(image: Image.Image, quality: int) -> bytes:
    output = io.BytesIO()
    image.save(output, format="WEBP", quality=quality, method=6)
    return output.getvalue()


def convert(source: Path) -> bytes:
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original)
        has_alpha = "A" in image.getbands() or "transparency" in image.info
        image = image.convert("RGBA" if has_alpha else "RGB")
        if max(image.size) > MAX_DIMENSION:
            scale = MAX_DIMENSION / max(image.size)
            size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
            image = image.resize(size, Image.Resampling.LANCZOS)

        best = None
        for quality in range(82, 19, -4):
            candidate = encode(image, quality)
            if best is None or abs(len(candidate) - TARGET_BYTES) < abs(len(best) - TARGET_BYTES):
                best = candidate
            if len(candidate) <= TARGET_BYTES:
                return candidate
        return best or encode(image, 35)


def valid_webp(content: bytes) -> bool:
    try:
        with Image.open(io.BytesIO(content)) as image:
            image.load()
            return image.format == "WEBP" and image.width > 0 and image.height > 0
    except Exception:
        return False


def optimize_existing_webp() -> None:
    for destination in sorted(DEST_ROOT.rglob("*.webp")):
        if destination.stat().st_size <= TARGET_BYTES:
            continue
        content = convert(destination)
        if not valid_webp(content):
            raise RuntimeError(f"Existing WebP validation failed: {destination}")
        temporary = destination.with_suffix(".webp.tmp")
        temporary.write_bytes(content)
        os.replace(temporary, destination)
        print(f"Re-optimized {destination.relative_to(ROOT)} ({len(content)} bytes)")


def write_manifest() -> None:
    manifest = {}
    for folder in FOLDERS:
        destination_dir = DEST_ROOT / folder
        manifest[folder] = sorted(
            f"catalog/{folder}/{image.name}"
            for image in destination_dir.glob("*.webp")
            if image.is_file()
        )
    manifest_path = ROOT / "catalog" / "images.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote image manifest: {manifest_path.relative_to(ROOT)}")


def main() -> int:
    processed = 0
    for folder in FOLDERS:
        source_dir = SOURCE_ROOT / folder
        destination_dir = DEST_ROOT / folder
        destination_dir.mkdir(parents=True, exist_ok=True)
        if not source_dir.exists():
            continue
        for source in sorted(source_dir.iterdir()):
            if not source.is_file() or source.suffix.lower() not in SOURCE_EXTENSIONS:
                continue
            content = convert(source)
            if not valid_webp(content):
                raise RuntimeError(f"Conversion validation failed: {source}")
            destination = destination_dir / f"{source.stem}.webp"
            # Replace an older version with the same base name only after validation.
            for old in destination_dir.glob(f"{source.stem}.*"):
                if old != destination and old.is_file() and old.suffix.lower() in SOURCE_EXTENSIONS:
                    old.unlink()
            temporary = destination.with_suffix(".webp.tmp")
            temporary.write_bytes(content)
            os.replace(temporary, destination)
            source.unlink()
            print(f"{source.relative_to(ROOT)} -> {destination.relative_to(ROOT)} ({len(content)} bytes)")
            processed += 1
    optimize_existing_webp()
    write_manifest()
    print(f"Processed {processed} image(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

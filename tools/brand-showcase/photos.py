"""Import photographic covers from a JSON object mapping brand slugs to source images."""
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps

from build import OUT, all_brands, export


def main(manifest_path):
    brands = all_brands()
    images = json.loads(Path(manifest_path).read_text(encoding="utf-8-sig"))
    known = {brand.slug for brand in brands}
    if missing := images.keys() - known:
        raise ValueError(f"Unknown brand slugs: {', '.join(sorted(missing))}")
    for slug, src in images.items():
        with Image.open(src) as source:
            photo = ImageOps.exif_transpose(source).convert("RGB")
        for width, filename, quality in (
            (1200, "foto-editorial.webp", 85),
            (640, "foto-editorial-640.webp", 80),
        ):
            image = ImageOps.fit(photo, (width, width * 3 // 4), Image.Resampling.LANCZOS)
            image.save(OUT / slug / filename, "WEBP", quality=quality, method=6)
    export(brands)


if __name__ == "__main__":
    main(sys.argv[1])

"""Publish the renders: .cache/renders/<slug>/<key>.png (2400x1800, supersampled) -> public/marcas/<slug>/foto-<key>.webp
(1600x1200, Lanczos), then refresh src/data/brand-showcase.json so the site uses them."""
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from build import OUT, all_brands, export  # noqa: E402

R = HERE.parent / ".cache" / "renders"
n = 0
for png in sorted(R.glob("*/*.png")):
    dst = OUT / png.parent.name / f"foto-{png.stem}.webp"
    if dst.exists() and dst.stat().st_mtime > png.stat().st_mtime:
        continue
    im = Image.open(png).convert("RGB")
    if im.size != (1600, 1200):
        im = im.resize((1600, 1200), Image.LANCZOS)
    im.save(dst, "WEBP", quality=84, method=6)
    n += 1
print(f"{n} photos written")
export(all_brands())

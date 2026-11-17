"""Contact sheet of renders for review: python sheet.py out.png slug/scene ..."""
import sys
from pathlib import Path
from PIL import Image
R = Path(__file__).resolve().parent.parent / ".cache" / "renders"
out, items = sys.argv[1], sys.argv[2:]
if len(items) == 1 and "/" not in items[0]:
    items = [f"{items[0]}/{p.stem}" for p in sorted((R / items[0]).glob("*.png"))]
cols = 3; w, h = 800, 600
S = Image.new("RGB", (cols * w, -(-len(items) // cols) * h), "white")
for i, it in enumerate(items):
    im = Image.open(R / f"{it}.png").convert("RGB").resize((w, h), Image.LANCZOS)
    S.paste(im, ((i % cols) * w, (i // cols) * h))
S.save(out)

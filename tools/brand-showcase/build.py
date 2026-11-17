"""Generate the brand showcase: logos, kit pieces, mockups and the data file used by the site.

Usage (from this folder):
  python3 fonts.py            # once: fetch the free typefaces into .cache/
  python3 build.py [slug ...] # all brands, or only the given ones
"""
import json
import sys
from pathlib import Path

from lib import cmyk, rgb, svg_doc

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "public" / "marcas"
DATA = ROOT / "src" / "data" / "brand-showcase.json"


def all_brands():
    from brands1 import BRANDS as b1
    out = list(b1)
    try:
        from brands2 import BRANDS as b2
        out += b2
    except ImportError:
        pass
    try:
        from brands3 import BRANDS as b3
        out += b3
    except ImportError:
        pass
    from brands4 import BRANDS as b4
    out += b4
    from notes import NOTES
    for b in out:
        b.notes = {**NOTES.get(b.slug, {}), **(b.notes or {})}
    return out


VERSIONS = [
    ("horizontal", "principal"), ("vertical", "principal"), ("simbolo", "principal"),
    ("inversa", "inversa"), ("negro", "negro"), ("blanco", "blanco"),
]


def write(path, svg):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
    return path.stat().st_size


def build_logos(b):
    d = OUT / b.slug
    sizes = {}
    for name, version in VERSIONS:
        if name == "vertical":
            box = b.vertical(version)
        elif name == "simbolo":
            box = b.mark(version)
        else:
            box = b.horizontal(version)
        svg = svg_doc(box, pad=0.0, title=f"{b.name} · {name}")
        sizes[name] = write(d / f"logo-{name}.svg", svg)
        r = box.ink
        sizes[name + "_ratio"] = round(r.w / r.h, 4)
    return sizes


def color_data(b):
    out = []
    for key, h, es, en, use_es, use_en in b.colors:
        out.append({"key": key, "hex": h.upper(), "rgb": list(rgb(h)), "cmyk": list(cmyk(h)),
                    "name": {"es": es, "en": en}, "use": {"es": use_es, "en": use_en}})
    return out


STYLES = [
    ("minimal", "Minimalista", "Minimal"), ("corporate", "Sobria y profesional", "Professional"),
    ("bold", "Llamativa", "Bold"), ("elegant", "Elegante", "Elegant"), ("organic", "Orgánica y artesanal", "Organic"),
    ("playful", "Divertida", "Playful"), ("retro", "Retro", "Retro"), ("tech", "Tecnológica", "Tech"),
    ("luxe", "Lujo y monogramas", "Luxury and monograms"),
]
LICENSES = {"OFL-1.1": "SIL Open Font License 1.1", "Apache-2.0": "Apache License 2.0"}


def export(brands):
    from fonts import FONTS, license_of
    from lib import contrast, on
    from mockups import CORPORATE, TEMPLATES
    from pieces import light, strong
    data = {"styles": [{"id": i, "label": {"es": es, "en": en}} for i, es, en in STYLES], "brands": []}
    for i, b in enumerate(brands):
        cols = color_data(b)
        for c in cols:
            c["text"] = on(c["hex"], "#FFFFFF", "#111111")
        fonts = []
        for role, f in (("display", b.display), ("body", b.body)):
            fam = FONTS[f[0]][1]
            fonts.append({"role": role, "family": fam, "weight": f[1], "italic": len(f) > 2 and bool(f[2]),
                          "license": LICENSES.get(license_of(f[0]), license_of(f[0])),
                          "url": "https://fonts.google.com/specimen/" + fam.replace(" ", "+"),
                          "file": "tipo-titulos.svg" if role == "display" else "tipo-textos.svg"})
        lv, lbg = light(b)
        sv, sbg = strong(b)
        ratios = {}
        for name, _v in VERSIONS:
            svg = (OUT / b.slug / f"logo-{name}.svg").read_text()
            import re
            m = re.search(r'width="([\d.]+)" height="([\d.]+)"', svg)
            ratios[name] = round(float(m.group(1)) / float(m.group(2)), 4)
        data["brands"].append({
            "n": i + 1, "slug": b.slug, "name": b.name, "style": b.style,
            "sector": b.sector, "concept": b.concept, "tagline": b.tagline, "personality": b.personality,
            "logoKind": b.logo_kind, "colors": cols, "fonts": fonts,
            "surfaces": {"light": lbg, "strong": sbg, "lightText": on(lbg, "#FFFFFF", "#111111"), "strongText": on(sbg, "#FFFFFF", "#111111")},
            "versions": [{"key": name, "bg": b.bg(v), "ratio": ratios[name]} for name, v in VERSIONS],
            "mockups": [{"key": k, "label": TEMPLATES[k][1]} for k in b.mockups],
            "corporate": [{"key": k, "label": TEMPLATES[k][1]} for k in CORPORATE],
        })
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {DATA.relative_to(ROOT)} ({len(brands)} brands)")


def main(only=()):
    brands = all_brands()
    sel = [b for b in brands if not only or b.slug in only]
    for b in sel:
        sizes = build_logos(b)
        print(f"{b.slug:16} logos {sum(v for k, v in sizes.items() if not k.endswith('_ratio')) / 1024:.0f} KB")
        import mockups
        import pieces
        pieces.build(b, OUT / b.slug)
        mockups.build(b, OUT / b.slug)
    export(brands)


if __name__ == "__main__":
    main(sys.argv[1:])

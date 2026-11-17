"""Core helpers: shaped text to SVG outlines, a tiny box layout engine and color utilities."""
import io
from html import escape as esc
import itertools
import math
from functools import lru_cache

import uharfbuzz as hb
from fontTools.misc.transform import Transform
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

from fonts import font_path

_ids = itertools.count(1)


def uid(prefix="m"):
    return f"{prefix}{next(_ids)}"


def n(v):
    """Compact number formatting for SVG output."""
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def n1(v):
    s = f"{v:.1f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ---------------------------------------------------------------- fonts / text
class Font:
    def __init__(self, key, weight, italic=False):
        src = TTFont(font_path(key, weight, italic))
        src.flavor = None
        buf = io.BytesIO()
        src.save(buf)
        data = buf.getvalue()
        self.tt = TTFont(io.BytesIO(data))
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.upm = self.tt["head"].unitsPerEm
        os2 = self.tt["OS/2"]
        self.cap = getattr(os2, "sCapHeight", 0) or self.upm * 0.7
        self.xh = getattr(os2, "sxHeight", 0) or self.upm * 0.5
        self.asc = self.tt["hhea"].ascent
        self.desc = self.tt["hhea"].descent
        self.hb = hb.Font(hb.Face(data))
        self.key, self.weight, self.italic = key, weight, italic


@lru_cache(maxsize=None)
def font(key, weight=400, italic=False):
    return Font(key, weight, italic)


class Rect:
    __slots__ = ("x0", "y0", "x1", "y1", "adv")

    def __init__(self, x0, y0, x1, y1):
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1

    w = property(lambda s: s.x1 - s.x0)
    h = property(lambda s: s.y1 - s.y0)

    def moved(self, dx, dy):
        return Rect(self.x0 + dx, self.y0 + dy, self.x1 + dx, self.y1 + dy)

    def scaled(self, s):
        return Rect(self.x0 * s, self.y0 * s, self.x1 * s, self.y1 * s)

    def union(self, o):
        return Rect(min(self.x0, o.x0), min(self.y0, o.y0), max(self.x1, o.x1), max(self.y1, o.y1))


def _glyph_d(f, gname, t):
    pen = SVGPathPen(f.gs, ntos=n1)
    f.gs[gname].draw(TransformPen(pen, t))
    bp = BoundsPen(f.gs)
    f.gs[gname].draw(TransformPen(bp, t))
    return pen.getCommands(), bp.bounds


def shape(f, text, features=None):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(f.hb, buf, features or {"kern": True, "liga": True})
    return [(f.order[i.codepoint], p.x_advance, p.x_offset, p.y_offset) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]


class Box:
    """Positioned SVG markup with a layout rect (for alignment) and an ink rect (for bounds)."""

    def __init__(self, markup, layout, ink=None):
        self.markup = markup
        self.layout = layout
        self.ink = ink or layout

    w = property(lambda s: s.layout.w)
    h = property(lambda s: s.layout.h)

    def move(self, dx, dy):
        if abs(dx) < 1e-6 and abs(dy) < 1e-6:
            return self
        return Box(f'<g transform="translate({n(dx)} {n(dy)})">{self.markup}</g>', self.layout.moved(dx, dy), self.ink.moved(dx, dy))

    def add(self, markup, rect=None):
        """Same box plus extra markup in its own coordinates (optionally growing the ink)."""
        ink = self.ink.union(rect) if rect else self.ink
        b = Box(self.markup + markup, self.layout, ink)
        b.slots = getattr(self, "slots", {})
        return b

    def at(self, x, y):
        """Place the layout rect's top-left at (x, y)."""
        return self.move(x - self.layout.x0, y - self.layout.y0)

    def scale(self, s):
        return Box(f'<g transform="scale({n(s)})">{self.markup}</g>', self.layout.scaled(s), self.ink.scaled(s))

    def fit(self, x, y, w, h, align="center", valign="middle", by="ink"):
        r = self.ink if by == "ink" else self.layout
        s = min(w / r.w, h / r.h)
        b = self.scale(s)
        r = b.ink if by == "ink" else b.layout
        dx = x - r.x0 + {"start": 0, "center": (w - r.w) / 2, "end": w - r.w}[align]
        dy = y - r.y0 + {"top": 0, "middle": (h - r.h) / 2, "bottom": h - r.h}[valign]
        return b.move(dx, dy)

    def width_to(self, w, by="ink"):
        r = self.ink if by == "ink" else self.layout
        return self.scale(w / r.w)

    def height_to(self, h, by="ink"):
        r = self.ink if by == "ink" else self.layout
        return self.scale(h / r.h)

    def center_at(self, cx, cy, by="ink"):
        r = self.ink if by == "ink" else self.layout
        return self.move(cx - (r.x0 + r.x1) / 2, cy - (r.y0 + r.y1) / 2)

    def wrap(self, before, after):
        return Box(before + self.markup + after, self.layout, self.ink)


def group(*boxes):
    boxes = [b for b in boxes if b is not None]
    lay = boxes[0].layout
    ink = boxes[0].ink
    for b in boxes[1:]:
        lay, ink = lay.union(b.layout), ink.union(b.ink)
    return Box("".join(b.markup for b in boxes), lay, ink)


def hstack(boxes, gap=0, valign="middle"):
    out, x = [], 0
    top = max(b.h for b in boxes)
    for b in boxes:
        y = {"top": 0, "middle": (top - b.h) / 2, "bottom": top - b.h}[valign]
        out.append(b.at(x, y))
        x += b.w + gap
    return group(*out)


def vstack(boxes, gap=0, align="center"):
    out, y = [], 0
    wide = max(b.w for b in boxes)
    for b in boxes:
        x = {"start": 0, "center": (wide - b.w) / 2, "end": wide - b.w}[align]
        out.append(b.at(x, y))
        i = len(out) - 1
        y += b.h + ((gap[i] if i < len(gap) else 0) if isinstance(gap, (list, tuple)) else gap)
    return group(*out)


def text(fkey, weight, s, size, fill="#000", tracking=0.0, italic=False, skew=0.0, box="cap", opacity=None, omit=(), swap=None):
    """Shaped text as one <path>. Origin at the baseline start. Layout rect: cap height to baseline
    (box='cap'), x-height (box='x') or the ink (box='ink')."""
    f = font(fkey, weight, italic)
    sc = size / f.upm
    parts, ink = [], None
    x = 0.0
    glyphs = shape_clusters(f, s)
    slots = {}
    for i, (g, adv, xo, yo, cl) in enumerate(glyphs):
        t = Transform(sc, 0, 0, -sc, x + xo * sc, -yo * sc)
        if skew:
            t = Transform(1, 0, -math.tan(math.radians(skew)), 1, 0, 0).transform(t)
        if swap and cl in swap:
            g = swap[cl]
        d, b = _glyph_d(f, g, t)
        if cl in omit or (swap and cl in swap):
            slots[cl] = Rect(*b) if b else Rect(x, -f.xh * sc, x + adv * sc, 0)
            slots[cl].adv = (x, x + adv * sc)
        if cl not in omit:
            if d:
                parts.append(d)
            if b:
                r = Rect(*b)
                ink = r if ink is None else ink.union(r)
        x += adv * sc + (tracking * size if i < len(glyphs) - 1 else 0)
    if ink is None:
        ink = Rect(0, -f.cap * sc, x, 0)
    op = f' opacity="{n(opacity)}"' if opacity is not None else ""
    markup = f'<path fill="{fill}"{op} d="{"".join(parts)}"/>'
    for r in slots.values():
        ink = ink.union(Rect(r.x0, r.y0, r.x1, r.y1))
    if box == "ink":
        lay = Rect(ink.x0, ink.y0, ink.x1, ink.y1)
    else:
        top = -(f.cap if box == "cap" else f.xh) * sc
        lay = Rect(ink.x0, top, ink.x1, 0)
    out = Box(markup, lay, ink)
    out.slots = slots
    out.metrics = {"cap": f.cap * sc, "xh": f.xh * sc, "adv": x}
    return out


def shape_clusters(f, text, features=None):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(f.hb, buf, features or {"kern": True, "liga": True})
    return [(f.order[i.codepoint], p.x_advance, p.x_offset, p.y_offset, i.cluster) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]


def advance(fkey, weight, s, size, tracking=0.0, italic=False):
    f = font(fkey, weight, italic)
    sc = size / f.upm
    g = shape(f, s)
    return sum(a for _, a, _, _ in g) * sc + tracking * size * (len(g) - 1)


def arc_text(fkey, weight, s, size, cx, cy, r, fill="#000", tracking=0.0, center=0.0, where="top"):
    """Text along a circle. where='top': reads clockwise above the center, baseline radius r, glyph tops outward.
    where='bottom': reads left to right below the center, baseline radius r, glyph tops toward the center."""
    f = font(fkey, weight)
    sc = size / f.upm
    glyphs = shape(f, s)
    advs = [a * sc + tracking * size for _, a, _, _ in glyphs]
    total = sum(advs) - tracking * size
    span = total / r
    parts = []
    pos = 0.0
    for (g, adv, xo, yo), a in zip(glyphs, advs):
        aw = adv * sc
        mid = pos + aw / 2
        th = math.radians(center) - span / 2 + mid / r
        if where == "top":
            px, py, rot = cx + r * math.sin(th), cy - r * math.cos(th), th
        else:
            px, py, rot = cx + r * math.sin(th), cy + r * math.cos(th), -th
        t = Transform().translate(px, py).rotate(rot).translate(-aw / 2, 0).scale(sc, -sc)
        d, _ = _glyph_d(f, g, t)
        if d:
            parts.append(d)
        pos += a
    return f'<path fill="{fill}" d="{"".join(parts)}"/>'


def symbol_box(markup, w, h):
    return Box(markup, Rect(0, 0, w, h))


def svg_doc(box, pad=0.0, bg=None, w=None, h=None, title=None):
    """Standalone SVG trimmed to the ink with uniform padding (fraction of the larger side)."""
    r = box.ink
    p = max(r.w, r.h) * pad
    x0, y0, vw, vh = r.x0 - p, r.y0 - p, r.w + 2 * p, r.h + 2 * p
    bgm = f'<rect x="{n(x0)}" y="{n(y0)}" width="{n(vw)}" height="{n(vh)}" fill="{bg}"/>' if bg else ""
    t = f"<title>{esc(title)}</title>" if title else ""
    ww = w or round(vw, 1)
    hh = h or round(vh, 1)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{n(x0)} {n(y0)} {n(vw)} {n(vh)}" '
            f'width="{n(ww)}" height="{n(hh)}">{t}{bgm}{box.markup}</svg>')


def canvas(w, h, body, title=None, defs=""):
    t = f"<title>{esc(title)}</title>" if title else ""
    d = f"<defs>{defs}</defs>" if defs else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{t}{d}{body}</svg>'


# ---------------------------------------------------------------- color
def rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexc(r, g, b):
    return "#{:02X}{:02X}{:02X}".format(*(max(0, min(255, round(v))) for v in (r, g, b)))


def mix(a, b, t):
    ra, rb = rgb(a), rgb(b)
    return hexc(*(x + (y - x) * t for x, y in zip(ra, rb)))


def cmyk(h):
    r, g, b = (v / 255 for v in rgb(h))
    k = 1 - max(r, g, b)
    if k >= 1:
        return (0, 0, 0, 100)
    c, m, y = ((1 - v - k) / (1 - k) for v in (r, g, b))
    return tuple(round(v * 100) for v in (c, m, y, k))


def lum(h):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def on(bg, light="#FFFFFF", dark="#111111"):
    return light if contrast(bg, light) >= contrast(bg, dark) else dark


def pbounds(*items):
    """Bounds of SVG path data: items are d strings or (d, Transform, stroke_width)."""
    from fontTools.svgLib.path import parse_path
    out = None
    for it in items:
        d, t, sw = (it, Transform(), 0) if isinstance(it, str) else (it + (0,))[:3] if len(it) == 2 else it
        bp = BoundsPen(None)
        parse_path(d, TransformPen(bp, t))
        b = bp.bounds
        r = Rect(b[0] - sw / 2, b[1] - sw / 2, b[2] + sw / 2, b[3] + sw / 2)
        out = r if out is None else out.union(r)
    return out


def rot(deg, cx, cy):
    return Transform().translate(cx, cy).rotate(math.radians(deg)).translate(-cx, -cy)


def foil(svg, gold):
    """Presentation-only gold foil: swap a flat gold for a metallic gradient."""
    if not gold:
        return svg
    import re as _re
    grad = (f'<linearGradient id="foil" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{mix(gold, "#FFFFFF", 0.38)}"/><stop offset=".32" stop-color="{gold}"/>'
            f'<stop offset=".55" stop-color="{mix(gold, "#000000", 0.28)}"/><stop offset=".78" stop-color="{mix(gold, "#FFFFFF", 0.3)}"/>'
            f'<stop offset="1" stop-color="{mix(gold, "#000000", 0.12)}"/></linearGradient>')
    svg = _re.sub(rf'fill="{gold}"', 'fill="url(#foil)"', svg, flags=_re.I)
    return svg.replace(">", ">" + "<defs>" + grad + "</defs>", 1) if "<svg" in svg[:5] else svg

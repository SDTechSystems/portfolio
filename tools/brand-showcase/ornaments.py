"""Fine-line ornaments and letter monograms for the luxury collection."""
import math
import re

from lib import n, text, uid
from model import C, E, P, knock


def glyph(fkey, weight, ch, size, italic=False):
    """Outline of a single letter: (d, ink rect) with the baseline at y=0."""
    t = text(fkey, weight, ch, size, "#000", box="ink", italic=italic)
    return re.search(r' d="([^"]*)"', t.markup).group(1), t.ink


def at(g, cx, cy, sx=1.0):
    """Transform that centers glyph g's ink on (cx, cy)."""
    d, r = g
    return f"translate({n(cx)} {n(cy)}) scale({n(sx)}) translate({n(-(r.x0 + r.x1) / 2)} {n(-(r.y0 + r.y1) / 2)})"


def letter(g, tr, fill):
    return f'<path d="{g[0]}" transform="{tr}" fill="{fill}"/>'


def outline(g, tr, gap):
    return f'<path d="{g[0]}" transform="{tr}" fill="#000" stroke="#000" stroke-width="{n(gap)}" stroke-linejoin="round"/>'


def weave(a, ta, b, tb, gap, fa, fb, split_y):
    """Two interlaced letters: b over a above split_y, a over b below it."""
    top, bot = uid("w"), uid("w")
    up = knock(letter(a, ta, fa), outline(b, tb, gap)) + letter(b, tb, fb)
    down = knock(letter(b, tb, fb), outline(a, ta, gap)) + letter(a, ta, fa)
    return (f'<clipPath id="{top}"><rect x="-500" y="-500" width="1400" height="{n(split_y + 500)}"/></clipPath>'
            f'<clipPath id="{bot}"><rect x="-500" y="{n(split_y)}" width="1400" height="1400"/></clipPath>'
            f'<g clip-path="url(#{top})">{up}</g><g clip-path="url(#{bot})">{down}</g>')


def over(a, ta, b, tb, gap, fa, fb):
    """b laid over a with a clean gap."""
    return knock(letter(a, ta, fa), outline(b, tb, gap)) + letter(b, tb, fb)


def ring(cx, cy, r, w, color):
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="none" stroke="{color}" stroke-width="{n(w)}"/>'


def line(d, color, w, cap="round"):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{n(w)}" stroke-linecap="{cap}" stroke-linejoin="round"/>'


def leaf(cx, cy, length, width, angle, fill):
    """Pointed leaf centred on (cx, cy), long axis rotated by `angle` degrees."""
    h, w = length / 2, width / 2
    d = f"M0 {n(-h)} C{n(w * 1.4)} {n(-h * 0.4)} {n(w * 1.4)} {n(h * 0.4)} 0 {n(h)} C{n(-w * 1.4)} {n(h * 0.4)} {n(-w * 1.4)} {n(-h * 0.4)} 0 {n(-h)} Z"
    return f'<path d="{d}" fill="{fill}" transform="translate({n(cx)} {n(cy)}) rotate({n(angle)})"/>'


def laurel(cx, cy, r, color, start=100, end=228, count=9, size=14, stem=1.6):
    """Wreath branch on the left; mirror for the right with mirror()."""
    out = []
    a0, a1 = math.radians(start), math.radians(end)
    d = f"M{n(cx + r * math.cos(a0))} {n(cy + r * math.sin(a0))} A{n(r)} {n(r)} 0 0 1 {n(cx + r * math.cos(a1))} {n(cy + r * math.sin(a1))}"
    out.append(line(d, color, stem))
    for i in range(count):
        t = (i + 0.6) / count
        a = a0 + (a1 - a0) * t
        k = 1 - 0.35 * t
        tang = math.degrees(a) + 90
        for side in (-1, 1):
            rr = r + side * size * 0.42 * k
            out.append(leaf(cx + rr * math.cos(a), cy + rr * math.sin(a), size * k, size * 0.42 * k, tang + side * 38, color))
    out.append(leaf(cx + r * math.cos(a1 + 0.08), cy + r * math.sin(a1 + 0.08), size * 0.7, size * 0.3, math.degrees(a1) + 90, color))
    return "".join(out)


def mirror(markup, cx):
    return f'<g transform="translate({n(2 * cx)} 0) scale(-1 1)">{markup}</g>'


def sparkle(cx, cy, r, fill, thin=0.18):
    k = r * thin
    return P(f"M{n(cx)} {n(cy - r)} Q{n(cx + k)} {n(cy - k)} {n(cx + r)} {n(cy)} Q{n(cx + k)} {n(cy + k)} {n(cx)} {n(cy + r)} "
             f"Q{n(cx - k)} {n(cy + k)} {n(cx - r)} {n(cy)} Q{n(cx - k)} {n(cy - k)} {n(cx)} {n(cy - r)} Z", fill)


def rays(cx, cy, r0, r1, a0, a1, count, w, color):
    out = []
    for i in range(count):
        a = math.radians(a0 + (a1 - a0) * i / (count - 1))
        x0, y0 = cx + r0 * math.cos(a), cy + r0 * math.sin(a)
        x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
        px, py = -math.sin(a) * w / 2, math.cos(a) * w / 2
        out.append(P(f"M{n(x0)} {n(y0)} L{n(x1 + px)} {n(y1 + py)} L{n(x1 - px)} {n(y1 - py)} Z", color))
    return "".join(out)


def crown(cx, cy, w, color, sw=2.4):
    h = w * 0.5
    x0, x1, y = cx - w / 2, cx + w / 2, cy
    d = (f"M{n(x0)} {n(y)} L{n(x0 + w * 0.06)} {n(y - h)} L{n(cx - w * 0.22)} {n(y - h * 0.45)} L{n(cx)} {n(y - h * 1.15)} "
         f"L{n(cx + w * 0.22)} {n(y - h * 0.45)} L{n(x1 - w * 0.06)} {n(y - h)} L{n(x1)} {n(y)} Z")
    dots = "".join(C(x, yy, sw * 1.3, color) for x, yy in ((x0 + w * 0.06, y - h), (cx, y - h * 1.15), (x1 - w * 0.06, y - h)))
    return line(d, color, sw) + line(f"M{n(x0)} {n(y + sw * 2.4)} H{n(x1)}", color, sw) + dots


def flourish(cx, cy, w, color, sw=1.6):
    """Symmetric scroll under a crest."""
    half = (f"M{n(cx)} {n(cy)} C{n(cx - w * 0.15)} {n(cy + w * 0.12)} {n(cx - w * 0.32)} {n(cy + w * 0.1)} {n(cx - w * 0.38)} {n(cy)} "
            f"C{n(cx - w * 0.43)} {n(cy - w * 0.09)} {n(cx - w * 0.33)} {n(cy - w * 0.14)} {n(cx - w * 0.28)} {n(cy - w * 0.06)} "
            f"M{n(cx - w * 0.38)} {n(cy)} C{n(cx - w * 0.44)} {n(cy + w * 0.06)} {n(cx - w * 0.48)} {n(cy + w * 0.04)} {n(cx - w * 0.5)} {n(cy)}")
    return line(half, color, sw) + mirror(line(half, color, sw), cx) + C(cx, cy, sw * 1.5, color)


def dot_ring(cx, cy, r, count, rad, color):
    return "".join(C(cx + r * math.cos(2 * math.pi * i / count), cy + r * math.sin(2 * math.pi * i / count), rad, color) for i in range(count))


def ticks(cx, cy, r0, r1, count, w, color, major=5):
    out = []
    for i in range(count):
        a = 2 * math.pi * i / count
        rr = r0 - (r1 - r0) * 0.8 if i % major == 0 else r0
        out.append(line(f"M{n(cx + rr * math.cos(a))} {n(cy + rr * math.sin(a))} L{n(cx + r1 * math.cos(a))} {n(cy + r1 * math.sin(a))}", color, w * (1.6 if i % major == 0 else 1), "butt"))
    return "".join(out)

"""Brand model, symbol drawing helpers and logo versions."""
from dataclasses import dataclass, field

from lib import Box, Rect, advance, group, hstack, n, symbol_box, text, uid, vstack

MONO_DARK, MONO_LIGHT = "#111111", "#FFFFFF"


# ---------------------------------------------------------------- drawing helpers
def P(d, fill, extra=""):
    return f'<path d="{d}" fill="{fill}"{extra}/>'


def R(x, y, w, h, fill, rx=0):
    r = f' rx="{n(rx)}"' if rx else ""
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}"{r} fill="{fill}"/>'


def C(cx, cy, r, fill):
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{fill}"/>'


def E(cx, cy, rx, ry, fill, rot=0):
    t = f' transform="rotate({n(rot)} {n(cx)} {n(cy)})"' if rot else ""
    return f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}" fill="{fill}"{t}/>'


def S(d, color, width, cap="round", join="round"):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{n(width)}" stroke-linecap="{cap}" stroke-linejoin="{join}"/>'


def knock(base, cuts, x=-50, y=-50, w=400, h=400):
    """Cut `cuts` (any fill) out of `base` so the background shows through (works in one ink)."""
    i = uid("k")
    return (f'<mask id="{i}" maskUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff"/><g fill="#000">{cuts}</g></mask>'
            f'<g mask="url(#{i})">{base}</g>')


def two_tone(base, detail_cut, detail_fill, mono):
    """Detail drawn in its own color; in one-ink versions it becomes a cut-out."""
    if mono:
        return knock(base, detail_cut)
    return knock(base, detail_cut) + detail_fill


def black(s):
    """Recolor helper: replace fill/stroke values with #000 for use inside masks."""
    import re
    return re.sub(r'(fill|stroke)="#[0-9A-Fa-f]{3,6}"', r'\1="#000"', s)


def justify(fkey, weight, s, size, width, fill, minimum=0.0):
    """Text tracked so its ink spans `width`."""
    plain = text(fkey, weight, s, size, fill)
    gaps = max(len(s) - 1, 1)
    tr = max((width - plain.ink.w) / gaps / size, minimum)
    return text(fkey, weight, s, size, fill, tracking=tr)


def ruled(label, width, color, thick):
    """Descriptor centered between two thin rules spanning `width`."""
    lw = max((width - label.ink.w) / 2 - thick * 6, thick * 4)
    y = label.layout.y0 + label.layout.h / 2 - thick / 2
    left = Box(R(0, y, lw, thick, color), Rect(0, label.layout.y0, lw, 0))
    lab = label.move(lw + thick * 6 - label.ink.x0, 0)
    right = Box(R(lab.ink.x1 + thick * 6, y, lw, thick, color), Rect(lab.ink.x1 + thick * 6, label.layout.y0, lab.ink.x1 + thick * 6 + lw, 0))
    return group(left, lab, right)


# ---------------------------------------------------------------- brand
@dataclass
class Brand:
    slug: str
    name: str
    style: str
    sector: dict
    concept: dict
    tagline: dict
    personality: dict
    colors: list            # [(key, hex, name_es, name_en, use_es, use_en)]
    display: tuple          # (font key, weight[, italic])
    body: tuple             # (font key, weight)
    roles: dict             # principal version roles -> color keys
    inverse: dict           # inverse version roles -> color keys
    base_bg: str            # color key the principal version sits on
    inverse_bg: str         # color key the inverse version sits on
    symbol: object          # fn(c, mono) -> Box
    wordmark: object        # fn(c, mono) -> Box
    mockups: list
    logo_kind: dict
    sym_k: float = 1.0      # symbol height relative to wordmark block (horizontal)
    gap_k: float = 0.32     # gap relative to symbol height
    vsym_k: float = 1.2     # symbol height relative to wordmark block (vertical)
    vgap_k: float = 0.22
    horizontal_fn: object = None
    vertical_fn: object = None
    emblem: object = None   # optional fn(c, mono) -> Box used for stickers / profile
    notes: dict = field(default_factory=dict)

    def hex(self, key):
        for k, h, *_ in self.colors:
            if k == key:
                return h
        raise KeyError(f"{self.slug}: no color {key}")

    def palette(self, version):
        if version == "principal":
            return {r: self.hex(k) for r, k in self.roles.items()}, False
        if version == "inversa":
            return {r: self.hex(k) for r, k in self.inverse.items()}, False
        ink = MONO_DARK if version == "negro" else MONO_LIGHT
        return {r: ink for r in set(self.roles) | set(self.inverse)}, True

    def bg(self, version):
        return {"principal": self.hex(self.base_bg), "inversa": self.hex(self.inverse_bg),
                "negro": "#FFFFFF", "blanco": MONO_DARK}[version]

    # -- lockups
    def sym(self, version="principal"):
        c, mono = self.palette(version)
        return self.symbol(c, mono)

    def word(self, version="principal", align="start"):
        c, mono = self.palette(version)
        return self.wordmark(c, mono, align)

    def horizontal(self, version="principal"):
        c, mono = self.palette(version)
        if self.horizontal_fn:
            return self.horizontal_fn(c, mono)
        wm = self.wordmark(c, mono, "start")
        s = self.symbol(c, mono).height_to(wm.h * self.sym_k, by="layout")
        return hstack([s, wm], gap=s.h * self.gap_k)

    def vertical(self, version="principal"):
        c, mono = self.palette(version)
        if self.vertical_fn:
            return self.vertical_fn(c, mono)
        wm = self.wordmark(c, mono, "center")
        s = self.symbol(c, mono).height_to(wm.h * self.vsym_k, by="layout")
        s = s if s.w <= wm.w * 1.4 else s.width_to(wm.w * 1.4, by="layout")
        return vstack([s, wm], gap=s.h * self.vgap_k)

    def mark(self, version="principal"):
        """Emblem if defined, else the symbol: what goes on profile images and stickers."""
        c, mono = self.palette(version)
        return (self.emblem or self.symbol)(c, mono)

    def font_list(self):
        from fonts import FONTS
        out = []
        for role, f in (("display", self.display), ("body", self.body)):
            out.append({"role": role, "key": f[0], "family": FONTS[f[0]][1], "weight": f[1]})
        return out


def word_block(main, sub=None, gap_k=0.28, align="center"):
    """Wordmark with an optional descriptor underneath."""
    if sub is None:
        return main
    return vstack([main, sub], gap=main.h * gap_k, align=align)


def cap_size(fkey, weight, size):
    from lib import font
    f = font(fkey, weight)
    return f.cap * size / f.upm


def width_of(fkey, weight, s, size, tracking=0):
    return advance(fkey, weight, s, size, tracking)


__all__ = ["P", "R", "C", "E", "S", "knock", "two_tone", "black", "justify", "ruled", "Brand", "word_block",
           "symbol_box", "text", "hstack", "vstack", "group", "Box", "Rect", "cap_size", "width_of", "MONO_DARK",
           "lens", "into", "n"]


def lens(x0, x1, y, h, fill):
    """Tapered horizontal stroke with pointed ends."""
    m = (x0 + x1) / 2
    return P(f"M{n(x0)} {n(y)} Q{n(m)} {n(y - h)} {n(x1)} {n(y)} Q{n(m)} {n(y + h)} {n(x0)} {n(y)} Z", fill)


def into(sym, slot, k=1.0, dy=0.0, valign="bottom"):
    """Fit a symbol into a letter slot (scaled by k, bottom/middle aligned)."""
    w, h = slot.w * k, slot.h * k
    x = (slot.x0 + slot.x1) / 2 - w / 2
    y = slot.y1 - h if valign == "bottom" else (slot.y0 + slot.y1) / 2 - h / 2
    return sym.fit(x, y + dy, w, h, valign="bottom" if valign == "bottom" else "middle")

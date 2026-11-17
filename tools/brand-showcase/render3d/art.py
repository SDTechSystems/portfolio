"""Flat print artwork used as textures by the 3D studio (cards, letterhead, labels, cans, tags...).

Everything is set in each brand's own typefaces (text converted to outlines), so the renders keep
the real typography. Output: tools/brand-showcase/.cache/art/<slug>/*.svg (not published).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from build import all_brands  # noqa: E402
from lib import canvas, contrast, mix  # noqa: E402
from mockups import B, bars, bold, dist, headline, logo_on, pal, pattern_tile, rr, stack_lines  # noqa: E402
from pieces import best_ink  # noqa: E402

OUT = HERE.parent / ".cache" / "art"


def gold_of(b):
    return next((h for k, h, *_ in b.colors if k == "gold"), None)


def card_front(b, p):
    W, H = 1750, 1000
    paper = mix(p.lbg, "#FFFFFF", .35)
    ink = best_ink(b, paper)
    sec = p.sec if contrast(p.sec, paper) > 2.4 else ink
    o = rr(0, 0, W, H, 0, paper)
    o += logo_on(b, paper, "h").fit(130, 120, 820, 230, align="start", valign="top").markup
    o += B(b, "Nombre Apellido", 66, ink, bold(b)).at(130, 600).markup
    o += B(b, "Cargo o área", 44, sec).at(130, 690).markup
    for i, w in enumerate((420, 340, 460)):
        o += f'<circle cx="1050" cy="{600 + i * 82}" r="15" fill="{sec}"/>' + rr(1090, 590 + i * 82, w, 22, 11, ink, ' opacity=".42"')
    o += rr(0, H - 30, W, 30, 0, gold_of(b) or p.sbg)
    return canvas(W, H, o)


def card_back(b, p, with_mark=True):
    W, H = 1750, 1000
    o = rr(0, 0, W, H, 0, p.sbg)
    if with_mark:
        o += b.mark(p.sv).fit(W / 2 - 300, H / 2 - 300, 600, 600).markup
    return canvas(W, H, o)


def letterhead(b, p):
    W, H = 1240, 1754
    ink = "#2b2d31"
    o = rr(0, 0, W, H, 0, "#FDFCFA")
    o += logo_on(b, "#FDFCFA", "h").fit(110, 120, 560, 150, align="start", valign="top").markup
    o += bars(W - 420, 150, [300, 220], ink, 18, 40, .25)
    o += bars(110, 420, [380, 300], ink, 18, 46, .32)
    o += bars(110, 600, [1010, 1000, 960, 1020, 900, 0, 1010, 980, 760, 0, 1000, 930, 640], ink, 15, 46, .16)
    o += B(b, "Nombre Apellido", 34, ink, bold(b)).at(110, 1330).markup + rr(110, 1385, 260, 14, 7, ink, ' opacity=".25"')
    o += rr(0, H - 120, W, 120, 0, p.sbg) + rr(110, H - 72, 520, 16, 8, best_ink(b, p.sbg), ' opacity=".55"')
    o += logo_on(b, p.sbg, "s").fit(W - 200, H - 104, 88, 88).markup
    return canvas(W, H, o)


def envelope(b, p):
    W, H = 2200, 1100
    paper = mix(p.lbg, "#FFFFFF", .45)
    ink = "#2b2d31"
    o = rr(0, 0, W, H, 0, paper)
    o += logo_on(b, paper, "h").fit(110, 100, 560, 150, align="start", valign="top").markup
    o += bars(1050, 600, [700, 600, 460], ink, 26, 62, .3)
    o += rr(W - 330, 90, 200, 240, 10, p.sec, ' opacity=".85"')
    return canvas(W, H, o)


def label(b, p, w=1400, h=1000, frame=True):
    paper = mix(p.lbg, "#FFFFFF", .25)
    o = rr(0, 0, w, h, 0, paper)
    if frame:
        ink = best_ink(b, paper)
        o += f'<rect x="{w * .26}" y="40" width="{w * .48}" height="{h - 80}" fill="none" stroke="{ink}" stroke-width="5" opacity=".75"/>'
        o += f'<rect x="{w * .26 + 16}" y="56" width="{w * .48 - 32}" height="{h - 112}" fill="none" stroke="{ink}" stroke-width="2" opacity=".6"/>'
    o += logo_on(b, paper, "v").fit(w * .31, h * .14, w * .38, h * .58).markup
    sub = B(b, b.sector["es"].upper(), 26, best_ink(b, paper), bold(b), tracking=.16)
    if sub.ink.w > w * .4:
        sub = sub.scale(w * .4 / sub.ink.w)
    o += sub.at((w - sub.w) / 2, h * .8).markup
    return canvas(w, h, o)


def can_wrap(b, p):
    W, H = 2400, 1000
    o = rr(0, 0, W, H, 0, p.sbg)
    o += pattern_tile(b, "blanco" if p.sbg < "#888888" else "negro", 0, 0, W, H, 150, 46, .1)
    o += b.vertical(p.sv).fit(W / 2 - 300, 140, 600, 520).markup
    band = p.sec
    o += rr(0, 760, W, 120, 0, band)
    lab = (b.notes.get("can") or ["330 ml"])[0]
    t = B(b, f"{lab}   ·   330 ml", 52, best_ink(b, band), bold(b), tracking=.2)
    o += t.at((W - t.w) / 2, 790).markup
    return canvas(W, H, o)


def tag_front(b, p):
    W, H = 600, 1000
    o = rr(0, 0, W, H, 0, p.sbg) + b.vertical(p.sv).fit(90, 300, W - 180, 520).markup
    return canvas(W, H, o)


def tag_back(b, p):
    W, H = 600, 1000
    ink = best_ink(b, p.lbg)
    o = rr(0, 0, W, H, 0, p.lbg)
    lines = headline(b, b.tagline["es"], 72, W - 140, ink, 3)
    m, y = stack_lines(lines, 70, 220)
    o += m + bars(70, y + 40, [380, 320, 360], ink, 14, 34, .25)
    o += "".join(rr(70 + i * 15, H - 220, [5, 3, 7, 3, 5, 9, 3, 5][i % 8], 130, 0, ink) for i in range(30))
    return canvas(W, H, o)


def paycard(b, p):
    W, H = 1712, 1080
    o = rr(0, 0, W, H, 0, p.sbg)
    o += f'<g opacity=".14">{b.sym(p.sv).fit(W * .5, -H * .1, W * .75, H * 1.2).markup}</g>'
    o += b.horizontal(p.sv).fit(110, 100, 620, 160, align="start").markup
    ink = best_ink(b, p.sbg)
    nb = B(b, "••••  ••••  ••••  4821", 84, ink, bold(b), tracking=.06)
    o += nb.at(110, 760).markup + rr(110, 920, 460, 30, 15, ink, ' opacity=".4"')
    return canvas(W, H, o)


def menu(b, p):
    W, H = 1000, 1500
    from pieces import disp
    paper = mix(p.lbg, "#FFFFFF", .3)
    ink = best_ink(b, paper)
    acc = p.sec if contrast(p.sec, paper) > 2.2 else p.sbg
    o = rr(0, 0, W, H, 0, paper) + logo_on(b, paper, "v").fit(W * .25, 80, W * .5, 300).markup
    y = 480
    for sec in b.notes.get("menu", ["Especiales", "Para compartir", "Bebidas"]):
        t = disp(b, sec, 62, acc)
        if t.ink.w > W - 240:
            t = t.scale((W - 240) / t.ink.w)
        o += t.at(120, y).markup
        y += t.h + 40
        for i in range(3):
            o += rr(120, y, [380, 320, 420][i], 20, 10, ink, ' opacity=".55"') + rr(120, y + 34, [500, 440, 480][i], 14, 7, ink, ' opacity=".2"')
            o += rr(W - 230, y, 110, 20, 10, ink, ' opacity=".5"')
            y += 92
        y += 40
    o += rr(0, H - 28, W, 28, 0, p.sbg)
    return canvas(W, H, o)


BOTTLE = {  # kind, label lines
    "orvieto": ("wine", "ROSSO DELLA CASA", "Selezione Orvieto"),
    "casa-duvall": ("wine", "RESERVA · TINTO", "Cosecha seleccionada"),
    "paramo": ("beer", "IPA DE ALTURA", "Cerveza artesanal · 330 ml"),
    "guayaba-club": ("juice", "GUAYABA + MANDARINA", "Jugo natural · 350 ml"),
}


def bottle_label(b, p, foil_only=False):
    """Wrap-around label (front panel centred). Gold brands get the symbol as a separate foil layer."""
    kind, l1, l2 = BOTTLE[b.slug]
    W, H = 1400, 1100
    gold = gold_of(b)
    if kind == "wine":
        paper = mix(p.lbg, "#E9DFCC", .5)
    elif kind == "beer":
        paper = p.sbg
    else:
        paper = "#FFFFFF"
    ink = best_ink(b, paper)
    if foil_only:
        return canvas(W, H, b.sym("negro").fit(W / 2 - 190, 110, 380, 400).markup.replace("#111111", "#FFFFFF"))
    o = rr(0, 0, W, H, 0, paper)
    if kind == "wine":
        o += f'<rect x="330" y="40" width="740" height="{H - 80}" fill="none" stroke="{gold or ink}" stroke-width="4"/>'
        o += f'<rect x="346" y="56" width="708" height="{H - 112}" fill="none" stroke="{gold or ink}" stroke-width="1.5"/>'
        if not gold:
            o += logo_on(b, paper, "s").fit(W / 2 - 190, 110, 380, 400).markup
        word = b.word("negro", "center")
        word.markup = word.markup.replace("#111111", ink)
        o += word.fit(390, 600, 620, 170).markup
        t1 = B(b, l1, 34, ink, bold(b), tracking=.18)
        o += t1.at((W - t1.w) / 2, 840).markup
        t2 = B(b, l2, 28, ink)
        o += t2.at((W - t2.w) / 2, 905).markup
    else:
        o += logo_on(b, paper, "v").fit(W / 2 - 300, 120, 600, 560).markup
        band = p.sec if dist(p.sec, paper) > 60 else ink
        o += rr(0, 760, W, 110, 0, band)
        t1 = B(b, l1, 46, best_ink(b, band), bold(b), tracking=.16)
        if t1.ink.w > W * .7:
            t1 = t1.scale(W * .7 / t1.ink.w)
        o += t1.at((W - t1.w) / 2, 788).markup
        t2 = B(b, l2, 30, ink)
        o += t2.at((W - t2.w) / 2, 930).markup
    return canvas(W, H, o)


ARTS = {"card-front": card_front, "card-back": card_back, "letterhead": letterhead, "envelope": envelope,
        "label": label, "can": can_wrap, "tag-front": tag_front, "tag-back": tag_back, "paycard": paycard, "menu": menu}


def build(b):
    p = pal(b)
    d = OUT / b.slug
    d.mkdir(parents=True, exist_ok=True)
    for name, fn in ARTS.items():
        (d / f"{name}.svg").write_text(fn(b, p), encoding="utf-8")
    (d / "card-back-plain.svg").write_text(card_back(b, p, False), encoding="utf-8")
    if b.slug in BOTTLE:
        (d / "bottle-label.svg").write_text(bottle_label(b, p), encoding="utf-8")
        (d / "bottle-foil.svg").write_text(bottle_label(b, p, True), encoding="utf-8")


if __name__ == "__main__":
    only = set(sys.argv[1:])
    for b in all_brands():
        if not only or b.slug in only:
            build(b)
    print("art written to", OUT)

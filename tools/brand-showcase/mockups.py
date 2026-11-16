"""Product and corporate-identity mockups (1200×900 SVG scenes) built from each brand's real logo files."""
import math
from colorsys import rgb_to_hls
from types import SimpleNamespace

from fonts import FONTS
from lib import Box, Rect, canvas, contrast, lum, mix, n, rgb, text, uid
from pieces import best_ink, body, disp, light, strong, wrap_lines

W, H = 1200, 900
DEFS = (
    '<filter id="b24" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="24"/></filter>'
    '<filter id="b12" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>'
    '<filter id="b5" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>'
    '<linearGradient id="cyl" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".34"/>'
    '<stop offset=".1" stop-color="#000" stop-opacity=".1"/><stop offset=".28" stop-color="#fff" stop-opacity=".26"/>'
    '<stop offset=".4" stop-color="#fff" stop-opacity="0"/><stop offset=".78" stop-color="#000" stop-opacity=".08"/>'
    '<stop offset="1" stop-color="#000" stop-opacity=".36"/></linearGradient>'
    '<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".2"/>'
    '<stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".14"/></linearGradient>'
    '<linearGradient id="vsh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".12"/>'
    '<stop offset="1" stop-color="#000" stop-opacity=".16"/></linearGradient>'
    '<linearGradient id="metal" x1="0" x2="1"><stop offset="0" stop-color="#8d9196"/><stop offset=".3" stop-color="#e9ebee"/>'
    '<stop offset=".55" stop-color="#b9bdc2"/><stop offset="1" stop-color="#7c8086"/></linearGradient>'
    '<linearGradient id="glassd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2b3644"/><stop offset=".5" stop-color="#18202a"/>'
    '<stop offset="1" stop-color="#0d1218"/></linearGradient>'
    '<radialGradient id="spot" cx=".5" cy=".3" r=".8"><stop offset="0" stop-color="#fff" stop-opacity=".55"/>'
    '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
    '<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/>'
    '<stop offset="1" stop-color="#000" stop-opacity=".09"/></linearGradient>'
)


# ---------------------------------------------------------------- helpers
def dist(a, b):
    return math.dist(rgb(a), rgb(b))


def sat(h):
    r, g, b = (v / 255 for v in rgb(h))
    return rgb_to_hls(r, g, b)[2]


def shade(h, t=0.18):
    return mix(h, "#000000", t)


def tint(h, t=0.2):
    return mix(h, "#FFFFFF", t)


def pal(b):
    lv, lbg = light(b)
    sv, sbg = strong(b)
    cols = [h for _k, h, *_ in b.colors]
    others = [h for h in cols if dist(h, sbg) > 70 and dist(h, lbg) > 70]
    sec = max(others, key=lambda h: sat(h) + 0.2 * (1 - abs(lum(h) - 0.35))) if others else tint(sbg, 0.3)
    dark = min(cols, key=lum)
    return SimpleNamespace(lv=lv, lbg=lbg, sv=sv, sbg=sbg, sec=sec, dark=dark, ink=best_ink(b, lbg),
                           neutral=mix(lbg, "#D9D5CF", 0.42))


def bold(b):
    ws = [w for w in FONTS[b.body[0]][2] if w <= 700]
    return max(ws)


def B(b, s, size, fill, weight=None, **kw):
    return text(b.body[0], weight or b.body[1], s, size, fill, **kw)


def lockup(b, kind, version):
    return {"h": b.horizontal, "v": b.vertical, "m": b.mark, "s": b.sym}[kind](version)


def logo_on(b, surface, kind="v"):
    """Logo version that reads on `surface`: the brand version made for it, or a one-ink print."""
    pb, ib = b.bg("principal"), b.bg("inversa")
    dp, di = dist(surface, pb), dist(surface, ib)
    if min(dp, di) < 46:
        return lockup(b, kind, "principal" if dp <= di else "inversa")
    cands = [h for _k, h, *_ in b.colors] + ["#FFFFFF", "#141414"]
    ink = max(cands, key=lambda h: contrast(h, surface) + (0.6 if sat(h) > 0.35 and contrast(h, surface) > 3 else 0))
    box = lockup(b, kind, "negro")
    box.markup = box.markup.replace("#111111", ink)
    return box


def place(box, x, y, w, h, **kw):
    return box.fit(x, y, w, h, **kw).markup


def bd(color, floor=True):
    f = '<rect y="560" width="1200" height="340" fill="url(#floor)"/>' if floor else ""
    return f'<rect width="{W}" height="{H}" fill="{color}"/><rect width="{W}" height="{H}" fill="url(#spot)"/>{f}'


def soft(cx, cy, rx, ry, op=0.3):
    return f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}" fill="#000" opacity="{n(op)}" filter="url(#b24)"/>'


def contact(cx, cy, rx, ry, op=0.32):
    return f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}" fill="#000" opacity="{n(op)}" filter="url(#b5)"/>'


def drop(x, y, w, h, rx=0, op=0.26, dx=10, dy=22, blur="b12"):
    return f'<rect x="{n(x + dx)}" y="{n(y + dy)}" width="{n(w)}" height="{n(h)}" rx="{n(rx)}" fill="#000" opacity="{n(op)}" filter="url(#{blur})"/>'


def rr(x, y, w, h, rx, fill, extra=""):
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{n(rx)}" fill="{fill}"{extra}/>'


def bars(x, y, widths, color, h=9, gap=20, op=0.22):
    return "".join(rr(x, y + i * gap, w, h, h / 2, color, f' opacity="{op}"') for i, w in enumerate(widths))


def clip(x, y, w, h, rx, inner):
    i = uid("c")
    return f'<clipPath id="{i}"><rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{n(rx)}"/></clipPath><g clip-path="url(#{i})">{inner}</g>'


def clip_path(d, inner):
    i = uid("c")
    return f'<clipPath id="{i}"><path d="{d}"/></clipPath><g clip-path="url(#{i})">{inner}</g>'


def rot(markup, deg, cx, cy):
    return f'<g transform="rotate({n(deg)} {n(cx)} {n(cy)})">{markup}</g>'


def tx(markup, x, y):
    return f'<g transform="translate({n(x)} {n(y)})">{markup}</g>'


def headline(b, s, size, width, fill, max_lines=3):
    lines = wrap_lines(b, s, size, width, fill)
    while (len(lines) > max_lines or max(l.ink.w for l in lines) > width) and size > 10:
        size *= 0.9
        lines = wrap_lines(b, s, size, width, fill)
    return lines


def stack_lines(lines, x, y, gap=0.18, align="start", width=0):
    out = []
    for ln in lines:
        h = ln.layout.h
        xx = x if align == "start" else x + (width - ln.ink.w) / 2 - (ln.ink.x0 - ln.layout.x0)
        out.append(ln.at(xx, y).markup)
        y += h * (1 + gap)
    return "".join(out), y


def pattern_tile(b, version, x, y, w, h, step, size, op):
    sym = b.sym(version)
    i = uid("p")
    s = size / max(sym.ink.w, sym.ink.h)
    g = f'<defs><g id="{i}">{sym.markup}</g></defs>'
    uses = []
    row, yy = 0, y - step / 2
    while yy < y + h + step:
        xx = x - step / 2 + (step / 2 if row % 2 else 0)
        while xx < x + w + step:
            uses.append(f'<use href="#{i}" transform="translate({n(xx - sym.ink.x0 * s)} {n(yy - sym.ink.y0 * s)}) scale({n(s)})"/>')
            xx += step
        yy += step * 0.86
        row += 1
    return clip(x, y, w, h, 0, g + f'<g opacity="{n(op)}">{"".join(uses)}</g>')


# ---------------------------------------------------------------- phone frame
def phone(x, y, w, h, content, shadow=True):
    r = w * 0.15
    sx, sy, sw, sh = x + 11, y + 11, w - 22, h - 22
    out = drop(x, y, w, h, r, 0.32, 16, 30, "b24") if shadow else ""
    out += rr(x, y, w, h, r, "#15171a") + rr(x + 2, y + 2, w - 4, h - 4, r - 2, "none", ' stroke="#3a3d42" stroke-width="2"')
    out += rr(x - 3, y + h * 0.2, 4, 56, 2, "#2a2c30") + rr(x + w - 1, y + h * 0.26, 4, 90, 2, "#2a2c30")
    out += clip(sx, sy, sw, sh, r - 10, content(sx, sy, sw, sh))
    out += rr(x + w / 2 - 44, sy + 10, 88, 24, 12, "#0b0c0e")
    return out


def status_bar(b, sx, sy, sw, ink):
    return (B(b, "9:41", 14, ink, bold(b)).at(sx + 26, sy + 14).markup
            + rr(sx + sw - 66, sy + 18, 22, 11, 3, ink) + rr(sx + sw - 94, sy + 18, 18, 11, 2, ink, ' opacity=".7"'))


# ---------------------------------------------------------------- templates
def m_cards(b):
    p = pal(b)
    cw, ch = 520, 300
    back = (drop(0, 0, cw, ch, 14) + rr(0, 0, cw, ch, 14, p.sbg)
            + place(b.mark(p.sv), cw / 2 - 95, ch / 2 - 95, 190, 190) + rr(0, 0, cw, ch, 14, "url(#sheen)"))
    ink, sec = best_ink(b, p.lbg), p.sec if contrast(p.sec, p.lbg) > 2 else p.ink
    front = drop(0, 0, cw, ch, 14) + rr(0, 0, cw, ch, 14, p.lbg)
    front += place(logo_on(b, p.lbg, "h"), 40, 40, 250, 68, align="start", valign="top")
    front += B(b, "Nombre Apellido", 27, ink, bold(b)).at(40, 186).markup
    front += B(b, "Cargo o área", 17, sec).at(40, 224).markup
    for i in range(3):
        front += f'<circle cx="342" cy="{170 + i * 34}" r="8" fill="{sec}"/>' + rr(360, 165 + i * 34, [118, 96, 130][i], 10, 5, ink, ' opacity=".28"')
    front += rr(0, ch - 12, cw, 12, 0, p.sbg) + rr(0, 0, cw, ch, 14, "url(#sheen)")
    front = clip(0, 0, cw, ch, 14, front[len(drop(0, 0, cw, ch, 14)):])
    body_ = bd(p.neutral)
    body_ += tx(rot(back, -9, cw / 2, ch / 2), 140, 150)
    body_ += tx(rot(drop(0, 0, cw, ch, 14) + front, 6, cw / 2, ch / 2), 520, 410)
    return body_


def social_tiles(b, p, x0, y0, sw):
    t = (sw - 4) / 3
    out = []
    for i in range(9):
        x, y = x0 + (i % 3) * (t + 2), y0 + (i // 3) * (t + 2)
        kind = i % 9
        if kind in (0, 8):
            c = p.sbg
            out.append(rr(x, y, t, t, 0, c) + place(b.mark(p.sv) if kind == 0 else logo_on(b, c, "h"), x + t * 0.2, y + t * 0.2, t * 0.6, t * 0.6))
        elif kind in (1, 6):
            c = p.lbg if kind == 1 else p.sec
            ink = best_ink(b, c)
            lines = headline(b, b.tagline["es"], 26, t - 26, ink, 3)
            m, _ = stack_lines(lines, x + 13, y + 16)
            out.append(rr(x, y, t, t, 0, c) + m)
        elif kind == 2:
            out.append(rr(x, y, t, t, 0, p.sec) + place(logo_on(b, p.sec, "s"), x + t * 0.25, y + t * 0.25, t * 0.5, t * 0.5))
        elif kind == 3:
            out.append(rr(x, y, t, t, 0, p.lbg) + place(logo_on(b, p.lbg, "h"), x + t * 0.12, y + t * 0.3, t * 0.76, t * 0.4))
        elif kind == 4:
            cols = [h for _k, h, *_ in b.colors]
            cw = t / len(cols)
            out.append("".join(rr(x + j * cw, y, cw + 0.5, t, 0, h) for j, h in enumerate(cols)))
        elif kind == 5:
            out.append(rr(x, y, t, t, 0, p.dark) + pattern_tile(b, "blanco", x, y, t, t, t / 2.2, t / 5, 0.35))
        else:
            out.append(rr(x, y, t, t, 0, tint(p.sec, 0.55)) + place(logo_on(b, tint(p.sec, 0.55), "m"), x + t * 0.28, y + t * 0.28, t * 0.44, t * 0.44))
    return "".join(out)


def social_screen(b, p):
    def content(sx, sy, sw, sh):
        ink = "#16181b"
        out = rr(sx, sy, sw, sh, 0, "#FFFFFF") + status_bar(b, sx, sy, sw, ink)
        out += B(b, b.name, 17, ink, bold(b)).at(sx + 22, sy + 56).markup
        ar = 42
        ax, ay = sx + 22 + ar, sy + 92 + ar
        out += f'<circle cx="{n(ax)}" cy="{n(ay)}" r="{ar + 5}" fill="{p.sec}"/><circle cx="{n(ax)}" cy="{n(ay)}" r="{ar + 2}" fill="#fff"/><circle cx="{n(ax)}" cy="{n(ay)}" r="{ar}" fill="{p.sbg}"/>'
        out += place(b.mark(p.sv), ax - ar * 0.62, ay - ar * 0.62, ar * 1.24, ar * 1.24)
        for i, (num, lab) in enumerate((("128", "publicaciones"), ("4.6 mil", "seguidores"), ("312", "seguidos"))):
            cx = sx + 150 + i * ((sw - 160) / 3) + (sw - 160) / 6
            nb = B(b, num, 17, ink, bold(b))
            lb = B(b, lab, 11, "#6b6f76")
            out += nb.at(cx - nb.w / 2, ay - 22).markup + lb.at(cx - lb.w / 2, ay + 4).markup
        out += B(b, b.sector["es"], 12.5, "#6b6f76").at(sx + 22, sy + 202).markup
        tg = B(b, b.tagline["es"], 13.5, ink)
        out += tg.at(sx + 22, sy + 224).markup
        out += rr(sx + 22, sy + 252, (sw - 52) / 2, 32, 9, p.sbg)
        fl = B(b, "Seguir", 13.5, best_ink(b, p.sbg), bold(b))
        out += fl.at(sx + 22 + ((sw - 52) / 2 - fl.w) / 2, sy + 262).markup
        out += rr(sx + 30 + (sw - 52) / 2, sy + 252, (sw - 52) / 2, 32, 9, "#eef0f2")
        ms = B(b, "Mensaje", 13.5, ink, bold(b))
        out += ms.at(sx + 30 + (sw - 52) / 2 + ((sw - 52) / 2 - ms.w) / 2, sy + 262).markup
        out += social_tiles(b, p, sx, sy + 300, sw)
        return out
    return content


def m_phone(b):
    p = pal(b)
    out = bd(tint(p.sec, 0.72) if lum(p.sec) < 0.5 else p.neutral)
    out += phone(330, 50, 380, 800, social_screen(b, p))
    st = (f'<circle cx="0" cy="0" r="150" fill="#fff"/><circle cx="0" cy="0" r="136" fill="{p.sbg}"/>'
          + place(b.vertical(p.sv), -86, -86, 172, 172))
    out += soft(915, 690, 150, 40, 0.25) + tx(rot(st, 8, 0, 0), 900, 600)
    return out


def m_app(b):
    p = pal(b)

    def content(sx, sy, sw, sh):
        bg, ink = p.lbg, best_ink(b, p.lbg)
        out = rr(sx, sy, sw, sh, 0, bg) + status_bar(b, sx, sy, sw, ink)
        out += place(logo_on(b, bg, "h"), sx + 22, sy + 50, 150, 34, align="start")
        out += f'<circle cx="{n(sx + sw - 40)}" cy="{n(sy + 67)}" r="18" fill="{ink}" opacity=".08"/>'
        lines = headline(b, b.tagline["es"], 30, sw - 50, ink, 2)
        m, y = stack_lines(lines, sx + 22, sy + 110)
        out += m
        cy = y + 14
        card = rr(sx + 16, cy, sw - 32, 150, 20, p.sbg)
        card += clip(sx + 16, cy, sw - 32, 150, 20, f'<g opacity=".18">{place(b.sym("blanco" if lum(p.sbg) < 0.4 else "negro"), sx + sw - 150, cy - 10, 170, 170)}</g>')
        li = best_ink(b, p.sbg)
        card += B(b, "Resumen", 13, li, bold(b)).at(sx + 36, cy + 26).markup
        card += rr(sx + 36, cy + 58, 150, 16, 8, li, ' opacity=".9"') + rr(sx + 36, cy + 84, 100, 10, 5, li, ' opacity=".45"')
        card += rr(sx + 36, cy + 108, 96, 26, 13, p.sec if dist(p.sec, p.sbg) > 60 else li)
        out += card
        qy = cy + 176
        for i in range(4):
            qx = sx + 22 + i * ((sw - 44) / 4) + (sw - 44) / 8
            out += f'<circle cx="{n(qx)}" cy="{n(qy + 26)}" r="25" fill="{p.sec}" opacity="{".9" if i == 0 else ".16"}"/>'
            out += rr(qx - 22, qy + 60, 44, 8, 4, ink, ' opacity=".25"')
        ly = qy + 94
        for i in range(3):
            out += rr(sx + 16, ly + i * 68, sw - 32, 58, 14, "#FFFFFF", ' opacity=".75"')
            out += rr(sx + 28, ly + i * 68 + 11, 36, 36, 10, [p.sbg, p.sec, p.dark][i], ' opacity=".9"')
            out += rr(sx + 76, ly + i * 68 + 15, [140, 110, 160][i], 10, 5, ink, ' opacity=".55"') + rr(sx + 76, ly + i * 68 + 34, 90, 8, 4, ink, ' opacity=".22"')
        out += rr(sx, sy + sh - 70, sw, 70, 0, "#FFFFFF", ' opacity=".9"')
        for i in range(4):
            out += f'<circle cx="{n(sx + sw / 8 + i * sw / 4)}" cy="{n(sy + sh - 40)}" r="9" fill="{p.sbg if i == 0 else ink}" opacity="{1 if i == 0 else .2}"/>'
        return out
    out = bd(p.neutral) + phone(250, 50, 380, 800, content)
    ic = 250
    out += drop(780, 300, ic, ic, ic * 0.22, 0.3, 10, 26, "b24") + rr(780, 300, ic, ic, ic * 0.22, p.sbg)
    out += place(b.mark(p.sv), 780 + ic * 0.2, 300 + ic * 0.2, ic * 0.6, ic * 0.6) + rr(780, 300, ic, ic, ic * 0.22, "url(#sheen)")
    nm = B(b, b.name.split(" ")[0], 26, best_ink(b, p.neutral), bold(b))
    out += nm.at(780 + (ic - nm.w) / 2, 300 + ic + 30).markup
    return out


def m_laptop(b):
    p = pal(b)

    def site(sx, sy, sw, sh, mobile=False):
        bg, ink = p.lbg, best_ink(b, p.lbg)
        out = rr(sx, sy, sw, sh, 0, bg)
        k = 0.62 if mobile else 1
        out += place(logo_on(b, bg, "h"), sx + 24 * k, sy + 16 * k, 140 * k, 28 * k, align="start")
        if not mobile:
            for i in range(4):
                out += rr(sx + sw - 330 + i * 64, sy + 27, 44, 8, 4, ink, ' opacity=".35"')
            out += rr(sx + sw - 92, sy + 18, 72, 26, 13, p.sbg)
        hy = sy + 70 * k
        kick = B(b, b.sector["es"].upper(), 11 * (0.9 if mobile else 1), p.sec if contrast(p.sec, bg) > 2.2 else ink, bold(b), tracking=0.12)
        if kick.ink.w > (sw * 0.5 if not mobile else sw - 40):
            kick = kick.scale((sw * 0.5 if not mobile else sw - 40) / kick.ink.w)
        out += kick.at(sx + 24 * k, hy).markup
        lines = headline(b, b.tagline["es"], 44 if not mobile else 26, (sw * 0.48) if not mobile else sw - 40, ink, 3)
        m, y = stack_lines(lines, sx + 24 * k, hy + 26 * k)
        out += m
        out += bars(sx + 24 * k, y + 6, [300 * k, 260 * k, 190 * k], ink, 8 * k + 1, 16 * k + 2, 0.22)
        by = y + 60 * k
        btn = B(b, "Conocer más", 13 * (0.85 if mobile else 1), best_ink(b, p.sbg), bold(b))
        out += rr(sx + 24 * k, by, btn.w + 36 * k, 34 * k, 17 * k, p.sbg) + btn.at(sx + 24 * k + 18 * k, by + (34 * k - btn.h) / 2).markup
        if not mobile:
            px, py, pw, ph = sx + sw * 0.56, sy + 66, sw * 0.4, sh * 0.56
            out += rr(px, py, pw, ph, 18, p.sbg) + clip(px, py, pw, ph, 18, pattern_tile(b, p.sv, px, py, pw, ph, 70, 26, 0.12))
            out += place(b.mark(p.sv), px + pw * 0.28, py + ph * 0.2, pw * 0.44, ph * 0.6)
            for i in range(3):
                cx = sx + 24 + i * (sw - 48) / 3
                out += rr(cx, sy + sh - 76, (sw - 48) / 3 - 14, 60, 12, shade(bg, 0.05))
                out += f'<circle cx="{n(cx + 24)}" cy="{n(sy + sh - 46)}" r="12" fill="{[p.sbg, p.sec, p.dark][i]}"/>'
                out += rr(cx + 46, sy + sh - 52, 120, 8, 4, ink, ' opacity=".3"')
        else:
            iy = by + 50 * k
            out += rr(sx + 14, iy, sw - 28, 120, 12, p.sbg) + place(b.mark(p.sv), sx + sw / 2 - 40, iy + 20, 80, 80)
        return out
    out = bd(p.neutral)
    out += soft(600, 650, 470, 40, 0.3)
    out += rr(190, 100, 820, 520, 26, "#1b1c1f") + rr(193, 103, 814, 514, 24, "none", ' stroke="#3b3d42" stroke-width="2"')
    out += clip(214, 124, 772, 476, 6, site(214, 124, 772, 476))
    out += f'<path d="M120 620 H1080 L1050 664 Q1044 672 1030 672 H170 Q156 672 150 664 Z" fill="url(#metal)"/>'
    out += rr(540, 620, 120, 10, 5, "#8a8d92") + rr(120, 618, 960, 5, 2, "#c9ccd0")
    out += phone(930, 380, 190, 390, lambda sx, sy, sw, sh: site(sx, sy + 26, sw, sh - 26, True))
    return out


def stationery_set(b, p):
    out = ""
    lx, ly, lw, lh = 140, 80, 420, 594
    ink = "#2b2d31"
    let = drop(lx, ly, lw, lh, 4, 0.22) + rr(lx, ly, lw, lh, 4, "#FDFCFA")
    let += place(logo_on(b, "#FDFCFA", "h"), lx + 40, ly + 44, 210, 58, align="start", valign="top")
    let += rr(lx + lw - 140, ly + 54, 100, 8, 4, ink, ' opacity=".25"') + rr(lx + lw - 110, ly + 70, 70, 8, 4, ink, ' opacity=".18"')
    let += bars(lx + 40, ly + 170, [150, 120], ink, 8, 18, 0.3)
    let += bars(lx + 40, ly + 240, [340, 340, 320, 338, 300, 0, 340, 330, 250, 0, 340, 300], ink, 7, 18, 0.16)
    let += B(b, "Nombre Apellido", 13, ink, bold(b)).at(lx + 40, ly + 482).markup
    let += rr(lx + 40, ly + 504, 90, 7, 3.5, ink, ' opacity=".25"')
    let += rr(lx, ly + lh - 46, lw, 46, 0, p.sbg) + rr(lx + 40, ly + lh - 27, 180, 7, 3.5, best_ink(b, p.sbg), ' opacity=".55"')
    let += place(logo_on(b, p.sbg, "s"), lx + lw - 70, ly + lh - 38, 30, 30)
    out += let
    ex, ey, ew, eh = 520, 470, 540, 270
    env = drop(0, 0, ew, eh, 6, 0.24) + rr(0, 0, ew, eh, 6, tint(p.lbg, 0.3))
    env += f'<path d="M0 0 L{ew / 2} {eh * 0.56} L{ew} 0" fill="none" stroke="#000" stroke-opacity=".07" stroke-width="2"/>'
    env += place(logo_on(b, tint(p.lbg, 0.3), "h"), 30, 30, 170, 46, align="start", valign="top")
    env += bars(ew * 0.48, eh * 0.56, [200, 170, 130], ink, 8, 18, 0.25)
    env += rr(ew - 84, 24, 56, 64, 4, p.sec, ' opacity=".85"') + rr(ew - 78, 30, 44, 52, 3, "none", ' stroke="#fff" stroke-width="2" stroke-dasharray="3 3"')
    out += tx(rot(env, -4, ew / 2, eh / 2), ex, ey)
    cw, ch = 350, 200
    card = drop(0, 0, cw, ch, 10, 0.3) + rr(0, 0, cw, ch, 10, p.sbg) + place(b.vertical(p.sv), cw * 0.22, ch * 0.16, cw * 0.56, ch * 0.68) + rr(0, 0, cw, ch, 10, "url(#sheen)")
    out += tx(rot(card, 8, cw / 2, ch / 2), 650, 170)
    pen = f'<rect x="0" y="0" width="300" height="14" rx="7" fill="{p.dark}"/><rect x="230" y="-2" width="44" height="18" rx="4" fill="url(#metal)"/><path d="M300 2 L330 7 L300 12 Z" fill="#9aa0a6"/>'
    out += contact(860, 812, 150, 6, 0.25) + tx(rot(pen, -6, 0, 0), 690, 790)
    return out


def m_stationery(b):
    p = pal(b)
    return bd(p.neutral) + stationery_set(b, p)


def m_digital(b):
    p = pal(b)
    ink = "#2b2d31"
    out = bd(p.neutral)
    wx, wy, ww, wh = 70, 90, 640, 700
    win = drop(wx, wy, ww, wh, 16, 0.25) + rr(wx, wy, ww, wh, 16, "#FFFFFF")
    win += rr(wx, wy, ww, 48, 16, "#f1f2f4") + rr(wx, wy + 32, ww, 16, 0, "#f1f2f4")
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        win += f'<circle cx="{wx + 28 + i * 22}" cy="{wy + 24}" r="7" fill="{c}"/>'
    for i, lab in enumerate(("Para:", "Asunto:")):
        win += B(b, lab, 15, "#7b8088").at(wx + 32, wy + 78 + i * 40).markup + rr(wx + 120, wy + 82 + i * 40, [220, 300][i], 9, 4.5, ink, ' opacity=".18"')
        win += rr(wx + 24, wy + 108 + i * 40, ww - 48, 1.5, 0, "#e3e5e8")
    win += bars(wx + 32, wy + 200, [560, 540, 575, 400, 0, 560, 480], ink, 8, 20, 0.14)
    sy = wy + 380
    win += rr(wx + 32, sy, 4, 190, 2, p.sbg)
    mk = 104
    win += rr(wx + 56, sy + 8, mk, mk, 18, p.sbg) + place(b.mark(p.sv), wx + 56 + mk * 0.16, sy + 8 + mk * 0.16, mk * 0.68, mk * 0.68)
    win += B(b, "Nombre Apellido", 22, ink, bold(b)).at(wx + 184, sy + 12).markup
    win += B(b, "Cargo o área · " + b.name, 15, p.sec if contrast(p.sec, "#fff") > 2.4 else "#6b6f76").at(wx + 184, sy + 46).markup
    for i in range(3):
        win += f'<circle cx="{wx + 192}" cy="{sy + 86 + i * 26}" r="7" fill="{p.sbg}"/>' + rr(wx + 208, sy + 81 + i * 26, [160, 200, 140][i], 9, 4.5, ink, ' opacity=".22"')
    win += place(logo_on(b, "#FFFFFF", "h"), wx + 56, sy + 150, 200, 40, align="start")
    out += win
    sx, sy2, sw, sh = 620, 330, 520, 292
    slide = drop(0, 0, sw, sh, 10, 0.3) + rr(0, 0, sw, sh, 10, p.sbg)
    slide += clip(0, 0, sw, sh, 10, pattern_tile(b, p.sv, 0, 0, sw, sh, 80, 28, 0.1))
    lines = headline(b, b.tagline["es"], 42, sw * 0.7, best_ink(b, p.sbg), 2)
    m, _ = stack_lines(lines, 36, 70)
    slide += m + place(b.horizontal(p.sv), 36, sh - 74, 170, 44, align="start")
    slide += rr(sw - 64, sh - 50, 34, 8, 4, best_ink(b, p.sbg), ' opacity=".4"')
    out += tx(slide, sx, sy2)
    out += tx(drop(0, 0, 300, 170, 10, 0.25) + rr(0, 0, 300, 170, 10, p.lbg) + place(logo_on(b, p.lbg, "v"), 60, 26, 180, 118), 820, 660)
    return out


def bag(x, y, w, h, color, logo, handle):
    g = w * 0.17
    out = soft(x + w * 0.55, y + h + 6, w * 0.62, 22, 0.32)
    out += f'<path d="M{n(x + w * 0.32 + 14)} {n(y + 4)} C{n(x + w * 0.32 + 14)} {n(y - h * 0.36)} {n(x + w * 0.68 + 14)} {n(y - h * 0.36)} {n(x + w * 0.68 + 14)} {n(y + 4)}" fill="none" stroke="{shade(handle, .25)}" stroke-width="9" stroke-linecap="round"/>'
    out += f'<path d="M{n(x + w)} {n(y)} L{n(x + w + g)} {n(y - g * 0.34)} L{n(x + w + g)} {n(y + h - g * 0.3)} L{n(x + w)} {n(y + h)} Z" fill="{shade(color, .22)}"/>'
    out += f'<path d="M{n(x + w + g / 2)} {n(y - g * 0.17)} V{n(y + h * 0.7)} L{n(x + w)} {n(y + h)} M{n(x + w + g / 2)} {n(y + h * 0.7)} L{n(x + w + g)} {n(y + h - g * 0.3)}" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="2"/>'
    out += rr(x, y, w, h, 2, color) + rr(x, y, w, h * 0.07, 0, "#000", ' opacity=".07"') + rr(x, y, w, h, 2, "url(#sheen)")
    out += logo.fit(x + w * 0.16, y + h * 0.26, w * 0.68, h * 0.46).markup
    for hx in (0.32, 0.68):
        out += f'<circle cx="{n(x + w * hx)}" cy="{n(y + h * 0.08)}" r="5" fill="#000" opacity=".35"/>'
    out += f'<path d="M{n(x + w * 0.32)} {n(y + h * 0.08)} C{n(x + w * 0.32)} {n(y - h * 0.3)} {n(x + w * 0.68)} {n(y - h * 0.3)} {n(x + w * 0.68)} {n(y + h * 0.08)}" fill="none" stroke="{handle}" stroke-width="9" stroke-linecap="round"/>'
    return out


def m_bag(b):
    p = pal(b)
    kraft = "#C9A77C"
    out = bd(p.neutral)
    out += bag(190, 380, 330, 400, kraft, logo_on(b, kraft, "v"), shade(kraft, 0.35))
    out += bag(560, 290, 400, 490, p.sbg, b.vertical(p.sv), p.sec if dist(p.sec, p.sbg) > 60 else p.lbg)
    return out


def m_tote(b):
    p = pal(b)
    canvas_c = "#EEE6D8"
    out = bd(tint(p.sec, 0.62) if dist(tint(p.sec, 0.62), canvas_c) > 50 else p.neutral)
    out += soft(600, 815, 270, 30, 0.3)
    strap = shade(canvas_c, 0.08)
    for x0, x1 in ((470, 560), (640, 730)):
        out += f'<path d="M{x0} 340 C{x0} 130 {x1} 130 {x1} 340" fill="none" stroke="{strap}" stroke-width="30"/>'
        out += f'<path d="M{x0} 340 C{x0} 130 {x1} 130 {x1} 340" fill="none" stroke="#000" stroke-opacity=".08" stroke-width="30" stroke-dasharray="2 6"/>'
    d = "M405 330 L795 330 L822 805 L378 805 Z"
    out += f'<path d="{d}" fill="{canvas_c}"/>' + f'<path d="{d}" fill="url(#sheen)"/>'
    out += f'<path d="M408 352 H792" stroke="#000" stroke-opacity=".12" stroke-width="2" stroke-dasharray="7 6"/>'
    out += logo_on(b, canvas_c, "v").fit(460, 430, 280, 260).markup
    pin = f'<circle r="54" fill="{p.sbg}"/>' + place(b.mark(p.sv), -32, -32, 64, 64) + '<circle r="54" fill="url(#sheen)"/>'
    out += contact(492, 778, 50, 8, 0.25) + tx(pin, 480, 720)
    return out


def cup(cx, top, h, tw, body_c, sleeve_c, lid_c, logo):
    bw = tw * 0.74
    xl = lambda y: cx - (tw / 2 - (tw - bw) / 2 * (y - top) / h)
    xr = lambda y: 2 * cx - xl(y)
    d = f"M{n(xl(top))} {n(top)} L{n(xr(top))} {n(top)} L{n(xr(top + h) - 6)} {n(top + h - 4)} Q{n(cx)} {n(top + h + 8)} {n(xl(top + h) + 6)} {n(top + h - 4)} Z"
    out = soft(cx + 10, top + h + 6, bw * 0.7, 18, 0.35)
    out += f'<path d="{d}" fill="{body_c}"/>'
    y1, y2 = top + h * 0.28, top + h * 0.7
    sl = f"M{n(xl(y1))} {n(y1)} L{n(xr(y1))} {n(y1)} L{n(xr(y2))} {n(y2)} L{n(xl(y2))} {n(y2)} Z"
    if sleeve_c:
        out += f'<path d="{sl}" fill="{sleeve_c}"/>'
    out += logo.fit(cx - (xr(y2) - xl(y2)) * 0.32, y1 + (y2 - y1) * 0.14, (xr(y2) - xl(y2)) * 0.64, (y2 - y1) * 0.72).markup
    out += f'<path d="{d}" fill="url(#cyl)"/>'
    out += rr(cx - tw / 2 - 10, top - 26, tw + 20, 30, 10, lid_c) + rr(cx - tw / 2 - 10, top - 26, tw + 20, 30, 10, "url(#cyl)")
    out += f'<path d="M{n(cx - tw / 2 + 2)} {n(top - 24)} Q{n(cx)} {n(top - 70)} {n(cx + tw / 2 - 2)} {n(top - 24)} Z" fill="{lid_c}"/>'
    out += f'<path d="M{n(cx - tw / 2 + 2)} {n(top - 24)} Q{n(cx)} {n(top - 70)} {n(cx + tw / 2 - 2)} {n(top - 24)} Z" fill="url(#cyl)"/>'
    out += f'<ellipse cx="{n(cx + tw * 0.18)}" cy="{n(top - 44)}" rx="14" ry="4" fill="#000" opacity=".35"/>'
    return out


def m_cup(b):
    p = pal(b)
    out = bd(p.neutral)
    lid = "#F4F2EE" if lum(p.sbg) < 0.3 else p.dark
    out += cup(820, 420, 310, 196, p.sbg, None, lid, logo_on(b, p.sbg, "v"))
    out += cup(500, 240, 480, 290, "#FAF8F4", p.sbg, lid, b.vertical(p.sv) if p.sv else b.mark(p.sv))
    return out


TSHIRT = ("M470 140 C520 172 680 172 730 140 L880 190 L1010 340 L905 410 L850 352 L850 800 Q850 814 836 814 "
          "L364 814 Q350 814 350 800 L350 352 L295 410 L190 340 L320 190 Z")


def m_tshirt(b):
    p = pal(b)
    col = p.sbg
    out = bd(tint(p.sec, 0.7) if dist(tint(p.sec, 0.7), col) > 60 else p.neutral)
    out += f'<path d="{TSHIRT}" fill="#000" opacity=".28" filter="url(#b12)" transform="translate(8 18)"/>'
    out += f'<path d="{TSHIRT}" fill="{col}"/>'
    out += f'<path d="M470 140 C520 172 680 172 730 140 C700 168 500 168 470 140 Z" fill="{shade(col, .3)}"/>'
    out += f'<path d="M466 138 C520 186 680 186 734 138" fill="none" stroke="{shade(col, .12)}" stroke-width="16"/>'
    folds = ("M350 360 Q420 420 400 560" , "M850 360 Q790 430 806 600", "M470 640 Q600 690 740 650", "M320 192 Q352 260 350 352", "M880 192 Q848 262 850 352")
    out += "".join(f'<path d="{d}" fill="none" stroke="#000" stroke-opacity=".1" stroke-width="10" stroke-linecap="round" filter="url(#b5)"/>' for d in folds)
    out += f'<path d="{TSHIRT}" fill="url(#sheen)"/>'
    out += logo_on(b, col, "v").fit(500, 280, 200, 180).markup
    tag = rr(578, 156, 44, 18, 3, "#fff", ' opacity=".9"')
    return out + tag


def m_cap(b):
    p = pal(b)
    col = p.sbg
    out = bd(p.neutral)
    out += soft(600, 650, 330, 34, 0.32)
    crown = "M330 560 C330 300 470 245 600 245 C730 245 870 300 870 560 Z"
    out += f'<path d="{crown}" fill="{col}"/>'
    out += f'<path d="M600 247 V548 M600 247 C520 300 462 420 452 552 M600 247 C680 300 738 420 748 552" fill="none" stroke="#000" stroke-opacity=".18" stroke-width="3"/>'
    out += f'<path d="{crown}" fill="url(#sheen)"/>'
    out += f'<ellipse cx="600" cy="246" rx="18" ry="8" fill="{shade(col, .25)}"/>'
    for x in (468, 732):
        out += f'<circle cx="{x}" cy="340" r="6" fill="{shade(col, .35)}"/>'
    out += logo_on(b, col, "m").fit(505, 345, 190, 150).markup
    out += f'<path d="M330 556 Q600 522 870 556 L870 570 Q600 536 330 570 Z" fill="{shade(col, .2)}"/>'
    brim = "M300 572 Q600 528 900 572 Q930 612 886 646 Q600 600 314 646 Q270 612 300 572 Z"
    out += f'<path d="{brim}" fill="{shade(col, .08)}"/><path d="{brim}" fill="url(#vsh)"/>'
    out += f'<path d="M318 640 Q600 596 882 640" fill="none" stroke="#000" stroke-opacity=".18" stroke-width="3" stroke-dasharray="6 6"/>'
    return out


def box3d(x, y, w, h, d, color, front, side=""):
    out = soft(x + w * 0.55 + d * 0.4, y + h + 4, w * 0.62 + d * 0.3, 22, 0.35)
    out += f'<path d="M{n(x)} {n(y)} L{n(x + d)} {n(y - d * 0.5)} L{n(x + w + d)} {n(y - d * 0.5)} L{n(x + w)} {n(y)} Z" fill="{tint(color, .14)}"/>'
    sp = f"M{n(x + w)} {n(y)} L{n(x + w + d)} {n(y - d * 0.5)} L{n(x + w + d)} {n(y + h - d * 0.5)} L{n(x + w)} {n(y + h)} Z"
    out += f'<path d="{sp}" fill="{shade(color, .24)}"/>'
    if side:
        out += clip_path(sp, side)
    out += rr(x, y, w, h, 0, color) + front + rr(x, y, w, h, 0, "url(#sheen)")
    out += f'<path d="M{n(x)} {n(y)} L{n(x + w)} {n(y)} L{n(x + w + d)} {n(y - d * 0.5)}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="2"/>'
    return out


def m_box(b):
    p = pal(b)
    out = bd(p.neutral)
    x, y, w, h, d = 490, 320, 400, 380, 150
    side = f'<g opacity=".22">{pattern_tile(b, "blanco" if lum(p.sbg) < .45 else "negro", x + w, y - d * .5, d, h + d * .5, 60, 22, 1)}</g>'
    out += box3d(x, y, w, h, d, p.sbg, b.vertical(p.sv).fit(x + w * 0.2, y + h * 0.2, w * 0.6, h * 0.6).markup, side)
    sx, sy, sw, sh, sd = 150, 600, 250, 170, 80
    out += box3d(sx, sy, sw, sh, sd, p.lbg, logo_on(b, p.lbg, "h").fit(sx + sw * 0.14, sy + sh * 0.25, sw * 0.72, sh * 0.5).markup)
    ribbon = rr(sx + sw * 0.88, sy, 14, sh, 0, p.sec, ' opacity=".9"')
    return out + ribbon


def jar(cx, base, w, h, body_c, lid_c, label_c, logo, glass=True):
    out = soft(cx + 8, base + 4, w * 0.62, 18, 0.35)
    out += rr(cx - w / 2, base - h, w, h, w * 0.14, body_c)
    out += rr(cx - w * 0.42, base - h - 16, w * 0.84, 22, 6, shade(body_c, .1))
    lh = h * 0.2
    out += rr(cx - w * 0.47, base - h - 16 - lh, w * 0.94, lh, 10, lid_c)
    out += "".join(rr(cx - w * 0.47 + 8 + i * 12, base - h - 16 - lh + 6, 3, lh - 12, 1.5, "#000", ' opacity=".1"') for i in range(int(w * 0.94 / 12) - 1))
    out += rr(cx - w * 0.47, base - h - 16 - lh, w * 0.94, lh, 10, "url(#cyl)")
    ly, lh2 = base - h * 0.78, h * 0.56
    out += rr(cx - w / 2, ly, w, lh2, 0, label_c) + logo.fit(cx - w * 0.36, ly + lh2 * 0.12, w * 0.72, lh2 * 0.76).markup
    out += rr(cx - w / 2, base - h, w, h, w * 0.14, "url(#cyl)")
    if glass:
        out += rr(cx - w / 2 + w * 0.1, base - h + 18, w * 0.06, h - 36, w * 0.03, "#fff", ' opacity=".28"')
    return out


def m_jar(b):
    p = pal(b)
    out = bd(p.neutral)
    body_c = p.sec if b.notes.get("jar") != "light" else p.lbg
    lid = p.dark if dist(p.dark, body_c) > 60 else "#C9A86A"
    out += jar(800, 760, 210, 250, shade(body_c, .05), lid, p.lbg, logo_on(b, p.lbg, "m"))
    out += jar(500, 790, 300, 380, shade(body_c, .05), lid, p.lbg, logo_on(b, p.lbg, "v"))
    return out


def m_bottles(b):
    p = pal(b)
    out = bd(p.neutral)
    glass = shade(p.sec, 0.15)
    out += soft(480, 770, 130, 16, 0.35)
    out += rr(385, 430, 190, 330, 34, glass) + rr(425, 388, 110, 46, 8, p.dark) + rr(445, 290, 70, 108, 35, shade(p.dark, .1))
    out += rr(385, 530, 190, 150, 0, p.lbg) + logo_on(b, p.lbg, "v").fit(405, 545, 150, 120).markup
    out += rr(385, 430, 190, 330, 34, "url(#cyl)") + rr(403, 446, 12, 298, 6, "#fff", ' opacity=".3"')
    out += rr(425, 388, 110, 46, 8, "url(#cyl)") + rr(445, 290, 70, 108, 35, "url(#cyl)")
    out += soft(740, 775, 150, 16, 0.35)
    out += rr(630, 330, 220, 440, 40, p.sbg) + rr(680, 296, 120, 40, 8, p.dark)
    out += rr(727, 236, 26, 66, 4, shade(p.dark, .15)) + rr(690, 214, 100, 30, 12, p.dark) + rr(770, 218, 74, 15, 7, p.dark)
    out += b.vertical(p.sv).fit(660, 450, 160, 200).markup
    out += rr(630, 330, 220, 440, 40, "url(#cyl)") + rr(680, 296, 120, 40, 8, "url(#cyl)") + rr(690, 214, 100, 30, 12, "url(#cyl)")
    return out


def can(cx, top, h, w, color, logo, band, label, b):
    out = soft(cx + 8, top + h + 2, w * 0.66, 16, 0.38)
    out += rr(cx - w / 2, top + 14, w, h - 14, 16, color)
    out += rr(cx - w / 2, top + h * 0.74, w, h * 0.09, 0, band)
    lt = B(b, label, 15, best_ink(b, band), bold(b), tracking=0.18)
    out += lt.at(cx - lt.w / 2, top + h * 0.74 + (h * 0.09 - lt.h) / 2).markup
    out += logo.fit(cx - w * 0.36, top + h * 0.17, w * 0.72, h * 0.48).markup
    out += rr(cx - w / 2, top + 14, w, h - 14, 16, "url(#cyl)")
    out += f'<ellipse cx="{n(cx)}" cy="{n(top + 16)}" rx="{n(w / 2 - 6)}" ry="13" fill="url(#metal)"/>'
    out += f'<ellipse cx="{n(cx)}" cy="{n(top + 14)}" rx="{n(w / 2 - 20)}" ry="8" fill="#9ca0a5"/>'
    out += rr(cx - w / 2 + 2, top + h - 12, w - 4, 12, 6, "url(#metal)")
    return out


def m_can(b):
    p = pal(b)
    out = bd(p.neutral)
    lab = b.notes.get("can", ["330 ml", "330 ml"])
    out += can(800, 280, 470, 230, p.sec, logo_on(b, p.sec, "v"), p.sbg, lab[1], b)
    out += can(530, 200, 580, 280, p.sbg, b.vertical(p.sv), p.sec, lab[0], b)
    return out


def bottle(cx, top, s, glass, label_c, logo, neck_c, b):
    d = (f"M{n(cx - 24 * s)} {n(top)} H{n(cx + 24 * s)} V{n(top + 40 * s)} C{n(cx + 24 * s)} {n(top + 120 * s)} {n(cx + 88 * s)} {n(top + 160 * s)} "
         f"{n(cx + 88 * s)} {n(top + 230 * s)} V{n(top + 640 * s)} Q{n(cx + 88 * s)} {n(top + 666 * s)} {n(cx + 62 * s)} {n(top + 666 * s)} "
         f"H{n(cx - 62 * s)} Q{n(cx - 88 * s)} {n(top + 666 * s)} {n(cx - 88 * s)} {n(top + 640 * s)} V{n(top + 230 * s)} "
         f"C{n(cx - 88 * s)} {n(top + 160 * s)} {n(cx - 24 * s)} {n(top + 120 * s)} {n(cx - 24 * s)} {n(top + 40 * s)} Z")
    out = soft(cx + 6, top + 668 * s, 100 * s, 14, 0.4)
    out += f'<path d="{d}" fill="{glass}"/>'
    out += rr(cx - 88 * s, top + 330 * s, 176 * s, 230 * s, 0, label_c) + logo.fit(cx - 70 * s, top + 350 * s, 140 * s, 190 * s).markup
    out += rr(cx - 26 * s, top + 70 * s, 52 * s, 44 * s, 0, neck_c)
    out += f'<path d="{d}" fill="url(#cyl)"/>'
    out += rr(cx - 62 * s, top + 250 * s, 10 * s, 380 * s, 5 * s, "#fff", ' opacity=".26"')
    out += rr(cx - 28 * s, top - 14 * s, 56 * s, 22 * s, 4 * s, "url(#metal)")
    return out


def m_bottle(b):
    p = pal(b)
    out = bd(p.neutral)
    glass = b.notes.get("glass", "#5B3414")
    out += bottle(760, 210, 0.86, glass, p.sec, logo_on(b, p.sec, "v"), p.sbg, b)
    out += bottle(500, 110, 1.04, glass, p.lbg, logo_on(b, p.lbg, "v"), p.sbg, b)
    return out


def m_storefront(b):
    p = pal(b)
    wall = mix(p.lbg, "#CFC8BE", 0.5)
    out = f'<rect width="{W}" height="{H}" fill="{wall}"/>'
    out += "".join(rr(0, y, W, 2, 0, "#000", ' opacity=".05"') for y in range(30, 820, 46))
    out += rr(0, 820, W, 80, 0, "#8f9296") + rr(0, 820, W, 8, 0, "#6f7276")
    out += rr(140, 120, 920, 700, 0, shade(wall, .08))
    sign = p.sbg
    out += drop(170, 140, 860, 130, 6, 0.25, 0, 14) + rr(170, 140, 860, 130, 6, sign)
    out += logo_on(b, sign, "h").fit(230, 162, 740, 86).markup
    aw_y, aw_h = 300, 86
    stripes = ""
    cols = [p.sbg, "#FFFFFF" if lum(p.sbg) < 0.6 else p.dark]
    for i in range(14):
        stripes += rr(160 + i * 63, aw_y, 63, aw_h, 0, cols[i % 2])
    scallop = "".join(f'<path d="M{160 + i * 63} {aw_y + aw_h} q31.5 34 63 0 Z" fill="{cols[i % 2]}"/>' for i in range(14))
    out += clip(160, aw_y, 882, aw_h + 40, 0, stripes + scallop) + rr(160, aw_y, 882, aw_h, 0, "url(#vsh)")
    out += rr(150, aw_y - 10, 902, 14, 4, shade(p.sbg, .3))
    gx, gy, gw, gh = 200, 430, 500, 360
    out += rr(gx - 12, gy - 12, gw + 24, gh + 24, 4, shade(wall, .4))
    out += rr(gx, gy, gw, gh, 0, "url(#glassd)")
    out += f'<path d="M{gx + 40} {gy} L{gx + 160} {gy} L{gx + 40} {gy + 200} Z M{gx + 220} {gy} L{gx + 270} {gy} L{gx + 80} {gy + gh} L{gx + 30} {gy + gh} Z" fill="#fff" opacity=".08"/>'
    dec = logo_on(b, "#18202a", "m")
    out += dec.fit(gx + gw / 2 - 70, gy + 70, 140, 140).markup
    tl = B(b, b.tagline["es"], 26, "#FFFFFF", bold(b))
    if tl.ink.w > gw - 80:
        tl = tl.scale((gw - 80) / tl.ink.w)
    out += tl.at(gx + (gw - tl.w) / 2, gy + 250).markup
    dx, dy, dw, dh = 770, 430, 230, 390
    out += rr(dx - 12, dy - 12, dw + 24, dh + 12, 4, shade(wall, .4)) + rr(dx, dy, dw, dh, 0, p.sec if dist(p.sec, wall) > 50 else p.dark)
    out += rr(dx + 30, dy + 30, dw - 60, 170, 4, "url(#glassd)") + rr(dx, dy, dw, dh, 0, "url(#sheen)")
    out += rr(dx + dw - 44, dy + 220, 12, 70, 6, "url(#metal)")
    out += rr(dx + 30, dy + 240, dw - 90, 26, 4, "#fff", ' opacity=".85"')
    op = B(b, "ABIERTO", 14, p.dark, bold(b), tracking=0.2)
    out += op.at(dx + 30 + (dw - 90 - op.w) / 2, dy + 246).markup
    for px in (120, 1080):
        out += rr(px - 34, 740, 68, 80, 8, shade(p.dark, 0)) + "".join(
            f'<ellipse cx="{px + dx_}" cy="{dy_}" rx="24" ry="48" fill="#3f7a4a" transform="rotate({r_} {px + dx_} {dy_})"/>' for dx_, dy_, r_ in ((-18, 690, -25), (16, 685, 20), (0, 665, 0)))
    blade = f'<circle r="74" fill="{p.sec if dist(p.sec, wall) > 50 else p.sbg}"/>' + logo_on(b, p.sec if dist(p.sec, wall) > 50 else p.sbg, "m").fit(-46, -46, 92, 92).markup
    out += rr(1040, 172, 110, 8, 4, "#3a3a3a") + tx(blade, 1110, 260)
    return out


def m_pouch(b):
    p = pal(b)
    out = bd(p.neutral)

    def pouch(cx, top, w, h, color, label_c, logo, weight):
        d = (f"M{n(cx - w / 2 + 10)} {n(top)} L{n(cx + w / 2 - 10)} {n(top)} L{n(cx + w / 2)} {n(top + h - 34)} "
             f"Q{n(cx + w / 2)} {n(top + h)} {n(cx + w / 2 - 34)} {n(top + h)} L{n(cx - w / 2 + 34)} {n(top + h)} "
             f"Q{n(cx - w / 2)} {n(top + h)} {n(cx - w / 2)} {n(top + h - 34)} Z")
        o = soft(cx + 8, top + h + 4, w * 0.6, 18, 0.35) + f'<path d="{d}" fill="{color}"/>'
        o += rr(cx - w / 2 + 10, top, w - 20, 40, 0, shade(color, .12))
        o += "".join(rr(cx - w / 2 + 14 + i * 9, top + 6, 4, 28, 2, "#000", ' opacity=".08"') for i in range(int((w - 28) / 9)))
        o += f'<path d="M{n(cx - w / 2 + 14)} {n(top + 64)} H{n(cx + w / 2 - 14)}" stroke="#000" stroke-opacity=".18" stroke-width="3" stroke-dasharray="10 5"/>'
        lx, ly, lw, lh = cx - w * 0.36, top + h * 0.28, w * 0.72, h * 0.48
        o += rr(lx, ly, lw, lh, 20, label_c) + logo.fit(lx + lw * 0.12, ly + lh * 0.1, lw * 0.76, lh * 0.68).markup
        wt = B(b, weight, 15, best_ink(b, label_c), bold(b))
        o += wt.at(cx - wt.w / 2, ly + lh * 0.82).markup
        o += f'<path d="{d}" fill="url(#cyl)" opacity=".7"/><path d="{d}" fill="url(#vsh)"/>'
        return o
    wts = b.notes.get("pouch", ["250 g", "500 g"])
    kraft = "#C6A479"
    out += pouch(820, 340, 270, 410, kraft if b.notes.get("kraft") else p.sec, p.lbg, logo_on(b, p.lbg, "v"), wts[0])
    out += pouch(500, 220, 340, 540, p.sbg, p.lbg, logo_on(b, p.lbg, "v"), wts[1])
    return out


def m_apron(b):
    p = pal(b)
    col = p.dark if lum(p.dark) < 0.15 else p.sbg
    out = bd(tint(p.sec, 0.68) if dist(tint(p.sec, 0.68), col) > 60 else p.neutral)
    strap = shade(col, 0.15)
    out += f'<path d="M505 178 C470 60 730 60 695 178" fill="none" stroke="{strap}" stroke-width="16"/>'
    out += f'<path d="M378 418 C300 430 260 480 240 560 M822 418 C900 430 940 480 960 560" fill="none" stroke="{strap}" stroke-width="16" stroke-linecap="round"/>'
    d = "M500 170 H700 L716 330 Q752 380 822 400 L842 828 H358 L378 400 Q448 380 484 330 Z"
    out += f'<path d="{d}" fill="#000" opacity=".28" filter="url(#b12)" transform="translate(8 16)"/><path d="{d}" fill="{col}"/>'
    out += f'<path d="M520 186 H680 L694 326 Q728 372 800 392 L818 806 H382 L400 392 Q472 372 506 326 Z" fill="none" stroke="#fff" stroke-opacity=".16" stroke-width="2" stroke-dasharray="6 6"/>'
    out += rr(462, 610, 276, 140, 6, shade(col, .1)) + rr(470, 618, 260, 124, 4, "none", ' stroke="#fff" stroke-opacity=".2" stroke-width="2" stroke-dasharray="6 6"')
    out += logo_on(b, col, "m").fit(530, 210, 140, 130).markup
    out += logo_on(b, col, "h").fit(484, 640, 232, 74).markup
    out += f'<path d="{d}" fill="url(#sheen)"/>'
    return out


def m_van(b):
    p = pal(b)
    body_c = "#F6F6F4" if lum(p.lbg) > 0.6 else p.lbg
    out = bd(p.neutral)
    out += rr(0, 700, W, 200, 0, "#000", ' opacity=".05"')
    d = "M120 640 V360 Q120 296 186 296 H770 Q826 296 858 336 L960 466 Q1004 474 1046 496 Q1072 516 1072 560 V640 Q1072 670 1042 670 H150 Q120 670 120 640 Z"
    out += soft(600, 690, 500, 28, 0.38) + f'<path d="{d}" fill="{body_c}"/>'
    out += clip_path(d, f'<path d="M100 560 C400 520 700 640 1100 520 V700 H100 Z" fill="{p.sbg}"/><path d="M100 610 C420 580 720 680 1100 590 V700 H100 Z" fill="{p.sec}"/>')
    out += f'<path d="M790 320 H850 Q870 320 884 338 L956 452 H790 Z" fill="url(#glassd)"/>'
    out += f'<path d="M770 300 V640 M640 300 V640" stroke="#000" stroke-opacity=".12" stroke-width="3"/>'
    out += rr(730, 470, 24, 8, 4, "#8b8f94")
    out += logo_on(b, body_c, "h").fit(180, 350, 420, 140).markup
    tg = B(b, b.tagline["es"], 22, best_ink(b, body_c), bold(b))
    out += tg.at(180, 520).markup if tg.ink.w < 440 else ""
    out += f'<path d="{d}" fill="url(#sheen)"/>'
    for wx in (300, 900):
        out += f'<circle cx="{wx}" cy="668" r="64" fill="#1c1d20"/><circle cx="{wx}" cy="668" r="34" fill="url(#metal)"/><circle cx="{wx}" cy="668" r="10" fill="#555"/>'
    out += rr(1040, 520, 26, 30, 6, "#ffd36b") + rr(122, 520, 14, 34, 4, "#d9473b")
    return out


def tag_shape(x, y, w, h):
    return (f"M{n(x + 26)} {n(y)} H{n(x + w - 26)} L{n(x + w)} {n(y + 40)} V{n(y + h - 20)} Q{n(x + w)} {n(y + h)} {n(x + w - 20)} {n(y + h)} "
            f"H{n(x + 20)} Q{n(x)} {n(y + h)} {n(x)} {n(y + h - 20)} V{n(y + 40)} Z")


def m_hangtag(b):
    p = pal(b)
    out = bd(tint(p.sec, 0.7) if lum(p.sec) < 0.7 else p.neutral)
    w, h = 300, 500
    d = tag_shape(0, 0, w, h)
    back = f'<path d="{d}" fill="#000" opacity=".25" filter="url(#b12)" transform="translate(8 18)"/><path d="{d}" fill="{p.lbg}"/>'
    ink = best_ink(b, p.lbg)
    lines = headline(b, b.tagline["es"], 40, w - 70, ink, 3)
    m, yy = stack_lines(lines, 36, 110)
    back += m + bars(36, yy + 20, [200, 170, 190], ink, 8, 18, 0.22)
    back += "".join(rr(36 + i * 7, h - 120, [3, 2, 4, 2, 3, 5, 2, 3, 2, 4, 3, 2, 5, 2, 3, 2, 4, 3][i % 18], 70, 0, ink) for i in range(30))
    back += f'<circle cx="{w / 2}" cy="46" r="14" fill="{p.neutral}"/>'
    out += tx(rot(back, 12, w / 2, h / 2), 600, 220)
    front = f'<path d="{d}" fill="#000" opacity=".3" filter="url(#b12)" transform="translate(8 18)"/><path d="{d}" fill="{p.sbg}"/><path d="{d}" fill="url(#sheen)"/>'
    front += b.vertical(p.sv).fit(40, 140, w - 80, 260).markup
    front += f'<circle cx="{w / 2}" cy="46" r="20" fill="none" stroke="url(#metal)" stroke-width="7"/><circle cx="{w / 2}" cy="46" r="13" fill="{p.neutral}"/>'
    out += tx(rot(front, -6, w / 2, h / 2), 330, 250)
    out += f'<path d="M478 296 C470 160 600 80 700 40 M478 296 C520 170 660 120 760 120" fill="none" stroke="#b9a07c" stroke-width="5" stroke-linecap="round"/>'
    return out


def m_mug(b):
    p = pal(b)
    out = bd(p.neutral)

    def mug(cx, top, w, h, col, logo):
        o = soft(cx + 20, top + h + 4, w * 0.7, 18, 0.35)
        o += f'<path d="M{n(cx + w / 2 - 8)} {n(top + h * 0.2)} C{n(cx + w / 2 + w * 0.42)} {n(top + h * 0.16)} {n(cx + w / 2 + w * 0.42)} {n(top + h * 0.8)} {n(cx + w / 2 - 8)} {n(top + h * 0.74)}" fill="none" stroke="{shade(col, .08)}" stroke-width="{n(w * 0.11)}" stroke-linecap="round"/>'
        bd_ = f"M{n(cx - w / 2)} {n(top)} H{n(cx + w / 2)} V{n(top + h - 30)} Q{n(cx + w / 2)} {n(top + h)} {n(cx + w / 2 - 30)} {n(top + h)} H{n(cx - w / 2 + 30)} Q{n(cx - w / 2)} {n(top + h)} {n(cx - w / 2)} {n(top + h - 30)} Z"
        o += f'<path d="{bd_}" fill="{col}"/>' + logo.fit(cx - w * 0.32, top + h * 0.2, w * 0.64, h * 0.6).markup + f'<path d="{bd_}" fill="url(#cyl)"/>'
        o += f'<ellipse cx="{n(cx)}" cy="{n(top)}" rx="{n(w / 2)}" ry="16" fill="{shade(col, .06)}"/><ellipse cx="{n(cx)}" cy="{n(top + 2)}" rx="{n(w / 2 - 12)}" ry="11" fill="#3b2416"/>'
        return o
    out += mug(820, 470, 230, 260, p.sbg, b.vertical(p.sv))
    out += mug(470, 330, 320, 400, "#FAF8F5", logo_on(b, "#FAF8F5", "v"))
    out += "".join(f'<path d="M{x} 300 C{x - 20} 270 {x + 20} 250 {x} 214" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="7" stroke-linecap="round" filter="url(#b5)"/>' for x in (430, 470, 510))
    return out


def m_idbadge(b):
    p = pal(b)
    out = bd(p.neutral)
    strap = p.sbg
    out += f'<path d="M470 -20 L585 300 M730 -20 L615 300" stroke="{strap}" stroke-width="44"/>'
    for i in range(4):
        t = 0.18 + i * 0.2
        x, y = 470 + 115 * t, -20 + 320 * t
        out += logo_on(b, strap, "s").fit(x - 14, y - 14, 28, 28).markup
        x, y = 730 - 115 * t, -20 + 320 * t
        out += logo_on(b, strap, "s").fit(x - 14, y - 14, 28, 28).markup
    out += rr(570, 290, 60, 40, 8, "url(#metal)") + rr(588, 320, 24, 34, 4, "url(#metal)")
    cx, cy, cw, ch = 440, 350, 320, 470
    card = drop(cx, cy, cw, ch, 22, 0.3) + rr(cx, cy, cw, ch, 22, "#FFFFFF")
    card += clip(cx, cy, cw, ch, 22, rr(cx, cy, cw, 130, 0, p.sbg) + pattern_tile(b, p.sv, cx, cy, cw, 130, 60, 20, 0.12) + rr(cx, cy + ch - 18, cw, 18, 0, p.sec))
    card += rr(cx + cw / 2 - 40, cy + 18, 80, 14, 7, "#fff", ' opacity=".9"')
    card += b.horizontal(p.sv).fit(cx + 50, cy + 52, cw - 100, 56).markup
    card += f'<circle cx="{cx + cw / 2}" cy="{cy + 210}" r="62" fill="#e8eaed"/><circle cx="{cx + cw / 2}" cy="{cy + 192}" r="24" fill="#c3c7cc"/>'
    card += clip(cx + cw / 2 - 62, cy + 148, 124, 124, 62, f'<ellipse cx="{cx + cw / 2}" cy="{cy + 262}" rx="46" ry="34" fill="#c3c7cc"/>')
    nm = B(b, "Nombre Apellido", 22, "#202226", bold(b))
    out_c = nm.at(cx + (cw - nm.w) / 2, cy + 302).markup
    rl = B(b, "Cargo o área", 15, p.sec if contrast(p.sec, "#fff") > 2.4 else "#6b6f76")
    out_c += rl.at(cx + (cw - rl.w) / 2, cy + 336).markup
    out_c += rr(cx + 70, cy + 380, cw - 140, 8, 4, "#202226", ' opacity=".18"') + rr(cx + 100, cy + 398, cw - 200, 8, 4, "#202226", ' opacity=".12"')
    return out + card + out_c + rr(cx, cy, cw, ch, 22, "url(#sheen)")


def m_wallsign(b):
    p = pal(b)
    wall = tint(p.lbg, 0.1)
    out = f'<rect width="{W}" height="{H}" fill="{wall}"/><rect width="{W}" height="{H}" fill="url(#spot)"/>'
    out += rr(0, 760, W, 140, 0, shade(wall, .18))
    logo = b.horizontal(p.lv).fit(240, 170, 720, 220)
    out += f'<g transform="translate(10 16)" opacity=".28" filter="url(#b12)">{b.horizontal("negro").fit(240, 170, 720, 220).markup}</g>' + logo.markup
    desk = p.sbg
    out += rr(250, 560, 700, 30, 6, tint(desk, .25)) + rr(270, 590, 660, 200, 0, desk) + rr(270, 590, 660, 200, 0, "url(#vsh)")
    out += logo_on(b, desk, "m").fit(560, 630, 80, 80).markup
    out += rr(0, 788, W, 4, 0, "#000", ' opacity=".08"')
    out += rr(1000, 640, 90, 120, 10, p.dark) + "".join(
        f'<ellipse cx="{1045 + dx}" cy="{cy}" rx="30" ry="80" fill="#3f7a4a" transform="rotate({r} {1045 + dx} {cy})"/>' for dx, cy, r in ((-30, 560, -24), (28, 552, 22), (0, 520, 0)))
    out += f'<path d="M120 0 V260" stroke="#2b2b2b" stroke-width="3"/><path d="M80 260 H160 L140 300 H100 Z" fill="{p.dark}"/>'
    return out


def m_bar(b):
    p = pal(b)
    out = bd(p.neutral)

    def bar(w, h, col, label):
        o = drop(0, 0, w, h, 10, 0.3, 10, 24, "b24") + rr(0, 0, w, h, 10, col)
        o += clip(0, 0, w, h, 10, f'<path d="M{w * 0.72} 0 H{w} V{h} H{w * 0.66} L{w * 0.7} {h * 0.8} L{w * 0.64} {h * 0.6} L{w * 0.7} {h * 0.4} L{w * 0.65} {h * 0.2} Z" fill="url(#metal)"/>'
                  + "".join(rr(w * 0.76 + i * w * 0.12, j * h / 3 + 10, w * 0.1, h / 3 - 20, 4, "#4a2a1c") for i in range(2) for j in range(3)))
        o += logo_on(b, col, "v").fit(w * 0.08, h * 0.12, w * 0.52, h * 0.62).markup
        lt = B(b, label, 16, best_ink(b, col), bold(b), tracking=0.2)
        o += lt.at(w * 0.34 - lt.w / 2, h * 0.82).markup + rr(0, 0, w, h, 10, "url(#sheen)")
        return o
    out += tx(rot(bar(560, 300, p.sec, b.notes.get("bars", ["", ""])[1]), 8, 280, 150), 470, 420)
    out += tx(rot(bar(580, 320, p.sbg, b.notes.get("bars", ["", ""])[0]), -7, 290, 160), 170, 200)
    for x, y in ((980, 720), (1060, 680), (1010, 640)):
        out += rr(x, y, 52, 40, 6, "#4a2a1c", f' transform="rotate(14 {x} {y})"') + rr(x + 6, y + 6, 40, 28, 4, "#5d3524", f' transform="rotate(14 {x} {y})"')
    return out


def m_popsicle(b):
    p = pal(b)
    out = bd(tint(p.sec, 0.6))

    def pop(col, deg, x, y):
        d = "M0 60 A60 60 0 0 1 120 60 V300 Q120 316 104 316 H16 Q0 316 0 300 Z"
        o = f'<path d="{d}" fill="#000" opacity=".25" filter="url(#b12)" transform="translate(8 16)"/>'
        o += rr(42, 300, 36, 150, 18, "#E2C391") + f'<path d="{d}" fill="{col}"/><path d="{d}" fill="url(#cyl)" opacity=".7"/>'
        o += rr(18, 40, 12, 230, 6, "#fff", ' opacity=".28"')
        return tx(rot(o, deg, 60, 220), x, y)
    out += pop(p.sec, -12, 760, 170) + pop(p.sbg, 10, 900, 210)
    wx, wy, ww, wh = 140, 300, 560, 330
    zz = "".join(f"L{wx + ww + (10 if i % 2 else 0)} {wy + i * 15}" for i in range(23))
    zl = "".join(f"L{wx - (10 if i % 2 else 0)} {wy + wh - i * 15}" for i in range(23))
    d = f"M{wx} {wy} H{wx + ww} {zz} L{wx + ww} {wy + wh} H{wx} {zl} Z"
    out += f'<path d="{d}" fill="#000" opacity=".28" filter="url(#b12)" transform="translate(8 18)"/><path d="{d}" fill="{p.sbg}"/>'
    out += b.horizontal(p.sv).fit(wx + 60, wy + 70, ww - 120, 150).markup
    tg = B(b, b.tagline["es"], 22, best_ink(b, p.sbg), bold(b))
    out += tg.at(wx + (ww - tg.w) / 2, wy + 250).markup if tg.ink.w < ww - 60 else ""
    out += f'<path d="{d}" fill="url(#sheen)"/>'
    return out


def m_menu(b):
    p = pal(b)
    out = bd(p.neutral)
    x, y, w, h = 360, 70, 480, 760
    paper = tint(p.lbg, 0.25)
    out += drop(x, y, w, h, 6, 0.28, 12, 26, "b24") + rr(x, y, w, h, 6, paper)
    out += logo_on(b, paper, "v").fit(x + w * 0.25, y + 40, w * 0.5, 150).markup
    ink = best_ink(b, paper)
    acc = p.sec if contrast(p.sec, paper) > 2.2 else p.sbg
    yy = y + 240
    for sec in b.notes.get("menu", ["Especiales", "Para compartir", "Bebidas"]):
        t = disp(b, sec, 30, acc)
        if t.ink.w > w - 120:
            t = t.scale((w - 120) / t.ink.w)
        out += t.at(x + 60, yy).markup
        yy += t.h + 22
        for i in range(3):
            out += rr(x + 60, yy, [180, 150, 200][i], 10, 5, ink, ' opacity=".55"') + rr(x + 60, yy + 18, [240, 210, 230][i], 7, 3.5, ink, ' opacity=".2"')
            out += rr(x + w - 110, yy, 50, 10, 5, ink, ' opacity=".5"')
            yy += 46
        yy += 22
    out += rr(x, y + h - 14, w, 14, 0, p.sbg)
    out += soft(1000, 720, 100, 20, 0.25) + f'<circle cx="990" cy="700" r="96" fill="{p.sbg}"/>' + b.mark(p.sv).fit(930, 640, 120, 120).markup
    return out


def m_poster(b):
    p = pal(b)
    wall = mix(p.neutral, "#9a9792", 0.35)
    out = f'<rect width="{W}" height="{H}" fill="{wall}"/>' + "".join(rr(0, y, W, 2, 0, "#000", ' opacity=".06"') for y in range(40, 900, 60))
    out += f'<rect width="{W}" height="{H}" fill="url(#spot)" opacity=".6"/>'
    out += rr(-60, 130, 280, 420, 0, p.lbg, ' transform="rotate(-3 80 340)"') + rr(-60, 130, 280, 420, 0, "url(#sheen)", ' transform="rotate(-3 80 340)"')
    x, y, w, h = 350, 70, 500, 740
    out += drop(x, y, w, h, 0, 0.3, 10, 20)
    out += rr(x, y, w, h, 0, p.sbg) + clip(x, y, w, h, 0, f'<g opacity=".14">{b.sym(p.sv).fit(x + w * 0.28, y + h * 0.22, w * 0.95, w * 0.95).markup}</g>')
    ink = best_ink(b, p.sbg)
    lines = headline(b, b.tagline["es"], 84, w - 90, ink, 3)
    m, yy = stack_lines(lines, x + 45, y + 70, 0.12)
    out += m
    out += b.horizontal(p.sv).fit(x + 45, y + h - 140, w - 200, 90, align="start").markup
    out += rr(x + w - 120, y + h - 110, 76, 76, 6, ink, ' opacity=".9"') + "".join(
        rr(x + w - 112 + (i % 5) * 13, y + h - 102 + (i // 5) * 13, 10, 10, 1, p.sbg) for i in range(25) if (i * 7) % 3)
    out += rr(x, y, w, h, 0, "url(#sheen)")
    for tx_, ty, r in ((x - 20, y - 10, -18), (x + w - 50, y - 12, 16)):
        out += rr(tx_, ty, 80, 30, 2, "#f4f1e8", f' opacity=".75" transform="rotate({r} {tx_ + 40} {ty + 15})"')
    return out


def m_paycard(b):
    p = pal(b)
    out = bd(p.neutral)
    cw, ch = 520, 328

    def card(col, light_card):
        o = drop(0, 0, cw, ch, 22, 0.32, 12, 28, "b24") + rr(0, 0, cw, ch, 22, col)
        ver = p.sv if not light_card else p.lv
        o += clip(0, 0, cw, ch, 22, f'<g opacity=".16">{b.sym(ver).fit(cw * 0.5, -ch * 0.1, cw * 0.7, ch * 1.2).markup}</g>')
        o += (b.horizontal(ver) if not light_card else logo_on(b, col, "h")).fit(34, 30, 190, 50, align="start").markup
        o += rr(34, 128, 64, 48, 9, "#d8b46a") + "".join(f'<path d="M34 {140 + i * 12} H98" stroke="#a88a4a" stroke-width="1.6"/>' for i in range(3))
        ink = best_ink(b, col)
        o += "".join(f'<path d="M{124 + i * 9} 136 q8 16 0 32" fill="none" stroke="{ink}" stroke-width="3" stroke-linecap="round" opacity=".55"/>' for i in range(3))
        nb = B(b, "••••  ••••  ••••  4821", 26, ink, bold(b), tracking=0.06)
        o += nb.at(34, 232).markup + rr(34, 280, 140, 9, 4.5, ink, ' opacity=".4"') + rr(cw - 120, 280, 70, 9, 4.5, ink, ' opacity=".4"')
        return o + rr(0, 0, cw, ch, 22, "url(#sheen)")
    out += tx(rot(card(p.sbg, False), -8, cw / 2, ch / 2), 110, 120)
    out += tx(rot(card(p.lbg, True), 7, cw / 2, ch / 2), 590, 430)
    return out


TEMPLATES = {
    "cards": (m_cards, {"es": "Tarjetas de presentación", "en": "Business cards"}),
    "phone": (m_phone, {"es": "Perfil en redes sociales", "en": "Social media profile"}),
    "app": (m_app, {"es": "App e ícono", "en": "App and icon"}),
    "laptop": (m_laptop, {"es": "Sitio web", "en": "Website"}),
    "stationery": (m_stationery, {"es": "Papelería corporativa", "en": "Corporate stationery"}),
    "digital": (m_digital, {"es": "Firma de correo y presentación", "en": "Email signature and slides"}),
    "bag": (m_bag, {"es": "Bolsas de compra", "en": "Shopping bags"}),
    "tote": (m_tote, {"es": "Bolsa de tela", "en": "Tote bag"}),
    "cup": (m_cup, {"es": "Vasos para llevar", "en": "Takeaway cups"}),
    "tshirt": (m_tshirt, {"es": "Camiseta", "en": "T-shirt"}),
    "cap": (m_cap, {"es": "Gorra", "en": "Cap"}),
    "box": (m_box, {"es": "Empaque", "en": "Packaging"}),
    "jar": (m_jar, {"es": "Frascos", "en": "Jars"}),
    "bottles": (m_bottles, {"es": "Envases", "en": "Bottles"}),
    "can": (m_can, {"es": "Latas", "en": "Cans"}),
    "bottle": (m_bottle, {"es": "Botellas", "en": "Bottles"}),
    "storefront": (m_storefront, {"es": "Fachada y aviso", "en": "Storefront and sign"}),
    "pouch": (m_pouch, {"es": "Bolsas de producto", "en": "Product pouches"}),
    "apron": (m_apron, {"es": "Delantal", "en": "Apron"}),
    "van": (m_van, {"es": "Vehículo", "en": "Vehicle"}),
    "hangtag": (m_hangtag, {"es": "Etiquetas", "en": "Tags"}),
    "mug": (m_mug, {"es": "Mugs", "en": "Mugs"}),
    "idbadge": (m_idbadge, {"es": "Carné y cinta", "en": "ID badge and lanyard"}),
    "wallsign": (m_wallsign, {"es": "Señalética interior", "en": "Interior signage"}),
    "bar": (m_bar, {"es": "Empaque de chocolate", "en": "Chocolate packaging"}),
    "popsicle": (m_popsicle, {"es": "Producto y empaque", "en": "Product and wrapper"}),
    "menu": (m_menu, {"es": "Menú", "en": "Menu"}),
    "poster": (m_poster, {"es": "Afiche", "en": "Poster"}),
    "paycard": (m_paycard, {"es": "Tarjetas de pago", "en": "Payment cards"}),
}
CORPORATE = ["stationery", "digital"]


def render(b, key):
    fn, label = TEMPLATES[key]
    return canvas(W, H, fn(b), f"{b.name} · {label['es']}", DEFS)


def build(b, out):
    names = []
    for key in list(b.mockups) + CORPORATE:
        (out / f"mockup-{key}.svg").write_text(render(b, key), encoding="utf-8")
        names.append(key)
    return names

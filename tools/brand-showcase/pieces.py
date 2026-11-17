"""Kit pieces: profile image, banners, stickers, type specimens, guide diagrams and the gallery cover."""
from lib import Box, Rect, canvas, contrast, lum, mix, n, text, uid

SANS = ("inter", 400)


def strong(b):
    """(version, background) for the brand's most saturated/dark surface."""
    if lum(b.bg("principal")) < lum(b.bg("inversa")):
        return "principal", b.bg("principal")
    return "inversa", b.bg("inversa")


def light(b):
    if lum(b.bg("principal")) >= lum(b.bg("inversa")):
        return "principal", b.bg("principal")
    return "inversa", b.bg("inversa")


def best_ink(b, bg, exclude=()):
    cands = [h for k, h, *_ in b.colors if k not in exclude] + ["#111111", "#FFFFFF"]
    return max(cands, key=lambda h: contrast(h, bg))


def accent_on(b, bg, minimum=2.6):
    """A palette color that is not the background and still reads on it (prefer saturated ones)."""
    from colorsys import rgb_to_hls
    from lib import rgb
    best = None
    for _k, h, *_ in b.colors:
        if h.upper() == bg.upper() or contrast(h, bg) < minimum:
            continue
        r, g, bb = (v / 255 for v in rgb(h))
        sat = rgb_to_hls(r, g, bb)[2]
        score = sat * 2 + contrast(h, bg) / 10
        if best is None or score > best[0]:
            best = (score, h)
    return best[1] if best else best_ink(b, bg)


def disp(b, s, size, fill, **kw):
    f = b.display
    return text(f[0], f[1], s, size, fill, italic=len(f) > 2 and f[2], **kw)


def body(b, s, size, fill, weight=None, **kw):
    return text(b.body[0], weight or b.body[1], s, size, fill, **kw)


def wrap_lines(b, s, size, width, fill, font="display"):
    """Greedy word wrap with the brand display font."""
    words, lines, cur = s.split(), [], ""
    fn = disp if font == "display" else body
    for w in words:
        t = (cur + " " + w).strip()
        if cur and fn(b, t, size, fill).ink.w > width:
            lines.append(cur)
            cur = w
        else:
            cur = t
    lines.append(cur)
    return [fn(b, ln, size, fill) for ln in lines]


def symbol_defs(b, version, ident):
    m = b.sym(version)
    return f'<g id="{ident}">{m.markup}</g>', m


def pattern(b, version, w, h, step, size, opacity, ident=None):
    """Tiled symbol pattern (uses <use> so the symbol is stored once)."""
    ident = ident or uid("s")
    g, m = symbol_defs(b, version, ident)
    s = size / max(m.ink.w, m.ink.h)
    out = []
    row = 0
    y = -step / 2
    while y < h + step:
        x = -step / 2 + (step / 2 if row % 2 else 0)
        while x < w + step:
            out.append(f'<use href="#{ident}" transform="translate({n(x - m.ink.x0 * s)} {n(y - m.ink.y0 * s)}) scale({n(s)})"/>')
            x += step
        y += step * 0.86
        row += 1
    return f"<defs>{g}</defs>", f'<g opacity="{n(opacity)}">{"".join(out)}</g>'


# ---------------------------------------------------------------- pieces
def profile(b):
    v, bg = strong(b)
    mk = b.mark(v).fit(1080 * 0.2, 1080 * 0.2, 1080 * 0.6, 1080 * 0.6)
    return canvas(1080, 1080, f'<rect width="1080" height="1080" fill="{bg}"/>{mk.markup}', f"{b.name} · perfil")


def cover_banner(b):
    W, H = 1640, 624
    v, bg = strong(b)
    defs, pat = pattern(b, v, W, H, 190, 70, 0.07)
    logo = b.horizontal(v).fit(W * 0.25, H * 0.2, W * 0.5, H * 0.42)
    tag = body(b, b.tagline["es"], 46, accent_on(b, bg), tracking=0.04)
    tag = tag.center_at(W / 2, logo.ink.y1 + 84)
    return canvas(W, H, f'<rect width="{W}" height="{H}" fill="{bg}"/>{pat}{logo.markup}{tag.markup}',
                  f"{b.name} · portada", defs)


def launch_post(b):
    W, H = 1080, 1350
    v, bg = light(b)
    sv, sbg = strong(b)
    ink = best_ink(b, bg)
    acc = accent_on(b, bg)
    head = wrap_lines(b, b.tagline["es"], 150, W - 200, ink)
    if len(head) > 3 or max(h.ink.w for h in head) > W - 200:
        head = wrap_lines(b, b.tagline["es"], 112, W - 200, ink)
    parts, y = [], 250
    for ln in head:
        y += ln.layout.h
        parts.append(ln.at(100, y - ln.layout.h).markup)
        y += 34
    kicker = body(b, "NUEVO", 34, acc, weight=b.body[1], tracking=0.3).at(100, 150)
    band = f'<rect x="0" y="{H - 330}" width="{W}" height="330" fill="{sbg}"/>'
    logo = b.horizontal(sv).fit(100, H - 330 + 95, W - 200, 140, align="start")
    big = b.sym(v)
    s = 520 / max(big.ink.w, big.ink.h)
    deco = big.scale(s).move(W - 360 - big.ink.x0 * s, y + 10 - big.ink.y0 * s)
    deco = f'<g opacity="0.16">{deco.markup}</g>' if y + 10 + big.ink.h * s > H - 330 else deco.markup
    clip = uid("c")
    return canvas(W, H, f'<rect width="{W}" height="{H}" fill="{bg}"/><clipPath id="{clip}"><rect width="{W}" height="{H - 330}"/></clipPath>'
                  f'<g clip-path="url(#{clip})">{deco}</g>{kicker.markup}{"".join(parts)}{band}{logo.markup}',
                  f"{b.name} · publicación")


def die_cut(markup, width):
    i = uid("d")
    return (f'<style>#{i} *{{fill:#fff!important;stroke:#fff!important;stroke-width:{n(width)}px!important;'
            f'stroke-linejoin:round!important;stroke-linecap:round!important}}</style><g id="{i}">{markup}</g>')


def sticker_round(b):
    S = 1200
    v, bg = strong(b)
    lockup = b.vertical(v)
    inner = lockup.fit(S * 0.24, S * 0.24, S * 0.52, S * 0.52)
    return canvas(S, S, f'<circle cx="600" cy="600" r="590" fill="#fff"/><circle cx="600" cy="600" r="552" fill="{bg}"/>{inner.markup}',
                  f"{b.name} · sticker logo")


def sticker_symbol(b):
    S = 1200
    v, bg = light(b)
    raw = b.mark(v)
    mk = raw.fit(S * 0.16, S * 0.16, S * 0.68, S * 0.68)
    outline = b.mark(v).fit(S * 0.16, S * 0.16, S * 0.68, S * 0.68)
    scale = mk.ink.w / raw.ink.w
    return canvas(S, S, die_cut(outline.markup, 110 / scale) + mk.markup, f"{b.name} · sticker símbolo")


def sticker_phrase(b):
    S = 1200
    sv, sbg = strong(b)
    ink = best_ink(b, sbg)
    lines = wrap_lines(b, b.tagline["es"], 120, 760, ink)
    blk_h = sum(ln.layout.h for ln in lines) + 40 * (len(lines) - 1)
    widest = max(ln.ink.w for ln in lines)
    k = min(1.0, 760 / widest, 430 / blk_h)
    lines = [ln.scale(k) for ln in lines]
    blk_h = sum(ln.layout.h for ln in lines) + 40 * k * (len(lines) - 1)
    widest = max(ln.ink.w for ln in lines)
    pw, ph = widest + 200, blk_h + 220
    x0, y0 = (S - pw) / 2, (S - ph) / 2
    out, y = [], y0 + 110
    for ln in lines:
        out.append(ln.at((S - ln.w) / 2, y).markup)
        y += ln.layout.h + 40 * k
    r = min(ph / 2, 120)
    acc = accent_on(b, sbg, 1.8)
    return canvas(S, S, f'<rect x="{n(x0 - 30)}" y="{n(y0 - 30)}" width="{n(pw + 60)}" height="{n(ph + 60)}" rx="{n(r + 30)}" fill="#fff"/>'
                        f'<rect x="{n(x0)}" y="{n(y0)}" width="{n(pw)}" height="{n(ph)}" rx="{n(r)}" fill="{sbg}"/>'
                        f'<rect x="{n(x0 + 22)}" y="{n(y0 + 22)}" width="{n(pw - 44)}" height="{n(ph - 44)}" rx="{n(max(r - 22, 0))}" fill="none" stroke="{acc}" stroke-width="5" stroke-dasharray="2 14" stroke-linecap="round"/>'
                        + "".join(out), f"{b.name} · sticker frase")


# ---------------------------------------------------------------- guide
def specimen(b, which):
    W, H = 1200, 640
    v, bg = light(b)
    ink = best_ink(b, bg)
    acc = accent_on(b, bg)
    f = b.display if which == "display" else b.body
    from fonts import FONTS
    italic = len(f) > 2 and f[2]
    weight = f[1]
    aa = text(f[0], weight, "Aa", 300, ink, italic=italic)
    if aa.ink.w > 400:
        aa = aa.scale(400 / aa.ink.w)
    aa = aa.at(80, 300 - aa.layout.h)
    name = text(f[0], weight, FONTS[f[0]][1], 56, ink, italic=italic)
    if name.ink.w > 560:
        name = name.scale(560 / name.ink.w)
    name = name.at(564, 140)
    role = text(*SANS, ("TÍTULOS Y LOGO" if which == "display" else "TEXTOS") + f" · {weight}", 22, acc, tracking=0.2).at(564, 92)
    rows = ["ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", "abcdefghijklmnñopqrstuvwxyz", "0123456789 ¿?¡! áéíóú & @ $ %"]
    out, y = [], 250
    for r in rows:
        t = text(f[0], weight, r, 40, ink, italic=italic)
        if t.ink.w > 560:
            t = t.scale(560 / t.ink.w)
        out.append(t.at(564, y).markup)
        y += 82
    line = f'<rect x="80" y="{H - 70}" width="{W - 160}" height="2" fill="{ink}" opacity="0.15"/>'
    return canvas(W, H, f'<rect width="{W}" height="{H}" fill="{bg}"/>{aa.markup}{role.markup}{name.markup}{"".join(out)}{line}',
                  f"{b.name} · {FONTS[f[0]][1]}")


def clear_space(b):
    W, H = 1200, 640
    v, bg = light(b)
    logo = b.horizontal(v).fit(260, 210, 680, 220)
    sym = b.sym(v)
    unit = min(logo.ink.h * 0.42, 90)
    r = logo.ink
    x0, y0, x1, y1 = r.x0 - unit, r.y0 - unit, r.x1 + unit, r.y1 + unit
    acc = "#E5484D"
    guide = (f'<rect x="{n(x0)}" y="{n(y0)}" width="{n(x1 - x0)}" height="{n(y1 - y0)}" fill="none" stroke="{acc}" stroke-width="2" stroke-dasharray="10 8"/>'
             f'<rect x="{n(r.x0)}" y="{n(r.y0)}" width="{n(r.w)}" height="{n(r.h)}" fill="none" stroke="{acc}" stroke-width="1.5" opacity="0.55"/>')
    marks = ""
    for (mx, my) in ((x0, y0), (r.x1, y0), (x0, r.y1), (r.x1, r.y1)):
        marks += f'<rect x="{n(mx)}" y="{n(my)}" width="{n(unit)}" height="{n(unit)}" fill="{acc}" opacity="0.14"/>'
    mini = sym.fit(r.x0 - unit + unit * 0.18, y0 + unit * 0.18, unit * 0.64, unit * 0.64)
    mini = f'<g opacity="0.55">{mini.markup}</g>'
    return canvas(W, H, f'<rect width="{W}" height="{H}" fill="{bg}"/>{marks}{guide}{mini}{logo.markup}', f"{b.name} · área de protección")


def misuse(b, kind):
    W, H = 600, 420
    v, bg = light(b)
    logo = b.horizontal(v)
    if kind == "deformar":
        lg = logo.fit(80, 120, 440, 180)
        r = lg.ink
        cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        inner = f'<g transform="translate({n(cx)} {n(cy)}) scale(1.35 0.62) translate({n(-cx)} {n(-cy)})">{lg.markup}</g>'
    elif kind == "rotar":
        lg = logo.fit(110, 130, 380, 160)
        r = lg.ink
        inner = f'<g transform="rotate(-16 {n((r.x0 + r.x1) / 2)} {n((r.y0 + r.y1) / 2)})">{lg.markup}</g>'
    elif kind == "colores":
        import re
        lg = logo.fit(80, 130, 440, 160)
        alt = ["#7B61FF", "#00C2A8", "#FF7A00", "#E4007C"]
        it = iter(alt * 50)

        def swap(m):
            if m.group(2).upper() in ("000000", "FFFFFF", "000", "FFF"):
                return m.group(0)
            return f'{m.group(1)}="{next(it)}"'
        inner = re.sub(r'(fill|stroke)="#([0-9A-Fa-f]{3,6})"', swap, lg.markup)
    else:  # contraste: principal version over a busy, low-contrast background
        lg = logo.fit(80, 130, 440, 160)
        busy = "".join(f'<circle cx="{x}" cy="{y}" r="{r_}" fill="{c}" opacity="0.85"/>' for x, y, r_, c in
                       [(90, 120, 110, mix(bg, "#000", 0.25)), (330, 300, 150, mix(bg, "#888", 0.5)), (520, 90, 130, mix(bg, "#000", 0.4)),
                        (250, 60, 70, mix(bg, "#fff", 0.2)), (500, 360, 90, mix(bg, "#000", 0.15))])
        inner = busy + lg.markup
    x = (f'<circle cx="552" cy="48" r="26" fill="#E5484D"/><path d="M541 37 L563 59 M563 37 L541 59" stroke="#fff" stroke-width="5" stroke-linecap="round"/>')
    i = uid("c")
    return canvas(W, H, f'<clipPath id="{i}"><rect width="{W}" height="{H}"/></clipPath><g clip-path="url(#{i})"><rect width="{W}" height="{H}" fill="{bg}"/>{inner}</g>{x}',
                  f"{b.name} · uso incorrecto")


# ---------------------------------------------------------------- gallery cover
def cover(b):
    W, H = 1200, 900
    v, bg = light(b)
    sv, sbg = strong(b)
    left = f'<rect width="{W}" height="{H}" fill="{bg}"/>'
    logo = b.horizontal(v).fit(80, 230, 640, 300)
    panel = f'<rect x="780" y="0" width="420" height="{H - 150}" fill="{sbg}"/>'
    mk = b.mark(sv).fit(850, (H - 150) / 2 - 140, 280, 280)
    chips, x = "", 0
    cols = [h for _k, h, *_ in b.colors]
    cw = W / len(cols)
    for h in cols:
        chips += f'<rect x="{n(x)}" y="{H - 150}" width="{n(cw + 1)}" height="150" fill="{h}"/>'
        x += cw
    return canvas(W, H, left + panel + logo.markup + mk.markup + chips, f"{b.name}")


def build(b, out):
    files = {
        "perfil.svg": profile(b), "banner-portada.svg": cover_banner(b), "post-lanzamiento.svg": launch_post(b),
        "sticker-logo.svg": sticker_round(b), "sticker-simbolo.svg": sticker_symbol(b), "sticker-frase.svg": sticker_phrase(b),
        "tipo-titulos.svg": specimen(b, "display"), "tipo-textos.svg": specimen(b, "body"),
        "guia-area.svg": clear_space(b), "portada.svg": __import__("lib").foil(cover(b), b.notes.get("foil")),
    }
    for k in ("deformar", "rotar", "colores", "contraste"):
        files[f"no-{k}.svg"] = misuse(b, k)
    for name, svg in files.items():
        (out / name).write_text(svg, encoding="utf-8")
    return list(files)

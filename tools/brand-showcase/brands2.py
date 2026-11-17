"""Brands 9–16: bold, elegant, organic and playful directions."""
import math

from lib import arc_text, n, pbounds, rot
from model import *  # noqa: F403


def L(es, en):
    return {"es": es, "en": en}


# 9 · GUAYABA CLUB · juice bar · bold --------------------------------------------
def guayaba_sym(c, mono):
    seeds = "".join(E(50 + 15 * math.cos(math.radians(a)), 56 + 15 * math.sin(math.radians(a)), 3.2, 5.2, c["s"], a + 90)
                    for a in range(-90, 270, 60))
    leaf_d = "M64 12 C70 0 88 -4 100 2 C96 14 82 22 66 18 Z"
    leaf = P(leaf_d, c["g"]) + ("" if mono else S("M68 15 C78 10 88 6 97 3", c["l"], 1.6))
    gap = f'<path d="{leaf_d}" fill="#000" stroke="#000" stroke-width="7" stroke-linejoin="round"/>'
    if mono:
        ring = P("M50 6 A50 50 0 1 1 49.99 6 Z M50 13 A43 43 0 1 0 50.01 13 Z", c["g"], ' fill-rule="evenodd"')
        flesh = P("M50 16 A40 40 0 1 1 49.99 16 Z M50 31 A25 25 0 1 0 50.01 31 Z", c["p"], ' fill-rule="evenodd"')
        return Box(knock(ring + flesh + seeds, gap) + leaf, Rect(0, -1, 100.5, 106))
    shine = P("M22 44 A30 30 0 0 1 44 24 A34 34 0 0 0 27 50 Z", c["l"])
    body = C(50, 56, 50, c["g"]) + C(50, 56, 43, c["p"]) + shine + C(50, 56, 26, c["l"]) + seeds
    return Box(knock(body, gap) + leaf, Rect(0, -1, 100.5, 106))


def guayaba_wm(c, mono, al="start"):
    main = text("syne", 700, "guayaba", 100, c["k"], tracking=-0.02, box="x")
    lab = text("syne", 800, "CLUB", 40, "#000", tracking=0.14)
    pw, ph = lab.ink.w + 40, lab.layout.h + 24
    pill = Box(knock(R(0, 0, pw, ph, c["pill"], ph / 2), lab.at(20, 12).markup, -10, -10, pw + 20, ph + 20), Rect(0, 0, pw, ph))
    x = main.ink.x1 - pw if al == "start" else (main.ink.x0 + main.ink.x1 - pw) / 2
    return group(main, pill.at(x, main.ink.y1 + 14))


guayaba = Brand(
    slug="guayaba-club", name="Guayaba Club", style="bold",
    sector=L("Bar de jugos y batidos", "Juice and smoothie bar"),
    concept=L("Una tajada de guayaba vista de frente y una etiqueta tipo club: fresco, tropical y para compartir. Rosa intenso con verde hoja.",
              "A guava slice seen head-on and a club-style tag: fresh, tropical and made for sharing. Hot pink with leaf green."),
    tagline=L("Jugos con mucha vida", "Juices full of life"),
    personality=L(["Vibrante", "Tropical", "Social"], ["Vibrant", "Tropical", "Social"]),
    colors=[("guayaba", "#FF4F79", "Guayaba", "Guava", "Principal", "Primary"),
            ("mandarina", "#FF9A2E", "Mandarina", "Tangerine", "Acento", "Accent"),
            ("hoja", "#1E8C5A", "Verde hoja", "Leaf green", "Secundario", "Secondary"),
            ("crema", "#FFF1EA", "Crema rosada", "Blush cream", "Fondo", "Background")],
    display=("syne", 800), body=("poppins", 400),
    roles={"g": "hoja", "p": "guayaba", "l": "crema", "s": "hoja", "k": "guayaba", "pill": "hoja", "pt": "crema"},
    inverse={"g": "mandarina", "p": "crema", "l": "guayaba", "s": "hoja", "k": "crema", "pill": "hoja", "pt": "crema"},
    base_bg="crema", inverse_bg="guayaba",
    symbol=guayaba_sym, wordmark=guayaba_wm, sym_k=1.0, gap_k=0.22, vsym_k=1.0,
    logo_kind=L("Símbolo + logotipo + etiqueta", "Symbol + wordmark + tag"),
    mockups=["cup", "bottle", "bag", "storefront", "menu", "tshirt"],
)


# 10 · ÉBANO · jewelry · elegant -------------------------------------------------
def ebano_sym(c, mono):
    a, k = c["a"], c.get("d", c["a"])
    facets = [("M30 10 H70 L62 35 H38 Z", a), ("M30 10 L38 35 H5 Z", k), ("M70 10 L95 35 H62 Z", k),
              ("M5 35 H38 L50 95 Z", a), ("M38 35 H62 L50 95 Z", k), ("M62 35 H95 L50 95 Z", a)]
    body = "".join(P(d, f if not mono else a) for d, f in facets)
    cuts = S("M5 35 H95 M30 10 L38 35 M70 10 L62 35 M38 35 L50 95 L62 35", "#000", 2.6)
    return Box(knock(body, cuts), Rect(5, 10, 95, 95))


def ebano_wm(c, mono, al="start"):
    main = text("bodoni-moda", 500, "ÉBANO", 100, c["k"], tracking=0.2)
    sub = text("raleway", 500, "JOYERÍA", 20, c["a"], tracking=0.9)
    return word_block(main, sub, 0.3, align="start" if al == "start" else "center")


ebano = Brand(
    slug="ebano", name="Ébano Joyería", style="elegant",
    sector=L("Joyería de autor", "Designer jewelry"),
    concept=L("Una gema facetada en champaña y negro que atrapa la luz, con una Bodoni de alto contraste: lujo sereno, sin exceso.",
              "A faceted gem in champagne and black that catches the light, with a high-contrast Bodoni: quiet luxury, never excessive."),
    tagline=L("Piezas que permanecen", "Pieces that endure"),
    personality=L(["Refinada", "Exclusiva", "Serena"], ["Refined", "Exclusive", "Poised"]),
    colors=[("ebano", "#121212", "Ébano", "Ebony", "Principal", "Primary"),
            ("champana", "#C9A96E", "Champaña", "Champagne", "Acento", "Accent"),
            ("marfil", "#F4EEE4", "Marfil", "Ivory", "Fondo", "Background"),
            ("perla", "#BDB7AE", "Gris perla", "Pearl gray", "Apoyo", "Support")],
    display=("bodoni-moda", 500), body=("raleway", 400),
    roles={"k": "ebano", "a": "champana", "d": "ebano"}, inverse={"k": "marfil", "a": "champana", "d": "perla"},
    base_bg="marfil", inverse_bg="ebano",
    symbol=ebano_sym, wordmark=ebano_wm, sym_k=1.05, gap_k=0.36, vsym_k=0.95, vgap_k=0.3,
    logo_kind=L("Símbolo lineal + logotipo Bodoni", "Line symbol + Bodoni wordmark"),
    mockups=["box", "bag", "cards", "hangtag", "phone", "poster"],
)


# 11 · HACIENDA MAGNOLIA · boutique hotel · elegant ------------------------------
PETAL = "M50 6 C63 22 65 46 50 66 C35 46 37 22 50 6 Z"


def magnolia_sym(c, mono):
    vein = lambda t: f'<path d="M50 14 C48 30 48 46 50 60" fill="none" stroke="#000" stroke-width="2.4" stroke-linecap="round"{t}/>'
    side = (f'<path d="{PETAL}" fill="{c["r"]}" transform="rotate(-52 50 68)"/>'
            f'<path d="{PETAL}" fill="{c["r"]}" transform="rotate(52 50 68)"/>')
    side = knock(side, vein(' transform="rotate(-52 50 68)"') + vein(' transform="rotate(52 50 68)"'))
    gap = f'<path d="{PETAL}" fill="none" stroke="#000" stroke-width="7"/>'
    center = knock(P(PETAL, c["a"]), vein(""))
    cup = P("M28 64 Q50 92 72 64 Q66 84 50 86 Q34 84 28 64 Z", c["p"])
    body = knock(side, gap) + center + cup
    return Box(body, pbounds((PETAL, rot(-52, 50, 68)), (PETAL, rot(52, 50, 68)), PETAL, "M28 64 Q50 92 72 64 Q66 84 50 86 Q34 84 28 64 Z"))


def magnolia_wm(c, mono, al="start"):
    top = text("montserrat", 500, "HACIENDA", 17, c["a"], tracking=0.62)
    main = text("cormorant-garamond", 600, "Magnolia", 112, c["p"], tracking=0.0, box="ink")
    sub = text("montserrat", 500, "HOTEL BOUTIQUE", 14, c["p"], tracking=0.5)
    a = "start" if al == "start" else "center"
    return vstack([top, main, sub], gap=[20, 18], align=a)


magnolia = Brand(
    slug="hacienda-magnolia", name="Hacienda Magnolia", style="elegant",
    sector=L("Hotel boutique y eventos", "Boutique hotel and events"),
    concept=L("Una magnolia que se abre como bienvenida, con una serif clásica y espacios generosos. Verde hacienda, latón y crema.",
              "A magnolia opening in welcome, with a classic serif and generous spacing. Estate green, brass and cream."),
    tagline=L("Quédate un poco más", "Stay a little longer"),
    personality=L(["Hospitalaria", "Clásica", "Serena"], ["Hospitable", "Classic", "Calm"]),
    colors=[("verde", "#23392F", "Verde hacienda", "Estate green", "Principal", "Primary"),
            ("laton", "#B48A4A", "Latón", "Brass", "Acento", "Accent"),
            ("magnolia", "#F2EBDF", "Magnolia", "Magnolia", "Fondo", "Background"),
            ("rosa", "#D9B8B0", "Rosa pétalo", "Petal pink", "Detalles", "Details")],
    display=("cormorant-garamond", 600), body=("montserrat", 400),
    roles={"p": "verde", "a": "laton", "r": "rosa"}, inverse={"p": "magnolia", "a": "laton", "r": "rosa"},
    base_bg="magnolia", inverse_bg="verde",
    symbol=magnolia_sym, wordmark=magnolia_wm, sym_k=0.92, gap_k=0.3, vsym_k=0.62, vgap_k=0.2,
    logo_kind=L("Símbolo floral + logotipo serif", "Floral symbol + serif wordmark"),
    mockups=["cards", "menu", "bottles", "wallsign", "mug", "bag"],
)


# 12 · ÁMBAR · chocolate · elegant ------------------------------------------------
POD = "M50 14 C80 32 80 82 50 100 C20 82 20 32 50 14 Z"


def ambar_sym(c, mono):
    left = "M50 14 C20 32 20 82 50 100 C38 74 38 42 50 22 Z"
    mid = "M50 22 C38 42 38 74 50 93 C62 74 62 42 50 22 Z"
    right = "M50 14 C80 32 80 82 50 100 C62 74 62 42 50 22 Z"
    ridges = S("M50 22 C38 42 38 74 50 93", "#000", 3.4) + S("M50 22 C62 42 62 74 50 93", "#000", 3.4)
    pod = knock(P(left, c["p"]) + P(mid, c["a"] if not mono else c["p"]) + P(right, c["p"]), ridges)
    leaf = P("M50 14 C52 4 62 -1 74 1 C70 11 60 15 50 14 Z", c["a"])
    return Box(pod + leaf, pbounds(POD, "M50 14 C52 4 62 -1 74 1 C70 11 60 15 50 14 Z"))


def ambar_wm(c, mono, al="start"):
    main = text("playfair-display", 700, "Ámbar", 112, c["p"], italic=True)
    sub = text("lato", 700, "CHOCOLATERÍA", 17, c["a"], tracking=0.52)
    return word_block(main, sub, 0.24, align="start" if al == "start" else "center")


ambar = Brand(
    slug="ambar", name="Ámbar Chocolatería", style="elegant",
    sector=L("Chocolatería de origen", "Single-origin chocolatier"),
    concept=L("Una mazorca de cacao con su hoja, trazada en pocas líneas, y una itálica cálida que se siente artesanal y premium. Cacao, ámbar y crema.",
              "A cacao pod with its leaf, drawn in a few lines, and a warm italic that feels handmade and premium. Cacao, amber and cream."),
    tagline=L("Cacao que se disfruta despacio", "Cacao to savor slowly"),
    personality=L(["Cálida", "Golosa", "Premium"], ["Warm", "Indulgent", "Premium"]),
    colors=[("cacao", "#3A2119", "Cacao", "Cacao", "Principal", "Primary"),
            ("ambar", "#D89436", "Ámbar", "Amber", "Acento", "Accent"),
            ("crema", "#F6ECDF", "Crema", "Cream", "Fondo", "Background"),
            ("frambuesa", "#9C2F45", "Frambuesa", "Raspberry", "Sabores", "Flavors")],
    display=("playfair-display", 700, True), body=("lato", 400),
    roles={"p": "cacao", "a": "ambar"}, inverse={"p": "crema", "a": "ambar"},
    base_bg="crema", inverse_bg="cacao",
    symbol=ambar_sym, wordmark=ambar_wm, sym_k=1.1, gap_k=0.34, vsym_k=1.0,
    logo_kind=L("Símbolo + logotipo itálico", "Symbol + italic wordmark"),
    mockups=["bar", "box", "bag", "cards", "phone", "poster"],
)


# 13 · MASA MADRE · bakery · organic ---------------------------------------------
def wheat(fill, cx=50, top=8, h=92):
    k = h / 92
    s = R(cx - 1.6 * k, top + 26 * k, 3.2 * k, 66 * k, fill, 1.6 * k)
    for i in range(3):
        y = top + (26 + i * 16) * k
        s += E(cx - 8 * k, y, 6 * k, 12 * k, fill, -32) + E(cx + 8 * k, y, 6 * k, 12 * k, fill, 32)
    s += E(cx, top + 12 * k, 6 * k, 12.5 * k, fill)
    return s


def masa_sym(c, mono):
    return Box(wheat(c["p"], 50, 0, 92), Rect(33.8, -0.5, 66.2, 92))


def masa_emblem(c, mono):
    p, a = c["p"], c["a"]
    ring = P("M100 2 A98 98 0 1 1 99.99 2 Z M100 10 A90 90 0 1 0 100.01 10 Z", p, ' fill-rule="evenodd"')
    inner = P("M100 44 A56 56 0 1 1 99.99 44 Z M100 48 A52 52 0 1 0 100.01 48 Z", p, ' fill-rule="evenodd"')
    top = arc_text("fraunces", 700, "MASA MADRE", 25, 100, 100, 66, p, tracking=0.12, where="top")
    bot = arc_text("libre-franklin", 600, "TALLER DE PAN", 15, 100, 100, 76, p, tracking=0.3, where="bottom")
    dots = C(26, 100, 4, a) + C(174, 100, 4, a)
    return symbol_box(ring + inner + top + bot + dots + wheat(p, 100, 58, 84), 200, 200)


def masa_wm(c, mono, al="start"):
    main = text("fraunces", 700, "Masa Madre", 100, c["p"], tracking=-0.01)
    sub = text("libre-franklin", 600, "TALLER DE PAN", 19, c["k"], tracking=0.45)
    return word_block(main, sub, 0.3, align="start" if al == "start" else "center")


def masa_vertical(c, mono):
    return masa_emblem(c, mono)


masa = Brand(
    slug="masa-madre", name="Masa Madre", style="organic",
    sector=L("Panadería artesanal de masa madre", "Artisan sourdough bakery"),
    concept=L("Un sello redondo como los de los costales de harina, con una espiga al centro: pan hecho a mano y sin afán. Corteza, trigo y harina.",
              "A round stamp like those on flour sacks, with a wheat ear at its heart: bread made by hand, without rushing. Crust, wheat and flour."),
    tagline=L("Pan con tiempo", "Bread that takes its time"),
    personality=L(["Artesanal", "Honesta", "Cálida"], ["Handmade", "Honest", "Warm"]),
    colors=[("corteza", "#5A3A22", "Corteza", "Crust", "Principal", "Primary"),
            ("trigo", "#D9A85B", "Trigo", "Wheat", "Acento", "Accent"),
            ("harina", "#F6EFE3", "Harina", "Flour", "Fondo", "Background"),
            ("carbon", "#2D2622", "Carbón suave", "Soft charcoal", "Texto", "Text")],
    display=("fraunces", 700), body=("libre-franklin", 400),
    roles={"p": "corteza", "a": "trigo", "k": "carbon"}, inverse={"p": "harina", "a": "trigo", "k": "trigo"},
    base_bg="harina", inverse_bg="corteza",
    symbol=masa_sym, wordmark=masa_wm, sym_k=1.35, gap_k=0.36, vertical_fn=masa_vertical, emblem=masa_emblem,
    logo_kind=L("Sello circular + logotipo", "Circular stamp + wordmark"),
    mockups=["bag", "box", "apron", "cup", "storefront", "cards"],
)


# 14 · MIEL DE MONTE · honey · organic -------------------------------------------
HEX = "M50 0 L93.3 25 L93.3 75 L50 100 L6.7 75 L6.7 25 Z"
PEAKS = "M18 74 L38 44 L48 58 L62 36 L84 74 Z"


def miel_sym(c, mono):
    hexa = P(HEX, c["a"])
    cut = f'<path d="{PEAKS}" fill="#000" stroke="#000" stroke-width="7" stroke-linejoin="round"/>'
    snow = "M30.7 55 L38 44 L44.7 53.3 L41 56 L38 52 L34 57 Z M53.6 48.6 L62 36 L71.5 52.3 L67 50 L62 54 L58 49 Z"
    peaks = f'<path d="{PEAKS}" fill="{c["p"]}" stroke="{c["p"]}" stroke-width="1" stroke-linejoin="round"/>'
    drop = P("M50 104 C55 112 58 116 58 120 A8 8 0 0 1 42 120 C42 116 45 112 50 104 Z", c["a"])
    if mono:
        body = knock(two_tone(hexa, cut, peaks, True), P(snow, "#000") + C(76, 30, 6, "#000"))
        return Box(body + drop, Rect(6.7, 0, 93.3, 128))
    body = two_tone(hexa, cut, peaks + P(snow, c["l"]), False) + C(76, 30, 6, c["p"])
    return Box(body + drop, Rect(6.7, 0, 93.3, 128))


def miel_wm(c, mono, al="start"):
    main = text("young-serif", 400, "Miel de Monte", 100, c["k"], tracking=-0.01)
    sub = text("mulish", 700, "MIEL PURA DE ABEJAS", 19, c["p"], tracking=0.32)
    return word_block(main, sub, 0.3, align="start" if al == "start" else "center")


miel = Brand(
    slug="miel-de-monte", name="Miel de Monte", style="organic",
    sector=L("Miel pura y productos de la colmena", "Raw honey and hive products"),
    concept=L("Una celda de panal que guarda la montaña y una gota que cae: miel de origen, de la finca a la mesa. Ámbar miel, verde monte y tierra.",
              "A honeycomb cell holding the mountain and a falling drop: honey with an origin, from farm to table. Honey amber, mountain green and earth."),
    tagline=L("Del monte a tu mesa", "From the mountain to your table"),
    personality=L(["Natural", "Auténtica", "Generosa"], ["Natural", "Authentic", "Generous"]),
    colors=[("miel", "#EFA51C", "Miel", "Honey", "Principal", "Primary"),
            ("monte", "#2E5A3A", "Verde monte", "Mountain green", "Secundario", "Secondary"),
            ("cera", "#FFF5DA", "Cera", "Beeswax", "Fondo", "Background"),
            ("tierra", "#3A2918", "Tierra", "Earth", "Texto", "Text")],
    display=("young-serif", 400), body=("mulish", 400),
    roles={"a": "miel", "p": "monte", "k": "tierra", "l": "cera"}, inverse={"a": "miel", "p": "monte", "k": "cera", "l": "cera"},
    base_bg="cera", inverse_bg="monte",
    symbol=miel_sym, wordmark=miel_wm, sym_k=1.4, gap_k=0.28, vsym_k=1.15,
    logo_kind=L("Símbolo + logotipo serif", "Symbol + serif wordmark"),
    mockups=["jar", "box", "tote", "pouch", "cards", "phone"],
)


# 15 · RAÍZ · organic produce · organic ------------------------------------------
def raiz_sym(c, mono):
    p, k = c["p"], c["k"]
    leaves = (P("M48 44 C34 44 22 34 20 18 C36 18 48 28 48 44 Z", p)
              + P("M52 38 C54 20 66 8 84 6 C84 26 72 38 52 38 Z", p) + R(47.5, 30, 5, 30, p, 2.5))
    ground = R(8, 60, 84, 6, k, 3)
    roots = S("M50 66 C48 76 40 82 34 92", k, 4.4) + S("M50 66 L50 98", k, 4.4) + S("M50 66 C52 76 60 82 66 92", k, 4.4)
    return symbol_box(f'<g transform="translate(-8 -6)">{leaves}{ground}{roots}</g>', 84, 94.2)


def raiz_wm(c, mono, al="start"):
    main = text("dm-serif-display", 400, "Raíz", 124, c["k"], swap={2: "dotlessi"})
    s = main.slots[2]
    h = main.metrics["cap"] * 0.42
    leaf_d = "M0 0 C-2 -26 14 -46 40 -50 C42 -24 26 -4 0 0 Z"
    sc = h / 50
    x, y = s.x0 + s.w * 0.15, s.y0 - main.metrics["cap"] * 0.05
    leaf = f'<g transform="translate({n(x)} {n(y)}) scale({n(sc)})">{P(leaf_d, c["p"])}</g>'
    main = main.add(leaf, Rect(x - 2 * sc, y - 50 * sc, x + 42 * sc, y))
    sub_ = text("dm-sans", 700, "HUERTA ORGÁNICA", 18, c["p"], tracking=0.32)
    return word_block(main, sub_, 0.26, align="start" if al == "start" else "center")


raiz = Brand(
    slug="raiz", name="Raíz Huerta Orgánica", style="organic",
    sector=L("Huerta orgánica y mercado a domicilio", "Organic farm and produce delivery"),
    concept=L("Un brote que crece sobre la tierra y unas raíces que se ven: lo que comes tiene origen. Verde brote, tierra y un toque zanahoria.",
              "A sprout growing above the soil with visible roots: what you eat has an origin. Sprout green, soil brown and a carrot accent."),
    tagline=L("Cosecha de esta semana", "This week's harvest"),
    personality=L(["Fresca", "Cercana", "Consciente"], ["Fresh", "Neighborly", "Mindful"]),
    colors=[("brote", "#4C9A3F", "Verde brote", "Sprout green", "Principal", "Primary"),
            ("tierra", "#6B3F24", "Tierra", "Soil", "Texto", "Text"),
            ("zanahoria", "#F07B2C", "Zanahoria", "Carrot", "Acento", "Accent"),
            ("crema", "#FBF5EA", "Crema", "Cream", "Fondo", "Background")],
    display=("dm-serif-display", 400), body=("dm-sans", 400),
    roles={"p": "brote", "k": "tierra", "a": "zanahoria"}, inverse={"p": "crema", "k": "crema", "a": "zanahoria"},
    base_bg="crema", inverse_bg="brote",
    symbol=raiz_sym, wordmark=raiz_wm, sym_k=1.05, gap_k=0.24, vsym_k=0.95,
    logo_kind=L("Símbolo ilustrado + logotipo serif", "Illustrated symbol + serif wordmark"),
    mockups=["tote", "box", "van", "apron", "pouch", "phone"],
)


# 16 · MICHI & FIRULAIS · pet shop · playful -------------------------------------
DOG_EAR = "M62 26 C72 10 92 10 98 28 C102 44 92 62 82 66 C80 52 74 38 62 26 Z"


def michi_sym(c, mono):
    p, a, k = c["p"], c["a"], c["k"]
    face = C(50, 60, 37, p) + P("M17 46 L9 10 L45 25 Z", p)
    feats = C(37, 56, 5.5, "#000") + C(63, 56, 5.5, "#000") + P("M44 68 H56 Q56 74 50 76 Q44 74 44 68 Z", "#000")
    ear_gap = f'<path d="{DOG_EAR}" fill="#000" stroke="#000" stroke-width="8"/>'
    if mono:
        body = knock(face, feats + ear_gap) + P(DOG_EAR, a)
    else:
        body = knock(face, feats.replace("#000", "#000") + ear_gap) + C(37, 56, 5.5, k) + C(63, 56, 5.5, k) + P("M44 68 H56 Q56 74 50 76 Q44 74 44 68 Z", k) + P(DOG_EAR, a)
    return Box(body, Rect(9, 10, 101, 97))


def michi_wm(c, mono, al="start"):
    l1 = hstack([text("fredoka", 700, "Michi", 100, c["p"]), text("fredoka", 700, "&", 100, c["a"])], gap=24, valign="bottom")
    l2 = text("fredoka", 700, "Firulais", 100, c["k"])
    sub = text("nunito", 800, "TIENDA DE MASCOTAS", 20, c["a"], tracking=0.22)
    return vstack([l1, l2, sub], gap=[16, 26], align="start" if al == "start" else "center")


michi = Brand(
    slug="michi-firulais", name="Michi & Firulais", style="playful",
    sector=L("Tienda de mascotas", "Pet shop"),
    concept=L("Una carita que es mitad gato y mitad perro: aquí todos son bienvenidos. Letras redondas, colores alegres y mucho cariño.",
              "A little face that's half cat, half dog: everyone is welcome here. Rounded letters, cheerful colors and lots of love."),
    tagline=L("Todo para tu peludo", "Everything for your furry friend"),
    personality=L(["Alegre", "Amigable", "Juguetona"], ["Cheerful", "Friendly", "Playful"]),
    colors=[("naranja", "#FF8A3D", "Naranja michi", "Kitty orange", "Principal", "Primary"),
            ("turquesa", "#18A5A7", "Turquesa", "Turquoise", "Secundario", "Secondary"),
            ("noche", "#1F2D4A", "Azul noche", "Night blue", "Texto", "Text"),
            ("crema", "#FFF6E9", "Crema", "Cream", "Fondo", "Background")],
    display=("fredoka", 700), body=("nunito", 400),
    roles={"p": "naranja", "a": "turquesa", "k": "noche"}, inverse={"p": "naranja", "a": "turquesa", "k": "crema"},
    base_bg="crema", inverse_bg="noche",
    symbol=michi_sym, wordmark=michi_wm, sym_k=0.82, gap_k=0.2, vsym_k=0.55,
    logo_kind=L("Mascota + logotipo redondeado", "Mascot + rounded wordmark"),
    mockups=["pouch", "storefront", "tshirt", "bag", "cards", "mug"],
)

BRANDS = [guayaba, ebano, magnolia, ambar, masa, miel, raiz, michi]

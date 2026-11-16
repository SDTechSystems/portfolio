"""Brands 17–24: playful, retro and tech directions."""
import math

from lib import arc_text, n, pbounds, rot
from model import *  # noqa: F403


def L(es, en):
    return {"es": es, "en": en}


def polar(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


# 17 · POMPÓN · kids clothing · playful ------------------------------------------
def pompon_sym(c, mono):
    puffs = C(50, 50, 38, c["p"]) + "".join(C(*polar(50, 50, 38, a), 13, c["p"]) for a in range(0, 360, 36))
    face = C(39, 50, 4.6, "#000") + C(61, 50, 4.6, "#000") + S("M42 60 Q50 67 58 60", "#000", 4.2)
    cheeks = "" if mono else E(31, 59, 5, 3.4, c["y"]) + E(69, 59, 5, 3.4, c["y"])
    return Box(knock(puffs, face) + cheeks, Rect(-1, -1, 101, 101))


def pompon_wm(c, mono, al="start"):
    main = text("baloo-2", 800, "pompón", 100, c["k"], tracking=-0.01, box="x", swap={4: "o"})
    s = main.slots[4]
    r = main.metrics["xh"] * 0.2
    cx, cy = (s.x0 + s.x1) / 2 + r * 0.4, s.y0 - r * 1.55
    puff = C(cx, cy, r, c["p"]) + "".join(C(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)), r * 0.36, c["p"]) for a in range(0, 360, 45))
    main = main.add(puff, Rect(cx - r * 1.36, cy - r * 1.36, cx + r * 1.36, cy + r * 1.36))
    sub_ = text("quicksand", 700, "ROPA Y JUGUETES", 19, c["a"], tracking=0.26)
    return word_block(main, sub_, 0.62, align="start" if al == "start" else "center")


pompon = Brand(
    slug="pompon", name="Pompón", style="playful",
    sector=L("Ropa y juguetes para niños", "Kids' clothing and toys"),
    concept=L("Un pompón suave con carita feliz, letras redondas y colores de dulce: tierno sin ser infantil de más.",
              "A soft pompom with a happy face, rounded letters and candy colors: sweet without being too childish."),
    tagline=L("Suave como un abrazo", "Soft as a hug"),
    personality=L(["Tierna", "Alegre", "Suave"], ["Sweet", "Cheerful", "Soft"]),
    colors=[("rosa", "#FF8FB1", "Rosa chicle", "Bubblegum pink", "Principal", "Primary"),
            ("cielo", "#5BB8EC", "Cielo", "Sky", "Secundario", "Secondary"),
            ("limon", "#FFE066", "Limón", "Lemon", "Acento", "Accent"),
            ("uva", "#4E3A8E", "Uva", "Grape", "Texto", "Text"),
            ("vainilla", "#FFF8EC", "Vainilla", "Vanilla", "Fondo", "Background")],
    display=("baloo-2", 800), body=("quicksand", 500),
    roles={"p": "rosa", "a": "cielo", "y": "limon", "k": "uva"}, inverse={"p": "rosa", "a": "limon", "y": "limon", "k": "vainilla"},
    base_bg="vainilla", inverse_bg="uva",
    symbol=pompon_sym, wordmark=pompon_wm, sym_k=1.05, gap_k=0.2, vsym_k=1.0,
    logo_kind=L("Personaje + logotipo redondeado", "Character + rounded wordmark"),
    mockups=["tshirt", "hangtag", "box", "bag", "phone", "cards"],
)


# 18 · PALETÓN · ice pops · playful ----------------------------------------------
POP = "M20 30 A30 30 0 0 1 80 30 V70 Q80 78 72 78 Q66 78 64 84 Q60 90 56 84 Q52 78 46 78 H28 Q20 78 20 70 Z"


def paleton_sym(c, mono):
    body = knock(P(POP, c["p"]), C(84, 14, 13, "#000") + C(41, 42, 4.6, "#000") + C(59, 42, 4.6, "#000")
                 + S("M42 54 Q50 62 58 54", "#000", 4.4))
    stick = R(43, 81, 14, 27, c["a"], 7)
    return Box(body + stick, Rect(20, 0, 80, 108))


def paleton_wm(c, mono, al="start"):
    main = text("bagel-fat-one", 400, "Paletón", 100, c["k"], tracking=0.01)
    sub = text("lexend", 700, "PALETAS ARTESANALES", 18, c["p"], tracking=0.22)
    return word_block(main, sub, 0.28, align="start" if al == "start" else "center")


paleton = Brand(
    slug="paleton", name="Paletón", style="playful",
    sector=L("Paletas y helados artesanales", "Artisan ice pops and ice cream"),
    concept=L("Una paleta mordida con sonrisa y una letra gordita que da ganas de probar. Colores frescos de sandía y menta.",
              "A bitten ice pop with a smile and a chubby typeface that makes you want a taste. Fresh watermelon and mint colors."),
    tagline=L("Frío que hace sonreír", "Cold treats, warm smiles"),
    personality=L(["Divertida", "Fresca", "Antojadiza"], ["Fun", "Fresh", "Craveable"]),
    colors=[("sandia", "#FF4D6D", "Sandía", "Watermelon", "Principal", "Primary"),
            ("menta", "#3DDBB0", "Menta", "Mint", "Secundario", "Secondary"),
            ("mora", "#3B1F5C", "Mora", "Blackberry", "Texto", "Text"),
            ("vainilla", "#FFF4E6", "Vainilla", "Vanilla", "Fondo", "Background")],
    display=("bagel-fat-one", 400), body=("lexend", 400),
    roles={"p": "sandia", "a": "menta", "k": "mora"}, inverse={"p": "sandia", "a": "menta", "k": "vainilla"},
    base_bg="vainilla", inverse_bg="mora",
    symbol=paleton_sym, wordmark=paleton_wm, sym_k=1.25, gap_k=0.24, vsym_k=1.05,
    logo_kind=L("Personaje + logotipo display", "Character + display wordmark"),
    mockups=["popsicle", "cup", "storefront", "poster", "tshirt", "cap"],
)


# 19 · LA NAVAJA · barbershop · retro --------------------------------------------
STACHE = ("M100 104 C92 90 74 88 64 97 C56 104 46 103 40 96 C43 112 60 120 76 113 C86 109 94 104 100 111 "
          "C106 104 114 109 124 113 C140 120 157 112 160 96 C154 103 144 104 136 97 C126 88 108 90 100 104 Z")


def star(cx, cy, r, fill):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        x, y = polar(cx, cy, rr, -90 + i * 36)
        pts.append(f"{n(x)} {n(y)}")
    return P("M" + " L".join(pts) + " Z", fill)


def navaja_sym(c, mono):
    return Box(P(STACHE, c["p"]), pbounds(STACHE))


def navaja_emblem(c, mono):
    cuts = (P("M100 10 A90 90 0 1 1 99.99 10 Z M100 14 A86 86 0 1 0 100.01 14 Z", "#000", ' fill-rule="evenodd"')
            + arc_text("alfa-slab-one", 400, "LA NAVAJA", 27, 100, 100, 58, "#000", tracking=0.1, where="top")
            + arc_text("oswald", 600, "BARBERÍA CLÁSICA", 16, 100, 100, 73, "#000", tracking=0.22, where="bottom")
            + P("M100 50 A50 50 0 1 1 99.99 50 Z M100 53 A47 47 0 1 0 100.01 53 Z", "#000", ' fill-rule="evenodd"')
            + f'<g transform="translate(0 -4)">{P(STACHE, "#000")}</g>'
            + star(29, 100, 6, "#000") + star(171, 100, 6, "#000")
            + R(76, 122, 48, 3, "#000", 1.5))
    return symbol_box(knock(C(100, 100, 98, c["p"]), cuts, -10, -10, 220, 220), 200, 200)


def navaja_wm(c, mono, al="start"):
    main = text("alfa-slab-one", 400, "LA NAVAJA", 100, c["k"], tracking=0.03)
    sub = ruled(text("oswald", 600, "BARBERÍA CLÁSICA", 30, c["a"], tracking=0.3), main.ink.w, c["a"], 2.6)
    return word_block(main, sub, 0.3)


def navaja_h(c, mono):
    wm = navaja_wm(c, mono)
    return vstack([navaja_sym(c, mono).width_to(wm.w * 0.42), wm], gap=wm.h * 0.12)


navaja = Brand(
    slug="la-navaja", name="La Navaja Barbería", style="retro",
    sector=L("Barbería clásica", "Classic barbershop"),
    concept=L("Un sello de barbería de antes con bigote al centro y letras de slab gruesas: oficio, ritual y buena conversación. Vino, crema y azul marino.",
              "An old-school barbershop seal with a mustache at its center and heavy slab letters: craft, ritual and good conversation. Wine, cream and navy."),
    tagline=L("El corte de siempre", "The classic cut"),
    personality=L(["Clásica", "Masculina", "Confiable"], ["Classic", "Rugged", "Reliable"]),
    colors=[("vino", "#7A1F2B", "Vino", "Wine", "Principal", "Primary"),
            ("crema", "#F1E6D2", "Crema", "Cream", "Fondo", "Background"),
            ("marino", "#1E2A3A", "Azul marino", "Navy", "Texto", "Text"),
            ("laton", "#B8914B", "Latón", "Brass", "Acento", "Accent")],
    display=("alfa-slab-one", 400), body=("oswald", 400),
    roles={"p": "vino", "k": "marino", "a": "vino"}, inverse={"p": "crema", "k": "crema", "a": "laton"},
    base_bg="crema", inverse_bg="marino",
    symbol=navaja_sym, wordmark=navaja_wm, sym_k=0.9, gap_k=0.16, emblem=navaja_emblem, horizontal_fn=navaja_h,
    vertical_fn=navaja_emblem,
    logo_kind=L("Emblema + logotipo slab", "Emblem + slab wordmark"),
    mockups=["storefront", "jar", "apron", "cards", "tshirt", "phone"],
)


# 20 · PÁRAMO · craft beer · retro -----------------------------------------------
def frailejon(fill, cx=50, top=24):
    s = R(cx - 4.5, top + 22, 9, 46, fill, 2)
    for a in (-90, -55, -125, -25, -155, -5, -175):
        x, y = polar(cx, top + 22, 15, a)
        s += E(x, y, 4.2, 15, fill, a + 90)
    return s


def paramo_sym(c, mono):
    sun = P("M6 70 A44 44 0 0 1 94 70 Z", c["a"])
    stripes = R(0, 52, 100, 3.5, "#000") + R(0, 60, 100, 4.5, "#000")
    plant_cut = f'<g stroke="#000" stroke-width="8" stroke-linejoin="round">{frailejon("#000")}</g>'
    body = knock(sun, stripes + plant_cut) + frailejon(c["g"])
    ground = R(0, 72, 100, 5, c["p"], 2.5)
    return Box(body + ground, Rect(0, 4, 100, 77))


def paramo_wm(c, mono, al="start"):
    main = text("shrikhand", 400, "Páramo", 108, c["p"], tracking=0.0, box="ink")
    sub = text("barlow-semi-condensed", 700, "CERVECERÍA ARTESANAL", 21, c["k"], tracking=0.3)
    return word_block(main, sub, 0.16, align="start" if al == "start" else "center")


paramo = Brand(
    slug="paramo", name="Páramo Cervecería", style="retro",
    sector=L("Cerveza artesanal de montaña", "Mountain craft brewery"),
    concept=L("Un frailejón frente a un sol de rayas setenteras y una letra con curvas generosas: cerveza de altura con espíritu retro.",
              "A frailejón plant before a striped seventies sun and a generously curved typeface: high-altitude beer with a retro spirit."),
    tagline=L("Cerveza de altura", "High-altitude beer"),
    personality=L(["Aventurera", "Retro", "Local"], ["Adventurous", "Retro", "Local"]),
    colors=[("mostaza", "#E2A626", "Mostaza", "Mustard", "Sol", "Sun"),
            ("oxido", "#C2512C", "Óxido", "Rust", "Principal", "Primary"),
            ("laguna", "#2D6E6A", "Laguna", "Lagoon", "Secundario", "Secondary"),
            ("hueso", "#F4E9D4", "Hueso", "Bone", "Fondo", "Background"),
            ("cafe", "#3A2618", "Café oscuro", "Dark brown", "Texto", "Text")],
    display=("shrikhand", 400), body=("barlow-semi-condensed", 500),
    roles={"a": "mostaza", "p": "oxido", "g": "laguna", "k": "cafe"}, inverse={"a": "mostaza", "p": "hueso", "g": "hueso", "k": "mostaza"},
    base_bg="hueso", inverse_bg="laguna",
    symbol=paramo_sym, wordmark=paramo_wm, sym_k=1.3, gap_k=0.2, vsym_k=0.95,
    logo_kind=L("Símbolo ilustrado + logotipo display", "Illustrated symbol + display wordmark"),
    mockups=["bottle", "can", "tshirt", "cap", "poster", "tote"],
)


# 21 · EL TRANVÍA · retro café ---------------------------------------------------
def tranvia_sym(c, mono):
    cup = P("M18 44 H74 V54 C74 72 62 84 46 84 C30 84 18 72 18 54 Z", c["p"])
    handle = P("M76 50 A13 13 0 1 1 76 76 L72 72 A8 8 0 1 0 74 56 Z", c["p"])
    saucer = R(6, 88, 80, 7, c["p"], 3.5)
    steam = "".join(S(f"M{x} 36 C{x - 7} 28 {x + 7} 22 {x} 12", c["k"], 4.6) for x in (34, 46, 58))
    return Box(cup + handle + saucer + steam, Rect(6, 9.7, 89.3, 95))


def tranvia_wm(c, mono, al="start"):
    main = text("pacifico", 400, "El Tranvía", 100, c["p"], tracking=0.0, box="ink")
    sub = text("josefin-sans", 700, "CAFÉ & POSTRES", 22, c["k"], tracking=0.38)
    return word_block(main, sub, 0.14, align="start" if al == "start" else "center")


tranvia = Brand(
    slug="el-tranvia", name="El Tranvía Café", style="retro",
    sector=L("Cafetería y postres", "Café and desserts"),
    concept=L("Una letra cursiva como los avisos pintados a mano de los años cincuenta y una taza humeante: el café del barrio de toda la vida.",
              "A script like hand-painted fifties signs and a steaming cup: the neighborhood café you've always known."),
    tagline=L("Un tinto y una buena charla", "Coffee and a good chat"),
    personality=L(["Nostálgica", "Cálida", "Conversadora"], ["Nostalgic", "Warm", "Chatty"]),
    colors=[("cereza", "#D7263D", "Cereza", "Cherry", "Principal", "Primary"),
            ("menta", "#8FD5C4", "Menta retro", "Retro mint", "Acento", "Accent"),
            ("crema", "#FBEEDB", "Crema", "Cream", "Fondo", "Background"),
            ("cafe", "#4A2C20", "Café", "Coffee", "Texto", "Text")],
    display=("pacifico", 400), body=("josefin-sans", 400),
    roles={"p": "cereza", "k": "cafe"}, inverse={"p": "crema", "k": "menta"},
    base_bg="crema", inverse_bg="cafe",
    symbol=tranvia_sym, wordmark=tranvia_wm, sym_k=0.95, gap_k=0.22, vsym_k=0.6,
    logo_kind=L("Símbolo + logotipo script", "Symbol + script wordmark"),
    mockups=["cup", "mug", "pouch", "storefront", "menu", "apron"],
)


# 22 · ÓRBITA · software studio · tech -------------------------------------------
RING = "M50 34 A48 15 0 1 1 49.99 34"


def orbita_sym(c, mono):
    ell = 'cx="50" cy="50" rx="49" ry="15" transform="rotate(-24 50 50)"'
    planet = knock(C(50, 50, 29, c["p"]), f'<path d="M0 50 A50 15.5 0 0 0 100 50" fill="none" stroke="#000" stroke-width="13" transform="rotate(-24 50 50)"/>')
    ring_back = f'<path d="M100 50 A49 15 0 0 0 0 50" fill="none" stroke="{c["a"]}" stroke-width="5" transform="rotate(-24 50 50)"/>'
    ring_front = f'<path d="M0 50 A49 15 0 0 0 100 50" fill="none" stroke="{c["a"]}" stroke-width="5" transform="rotate(-24 50 50)"/>'
    back_cut = knock(ring_back, C(50, 50, 33, "#000"))
    sat = C(*polar(50, 50, 42, -60), 6, c["a"])
    return Box(back_cut + planet + ring_front + sat, Rect(1, 9, 99, 91))


def orbita_wm(c, mono, al="start"):
    main = text("space-grotesk", 700, "órbita", 100, c["k"], tracking=-0.03)
    sub = text("space-grotesk", 500, "ESTUDIO DE SOFTWARE", 17, c["a2"], tracking=0.2)
    return word_block(main, sub, 0.3, align="start" if al == "start" else "center")


orbita = Brand(
    slug="orbita", name="Órbita Software", style="tech",
    sector=L("Estudio de desarrollo de software", "Software development studio"),
    concept=L("Un planeta con su anillo y un satélite: ideas que entran en órbita y se vuelven productos. Violeta, cian y azul noche.",
              "A planet with its ring and a satellite: ideas that reach orbit and become products. Violet, cyan and night blue."),
    tagline=L("Ideas en órbita", "Ideas in orbit"),
    personality=L(["Innovadora", "Precisa", "Curiosa"], ["Innovative", "Precise", "Curious"]),
    colors=[("violeta", "#6C4CFF", "Violeta", "Violet", "Principal", "Primary"),
            ("cian", "#29D3F5", "Cian", "Cyan", "Acento", "Accent"),
            ("noche", "#0B0F2A", "Azul noche", "Night blue", "Texto y fondos", "Text and backgrounds"),
            ("hielo", "#EEF1FF", "Hielo", "Ice", "Fondo", "Background")],
    display=("space-grotesk", 700), body=("inter", 400),
    roles={"p": "violeta", "a": "cian", "k": "noche", "a2": "violeta"}, inverse={"p": "violeta", "a": "cian", "k": "hielo", "a2": "cian"},
    base_bg="hielo", inverse_bg="noche",
    symbol=orbita_sym, wordmark=orbita_wm, sym_k=1.12, gap_k=0.22, vsym_k=1.0,
    logo_kind=L("Símbolo geométrico + logotipo", "Geometric symbol + wordmark"),
    mockups=["laptop", "app", "cards", "tshirt", "idbadge", "poster"],
)


# 23 · KAMBIO · fintech · tech ---------------------------------------------------
def arrow_arc(cx, cy, r, a0, a1, w, fill):
    p0, p1 = polar(cx, cy, r, a0), polar(cx, cy, r, a1)
    arc = f'<path d="M{n(p0[0])} {n(p0[1])} A{r} {r} 0 0 1 {n(p1[0])} {n(p1[1])}" fill="none" stroke="{fill}" stroke-width="{w}"/>'
    tip = polar(cx, cy, r, a1 + 24)
    b1, b2 = polar(cx, cy, r - w * 1.05, a1 - 1), polar(cx, cy, r + w * 1.05, a1 - 1)
    head = P(f"M{n(b1[0])} {n(b1[1])} L{n(tip[0])} {n(tip[1])} L{n(b2[0])} {n(b2[1])} Z", fill, ' stroke-linejoin="round"')
    return arc + head


def kambio_sym(c, mono):
    return Box(arrow_arc(50, 50, 36, 196, 318, 13, c["p"]) + arrow_arc(50, 50, 36, 16, 138, 13, c["a"]), Rect(0.5, 0.5, 99.5, 99.5))


def kambio_wm(c, mono, al="start"):
    if al == "center":
        return text("sora", 700, "kambio", 100, c["k"], tracking=-0.03)
    t = text("sora", 700, "kambio", 100, c["k"], tracking=-0.03, omit={5})
    s = t.slots[5]
    sym = kambio_sym(c, mono).fit(s.x0 - s.w * 0.12, s.y0 - s.h * 0.12, s.w * 1.24, s.h * 1.24)
    return t.add(sym.markup, sym.ink)


kambio = Brand(
    slug="kambio", name="Kambio", style="tech",
    sector=L("Billetera digital y pagos", "Digital wallet and payments"),
    concept=L("Dos flechas que se pasan el valor de una a otra: mandar y recibir plata sin enredos. Verde que da confianza con un lila amable.",
              "Two arrows passing value to each other: send and receive money without hassle. A trustworthy green with a friendly lilac."),
    tagline=L("Tu plata, sin enredos", "Your money, no hassle"),
    personality=L(["Simple", "Segura", "Ágil"], ["Simple", "Secure", "Agile"]),
    colors=[("verde", "#00B386", "Verde Kambio", "Kambio green", "Principal", "Primary"),
            ("lila", "#B9A6FF", "Lila", "Lilac", "Acento", "Accent"),
            ("negro", "#0F1514", "Negro", "Black", "Texto", "Text"),
            ("hueso", "#F6F7F5", "Blanco hueso", "Off-white", "Fondo", "Background")],
    display=("sora", 700), body=("figtree", 400),
    roles={"p": "verde", "a": "lila", "k": "negro"}, inverse={"p": "verde", "a": "lila", "k": "hueso"},
    base_bg="hueso", inverse_bg="negro",
    symbol=kambio_sym, wordmark=kambio_wm, sym_k=1.05, gap_k=0.22, vsym_k=1.3,
    horizontal_fn=lambda c, mono: kambio_wm(c, mono, "start"),
    logo_kind=L("Logotipo con símbolo integrado", "Wordmark with integrated symbol"),
    mockups=["app", "paycard", "laptop", "cards", "poster", "tote"],
)


# 24 · RUMBO · logistics · tech --------------------------------------------------
PIN = "M50 104 C40 90 8 70 8 42 A42 42 0 1 1 92 42 C92 70 60 90 50 104 Z"


def rumbo_sym(c, mono):
    arrow = S("M30 42 H64 M50 27 L66 42 L50 57", "#000", 10)
    return Box(knock(P(PIN, c["p"]), arrow), Rect(8, 0, 92, 104))


def rumbo_wm(c, mono, al="start"):
    if al == "center":
        main = text("archivo-black", 400, "RUMBO", 100, c["k"], tracking=0.04)
    else:
        main = text("archivo-black", 400, "RUMBO", 100, c["k"], tracking=0.04, omit={4})
        s = main.slots[4]
        h = s.h * 1.32
        pin = rumbo_sym(c, mono).fit((s.x0 + s.x1) / 2 - h * 0.42, s.y0 - s.h * 0.02, h * 0.84, h, valign="top")
        main = main.add(pin.markup, pin.ink)
    sub_ = justify("archivo", 700, "LOGÍSTICA Y ENVÍOS", 18, main.layout.w, c["a"])
    return word_block(main, sub_, 0.42, align="start" if al == "start" else "center")


rumbo = Brand(
    slug="rumbo", name="Rumbo Logística", style="tech",
    sector=L("Logística y envíos", "Logistics and deliveries"),
    concept=L("Un pin de ubicación con una flecha que avanza: cada envío sabe para dónde va. Naranja de alta visibilidad con azul acero.",
              "A location pin with a forward arrow: every package knows where it's going. High-visibility orange with steel blue."),
    tagline=L("Tu envío, en camino", "Your package, on its way"),
    personality=L(["Eficiente", "Puntual", "Confiable"], ["Efficient", "Punctual", "Reliable"]),
    colors=[("naranja", "#FF6A13", "Naranja ruta", "Route orange", "Principal", "Primary"),
            ("acero", "#15304B", "Azul acero", "Steel blue", "Texto", "Text"),
            ("asfalto", "#5B6670", "Asfalto", "Asphalt", "Apoyo", "Support"),
            ("blanco", "#F3F5F7", "Blanco", "White", "Fondo", "Background")],
    display=("archivo-black", 400), body=("archivo", 400),
    roles={"p": "naranja", "k": "acero", "a": "naranja"}, inverse={"p": "naranja", "k": "blanco", "a": "naranja"},
    base_bg="blanco", inverse_bg="acero",
    symbol=rumbo_sym, wordmark=rumbo_wm, sym_k=1.12, gap_k=0.22, vsym_k=1.1,
    horizontal_fn=lambda c, mono: rumbo_wm(c, mono, "start"),
    logo_kind=L("Logotipo pesado con símbolo integrado", "Heavy wordmark with integrated symbol"),
    mockups=["van", "box", "cap", "tshirt", "app", "cards"],
)

BRANDS = [pompon, paleton, navaja, paramo, tranvia, orbita, kambio, rumbo]

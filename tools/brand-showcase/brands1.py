"""Brands 1–8: minimal, professional and bold directions."""
import math

from lib import n

from model import *  # noqa: F403


def L(es, en):
    return {"es": es, "en": en}


# 1 · SERENO · skincare · minimal ------------------------------------------------
def sereno_sym(c, mono):
    m = P("M14 36 A36 36 0 0 1 86 36 Z", c["a"]) + lens(6, 94, 40.5, 3.6, c["k"])
    for dy, hw, th in ((8.5, 34.8, 3.2), (16.5, 31.6, 2.9), (24.5, 26.2, 2.6), (32, 17.5, 2.2)):
        m += lens(50 - hw, 50 + hw, 40 + dy, th, c["a"])
    return Box(m, Rect(6, 0, 94, 74.5))


def sereno_wm(c, mono, al="start"):
    if al == "center":
        return text("jost", 400, "sereno", 100, c["k"], tracking=0.1, box="x")
    t = text("jost", 400, "sereno", 100, c["k"], tracking=0.1, box="x", omit={5})
    s = t.slots[5]
    sun = sereno_sym(c, mono).height_to(s.h * 1.22).center_at((s.x0 + s.x1) / 2 + s.w * 0.08, (s.y0 + s.y1) / 2 + s.h * 0.08)
    return t.add(sun.markup, sun.ink)


sereno = Brand(
    slug="sereno", name="Sereno", style="minimal",
    sector=L("Cuidado de la piel", "Skincare"),
    concept=L("Un sol que aparece sobre el agua quieta: la calma de una rutina sencilla. Formas mínimas, mucho aire y colores de tierra suave.",
              "A sun rising over still water: the calm of a simple routine. Minimal shapes, plenty of air and soft earthy colors."),
    tagline=L("Piel en calma", "Calm skin"),
    personality=L(["Calma", "Natural", "Honesta"], ["Calm", "Natural", "Honest"]),
    colors=[("hueso", "#F4F0EA", "Hueso", "Bone", "Fondo", "Background"),
            ("arena", "#DCCFBE", "Arena", "Sand", "Apoyo", "Support"),
            ("salvia", "#8C9A84", "Salvia", "Sage", "Símbolo", "Symbol"),
            ("carbon", "#2E2E2C", "Carbón", "Charcoal", "Texto", "Text")],
    display=("jost", 400), body=("karla", 400),
    roles={"k": "carbon", "a": "salvia"}, inverse={"k": "hueso", "a": "arena"},
    base_bg="hueso", inverse_bg="carbon",
    symbol=sereno_sym, wordmark=sereno_wm, sym_k=1.75, gap_k=0.3, vsym_k=1.9,
    horizontal_fn=lambda c, mono: sereno_wm(c, mono, "start"),
    logo_kind=L("Logotipo con símbolo integrado", "Wordmark with integrated symbol"),
    mockups=["bottles", "box", "jar", "tote", "phone", "cards"],
)


# 2 · NIDO · architecture · minimal ---------------------------------------------
def nido_sym(c, mono):
    frame = P("M0 0 H60 L46 14 H14 V86 H86 V54 L100 40 V100 H0 Z", c["k"])
    egg = E(42, 60, 15, 19.5, c["a"], -16)
    return Box(frame + egg, Rect(0, 0, 100, 100))


def nido_wm(c, mono, al="start"):
    main = text("syncopate", 700, "NIDO", 100, c["k"], tracking=0.16)
    sub = justify("syncopate", 400, "ARQUITECTURA", 19, main.ink.w, c["k"])
    return word_block(main, sub, 0.34, align="start" if al == "start" else "center")


nido = Brand(
    slug="nido", name="Nido Arquitectura", style="minimal",
    sector=L("Estudio de arquitectura e interiores", "Architecture and interiors studio"),
    concept=L("Un marco abierto que protege un huevo: el espacio como nido. Geometría precisa con cortes en diagonal y una sola forma orgánica en barro.",
              "An open frame sheltering an egg: space as a nest. Precise geometry with diagonal cuts and a single organic shape in clay."),
    tagline=L("Espacios que abrazan", "Spaces that embrace"),
    personality=L(["Precisa", "Cálida", "Atemporal"], ["Precise", "Warm", "Timeless"]),
    colors=[("negro", "#141414", "Negro grafito", "Graphite black", "Principal", "Primary"),
            ("cal", "#F5F4F1", "Blanco cal", "Lime white", "Fondo", "Background"),
            ("concreto", "#CFCCC6", "Concreto", "Concrete", "Apoyo", "Support"),
            ("terracota", "#C0613B", "Terracota", "Terracotta", "Acento", "Accent")],
    display=("syncopate", 700), body=("work-sans", 400),
    roles={"k": "negro", "a": "terracota"}, inverse={"k": "cal", "a": "terracota"},
    base_bg="cal", inverse_bg="negro",
    symbol=nido_sym, wordmark=nido_wm, sym_k=1.0, gap_k=0.3, vsym_k=1.25,
    logo_kind=L("Símbolo geométrico + logotipo", "Geometric symbol + wordmark"),
    mockups=["cards", "laptop", "wallsign", "tote", "poster", "mug"],
)


# 3 · LINO · candles & home · minimal -------------------------------------------
def lino_sym(c, mono):
    p, a = c["p"], c["a"]
    frame = P("M0 100 V44 A44 44 0 0 1 88 44 V100 Z M9 91 H79 V44 A35 35 0 0 0 9 44 Z", p, ' fill-rule="evenodd"')
    flame_d = "M44 24 C52 36 57 44 57 52 A13 13 0 0 1 31 52 C31 44 36 36 44 24 Z"
    core = "M44 42 C48 48 50 51 50 55 A6 6 0 0 1 38 55 C38 51 40 48 44 42 Z"
    flame = knock(P(flame_d, a), P(core, "#000")) + ("" if mono else P(core, c.get("l", a)))
    candle = R(35, 70, 18, 21, p) + R(43, 64, 2, 7, p, 1)
    return Box(frame + flame + candle, Rect(0, 0, 88, 100))


def lino_wm(c, mono, al="start"):
    main = text("instrument-serif", 400, "Lino", 120, c["p"], swap={1: "dotlessi"})
    s = main.slots[1]
    cx = (s.x0 + s.x1) / 2
    h = main.metrics["cap"] * 0.34
    fl = P("M0 -100 C14 -78 22 -64 22 -48 A22 22 0 0 1 -22 -48 C-22 -64 -14 -78 0 -100 Z", c["a"])
    sc = h / 70
    flame = f'<g transform="translate({n(cx)} {n(s.y0 - h * 0.18)}) scale({n(sc)})">{fl}</g>'
    main = main.add(flame, Rect(cx - 22 * sc, s.y0 - h * 0.18 - 100 * sc, cx + 22 * sc, s.y0))
    sub_ = text("manrope", 600, "VELAS & HOGAR", 18, c["k"], tracking=0.32)
    return word_block(main, sub_, 0.26, align="start" if al == "start" else "center")


lino = Brand(
    slug="lino", name="Lino", style="minimal",
    sector=L("Velas aromáticas y textiles para el hogar", "Scented candles and home textiles"),
    concept=L("Una ventana en arco con una vela encendida: el rincón tranquilo de la casa. Serif delicada y tonos de rosa empolvado y ciruela.",
              "An arched window with a lit candle: the quiet corner of a home. A delicate serif with dusty rose and plum tones."),
    tagline=L("Luz para quedarse", "Light to stay in"),
    personality=L(["Íntima", "Delicada", "Acogedora"], ["Intimate", "Delicate", "Cozy"]),
    colors=[("cera", "#F6EFE7", "Cera", "Wax", "Fondo", "Background"),
            ("rosa", "#D9A9A0", "Rosa polvo", "Dusty rose", "Acento", "Accent"),
            ("ciruela", "#4B2A3F", "Ciruela", "Plum", "Principal", "Primary"),
            ("humo", "#8A8288", "Gris humo", "Smoke gray", "Texto secundario", "Secondary text")],
    display=("instrument-serif", 400), body=("manrope", 400),
    roles={"p": "ciruela", "a": "rosa", "k": "humo", "l": "cera"}, inverse={"p": "cera", "a": "rosa", "k": "rosa", "l": "ciruela"},
    base_bg="cera", inverse_bg="ciruela",
    symbol=lino_sym, wordmark=lino_wm, sym_k=1.0, gap_k=0.28, vsym_k=1.35,
    logo_kind=L("Símbolo + logotipo serif", "Symbol + serif wordmark"),
    mockups=["jar", "box", "hangtag", "bag", "phone", "cards"],
)


# 4 · CASTELAR · law firm · professional ----------------------------------------
def castelar_sym(c, mono):
    wedge = "M100 50 L62 22 L62 78 Z M120 0 L74 30 L74 70 L120 100 Z"
    ring = knock(C(50, 50, 50, c["a"]), C(57, 50, 38.5, "#000") + P("M58 50 L104 12 V88 Z", "#000"), -10, -10, 130, 130)
    p = c["p"]
    col = (R(35, 23, 30, 5, p, 1.5) + C(36.5, 30, 3.2, p) + C(63.5, 30, 3.2, p) + R(39, 29, 22, 3, p)
           + knock(P("M41 33 H59 L57.5 69 H42.5 Z", p), R(46.6, 36, 1.6, 30, "#000") + R(51.8, 36, 1.6, 30, "#000"))
           + R(38, 70, 24, 3.5, p, 1) + R(34, 74.5, 32, 4.5, p, 1.5))
    return Box(ring + col, Rect(0, 0, 100, 100))


def castelar_wm(c, mono, al="start"):
    main = text("libre-caslon-display", 400, "CASTELAR", 100, c["p"], tracking=0.1)
    sub = ruled(text("source-sans-3", 600, "ABOGADOS", 25, c["a"], tracking=0.55), main.ink.w, c["a"], 2)
    return word_block(main, sub, 0.32)


castelar = Brand(
    slug="castelar", name="Castelar Abogados", style="corporate",
    sector=L("Firma de abogados", "Law firm"),
    concept=L("Una columna clásica dentro de la C: solidez, estructura y confianza. Serif de tradición con azul noche y oro viejo.",
              "A classical column inside the C: solidity, structure and trust. A traditional serif with midnight blue and antique gold."),
    tagline=L("Firmeza en cada caso", "Steady in every case"),
    personality=L(["Confiable", "Sólida", "Discreta"], ["Trustworthy", "Solid", "Discreet"]),
    colors=[("noche", "#13233F", "Azul noche", "Midnight blue", "Principal", "Primary"),
            ("oro", "#B39158", "Oro viejo", "Antique gold", "Acento", "Accent"),
            ("marfil", "#F3EFE6", "Marfil", "Ivory", "Fondo", "Background"),
            ("pizarra", "#5A6272", "Pizarra", "Slate", "Texto", "Text")],
    display=("libre-caslon-display", 400), body=("source-sans-3", 400),
    roles={"p": "noche", "a": "oro"}, inverse={"p": "marfil", "a": "oro"},
    base_bg="marfil", inverse_bg="noche",
    symbol=castelar_sym, wordmark=castelar_wm, sym_k=1.22, gap_k=0.3, vsym_k=1.2,
    logo_kind=L("Monograma + logotipo serif", "Monogram + serif wordmark"),
    mockups=["cards", "wallsign", "laptop", "idbadge", "mug", "phone"],
)


# 5 · BALANCE · accounting · professional ---------------------------------------
def balance_sym(c, mono):
    top = P("M11 0 H84 L71 22 H11 A11 11 0 0 1 11 0 Z", c["p"])
    bot = P("M29 42 H89 A11 11 0 0 1 89 64 H16 Z", c["a"])
    fold = "" if mono else P("M71 22 L84 0 L84 14 Z", c["k"]) + P("M29 42 L16 64 L16 50 Z", c["k"])
    return Box(top + bot + fold, Rect(0, 0, 100, 64))


def balance_wm(c, mono, al="start"):
    main = text("ibm-plex-sans", 600, "balance", 100, c["k"], tracking=-0.01)
    sub = justify("ibm-plex-mono", 500, "CONSULTORÍA CONTABLE", 18, main.ink.w, c["p"])
    return word_block(main, sub, 0.3, align="start" if al == "start" else "center")


balance = Brand(
    slug="balance", name="Balance", style="corporate",
    sector=L("Consultoría contable y financiera", "Accounting and financial consulting"),
    concept=L("Dos barras que se equilibran, como un signo igual en movimiento: cuentas claras que avanzan. Sans técnica con detalles monoespaciados.",
              "Two balancing bars, like an equals sign in motion: clear accounts moving forward. A technical sans with monospaced details."),
    tagline=L("Cuentas claras, decisiones firmes", "Clear numbers, confident decisions"),
    personality=L(["Clara", "Ordenada", "Cercana"], ["Clear", "Orderly", "Approachable"]),
    colors=[("petroleo", "#0E4D5A", "Petróleo", "Petrol", "Principal", "Primary"),
            ("menta", "#4FB39A", "Menta", "Mint", "Acento", "Accent"),
            ("niebla", "#EAF1F1", "Niebla", "Mist", "Fondo", "Background"),
            ("grafito", "#23323A", "Grafito", "Graphite", "Texto", "Text")],
    display=("ibm-plex-sans", 600), body=("ibm-plex-mono", 400),
    roles={"p": "petroleo", "a": "menta", "k": "grafito"}, inverse={"p": "niebla", "a": "menta", "k": "niebla"},
    base_bg="niebla", inverse_bg="petroleo",
    symbol=balance_sym, wordmark=balance_wm, sym_k=0.82, gap_k=0.34, vsym_k=0.9,
    logo_kind=L("Símbolo abstracto + logotipo", "Abstract symbol + wordmark"),
    mockups=["cards", "laptop", "idbadge", "wallsign", "mug", "app"],
)


# 6 · ARCO · dental clinic · professional ---------------------------------------
TOOTH = ("M18 8 C30 0 40 6 50 10 C60 6 70 0 82 8 C96 18 94 42 88 56 C84 68 82 84 76 94 C72 100 66 98 64 90 "
         "L58 70 C56 62 44 62 42 70 L36 90 C34 98 28 100 24 94 C18 84 16 68 12 56 C6 42 4 18 18 8 Z")


def sparkle(cx, cy, r, fill):
    k = r * 0.28
    return P(f"M{n(cx)} {n(cy - r)} C{n(cx + k * 0.3)} {n(cy - k)} {n(cx + k)} {n(cy - k * 0.3)} {n(cx + r)} {n(cy)} "
             f"C{n(cx + k)} {n(cy + k * 0.3)} {n(cx + k * 0.3)} {n(cy + k)} {n(cx)} {n(cy + r)} "
             f"C{n(cx - k * 0.3)} {n(cy + k)} {n(cx - k)} {n(cy + k * 0.3)} {n(cx - r)} {n(cy)} "
             f"C{n(cx - k)} {n(cy - k * 0.3)} {n(cx - k * 0.3)} {n(cy - k)} {n(cx)} {n(cy - r)} Z", fill)


def arco_sym(c, mono):
    tooth = knock(P(TOOTH, c["p"]), S("M27 33 Q50 54 73 33", "#000", 8))
    return Box(tooth + sparkle(98, 4, 11, c["a"]) + sparkle(110, 22, 5.5, c["a"]), Rect(4.9, -7, 115.5, 99.5))


def arco_wm(c, mono, al="start"):
    main = text("plus-jakarta-sans", 800, "arco", 100, c["p"], tracking=-0.02, box="x")
    sub = justify("plus-jakarta-sans", 600, "ODONTOLOGÍA", 15, main.ink.w, c["k"])
    return word_block(main, sub, 0.42, align="start" if al == "start" else "center")


arco = Brand(
    slug="arco", name="Arco Odontología", style="corporate",
    sector=L("Clínica odontológica", "Dental clinic"),
    concept=L("Un diente dibujado como un arco con una sonrisa: tecnología amable y cercana. Azul clínico con un destello aguamarina.",
              "A tooth drawn as an arch with a smile: friendly, approachable care. Clinical blue with an aqua sparkle."),
    tagline=L("Sonríe con confianza", "Smile with confidence"),
    personality=L(["Amable", "Limpia", "Profesional"], ["Friendly", "Clean", "Professional"]),
    colors=[("azul", "#1C5DB0", "Azul clínico", "Clinical blue", "Principal", "Primary"),
            ("aqua", "#35C2C9", "Aguamarina", "Aquamarine", "Acento", "Accent"),
            ("nube", "#F4F9FC", "Blanco nube", "Cloud white", "Fondo", "Background"),
            ("pizarra", "#2B3443", "Pizarra", "Slate", "Texto", "Text")],
    display=("plus-jakarta-sans", 800), body=("nunito-sans", 400),
    roles={"p": "azul", "a": "aqua", "k": "pizarra"}, inverse={"p": "nube", "a": "aqua", "k": "nube"},
    base_bg="nube", inverse_bg="azul",
    symbol=arco_sym, wordmark=arco_wm, sym_k=1.0, gap_k=0.28, vsym_k=1.1,
    logo_kind=L("Símbolo + logotipo redondeado", "Symbol + rounded wordmark"),
    mockups=["cards", "tshirt", "wallsign", "app", "idbadge", "mug"],
)


# 7 · BRASA BRAVA · burgers · bold ----------------------------------------------
FLAME_OUT = ("M40 0 C48 18 70 30 72 58 C74 84 58 100 40 100 C20 100 6 86 8 64 C9 50 16 42 22 34 "
             "C24 46 28 52 34 54 C30 36 32 16 40 0 Z")
FLAME_IN = "M41 48 C47 60 56 66 56 79 C56 90 49 96 40.5 96 C31.5 96 25 90 26 81 C27 72 33 67 35 59 C37 64 39 66 41 66 C40 60 39.5 54 41 48 Z"


FLAME_MID = "M40 22 C46 36 62 46 62 66 C62 86 52 97 40 97 C26 97 15 87 16 70 C17 58 23 52 27 46 C29 54 32 58 36 59 C34 46 35 34 40 22 Z"


def brasa_sym(c, mono):
    if mono:
        return Box(knock(P(FLAME_OUT, c["p"]), P(FLAME_IN, "#000")), Rect(7.9, 0, 72.1, 100))
    return Box(P(FLAME_OUT, c["p"]) + P(FLAME_MID, c["o"]) + P(FLAME_IN, c["a"]), Rect(7.9, 0, 72.1, 100))


def brasa_emblem(c, mono):
    from lib import arc_text
    cuts = (P("M100 9 A91 91 0 1 1 99.99 9 Z M100 14 A86 86 0 1 0 100.01 14 Z", "#000", ' fill-rule="evenodd"')
            + arc_text("anton", 400, "BRASA BRAVA", 34, 100, 100, 60, "#000", tracking=0.06, where="top")
            + arc_text("barlow", 700, "HAMBURGUESAS AL CARBÓN", 13.5, 100, 100, 74, "#000", tracking=0.16, where="bottom"))
    disk = knock(C(100, 100, 98, c["k"]), cuts, -10, -10, 220, 220)
    fl = brasa_sym(c, mono).fit(70, 62, 60, 82)
    return Box(disk + fl.markup, Rect(2, 2, 198, 198))


def brasa_wm(c, mono, al="start"):
    a = text("anton", 400, "BRASA", 100, c["k"], tracking=0.03)
    b = text("anton", 400, "BRAVA", 100, c["p"], tracking=0.03)
    w = max(a.ink.w, b.ink.w)
    sub = justify("barlow", 700, "HAMBURGUESAS AL CARBÓN", 16, w, c["k"])
    return vstack([a, b, sub], gap=[a.h * 0.13, a.h * 0.2], align="start" if al == "start" else "center")


brasa = Brand(
    slug="brasa-brava", name="Brasa Brava", style="bold",
    sector=L("Hamburguesas a la parrilla", "Flame-grilled burgers"),
    concept=L("Una llama con carácter y letras condensadas que gritan sabor: hecha para verse desde la calle. Rojo brasa, mostaza y carbón.",
              "A flame with attitude and condensed letters that shout flavor: built to be seen from the street. Ember red, mustard and charcoal."),
    tagline=L("Al carbón y sin miedo", "Charcoal-grilled, no fear"),
    personality=L(["Audaz", "Callejera", "Apetitosa"], ["Bold", "Streetwise", "Appetizing"]),
    colors=[("rojo", "#E1341E", "Rojo brasa", "Ember red", "Principal", "Primary"),
            ("mostaza", "#FFC12E", "Mostaza", "Mustard", "Acento", "Accent"),
            ("naranja", "#F57A1F", "Naranja fuego", "Fire orange", "Volumen de la llama", "Flame depth"),
            ("carbon", "#1B1615", "Carbón", "Charcoal", "Texto", "Text"),
            ("crema", "#FFF3E2", "Crema", "Cream", "Fondo", "Background")],
    display=("anton", 400), body=("barlow", 400),
    roles={"p": "rojo", "a": "mostaza", "k": "carbon", "o": "naranja"}, inverse={"p": "rojo", "a": "mostaza", "k": "crema", "o": "naranja"},
    base_bg="crema", inverse_bg="carbon",
    symbol=brasa_sym, wordmark=brasa_wm, sym_k=0.95, gap_k=0.22, vsym_k=0.8, emblem=brasa_emblem,
    logo_kind=L("Símbolo + logotipo condensado", "Symbol + condensed wordmark"),
    mockups=["box", "bag", "cup", "apron", "storefront", "tshirt"],
)


# 8 · VOLTIO · energy drink · bold ----------------------------------------------
BOLT = "M60 8 L26 58 H47 L40 92 L74 40 H53 Z"


def voltio_sym(c, mono):
    return Box(knock(C(50, 50, 50, c["a"]), P(BOLT, "#000")), Rect(0, 0, 100, 100))


def voltio_disc_speed(c, mono):
    lines = lens(-62, -8, 34, 3.2, c["a"]) + lens(-84, -10, 50, 3.6, c["a"]) + lens(-56, -8, 66, 3.2, c["a"])
    return Box(lines + knock(C(50, 50, 50, c["a"]), P(BOLT, "#000")), Rect(-84, 0, 100, 100))


def voltio_wm(c, mono, al="start"):
    if al == "center":
        main = text("unbounded", 800, "VOLTIO", 100, c["k"], tracking=0.01, skew=12)
    else:
        main = text("unbounded", 800, "VOLTIO", 100, c["k"], tracking=0.01, skew=12, omit={5})
        s = main.slots[5]
        d = voltio_sym(c, mono).fit(s.x0 - s.w * 0.02, s.y0 - s.h * 0.04, s.w * 1.08, s.h * 1.08)
        main = main.add(d.markup, d.ink)
    sub_ = text("rubik", 700, "BEBIDA ENERGÉTICA", 19, c["s"], tracking=0.34)
    return word_block(main, sub_, 0.3, align="start" if al == "start" else "center")


voltio = Brand(
    slug="voltio", name="Voltio", style="bold",
    sector=L("Bebida energética", "Energy drink"),
    concept=L("Un rayo que atraviesa un círculo de luz y letras inclinadas que van hacia adelante. Negro absoluto con lima eléctrica.",
              "A bolt cutting through a disc of light and forward-leaning letters. Absolute black with electric lime."),
    tagline=L("Energía que se nota", "Energy you can feel"),
    personality=L(["Intensa", "Rápida", "Joven"], ["Intense", "Fast", "Young"]),
    colors=[("negro", "#0D0D0F", "Negro total", "Total black", "Fondo principal", "Main background"),
            ("lima", "#C8FF1F", "Lima eléctrica", "Electric lime", "Principal", "Primary"),
            ("naranja", "#FF5B1F", "Naranja voltaje", "Voltage orange", "Sabores y avisos", "Flavors and callouts"),
            ("blanco", "#F5F5F7", "Blanco", "White", "Texto", "Text")],
    display=("unbounded", 800), body=("rubik", 400),
    roles={"a": "lima", "k": "blanco", "s": "lima"}, inverse={"a": "negro", "k": "negro", "s": "naranja"},
    base_bg="negro", inverse_bg="blanco",
    symbol=voltio_sym, wordmark=voltio_wm, sym_k=1.0, gap_k=0.26, vsym_k=1.2,
    horizontal_fn=lambda c, mono: voltio_wm(c, mono, "start"),
    logo_kind=L("Logotipo itálico con símbolo integrado", "Italic wordmark with integrated symbol"),
    mockups=["can", "poster", "tshirt", "cap", "phone", "tote"],
)

BRANDS = [sereno, nido, lino, castelar, balance, arco, brasa, voltio]

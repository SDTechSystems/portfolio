"""Brands 25–36: luxury collection — interlaced monograms, fine-line emblems and script signatures."""
from lib import Rect, n
from model import Box, Brand, ruled, text, vstack
from ornaments import (at, pair, crown, dot_ring, flourish, glyph, laurel, leaf, letter, line, mirror, outline, over, rays,
                       ring, sparkle, ticks, weave)
from model import knock


def L(es, en):
    return {"es": es, "en": en}


def gb(g, cx, cy, s=1.0):
    r = g[1]
    w, h = r.w * s, r.h * s
    return Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


def ellipse_line(cx, cy, rx, ry, color, w):
    return f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}" fill="none" stroke="{color}" stroke-width="{n(w)}"/>'


def wm(al, *parts, gaps=None):
    a = "start" if al == "start" else "center"
    return vstack(list(parts), gap=gaps or [18] * (len(parts) - 1), align=a)


def caps(s, size, fill, font=("montserrat", 500), tr=0.5):
    return text(font[0], font[1], s, size, fill, tracking=tr)


def lux(slug, name, sector, concept, tagline, personality, colors, display, body, symbol, wordmark, mockups, kind,
        sym_k=1.35, vsym_k=1.9, gap_k=0.26, light=False, dark="dark", gold="gold", soft="soft", base=None):
    """Luxury brands: gold on a deep color by default; light-based ones flip the roles."""
    if light:
        roles = {"g": dark, "s": gold}
        inverse = {"g": soft, "s": gold}
        base_bg, inv_bg = base or soft, dark
    else:
        roles = {"g": gold, "s": soft}
        inverse = {"g": dark, "s": gold}
        base_bg, inv_bg = dark, soft
    return Brand(slug=slug, name=name, style="luxe", sector=sector, concept=concept, tagline=tagline, personality=personality,
                 colors=colors, display=display, body=body, roles=roles, inverse=inverse, base_bg=base_bg, inverse_bg=inv_bg,
                 symbol=symbol, wordmark=wordmark, mockups=mockups, logo_kind=kind, sym_k=sym_k, vsym_k=vsym_k, gap_k=gap_k,
                 notes={"foil": next(h for k, h, *_ in colors if k == gold)})


# 25 · AURELIA · hotel & spa ------------------------------------------------------
def aurelia_sym(c, mono):
    g = c["g"]
    A = glyph("cormorant-garamond", 500, "A", 112)
    lau = laurel(100, 100, 73, g, start=102, end=222, count=8, size=15)
    m = ring(100, 100, 92, 1.8, g) + ring(100, 100, 86.5, 0.8, g) + lau + mirror(lau, 100)
    m += letter(A, at(A, 100, 106), g) + sparkle(100, 40, 9, g)
    return Box(m, Rect(7, 7, 193, 193))


def aurelia_wm(c, mono, al="start"):
    main = text("cinzel", 400, "AURELIA", 72, c["g"], tracking=0.3)
    sub = ruled(caps("HOTEL & SPA", 15, c["s"], tr=0.6), main.ink.w, c["s"], 1.2)
    return wm(al, main, sub, gaps=[20])


aurelia = lux(
    "aurelia", "Aurelia Hotel & Spa", L("Hotel boutique y spa", "Boutique hotel and spa"),
    L("Una A clásica coronada por laureles y una estrella: descanso con categoría. Oro sobre verde esmeralda, con letras romanas de gran espacio.",
      "A classical A crowned with laurels and a star: rest with distinction. Gold on emerald green, with widely spaced Roman capitals."),
    L("Donde el tiempo descansa", "Where time slows down"), L(["Serena", "Distinguida", "Cálida"], ["Serene", "Distinguished", "Warm"]),
    [("dark", "#0F3B32", "Verde esmeralda", "Emerald green", "Fondo principal", "Main background"),
     ("gold", "#C9A45C", "Oro", "Gold", "Logo y detalles", "Logo and details"),
     ("soft", "#F3EDE1", "Marfil", "Ivory", "Fondo claro", "Light background"),
     ("sage", "#8FA89A", "Salvia", "Sage", "Apoyo", "Support")],
    ("cinzel", 400), ("montserrat", 400), aurelia_sym, aurelia_wm,
    ["cards", "bottles", "wallsign", "menu", "bag", "mug"], L("Emblema con monograma y laureles", "Monogram emblem with laurels"),
    sym_k=1.5, vsym_k=2.1)


# 26 · MAISON VELOUR · perfumery ---------------------------------------------------
def velour_sym(c, mono):
    g = c["g"]
    M = glyph("bodoni-moda", 500, "M", 50)
    V = glyph("bodoni-moda", 500, "V", 50)
    mono_ = pair(M, V, 100, 118, 4, g, g)
    arch = line("M44 182 V88 A56 56 0 0 1 156 88 V182 Z", g, 2) + line("M51 175 V89 A49 49 0 0 1 149 89 V175 Z", g, 0.8)
    return Box(arch + mono_ + sparkle(100, 52, 7, g), Rect(43, 31, 157, 183))


def velour_wm(c, mono, al="start"):
    top = caps("MAISON", 16, c["s"], tr=0.95)
    main = text("bodoni-moda", 500, "VELOUR", 78, c["g"], tracking=0.22)
    sub = caps("PERFUMERÍA DE AUTOR", 13, c["s"], tr=0.5)
    return wm(al, top, main, sub, gaps=[16, 20])


velour = lux(
    "maison-velour", "Maison Velour", L("Perfumería de autor", "Niche perfumery"),
    L("Una M y una V que se entrelazan como dos notas de un mismo perfume, dentro de un arco de boutique parisina. Burdeos y oro rosa.",
      "An M and a V woven together like two notes of one scent, inside a Parisian boutique arch. Burgundy and rose gold."),
    L("Un aroma que te nombra", "A scent that speaks your name"), L(["Sensual", "Exclusiva", "Íntima"], ["Sensual", "Exclusive", "Intimate"]),
    [("dark", "#5A1428", "Burdeos", "Burgundy", "Fondo principal", "Main background"),
     ("gold", "#D4A373", "Oro rosa", "Rose gold", "Logo y detalles", "Logo and details"),
     ("soft", "#F5EBE0", "Crema", "Cream", "Fondo claro", "Light background"),
     ("mauve", "#A26769", "Malva", "Mauve", "Apoyo", "Support")],
    ("bodoni-moda", 500), ("montserrat", 400), velour_sym, velour_wm,
    ["bottles", "box", "bag", "cards", "phone", "poster"], L("Monograma entrelazado en arco", "Interlaced monogram in an arch"),
    sym_k=1.25, vsym_k=1.5)


# 27 · LUDOVICA · bridal atelier ---------------------------------------------------
def sprig(cx, cy, color, flip=1):
    m = line(f"M{cx} {cy} C{cx - 14 * flip} {cy - 4} {cx - 28 * flip} {cy - 14} {cx - 36 * flip} {cy - 30}", color, 1.3)
    for t, (dx, dy, a) in enumerate(((-12, -4, -70), (-22, -11, -55), (-30, -21, -40), (-36, -31, -20))):
        m += leaf(cx + dx * flip, cy + dy, 9 - t, 3.6 - t * 0.4, a * flip + (180 if t % 2 else 0) * 0, color)
    return m


def ludovica_sym(c, mono):
    g = c["g"]
    Lg = glyph("great-vibes", 400, "L", 96)
    m = ellipse_line(100, 100, 56, 76, g, 1.8) + ellipse_line(100, 100, 50.5, 70.5, g, 0.8)
    m += letter(Lg, at(Lg, 102, 100), g)
    m += sprig(100, 182, g, 1) + sprig(100, 182, g, -1) + sparkle(100, 14, 6, g)
    return Box(m, Rect(43, 7, 157, 184))


def ludovica_wm(c, mono, al="start"):
    main = text("pinyon-script", 400, "Ludovica", 112, c["g"], box="ink")
    sub = caps("ATELIER DE NOVIAS", 17, c["s"], font=("cormorant-garamond", 600), tr=0.55)
    return wm(al, main, sub, gaps=[14])


ludovica = lux(
    "ludovica", "Ludovica", L("Atelier de vestidos de novia", "Bridal gown atelier"),
    L("Una L caligráfica dentro de un medallón, con ramitas como de un ramo de novia y una firma escrita a mano. Ciruela suave y oro sobre rubor.",
      "A calligraphic L in a medallion, with sprigs like a bridal bouquet and a handwritten signature. Soft plum and gold on blush."),
    L("Tu historia, a la medida", "Your story, made to measure"), L(["Romántica", "Delicada", "Atemporal"], ["Romantic", "Delicate", "Timeless"]),
    [("soft", "#EAD7D1", "Rubor", "Blush", "Fondo principal", "Main background"),
     ("dark", "#6B4E5A", "Ciruela suave", "Soft plum", "Logo y textos", "Logo and text"),
     ("gold", "#9A7A45", "Oro", "Gold", "Detalles", "Details"),
     ("pearl", "#FBF7F4", "Perla", "Pearl", "Papelería", "Stationery")],
    ("pinyon-script", 400), ("cormorant-garamond", 500), ludovica_sym, ludovica_wm,
    ["hangtag", "bag", "box", "cards", "phone", "poster"], L("Medallón caligráfico + firma", "Calligraphic medallion + signature"),
    sym_k=1.2, vsym_k=1.25, light=True)


# 28 · ORVIETO · wine bar ----------------------------------------------------------
def orvieto_sym(c, mono):
    g = c["g"]
    O = glyph("cinzel", 500, "O", 84)
    t = at(O, 100, 122)
    frame = line("M100 6 L194 100 L100 194 L6 100 Z", g, 2) + line("M100 17 L183 100 L100 183 L17 100 Z", g, 0.9)
    burst = knock(rays(100, 122, 36, 70, -156, -24, 15, 3.4, g), outline(O, t, 10))
    return Box(frame + burst + letter(O, t, g) + line("M66 168 H134", g, 1.2) + C_(100, 168, 2.6, g), Rect(5, 5, 195, 195))


def C_(cx, cy, r, fill):
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{fill}"/>'


def orvieto_wm(c, mono, al="start"):
    main = text("cinzel", 500, "ORVIETO", 70, c["g"], tracking=0.3)
    sub = ruled(caps("VINOTECA & COCINA", 14, c["s"], tr=0.5), main.ink.w, c["s"], 1.2)
    return wm(al, main, sub, gaps=[20])


orvieto = lux(
    "orvieto", "Orvieto", L("Vinoteca y cocina italiana", "Wine bar and Italian kitchen"),
    L("Un sol art déco que nace detrás de la O, dentro de un rombo de doble línea: noches largas, copas finas. Oro sobre negro con un toque vino.",
      "An art deco sun rising behind the O, inside a double-line diamond: long evenings, fine glasses. Gold on black with a touch of wine."),
    L("Brindemos sin prisa", "A toast, unhurried"), L(["Sofisticada", "Nocturna", "Generosa"], ["Sophisticated", "Nocturnal", "Generous"]),
    [("dark", "#141414", "Negro", "Black", "Fondo principal", "Main background"),
     ("gold", "#CDA349", "Oro antiguo", "Antique gold", "Logo y detalles", "Logo and details"),
     ("wine", "#6E1E2B", "Vino", "Wine", "Acento", "Accent"),
     ("soft", "#EFE6D2", "Hueso", "Bone", "Fondo claro", "Light background")],
    ("cinzel", 500), ("montserrat", 400), orvieto_sym, orvieto_wm,
    ["bottle", "menu", "storefront", "cards", "wallsign", "bag"], L("Emblema art déco", "Art deco emblem"), sym_k=1.45, vsym_k=2.0)


# 29 · ALTAMAR · yacht club --------------------------------------------------------
def altamar_sym(c, mono):
    g = c["g"]
    a = (ring(100, 44, 9, 4, g) + line("M100 53 V158", g, 4.2) + line("M76 72 H124", g, 4) + C_(73, 72, 3.6, g) + C_(127, 72, 3.6, g)
         + line("M56 120 Q62 154 100 160 Q138 154 144 120", g, 4) + line("M47 131 L56 115 L67 127", g, 4) + line("M133 127 L144 115 L153 131", g, 4))
    m = ring(100, 100, 82, 1.8, g) + dot_ring(100, 100, 91, 44, 2.3, g) + a
    return Box(m, Rect(6.7, 6.7, 193.3, 193.3))


def altamar_wm(c, mono, al="start"):
    main = text("marcellus", 400, "ALTAMAR", 78, c["g"], tracking=0.28)
    sub = caps("CLUB NÁUTICO", 15, c["s"], tr=0.75)
    return wm(al, main, sub, gaps=[18])


altamar = lux(
    "altamar", "Altamar Club Náutico", L("Club náutico y alquiler de veleros", "Yacht club and sailboat charters"),
    L("Un ancla de línea fina rodeada por un cordón de cuentas, como un sello marinero bordado. Oro sobre azul marino profundo.",
      "A fine-line anchor encircled by a beaded cord, like an embroidered sailor's crest. Gold on deep navy."),
    L("El mar, a tu manera", "The sea, your way"), L(["Clásica", "Aventurera", "Exclusiva"], ["Classic", "Adventurous", "Exclusive"]),
    [("dark", "#0E2340", "Azul marino", "Navy", "Fondo principal", "Main background"),
     ("gold", "#C8A55F", "Oro", "Gold", "Logo y detalles", "Logo and details"),
     ("soft", "#F4EFE6", "Arena blanca", "White sand", "Fondo claro", "Light background"),
     ("teal", "#2E6F73", "Verde mar", "Sea green", "Apoyo", "Support")],
    ("marcellus", 400), ("montserrat", 400), altamar_sym, altamar_wm,
    ["cap", "tshirt", "cards", "wallsign", "tote", "phone"], L("Emblema marinero", "Nautical crest"), sym_k=1.45, vsym_k=2.0)


# 30 · SABLE & CO. · tailoring -----------------------------------------------------
def sable_sym(c, mono):
    g = c["g"]
    S = glyph("bodoni-moda", 500, "S", 96)
    Cc = glyph("bodoni-moda", 500, "C", 96)
    letters = pair(S, Cc, 104, 104, 6, g, g)
    # the needle lies under the letters like a tailor's rule, its thread curling back: nothing crosses the monogram
    needle = line("M40 158 L168 158", g, 1.8) + f'<ellipse cx="162" cy="158" rx="5.5" ry="2.2" fill="none" stroke="{g}" stroke-width="1.2"/>'
    thread = line("M162 158 C184 158 188 176 166 180 C140 184 112 172 92 178", g, 1.1)
    return Box(letters + needle + thread, Rect(38, 50, 186, 182))


def sable_wm(c, mono, al="start"):
    main = text("forum", 400, "SABLE & CO.", 76, c["g"], tracking=0.14)
    sub = caps("SASTRERÍA A LA MEDIDA", 13, c["s"], tr=0.55)
    return wm(al, main, sub, gaps=[18])


sable = lux(
    "sable-co", "Sable & Co.", L("Sastrería a la medida", "Bespoke tailoring"),
    L("Una S y una C de alto contraste que se entrelazan, subrayadas por una aguja con su hilo: el oficio a la vista. Carbón, hueso y oro viejo.",
      "A high-contrast S and C woven together, underlined by a threaded needle: craft in plain sight. Charcoal, bone and antique gold."),
    L("Hecho para ti, a mano", "Made for you, by hand"), L(["Precisa", "Clásica", "Masculina"], ["Precise", "Classic", "Masculine"]),
    [("dark", "#1F1F22", "Carbón", "Charcoal", "Fondo principal", "Main background"),
     ("gold", "#B08D57", "Oro viejo", "Antique gold", "Logo y detalles", "Logo and details"),
     ("soft", "#EDE6DA", "Hueso", "Bone", "Fondo claro", "Light background"),
     ("gray", "#7A7A80", "Gris paño", "Cloth gray", "Apoyo", "Support")],
    ("forum", 400), ("montserrat", 400), sable_sym, sable_wm,
    ["hangtag", "box", "bag", "cards", "storefront", "phone"], L("Monograma con aguja", "Monogram with needle"), sym_k=1.35, vsym_k=1.7)


# 31 · VILLA SERENA · luxury real estate --------------------------------------------
def villa_sym(c, mono):
    g, s = c["g"], c["s"]
    V = glyph("cormorant-garamond", 500, "V", 150)
    S = glyph("cormorant-garamond", 500, "S", 46, italic=True)
    tv, ts = at(V, 100, 112), at(S, 101, 82)
    roof = line("M54 44 L100 16 L146 44", g, 2.2) + line("M128 33 V22 H136 V38", g, 2)
    body = letter(V, tv, g) + letter(S, ts, s)
    r = gb(V, 100, 112).union(Rect(53, 15, 147, 45))
    return Box(roof + body, r)


def villa_wm(c, mono, al="start"):
    main = text("tenor-sans", 400, "VILLA SERENA", 58, c["g"], tracking=0.3)
    sub = caps("PROPIEDADES EXCLUSIVAS", 13, c["s"], tr=0.55)
    return wm(al, main, sub, gaps=[18])


villa = lux(
    "villa-serena", "Villa Serena", L("Inmobiliaria de propiedades exclusivas", "Luxury real estate"),
    L("Una V y una S que forman una casa bajo un tejado de dos aguas: el monograma como hogar. Azul pizarra y bronce sobre arena.",
      "A V and an S that form a house under a gabled roof: the monogram as a home. Slate blue and bronze on sand."),
    L("Vivir en otro nivel", "Living on another level"), L(["Confiable", "Exclusiva", "Sobria"], ["Trustworthy", "Exclusive", "Understated"]),
    [("soft", "#E9E2D6", "Arena", "Sand", "Fondo principal", "Main background"),
     ("dark", "#2F3E4E", "Azul pizarra", "Slate blue", "Logo y textos", "Logo and text"),
     ("gold", "#86683F", "Bronce", "Bronze", "Detalles", "Details"),
     ("white", "#FAF8F4", "Blanco cal", "Lime white", "Papelería", "Stationery")],
    ("tenor-sans", 400), ("montserrat", 400), villa_sym, villa_wm,
    ["cards", "wallsign", "laptop", "poster", "idbadge", "mug"], L("Monograma arquitectónico", "Architectural monogram"),
    sym_k=2.2, vsym_k=2.1, light=True)


# 32 · ALMA BOTÁNICA · luxury skincare ---------------------------------------------
def alma_sym(c, mono):
    g = c["g"]
    m = ellipse_line(100, 100, 54, 80, g, 1.8) + ellipse_line(100, 100, 49, 75, g, 0.7)
    m += line("M100 166 C93 130 107 82 100 36", g, 2)
    for y, side, size in ((150, -1, 22), (134, 1, 24), (117, -1, 25), (100, 1, 25), (83, -1, 23), (67, 1, 20), (52, -1, 16)):
        m += leaf(100 + side * 11.5, y - 4, size, size * 0.42, side * 52, g)
    m += leaf(100, 31, 13, 5.5, 0, g)
    return Box(m, Rect(45, 19, 155, 181))


def alma_wm(c, mono, al="start"):
    main = text("parisienne", 400, "Alma", 104, c["g"], box="ink")
    sub = text("tenor-sans", 400, "BOTÁNICA", 26, c["s"], tracking=0.62)
    return wm(al, main, sub, gaps=[12])


alma = lux(
    "alma-botanica", "Alma Botánica", L("Cuidado de la piel con ingredientes botánicos", "Botanical skincare"),
    L("Una rama dibujada con pulso fino dentro de un óvalo, y un nombre que combina caligrafía con mayúsculas espaciadas. Salvia profunda y oro.",
      "A finely drawn branch inside an oval, and a name that pairs calligraphy with spaced capitals. Deep sage and gold."),
    L("Tu ritual, tu calma", "Your ritual, your calm"), L(["Natural", "Refinada", "Serena"], ["Natural", "Refined", "Serene"]),
    [("dark", "#3E4F44", "Salvia profunda", "Deep sage", "Fondo principal", "Main background"),
     ("gold", "#C5A46D", "Oro suave", "Soft gold", "Logo y detalles", "Logo and details"),
     ("soft", "#F2EDE3", "Crema", "Cream", "Fondo claro", "Light background"),
     ("clay", "#C98B6B", "Arcilla", "Clay", "Acento", "Accent")],
    ("parisienne", 400), ("tenor-sans", 400), alma_sym, alma_wm,
    ["bottles", "jar", "box", "bag", "cards", "phone"], L("Emblema botánico + firma", "Botanical emblem + signature"),
    sym_k=1.45, vsym_k=1.4)


# 33 · CASA DUVALL · family winery -------------------------------------------------
def duvall_sym(c, mono):
    g = c["g"]
    Cg = glyph("cinzel", 500, "C", 44)
    Dg = glyph("cinzel", 500, "D", 44)
    shield = line("M58 64 H142 V112 Q142 150 100 172 Q58 150 58 112 Z", g, 2) + line("M64 70 H136 V112 Q136 145 100 165 Q64 145 64 112 Z", g, 0.8)
    mono_ = pair(Cg, Dg, 100, 110, 3, g, g)
    return Box(shield + mono_ + crown(100, 54, 52, g, 2) + flourish(100, 184, 112, g), Rect(42, 21, 158, 198))


def duvall_wm(c, mono, al="start"):
    top = caps("CASA", 16, c["s"], tr=0.95)
    main = text("cinzel", 500, "DUVALL", 78, c["g"], tracking=0.24)
    sub = ruled(caps("BODEGA FAMILIAR", 13, c["s"], tr=0.5), main.ink.w, c["s"], 1.2)
    return wm(al, top, main, sub, gaps=[16, 20])


duvall = lux(
    "casa-duvall", "Casa Duvall", L("Bodega de vinos familiar", "Family winery"),
    L("Un escudo con corona y un monograma CD entrelazado, rematado por arabescos: tradición que se hereda. Oro sobre burdeos.",
      "A crowned shield with an interlaced CD monogram, finished with scrolls: tradition passed down. Gold on burgundy."),
    L("Cosechas con historia", "Harvests with a history"), L(["Tradicional", "Noble", "Cálida"], ["Traditional", "Noble", "Warm"]),
    [("dark", "#4A0F1D", "Burdeos", "Burgundy", "Fondo principal", "Main background"),
     ("gold", "#C9A45C", "Oro", "Gold", "Logo y detalles", "Logo and details"),
     ("soft", "#F3EBDD", "Crema", "Cream", "Fondo claro", "Light background"),
     ("olive", "#59603A", "Oliva", "Olive", "Apoyo", "Support")],
    ("cinzel", 500), ("montserrat", 400), duvall_sym, duvall_wm,
    ["bottle", "box", "menu", "cards", "bag", "poster"], L("Escudo heráldico con monograma", "Heraldic crest with monogram"),
    sym_k=1.3, vsym_k=1.55)


# 34 · REGALIA · weddings & events --------------------------------------------------
def regalia_sym(c, mono):
    g = c["g"]
    R = glyph("great-vibes", 400, "R", 86)
    m = ring(100, 114, 62, 1.8, g) + ring(100, 114, 56.5, 0.8, g) + crown(100, 40, 58, g, 2.2)
    m += letter(R, at(R, 103, 116), g) + C_(32, 114, 2.6, g) + C_(168, 114, 2.6, g)
    return Box(m, Rect(29.4, 5, 170.6, 177))


def regalia_wm(c, mono, al="start"):
    main = text("italiana", 400, "REGALIA", 80, c["g"], tracking=0.3)
    sub = text("parisienne", 400, "Bodas & eventos", 40, c["s"], box="ink")
    return wm(al, main, sub, gaps=[14])


regalia = lux(
    "regalia", "Regalia", L("Planeación de bodas y eventos", "Wedding and event planning"),
    L("Una R caligráfica coronada dentro de un doble anillo: cada celebración tratada como realeza. Oro sobre ciruela con rosa empolvado.",
      "A crowned calligraphic R inside a double ring: every celebration treated like royalty. Gold on plum with dusty rose."),
    L("Celebraciones dignas de recordar", "Celebrations worth remembering"), L(["Festiva", "Elegante", "Detallista"], ["Festive", "Elegant", "Meticulous"]),
    [("dark", "#3B1E3F", "Ciruela", "Plum", "Fondo principal", "Main background"),
     ("gold", "#D1B06B", "Oro", "Gold", "Logo y detalles", "Logo and details"),
     ("rose", "#E6C9C3", "Rosa empolvado", "Dusty rose", "Acento", "Accent"),
     ("soft", "#F7F2EE", "Perla", "Pearl", "Fondo claro", "Light background")],
    ("italiana", 400), ("parisienne", 400), regalia_sym, regalia_wm,
    ["cards", "box", "phone", "poster", "bag", "hangtag"], L("Monograma coronado", "Crowned monogram"), sym_k=1.55, vsym_k=1.75)


# 35 · CÉLESTE · fine watches ------------------------------------------------------
def celeste_sym(c, mono):
    g = c["g"]
    star = sparkle(100, 100, 66, g, 0.13) + f'<g transform="rotate(45 100 100)">{sparkle(100, 100, 38, g, 0.2)}</g>'
    m = ring(100, 100, 80, 1.6, g) + ticks(100, 100, 86, 92, 60, 1.1, g, 5) + knock(star, C_(100, 100, 4.2, "#000")) + ring(100, 100, 4.2, 1.2, g)
    return Box(m, Rect(7.4, 7.4, 192.6, 192.6))


def celeste_wm(c, mono, al="start"):
    main = text("italiana", 400, "CÉLESTE", 82, c["g"], tracking=0.32)
    sub = caps("RELOJERÍA FINA", 14, c["s"], tr=0.62)
    return wm(al, main, sub, gaps=[18])


celeste = lux(
    "celeste", "Céleste", L("Relojería fina y accesorios", "Fine watches and accessories"),
    L("Una estrella polar sobre la esfera de un reloj, con marcas de minutos finísimas: precisión que guía. Champaña sobre azul noche.",
      "A north star over a watch dial with hairline minute marks: precision that guides. Champagne on midnight blue."),
    L("El tiempo, en su mejor forma", "Time, at its finest"), L(["Precisa", "Celestial", "Exclusiva"], ["Precise", "Celestial", "Exclusive"]),
    [("dark", "#101B33", "Azul noche", "Midnight blue", "Fondo principal", "Main background"),
     ("gold", "#D8C08A", "Champaña", "Champagne", "Logo y detalles", "Logo and details"),
     ("silver", "#C9CCD3", "Plata", "Silver", "Apoyo", "Support"),
     ("soft", "#F4F1EA", "Marfil", "Ivory", "Fondo claro", "Light background")],
    ("italiana", 400), ("montserrat", 400), celeste_sym, celeste_wm,
    ["box", "bag", "cards", "hangtag", "phone", "poster"], L("Emblema de esfera y estrella", "Dial and star emblem"), sym_k=1.45, vsym_k=1.9)


# 36 · BRAMANTE · interior design ---------------------------------------------------
def bramante_sym(c, mono):
    g = c["g"]
    b = (line("M86 58 V142", g, 2.6) + line("M86 58 H103 A21 21 0 0 1 103 100 H86", g, 2.6)
         + line("M86 100 H107 A21 21 0 0 1 107 142 H86", g, 2.6))
    m = ring(100, 100, 70, 2.2, g) + ring(100, 100, 76, 0.7, g) + line("M8 100 H192", g, 1.1, "butt") + b
    return Box(m, Rect(8, 23.6, 192, 176.4))


def bramante_wm(c, mono, al="start"):
    main = text("tenor-sans", 400, "BRAMANTE", 64, c["g"], tracking=0.34)
    sub = text("parisienne", 400, "interiores", 46, c["s"], box="ink")
    return wm(al, main, sub, gaps=[10])


bramante = lux(
    "bramante", "Bramante Interiores", L("Estudio de diseño interior", "Interior design studio"),
    L("Una B construida con líneas de plano arquitectónico dentro de un círculo atravesado por el horizonte, firmada con caligrafía. Grafito, lino y oro.",
      "A B built from architectural drafting lines inside a circle crossed by the horizon, signed in calligraphy. Graphite, linen and gold."),
    L("Espacios con alma", "Spaces with soul"), L(["Moderna", "Cálida", "Refinada"], ["Modern", "Warm", "Refined"]),
    [("dark", "#1C1C1C", "Grafito", "Graphite", "Fondo principal", "Main background"),
     ("gold", "#BFA06A", "Oro", "Gold", "Logo y detalles", "Logo and details"),
     ("soft", "#E7E1D6", "Lino", "Linen", "Fondo claro", "Light background"),
     ("taupe", "#8C7F72", "Taupe", "Taupe", "Apoyo", "Support")],
    ("tenor-sans", 400), ("parisienne", 400), bramante_sym, bramante_wm,
    ["cards", "laptop", "wallsign", "tote", "mug", "poster"], L("Monograma lineal + firma", "Line monogram + signature"), sym_k=1.7, vsym_k=1.45)

BRANDS = [aurelia, velour, ludovica, orvieto, altamar, sable, villa, alma, duvall, regalia, celeste, bramante]

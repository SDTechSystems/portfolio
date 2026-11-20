"""Six opening projects for the brand gallery."""
from brands3 import L
from lib import Box, Rect, text
from model import Brand, C, P, S, knock


def identity(slug, name, style, sector, concept, tagline, personality, palette, font, symbol, products):
    colors = [
        (key, value, es, en, use_es, use_en)
        for (key, use_es, use_en), (value, es, en) in zip(
            [("ink", "Logotipo", "Wordmark"), ("light", "Fondo", "Background"),
             ("signal", "Símbolo y detalle", "Symbol and detail"), ("extra", "Contraste", "Contrast")],
            palette, strict=True)
    ]

    def mark(c, mono):
        return Box(symbol(c, mono), Rect(0, 0, 100, 100))

    def word(c, _mono, _align):
        return text(*font, name, 100, c["ink"], tracking=-.02)

    return Brand(
        slug=slug, name=name, style=style, sector=sector, concept=concept, tagline=tagline,
        personality=personality, colors=colors, display=font, body=("dm-sans", 500),
        roles={"ink": "ink", "signal": "signal", "extra": "extra"},
        inverse={"ink": "light", "signal": "extra", "extra": "signal"},
        base_bg="light", inverse_bg="ink", symbol=mark, wordmark=word,
        mockups=products, logo_kind=L("Símbolo y logotipo", "Symbol and wordmark"),
        sym_k=.94, vsym_k=1.45,
    )


def tide(c, mono):
    drop = P("M50 4C39 28 14 43 14 64a36 36 0 0 0 72 0C86 43 61 28 50 4Z", c["ink"])
    wave = S("M6 62C25 38 50 87 92 56", "#000", 9)
    return knock(drop, wave) + ("" if mono else S("M16 60C35 51 53 84 82 63", c["signal"], 4))


def nimbo(c, mono):
    # A geometric cloud (three circles on a rounded base) crossed by a bolt with a clear gap around it.
    ink = c["ink"]
    cloud = C(32, 55, 17, ink) + C(53, 42, 24, ink) + C(74, 56, 15, ink) + P("M15 55h74v8.5a8.5 8.5 0 0 1-8.5 8.5h-57A8.5 8.5 0 0 1 15 63.5z", ink)
    bolt = "M60 22 40 60h13L45 94l28-42H59l9-30z"
    gap = P(bolt, "#000") + S(bolt, "#000", 6)
    return knock(cloud, gap) + P(bolt, ink if mono else c["signal"])


def stratum(c, mono):
    return (P("M50 7 92 31 50 53 8 31z", c["ink"])
            + P("M8 41 50 63 92 41v11L50 74 8 52z", c["signal"])
            + P("M8 62 50 84 92 62v11L50 95 8 73z", c["ink"]))


def cacao(c, mono):
    pod = "M82 13C77 47 66 85 34 86 8 86 15 55 30 39 47 22 68 27 82 13Z"
    grooves = "M29 77C35 53 59 49 72 27M40 80C57 67 64 54 71 39"
    return knock(P(pod, c["ink"]), S(grooves, "#000", 4.5)) + ("" if mono else C(82, 70, 9, c["signal"]))


def giro(c, mono):
    return P("M14 59 43 10h22L36 59h22l-9 16H5zM58 42h22L62 74h29L81 91H30z", c["ink"]) + P("M67 10h28L84 30H56z", c["signal"])


def fosforo(c, mono):
    flame = "M60 8C81 33 93 45 89 66a40 40 0 0 1-79-6c0-14 7-26 17-37-2 14 2 21 10 24C48 34 54 22 60 8Z"
    cut = "M54 49C60 61 70 68 62 78c-10 12-28 2-22-10 3-6 9-10 14-19Z"
    return knock(P(flame, c["ink"]), P(cut, "#000")) + ("" if mono else P("M53 61c4 6 9 11 4 16-5 5-12 0-9-5z", c["signal"]))


BRANDS = [
    identity("tinta-marea", "Tinta Marea", "elegant", L("Tintas y escritura", "Ink and writing"),
             L("Una tinta de autor inspirada en el Pacífico. El símbolo corta una gota con el trazo de una ola.",
               "A signature ink inspired by the Pacific. A wave cuts through the silhouette of a droplet."),
             L("Escribe a tu ritmo", "Write to your own rhythm"), L(["Serena", "Precisa"], ["Quiet", "Precise"]),
             [("#132F37", "Petróleo", "Petrol"), ("#EAE1CC", "Papel", "Paper"),
              ("#247C75", "Marea", "Tide"), ("#B6D8C4", "Espuma", "Sea foam")],
             ("instrument-serif", 400), tide, ["bottles", "box", "cards", "bag", "poster", "tote"]),
    identity("nimbo", "Nimbo", "bold", L("Sodas cítricas", "Citrus sodas"),
             L("Una soda ácida y chispeante con azul cobalto, mandarina y una nube que descarga un rayo.",
               "A bright, tart soda in cobalt and tangerine, with a cloud that strikes like lightning."),
             L("Destapa el trueno", "Crack open the thunder"), L(["Chispeante", "Enérgica"], ["Fizzy", "Energetic"]),
             [("#2027A9", "Cobalto", "Cobalt"), ("#FFF2CE", "Lima clara", "Pale lime"),
              ("#EB511D", "Mandarina", "Tangerine"), ("#FFD26F", "Rayo", "Lightning")],
             ("archivo-black", 400), nimbo, ["can", "cup", "poster", "tshirt", "cap", "tote"]),
    identity("senda-mineral", "Senda Mineral", "minimal", L("Cuidado corporal", "Body care"),
             L("Capas de piedra y verdes apagados para una línea de cuidado corporal inspirada en los páramos.",
               "Stone strata and muted greens for a body-care line inspired by the Andean highlands."),
             L("Vuelve a lo esencial", "Return to essentials"), L(["Mineral", "Sensorial"], ["Mineral", "Tactile"]),
             [("#25362E", "Pizarra", "Slate"), ("#E7E5D7", "Caliza", "Limestone"),
              ("#637851", "Musgo", "Moss"), ("#BDCE9B", "Liquen", "Lichen")],
             ("manrope", 700), stratum, ["jar", "bottles", "box", "bag", "cards", "tote"]),
    identity("canto-cacao", "Canto Cacao", "organic", L("Chocolate de origen", "Single-origin chocolate"),
             L("Una mazorca dibujada a partir de sus surcos y una paleta de cacao, guayaba y pulpa fresca.",
               "A cacao pod shaped by its grooves, with colors drawn from cacao, guava, and fresh pulp."),
             L("La tierra también canta", "The land has a voice"), L(["Cálida", "Artesanal"], ["Warm", "Handcrafted"]),
             [("#44221E", "Cacao", "Cacao"), ("#F6E6CF", "Pulpa", "Pulp"),
              ("#A73451", "Guayaba", "Guava"), ("#F7A6A5", "Flor", "Blossom")],
             ("fraunces", 700), cacao, ["bar", "pouch", "box", "bag", "cards", "poster"]),
    identity("giro-sur", "Giro Sur", "tech", L("Ciclismo urbano", "Urban cycling"),
             L("Dos curvas encadenadas dibujan un cambio de carril. La identidad lleva el amarillo de señalización a la ropa y los accesorios.",
               "Two linked turns trace a lane change. The identity brings traffic-sign yellow to apparel and accessories."),
             L("La calle es tu ruta", "The streets are your route"), L(["Ágil", "Urbana"], ["Agile", "Urban"]),
             [("#22233D", "Asfalto", "Asphalt"), ("#F3EFDF", "Tiza", "Chalk"),
              ("#7168B2", "Violeta", "Violet"), ("#E8F47C", "Señal", "Signal")],
             ("space-grotesk", 700), giro, ["cap", "tshirt", "tote", "hangtag", "poster", "cards"]),
    identity("fosforo", "Fósforo", "playful", L("Pizzería de horno", "Wood-fired pizzeria"),
             L("Una llama compacta y letras carnosas. La identidad cruza el color del horno con papel crema y tinta berenjena.",
               "A compact flame and chunky lettering pair the warmth of the oven with cream paper and aubergine ink."),
             L("Que prenda el hambre", "Fire up your appetite"), L(["Traviesa", "Cálida"], ["Mischievous", "Warm"]),
             [("#4A203D", "Berenjena", "Aubergine"), ("#FFEDCA", "Masa", "Dough"),
              ("#DE452A", "Brasa", "Ember"), ("#FFAA55", "Horno", "Oven")],
             ("baloo-2", 800), fosforo, ["box", "cup", "apron", "bag", "menu", "storefront"]),
]
BRANDS[1].notes = {"can": ["Mandarina eléctrica", "Lima chispeante"]}
BRANDS[1].sym_k = 1.32  # the cloud fills only part of its square, so it needs more height
BRANDS[3].notes = {"bars": ["70% Cacao", "Cacao y nibs"]}

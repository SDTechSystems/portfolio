"""Character artwork for the identities that can use a recurring illustrated voice."""
from brands3 import L
from lib import canvas
from model import C, E, P, S
from pieces import accent_on, light, strong


MASCOTS = {
    "nimbo": {"name": "Trueno", "description": L(
        "Una nube chispeante que abraza su rayo. Su silueta funciona en latas, stickers y lanzamientos de nuevos sabores.",
        "A bubbly cloud hugs its lightning bolt. Its silhouette works on cans, stickers and new flavor launches.")},
    "fosforo": {"name": "Chispa", "description": L(
        "La llama del horno cobra vida. Saluda desde las cajas, los delantales y las piezas para llevar.",
        "The oven flame comes to life on boxes, aprons and takeaway pieces.")},
    "pompon": {"name": "Pompón", "description": L(
        "El pompón del logo se vuelve un personaje para etiquetas, parches y estampados infantiles.",
        "The pompom in the logo becomes a character for tags, patches and children’s prints.")},
    "paleton": {"name": "Paletón", "description": L(
        "La paleta mordida sale del logo para acompañar sabores, envoltorios y carteles de temporada.",
        "The bitten ice pop steps out of the logo to introduce flavors, wrappers and seasonal posters.")},
    "michi-firulais": {"name": "Michi y Firulais", "description": L(
        "El gato curioso y el perro entusiasta acompañan las etiquetas, las bolsas y las guías para nuevos cuidadores.",
        "A curious cat and an enthusiastic dog appear on labels, bags and guides for new pet owners.")},
    "brasa-brava": {"name": "La Bravita", "description": L(
        "La flama de la parrilla saluda con su delantal y sus guantes. Está pensada para empaques para llevar y promociones.",
        "The grill flame waves in its apron and mitts. Designed for takeaway packaging and promotions.")},
    "miel-de-monte": {"name": "Zumba", "description": L(
        "Una abeja curiosa que señala los sabores y cuenta el origen de la miel en etiquetas y publicaciones.",
        "A curious bee points out flavors and tells the honey’s story on labels and social posts.")},
}


def mascot_art(b, ink, color, accent, paper):
    """Draw the character alone on a 240 × 240 transparent artboard."""
    outline = lambda d: S(d, ink, 7)
    eyes = lambda x, y: C(x - 14, y, 4.5, ink) + C(x + 14, y, 4.5, ink)
    smile = lambda x, y: outline(f"M{x-8} {y}q8 9 16 0")
    limbs = outline("M71 121Q46 150 29 130M174 119q24 13 38-14M95 144q-13 55-23 55H58m86-55q11 55 34 55h10")
    hands = (E(27, 128, 12, 8, ink, 28) + E(27, 128, 8, 4, paper, 28)
             + E(213, 103, 12, 8, ink, -43) + E(213, 103, 8, 4, paper, -43))
    shoes = E(62, 202, 20, 9, ink, -7) + E(180, 202, 20, 9, ink, 7)
    if b.slug == "michi-firulais":
        cat = P("M20 117V55l29 17a50 50 0 0 1 37 0l27-17v62c0 45-93 45-93 0Z", color)
        dog = E(171, 118, 46, 45, accent) + E(134, 105, 14, 28, color, 24) + E(208, 105, 14, 28, color, -24)
        return (cat + dog + eyes(67, 109) + eyes(171, 109) + C(67, 121, 5, ink) + C(171, 121, 5, ink)
                + smile(67, 130) + smile(171, 130) + outline("M27 130H10m18 11-14 7m89-18h14m-16 11 12 7")
                + E(41, 165, 15, 8, ink) + E(93, 165, 15, 8, ink) + E(152, 165, 15, 8, ink) + E(192, 165, 15, 8, ink))
    if b.slug == "miel-de-monte":
        return (outline("M136 76q6-20 17-24m-26 21q-5-20-15-24M40 124q-17 2-23 11m26 10H20")
                + E(92, 78, 20, 34, paper, -41) + E(115, 70, 17, 30, paper, -13)
                + E(119, 122, 65, 41, accent, -14) + outline("M74 99q-1 27 17 46m7-52q1 29 20 58")
                + C(152, 111, 31, color) + eyes(151, 105) + smile(153, 117) + P("M60 128l-17 14 22 1z", ink))
    if b.slug in {"nimbo", "fosforo", "brasa-brava"}:
        if b.slug == "nimbo":
            shape = P("M67 151c-35 0-47-42-14-58 0-25 28-40 52-27 12-28 59-24 67 8 45 1 56 77 10 77Z", color)
            detail = P("M126 86l-28 31h19l-6 25 30-35h-20z", accent)
            return limbs + shoes + shape + detail + C(88, 111, 5, ink) + C(153, 111, 5, ink) + smile(122, 143) + hands
        shape = P("M68 153c-25-28-10-60 15-82-4 20 1 27 9 31 18-18 36-45 35-74 47 42 70 77 53 114-17 42-82 49-112 11Z", color)
        detail = P("M89 145c5-21 30-25 35-41 11 12 25 19 28 39 4 31-64 38-63 2Z", accent)
        return limbs + shoes + shape + detail + eyes(120, 135) + smile(120, 149) + hands
    version, _ = light(b)
    mark = b.mark(version).fit(52, 42, 136, 126)
    return limbs + shoes + mark.markup + hands


def write_mascot(b, dir_path):
    profile = MASCOTS.get(b.slug)
    if not profile:
        return
    _, paper = light(b)
    _, ink = strong(b)
    color = b.hex(b.roles["signal"]) if "signal" in b.roles else accent_on(b, paper)
    accent = b.hex(b.roles["extra"]) if "extra" in b.roles else accent_on(b, ink)
    character = mascot_art(b, ink, color, accent, paper)
    (dir_path / "mascota.svg").write_text(canvas(240, 240, character, profile["name"]), encoding="utf-8")

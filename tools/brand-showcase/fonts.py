"""Free commercial-use typefaces for the brand showcase, fetched from Fontsource (npm).

Only the Latin subset is used (covers Spanish: á é í ó ú ñ ü ¿ ¡). Fonts are cached in
.cache/fonts (git-ignored); the published SVGs carry outlines, never font files.
"""
import json
import subprocess
import tarfile
from pathlib import Path

CACHE = Path(__file__).parent / ".cache" / "fonts"

# key: (fontsource package id, display name, weights, google fonts slug)
FONTS = {
    "jost": ("jost", "Jost", [300, 400, 500, 600]),
    "karla": ("karla", "Karla", [400, 600]),
    "syncopate": ("syncopate", "Syncopate", [400, 700]),
    "work-sans": ("work-sans", "Work Sans", [400, 500, 600]),
    "instrument-serif": ("instrument-serif", "Instrument Serif", [400]),
    "manrope": ("manrope", "Manrope", [400, 600, 700]),
    "libre-caslon-display": ("libre-caslon-display", "Libre Caslon Display", [400]),
    "source-sans-3": ("source-sans-3", "Source Sans 3", [400, 600]),
    "ibm-plex-sans": ("ibm-plex-sans", "IBM Plex Sans", [400, 600, 700]),
    "ibm-plex-mono": ("ibm-plex-mono", "IBM Plex Mono", [400, 500]),
    "plus-jakarta-sans": ("plus-jakarta-sans", "Plus Jakarta Sans", [400, 600, 700, 800]),
    "nunito-sans": ("nunito-sans", "Nunito Sans", [400, 700]),
    "anton": ("anton", "Anton", [400]),
    "barlow": ("barlow", "Barlow", [400, 600, 700]),
    "unbounded": ("unbounded", "Unbounded", [400, 700, 800]),
    "rubik": ("rubik", "Rubik", [400, 500, 700]),
    "syne": ("syne", "Syne", [400, 600, 700, 800]),
    "poppins": ("poppins", "Poppins", [400, 500, 600, 700]),
    "bodoni-moda": ("bodoni-moda", "Bodoni Moda", [400, 500, 600]),
    "raleway": ("raleway", "Raleway", [300, 400, 500, 600]),
    "cormorant-garamond": ("cormorant-garamond", "Cormorant Garamond", [400, 500, 600, 700]),
    "montserrat": ("montserrat", "Montserrat", [400, 500, 600, 700]),
    "playfair-display": ("playfair-display", "Playfair Display", [400, 600, 700]),
    "lato": ("lato", "Lato", [400, 700]),
    "fraunces": ("fraunces", "Fraunces", [400, 600, 700, 800]),
    "libre-franklin": ("libre-franklin", "Libre Franklin", [400, 500, 600]),
    "young-serif": ("young-serif", "Young Serif", [400]),
    "mulish": ("mulish", "Mulish", [400, 600, 700]),
    "dm-serif-display": ("dm-serif-display", "DM Serif Display", [400]),
    "dm-sans": ("dm-sans", "DM Sans", [400, 500, 700]),
    "fredoka": ("fredoka", "Fredoka", [400, 500, 600, 700]),
    "nunito": ("nunito", "Nunito", [400, 700, 800]),
    "baloo-2": ("baloo-2", "Baloo 2", [400, 600, 800]),
    "quicksand": ("quicksand", "Quicksand", [400, 500, 700]),
    "bagel-fat-one": ("bagel-fat-one", "Bagel Fat One", [400]),
    "lexend": ("lexend", "Lexend", [400, 500, 700]),
    "alfa-slab-one": ("alfa-slab-one", "Alfa Slab One", [400]),
    "oswald": ("oswald", "Oswald", [400, 500, 600]),
    "shrikhand": ("shrikhand", "Shrikhand", [400]),
    "barlow-semi-condensed": ("barlow-semi-condensed", "Barlow Semi Condensed", [400, 500, 600, 700]),
    "pacifico": ("pacifico", "Pacifico", [400]),
    "josefin-sans": ("josefin-sans", "Josefin Sans", [400, 600, 700]),
    "space-grotesk": ("space-grotesk", "Space Grotesk", [400, 500, 700]),
    "inter": ("inter", "Inter", [400, 500, 600, 700]),
    "sora": ("sora", "Sora", [400, 600, 700]),
    "figtree": ("figtree", "Figtree", [400, 500, 700]),
    "archivo-black": ("archivo-black", "Archivo Black", [400]),
    "archivo": ("archivo", "Archivo", [400, 500, 700]),
}


def font_path(key, weight=400, italic=False):
    pkg = FONTS[key][0]
    return CACHE / pkg / f"{pkg}-latin-{weight}-{'italic' if italic else 'normal'}.woff"


def license_of(key):
    meta = CACHE / FONTS[key][0] / "meta.json"
    return json.loads(meta.read_text())["license"] if meta.exists() else "OFL-1.1"


def fetch(keys=None, italics=()):
    """Download (npm pack) and extract the needed WOFF files. Idempotent."""
    CACHE.mkdir(parents=True, exist_ok=True)
    for key in keys or FONTS:
        pkg, _name, weights = FONTS[key]
        dest = CACHE / pkg
        wanted = [font_path(key, w) for w in weights] + [font_path(key, w, True) for (k, w) in italics if k == key]
        if all(p.exists() for p in wanted):
            continue
        dest.mkdir(parents=True, exist_ok=True)
        out = subprocess.run(["npm", "pack", f"@fontsource/{pkg}", "--pack-destination", str(dest), "--silent"],
                             capture_output=True, text=True, check=True).stdout.strip().splitlines()[-1]
        tgz = dest / out
        with tarfile.open(tgz) as tar:
            meta = json.load(tar.extractfile("package/package.json"))
            (dest / "meta.json").write_text(json.dumps({"license": meta.get("license", ""), "version": meta["version"]}))
            for p in wanted:
                try:
                    data = tar.extractfile(f"package/files/{p.name}").read()
                except KeyError:
                    print(f"  missing {p.name}")
                    continue
                p.write_bytes(data)
            try:
                (dest / "LICENSE").write_bytes(tar.extractfile("package/LICENSE").read())
            except KeyError:
                pass
        tgz.unlink()
        print(f"fetched {pkg}")


if __name__ == "__main__":
    fetch(italics=[("playfair-display", 700), ("playfair-display", 600), ("fraunces", 600), ("cormorant-garamond", 500), ("cormorant-garamond", 600), ("instrument-serif", 400), ("bodoni-moda", 400)])

#!/usr/bin/env bash
# Blender bottle renders for the four drinks brands. Needs a Python with `bpy` (BPY=/path/to/python).
set -e
cd "$(dirname "$0")"; A=../.cache/art; O=../.cache/renders; S=${SAMPLES:-128}; PY=${BPY:-python3}
run() { mkdir -p $O/$1; foil=-; [ "$4" = foil ] && foil=$A/$1/bottle-foil.png
  $PY bottle_cycles.py $2 $A/$1/bottle-label.png $foil $O/$1/bottle.png $3 $5 $6 $S ${7:-} >/dev/null; echo "ok $1/bottle"; }
[ "${BOTTLES:-1}" = 1 ] && {
run orvieto      wine  "#3B0F18" foil "#2b2321" "#141414"
run casa-duvall  wine  "#2E0A12" foil "#542c32" "#4A0F1D"
run paramo       beer  "#9a5214" no   "#e5d6bd" "#2D6E6A"
run guayaba-club juice "#f2f7f5" no   "#ffd9c2" "#1E8C5A" "#ff5f86"
}

# glass jars (alma-botanica, sereno, lino, miel-de-monte, la-navaja): label.svg rasterised, then jar kind
jar() { mkdir -p $O/$1; [ -f $A/$1/label.png ] || node raster.cjs $A/$1/label.svg $A/$1/label.png 2800 2000
  $PY bottle_cycles.py jar $A/$1/label.png - $O/$1/jar.png "#f4f7f6" $2 $3 $S $4 $5 >/dev/null; echo "ok $1/jar"; }
if [ "${JARS:-1}" = 1 ]; then
jar alma-botanica "#e2dbcd" "#c5a46d" "#f1ebe0" cream
jar sereno        "#e3e0d8" "#c9c9c4" "#ece6db" cream
jar lino          "#e8dfd6" "#c9a46a" "#efe3d3" cream
jar miel-de-monte "#efe2bf" "#d9a441" "#e39b1b" honey
jar la-navaja     "#e4d8c3" "#2a2a2e" "#2c2a2a" cream
fi

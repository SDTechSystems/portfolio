#!/usr/bin/env bash
# Blender bottle renders for the four drinks brands. Needs a Python with `bpy` (BPY=/path/to/python).
set -e
cd "$(dirname "$0")"; A=../.cache/art; O=../.cache/renders; S=${SAMPLES:-128}; PY=${BPY:-python3}
run() { mkdir -p $O/$1; foil=-; [ "$4" = foil ] && foil=$A/$1/bottle-foil.png
  $PY bottle_cycles.py $2 $A/$1/bottle-label.png $foil $O/$1/bottle.png $3 $5 $6 $S ${7:-} >/dev/null; echo "ok $1/bottle"; }
run orvieto      wine  "#3B0F18" foil "#2b2321" "#141414"
run casa-duvall  wine  "#2E0A12" foil "#542c32" "#4A0F1D"
run paramo       beer  "#9a5214" no   "#e5d6bd" "#2D6E6A"
run guayaba-club juice "#f2f7f5" no   "#ffd9c2" "#1E8C5A" "#ff5f86"

"""Blender Cycles render of a brand's glass bottles (wine, beer or juice): real refraction, wrapped
label, optional gold-foil symbol, studio sweep, area lights and shallow depth of field.

Run with the `bpy` module: python bottle_cycles.py <kind> <label.png> <foil.png|-> <out.png> <glass hex>
<backdrop hex> <cap hex> [samples] [liquid hex]
"""
import math
import sys

import bpy

KIND, LABEL, FOIL, OUT, GLASS, BACK, CAP = sys.argv[1:8]
SAMPLES = int(sys.argv[8]) if len(sys.argv) > 8 else 128
LIQUID = sys.argv[9] if len(sys.argv) > 9 else None


def lin(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c) + (1,)


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 16
sc.cycles.transmission_bounces = 16
sc.cycles.transparent_max_bounces = 16
sc.render.resolution_x, sc.render.resolution_y = 1600, 1200
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "AgX - Punchy" if KIND != "wine" else "AgX - Medium High Contrast"


def principled(name, **kw):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    for k, v in kw.items():
        b.inputs[k].default_value = v
    return m


def mesh(name, verts, faces, smooth=True, uvs=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    if uvs:
        layer = me.uv_layers.new()
        for poly in me.polygons:
            for li in poly.loop_indices:
                layer.data[li].uv = uvs[me.loops[li].vertex_index]
    for p in me.polygons:
        p.use_smooth = smooth
    ob = bpy.data.objects.new(name, me)
    sc.collection.objects.link(ob)
    return ob


def lathe(name, prof, segs=160):
    verts, faces = [], []
    n = len(prof)
    for i in range(segs):
        a = 2 * math.pi * i / segs
        verts += [(r * math.cos(a), r * math.sin(a), z) for r, z in prof]
    for i in range(segs):
        j = (i + 1) % segs
        faces += [(i * n + k, j * n + k, j * n + k + 1, i * n + k + 1) for k in range(n - 1)]
    return mesh(name, verts, faces)


def band(name, r, z0, z1, arc, segs=128):
    verts, faces, uvs = [], [], []
    for i in range(segs + 1):
        a = -arc / 2 + arc * i / segs - math.pi / 2
        for t, z in ((0, z0), (1, z1)):
            verts.append((r * math.cos(a), r * math.sin(a), z))
            uvs.append((i / segs, t))
    faces = [(i * 2, (i + 1) * 2, (i + 1) * 2 + 1, i * 2 + 1) for i in range(segs)]
    return mesh(name, verts, faces, uvs=uvs)


def image_mat(name, path, rough=0.8, foil=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tx = nt.nodes.new("ShaderNodeTexImage")
    tx.image = bpy.data.images.load(path)
    tx.interpolation = "Cubic"
    if foil:
        b.inputs["Base Color"].default_value = (0.86, 0.62, 0.26, 1)
        b.inputs["Metallic"].default_value = 1.0
        b.inputs["Roughness"].default_value = 0.22
        nt.links.new(tx.outputs["Alpha"], b.inputs["Alpha"])
        bump = nt.nodes.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value = 0.35
        nt.links.new(tx.outputs["Alpha"], bump.inputs["Height"])
        nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    else:
        nt.links.new(tx.outputs["Color"], b.inputs["Base Color"])
        b.inputs["Roughness"].default_value = rough
        noise = nt.nodes.new("ShaderNodeTexNoise")
        noise.inputs["Scale"].default_value = 900
        bump = nt.nodes.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value = 0.04
        nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
        nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


def glass_mat(name, hexc, absorb):
    """Thin-wall glass: clear refraction tinted by a volume absorption so thick parts read darker."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(hexc)
    b.inputs["Roughness"].default_value = 0.02
    b.inputs["IOR"].default_value = 1.5
    b.inputs["Transmission Weight"].default_value = 1.0
    vol = nt.nodes.new("ShaderNodeVolumeAbsorption")
    vol.inputs["Color"].default_value = lin(hexc)
    vol.inputs["Density"].default_value = absorb
    nt.links.new(vol.outputs["Volume"], nt.nodes["Material Output"].inputs["Volume"])
    return m


# ------------------------------------------------------------------ studio sweep
prof = [(-14, 0)]
for i in range(25):
    a = math.pi / 2 * i / 24
    prof.append((2 + math.sin(a) * 4, 4 - math.cos(a) * 4))
prof.append((6, 14))
verts = [(x, y, z) for x in (-16, 16) for y, z in prof]
n = len(prof)
sweep = mesh("sweep", verts, [(k, k + 1, n + k + 1, n + k) for k in range(n - 1)])
sweep.data.materials.append(principled("sweep", **{"Base Color": lin(BACK), "Roughness": 0.8}))

# ------------------------------------------------------------------ bottle shapes (radius, height) outer profiles
if KIND == "wine":
    OUTER = [(0, 0.02), (0.3, 0), (0.37, 0.02), (0.38, 0.1), (0.38, 1.78), (0.372, 1.9), (0.33, 2.05), (0.24, 2.2), (0.15, 2.33),
             (0.122, 2.45), (0.118, 2.6), (0.118, 3.02), (0.132, 3.05), (0.132, 3.1)]
    LAB = (0.62, 1.57, 2.5)
    FILL = 2.25
elif KIND == "beer":
    OUTER = [(0, 0.02), (0.27, 0), (0.31, 0.02), (0.32, 0.1), (0.32, 1.35), (0.305, 1.5), (0.22, 1.78), (0.14, 2.05),
             (0.115, 2.25), (0.112, 2.62), (0.125, 2.65), (0.125, 2.7)]
    LAB = (0.32, 1.12, 2.6)
    FILL = 2.15
else:  # juice
    OUTER = [(0, 0.02), (0.31, 0), (0.35, 0.02), (0.36, 0.1), (0.36, 1.45), (0.35, 1.6), (0.28, 1.75), (0.2, 1.85),
             (0.19, 1.95), (0.19, 2.05)]
    LAB = (0.38, 1.18, 2.7)
    FILL = 1.82
WALL = 0.012


def shell(outer):
    """Closed glass wall: outer profile up, inner profile back down (so refraction sees two surfaces)."""
    inner = [(max(r - WALL, 0), z + (WALL if i == 0 else 0)) for i, (r, z) in enumerate(outer)]
    top_r, top_z = outer[-1]
    return outer + [(top_r - WALL, top_z)] + inner[::-1][1:]


def liquid(outer, level):
    pts = [(0, WALL * 1.6)]
    for r, z in outer[1:]:
        if z >= level:
            break
        pts.append((max(r - WALL * 1.6, 0.001), max(z, WALL * 1.6)))
    rr = next(r for r, z in reversed(outer) if z <= level) - WALL * 1.6
    pts += [(rr, level), (0, level)]
    return pts


glass = glass_mat("glass", GLASS, {"wine": 9.0, "beer": 1.5, "juice": 0.4}[KIND])
liq_hex = LIQUID or {"wine": "#2a0308", "beer": "#c77412", "juice": "#ff6f8c"}[KIND]
liq = bpy.data.materials.new("liquid")
liq.use_nodes = True
lb = liq.node_tree.nodes["Principled BSDF"]
lb.inputs["Base Color"].default_value = lin(liq_hex)
lb.inputs["Roughness"].default_value = 0.05
if KIND == "juice":   # cloudy fruit juice: mostly diffuse with a bit of subsurface glow
    lb.inputs["Subsurface Weight"].default_value = 0.6
    lb.inputs["Subsurface Radius"].default_value = (0.4, 0.15, 0.1)
    lb.inputs["Subsurface Scale"].default_value = 0.05
else:
    lb.inputs["Transmission Weight"].default_value = 1.0
    vol = liq.node_tree.nodes.new("ShaderNodeVolumeAbsorption")
    vol.inputs["Color"].default_value = lin(liq_hex)
    vol.inputs["Density"].default_value = 30 if KIND == "wine" else 1.6
    liq.node_tree.links.new(vol.outputs["Volume"], liq.node_tree.nodes["Material Output"].inputs["Volume"])

paper = image_mat("paper", LABEL, 0.75 if KIND != "juice" else 0.45)
foil = image_mat("foil", FOIL, foil=True) if FOIL != "-" else None
capm = principled("cap", **{"Base Color": lin(CAP), "Roughness": 0.3, "Metallic": 0.35, "Coat Weight": 0.8})
gold = principled("gold", **{"Base Color": (0.86, 0.62, 0.26, 1), "Metallic": 1.0, "Roughness": 0.2})
steel = principled("steel", **{"Base Color": lin(CAP), "Metallic": 0.9, "Roughness": 0.28})

PLACES = ((-0.5, 0.25, 0.86, 14), (0.42, -0.15, 1.0, -8))
for x, y, s, rot in PLACES:
    parts = []
    b = lathe("bottle", shell(OUTER))
    b.data.materials.append(glass)
    parts.append(b)
    lq = lathe("liquid", liquid(OUTER, FILL))
    lq.data.materials.append(liq)
    parts.append(lq)
    r_lab = next(r for r, z in OUTER if z >= LAB[0]) + 0.0015
    lab = band("label", r_lab, LAB[0], LAB[1], LAB[2])
    lab.data.materials.append(paper)
    parts.append(lab)
    if foil:
        fl = band("foil", r_lab + 0.001, LAB[0], LAB[1], LAB[2])
        fl.data.materials.append(foil)
        parts.append(fl)
    tr, tz = OUTER[-1]
    if KIND == "wine":
        c = lathe("capsule", [(0, 2.48), (0.128, 2.48), (0.128, 3.12), (0.11, 3.13), (0, 3.13)])
        c.data.materials.append(capm)
        r = lathe("ring", [(0.1295, 2.515), (0.1295, 2.55)])
        r.data.materials.append(gold)
        parts += [c, r]
    elif KIND == "beer":
        c = lathe("crown", [(0, tz + 0.06), (0.135, tz + 0.055), (0.145, tz + 0.02), (0.14, tz - 0.06), (0.13, tz - 0.06)], 21)
        c.data.materials.append(steel)
        parts.append(c)
    else:
        c = lathe("cap", [(0, tz + 0.2), (0.2, tz + 0.2), (0.21, tz + 0.18), (0.21, tz - 0.06), (0.195, tz - 0.07)])
        c.data.materials.append(capm)
        parts.append(c)
    for o in parts:
        o.scale = (s, s, s)
        o.location = (x, y, 0)
        o.rotation_euler.z = math.radians(rot)


def area(name, loc, rot, size, energy, color=(1, 0.95, 0.88), sy=None):
    light = bpy.data.lights.new(name, "AREA")
    light.energy, light.color, light.shape, light.size = energy, color, "RECTANGLE", size
    light.size_y = sy or size
    o = bpy.data.objects.new(name, light)
    o.location, o.rotation_euler = loc, [math.radians(v) for v in rot]
    sc.collection.objects.link(o)


bright = KIND != "wine"
area("key", (-3.5, -2.2, 3.6), (58, 0, -50), 2.2, 340 if bright else 380)
area("rim_r", (2.2, 1.0, 1.8), (80, 0, 115), 0.4, 420, (1, 0.9, 0.8), 3.5)
area("rim_l", (-2.4, 1.2, 1.8), (80, 0, -115), 0.35, 220, (1, 0.92, 0.88), 3.5)
area("wall", (0, -1.0, 5.5), (-35, 0, 0), 5.0, 360 if bright else 260)
area("fill", (0.5, -6, 2.5), (75, 0, 0), 3.0, 140 if bright else 70, (0.95, 0.96, 1))
w = bpy.data.worlds.new("w")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = lin(BACK)[:3] + (1,)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.25
sc.world = w

top = max(z for _r, z in OUTER) + 0.2
cam = bpy.data.cameras.new("cam")
cam.lens = 75
cam.dof.use_dof = True
cam.dof.aperture_fstop = 2.4
co = bpy.data.objects.new("cam", cam)
sc.collection.objects.link(co)
dist_ = {"wine": 3.2, "beer": 3.4, "juice": 4.1}[KIND] * top
co.location = (-0.05, -dist_, top * 0.6)
co.rotation_euler = (math.radians(88), 0, 0)
sc.camera = co
focus = bpy.data.objects.new("focus", None)
sc.collection.objects.link(focus)
focus.location = (0.42, -0.15, top * 0.4)
cam.dof.focus_object = focus
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("rendered", OUT)

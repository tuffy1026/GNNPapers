"""Simplified CroplandGPT architecture (Fig. 3): two swim lanes, one colour family per function."""
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon
from matplotlib.lines import Line2D

plt.rcParams.update({"font.family": "Liberation Sans", "mathtext.fontset": "custom",
                     "mathtext.rm": "Liberation Sans", "mathtext.it": "Liberation Sans:italic",
                     "mathtext.bf": "Liberation Sans:bold", "pdf.fonttype": 42, "svg.fonttype": "none"})

W, H = 184, 96
BLUE = dict(dark="#2E5A87", mid="#5B86B5", light="#DCE8F4", pale="#B9CFE6", lane="#F2F6FB")
GREEN = dict(dark="#3D7A4C", mid="#7FB38A", light="#E0F0E3", lane="#F3F8F3")
ORANGE = dict(dark="#BF6A1F", mid="#EFA35E", light="#FCEBDA", bar="#F6CBA2")
GRAY = dict(dark="#4D4D4D", light="#F3F3F3")
INK = "#262626"
ARROW = "#4A4A4A"

fig = plt.figure(figsize=(W / 25.4, H / 25.4))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect("equal")
ax.axis("off")
SCENE = []


def rbox(x, y, w, h, fc, ec=None, lw=0.6, r=1.2, text=None, fs=6.2, color=INK, bold=False, italic=False,
         z=2, name="Card", t="rbox"):
    SCENE.append(dict(t=t, x=x, y=y, w=w, h=h, fc=fc, ec=ec, lw=lw, r=r, text=text, fs=fs, color=color,
                      bold=bold, italic=italic, z=z, name=name))
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc,
                                ec=ec or "none", lw=lw if ec else 0, zorder=z))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color,
                fontweight="bold" if bold else "normal", style="italic" if italic else "normal",
                zorder=z + 0.5, linespacing=1.3)
    return dict(l=x, r=x + w, b=y, t=y + h, cx=x + w / 2, cy=y + h / 2)


def poly(pts, fc, ec=None, lw=0.6, text=None, fs=6.2, color="#FFFFFF", bold=True, z=2, name="Shape",
         text_xy=None):
    SCENE.append(dict(t="poly", pts=pts, fc=fc, ec=ec, lw=lw, text=text, fs=fs, color=color, bold=bold, z=z,
                      name=name))
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec or "none", lw=lw if ec else 0, zorder=z,
                         joinstyle="round"))
    if text:
        xs, ys = zip(*pts)
        tx, ty = text_xy or ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
        ax.text(tx, ty, text, ha="center", va="center", fontsize=fs, color=color,
                fontweight="bold" if bold else "normal", zorder=z + 0.5, linespacing=1.3)


def text(x, y, s, fs=6.0, color=INK, bold=False, italic=False, ha="center", va="center"):
    SCENE.append(dict(t="text", x=x, y=y, text=s, fs=fs, ha=ha, va=va, italic=italic, rot=0, color=color,
                      bold=bold))
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=color, fontweight="bold" if bold else "normal",
            style="italic" if italic else "normal", zorder=6, linespacing=1.3)


def arrow(pts, color=ARROW, lw=0.8):
    SCENE.append(dict(t="path", pts=list(pts), dashed=False, head=True, color=color, lw=lw))
    if len(pts) > 2:
        xs, ys = zip(*pts[:-1])
        ax.add_line(Line2D(xs, ys, color=color, lw=lw, zorder=1, solid_joinstyle="miter"))
    ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle="-|>,head_length=1.8,head_width=1.05",
                                 mutation_scale=1, color=color, lw=lw, shrinkA=0, shrinkB=0, zorder=1))


def header_card(x, y, w, h, hh, pal, title, fs=6.3):
    rbox(x, y, w, h, pal["light"], pal["dark"], lw=0.7, r=1.6, name=title)
    r, top, n = 1.6, y + h, 6
    pts = [(x, top - hh), (x, top - r)]
    pts += [(x + r - r * math.cos(a), top - r + r * math.sin(a))
            for a in [i * math.pi / 2 / n for i in range(1, n)]]
    pts += [(x + r, top), (x + w - r, top)]
    pts += [(x + w - r + r * math.sin(a), top - r + r * math.cos(a))
            for a in [i * math.pi / 2 / n for i in range(1, n)]]
    pts += [(x + w, top - r), (x + w, top - hh)]
    poly(pts, pal["dark"], None, text=title, fs=fs, z=3, name=title + " header")
    return dict(l=x, r=x + w, b=y, t=top, cx=x + w / 2, cy=y + h / 2, body_top=top - hh)


def tokens(cx, cy, n, fc, ec, size=2.4, gap=0.7, label=None):
    x0 = cx - (n * size + (n - 1) * gap) / 2
    for i in range(n):
        rbox(x0 + i * (size + gap), cy - size / 2, size, size, fc, ec, lw=0.5, r=0.35, z=4, name="Token")
    if label:
        text(cx, cy + size / 2 + 2.2, label, fs=6.4, bold=True, color=ec)


# ------------------------------------------------------------------ swim lanes
rbox(2, 50, 180, 43, BLUE["lane"], None, r=2.0, z=0, name="Lane spatial", t="lane")
rbox(2, 4, 180, 43, GREEN["lane"], None, r=2.0, z=0, name="Lane evidence", t="lane")
text(4.5, 90.2, "CONTINUOUS SPATIAL PATH", fs=5.6, bold=True, color=BLUE["dark"], ha="left")
text(4.5, 44.2, "EXPLICIT EVIDENCE PATH", fs=5.6, bold=True, color=GREEN["dark"], ha="left")

yT, yB = 70.5, 25.0

# ------------------------------------------------------------------ inputs
rs = rbox(6, 57, 27, 28, "#FFFFFF", "#AFC4DA", lw=0.6, r=1.6, name="Input imagery")
for k, (dx, dy, fc) in enumerate([(3.0, -2.6, BLUE["pale"]), (1.5, -1.3, BLUE["mid"]), (0, 0, BLUE["dark"])]):
    bx, by = 13.0 + dx, 74.5 + dy
    poly([(bx, by), (bx + 9, by), (bx + 11, by + 6), (bx + 2, by + 6)], fc, "#FFFFFF", lw=0.5, z=3 + k,
         name="Image tile")
p0, p1, p3 = (13.0, 74.5), (22.0, 74.5), (15.0, 80.5)


def on_tile(u, v):
    return (p0[0] + u * (p1[0] - p0[0]) + v * (p3[0] - p0[0]), p0[1] + u * (p1[1] - p0[1]) + v * (p3[1] - p0[1]))


for (u0, u1, v0, v1, fc) in [(0.08, 0.47, 0.12, 0.47, "#9CCB86"), (0.53, 0.92, 0.12, 0.47, "#E6D07A"),
                             (0.08, 0.47, 0.55, 0.88, "#E6D07A"), (0.53, 0.92, 0.55, 0.88, "#9CCB86")]:
    poly([on_tile(u0, v0), on_tile(u1, v0), on_tile(u1, v1), on_tile(u0, v1)], fc, None, z=7, name="Field")
text(rs["cx"], 63.2, "Remote sensing\nimagery, time series", fs=6.0)

rec = rbox(6, 11, 27, 28, "#FFFFFF", "#A9CDB1", lw=0.6, r=1.6, name="Input records")
rbox(12, 29.5, 15, 3.0, GREEN["dark"], None, r=0.5, z=3, name="Table header")
for i in range(3):
    rbox(12, 26.2 - i * 3.0, 15, 2.4, GREEN["light"], None, r=0.4, z=3, name="Table row")
text(rec["cx"], 16.0, "Soil, climate, terrain,\nmanagement records", fs=6.0)

# ------------------------------------------------------------------ encoder, H, adapter
enc = [(40, 57), (66, 63), (66, 78), (40, 84)]
poly(enc, BLUE["dark"], None, text="Geospatial\nencoder\n+ fusion", fs=6.4, name="Encoder",
     text_xy=(52.0, yT))
arrow([(rs["r"], yT), (40, yT)])
text(36.5, yT + 2.4, "S", fs=6.4, bold=True, color=BLUE["dark"])
arrow([(rec["r"], 32.5), (47, 32.5), (47, 58.6)])
text(48.8, 45.5, "M", fs=6.4, bold=True, color=GREEN["dark"], ha="left")

for layer, (off, fc) in enumerate([(1.1, BLUE["pale"]), (0.0, BLUE["mid"])]):
    for i in range(3):
        for j in range(3):
            rbox(71.5 + off + i * 3.1, yT - 4.6 + off + j * 3.1, 2.7, 2.7, fc, "#FFFFFF", lw=0.4, r=0.3,
                 z=3 + layer, name="Feature cell")
arrow([(66, yT), (71.2, yT)])
text(76.2, yT + 8.4, "H", fs=6.6, bold=True, color=BLUE["dark"])

adp = [(89, 63.0), (105, 66.0), (105, 75.0), (89, 78.0)]
poly(adp, ORANGE["light"], ORANGE["dark"], lw=0.7, text="Query\nadapter", fs=6.1, color=ORANGE["dark"],
     name="Query adapter", text_xy=(96.6, yT))
arrow([(82.2, yT), (89, yT)])

# ------------------------------------------------------------------ language decoder
llm = header_card(132, 12, 26, 74, 9.0, ORANGE, "Language\ndecoder", fs=6.2)
for i in range(5):
    rbox(136, 30 + i * 8.0, 18, 5.0, ORANGE["bar"], None, r=1.0, z=3, name="Decoder layer")
text(llm["cx"], 19.5, "pretrained LLM\n(LoRA optional)", fs=5.6, italic=True, color=ORANGE["dark"])

arrow([(105, yT), (132, yT)])
tokens(118.5, yT, 4, ORANGE["mid"], ORANGE["dark"], label="V")

# ------------------------------------------------------------------ evidence lane
mp = rbox(57, 19, 27, 14, BLUE["light"], BLUE["dark"], lw=0.7, r=1.6,
          text="Mapping head\nmaps, parcel attributes", fs=5.9, color=BLUE["dark"], name="Mapping head")
arrow([(75.7, yT - 5.2), (75.7, 51.5), (70.5, 51.5), (70.5, mp["t"])])

ev = header_card(96, 11, 24, 28, 7.0, GREEN, "Evidence", fs=6.2)
text(ev["cx"], 22.3, "observed and\npredicted values,\nretrieved\nknowledge", fs=5.7)
arrow([(mp["r"], mp["cy"]), (ev["l"], mp["cy"])])
arrow([(rec["r"], 15.0), (ev["l"], 15.0)])
text(47.0, 16.9, "observed", fs=5.5, italic=True, color=GREEN["dark"])
text(90.0, mp["cy"] + 2.0, "predicted", fs=5.3, italic=True, color=GREEN["dark"])

arrow([(ev["r"], yB), (132, yB)])
tokens(126.0, yB, 3, GREEN["mid"], GREEN["dark"], size=2.2, gap=0.6, label="T")

# ------------------------------------------------------------------ output
out = header_card(163, 25, 18, 46, 7.0, GRAY, "Output", fs=6.2)
shade = ["#DCE8F4", "#9DBBD9", "#5D89B8"]
gx0, gy0, cw, ch, g = 166.6, 44.0, 3.2, 2.0, 0.45
for j in range(6):
    for i in range(3):
        rbox(gx0 + i * (cw + g), gy0 + (5 - j) * (ch + g), cw, ch, shade[i], None, r=0.25, z=3,
             name="Assessment cell")
text(out["cx"], 40.2, "D1–D6 × L1–L3", fs=5.5, bold=True, color=GRAY["dark"])
text(out["cx"], 32.0, "scoped,\nevidence-\nchecked", fs=5.4, italic=True, color=GRAY["dark"])
arrow([(llm["r"], 48.0), (out["l"], 48.0)])

for ext in ("pdf", "svg"):
    fig.savefig(f"/tmp/v18/Fig3_CroplandGPT_architecture.{ext}")
fig.savefig("/tmp/v18/Fig3_CroplandGPT_architecture.png", dpi=600)
fig.savefig("/tmp/v18/Fig3_CroplandGPT_architecture_300dpi.png", dpi=300)
fig.savefig("/tmp/v18/Fig3_preview.png", dpi=170)

from visio_writer import write_vsdx

write_vsdx(SCENE, {}, W, H, "/tmp/v18/Fig3_CroplandGPT_architecture.vsdx", page_name="Fig. 3")
print("ok")

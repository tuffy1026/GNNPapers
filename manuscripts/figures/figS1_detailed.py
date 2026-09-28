import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.lines import Line2D

plt.rcParams.update({
    "font.family": "Liberation Sans",
    "mathtext.fontset": "custom",
    "mathtext.rm": "Liberation Sans",
    "mathtext.it": "Liberation Sans:italic",
    "mathtext.bf": "Liberation Sans:bold",
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
})

W_MM, H_MM = 184, 202
COL = {
    "eo": ("#DCE9F5", "#4A78A8"),
    "aux": ("#DFF0E3", "#4E8A5E"),
    "att": ("#FBEFC7", "#B08A1E"),
    "lang": ("#E8E1F3", "#6E58A0"),
    "out": ("#EEEEEE", "#6B6B6B"),
}
LINE = "#3C3C3C"
FS = 6.6

fig = plt.figure(figsize=(W_MM / 25.4, H_MM / 25.4))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W_MM)
ax.set_ylim(0, H_MM)
ax.set_aspect("equal")
ax.axis("off")


SCENE = []


def box(x, y, w, h, text, kind, fs=FS, bold=False, ls="-"):
    SCENE.append(dict(t="box", x=x, y=y, w=w, h=h, text=text, kind=kind, fs=fs, bold=bold, dashed=ls != "-"))
    fc, ec = COL[kind]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=fc, ec=ec, lw=0.7, ls=ls, zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", zorder=3, linespacing=1.25)
    return dict(l=x, r=x + w, b=y, t=y + h, cx=x + w / 2, cy=y + h / 2)


def path(points, dashed=False, head=True, color=LINE):
    SCENE.append(dict(t="path", pts=list(points), dashed=dashed, head=head))
    ls = (0, (2.5, 1.6)) if dashed else "-"
    for (x0, y0), (x1, y1) in zip(points[:-2], points[1:-1]):
        ax.add_line(Line2D([x0, x1], [y0, y1], color=color, lw=0.7, ls=ls, zorder=1,
                           solid_capstyle="butt"))
    ax.add_patch(FancyArrowPatch(points[-2], points[-1],
                                 arrowstyle="-|>,head_length=1.6,head_width=0.9" if head else "-",
                                 mutation_scale=1, color=color, lw=0.7, ls=ls,
                                 shrinkA=0, shrinkB=0, zorder=1))


def label(x, y, text, fs=6.0, ha="center", va="center", style="normal", rot=0, color="#222222", bold=False):
    SCENE.append(dict(t="text", x=x, y=y, text=text, fs=fs, ha=ha, va=va, italic=style == "italic", rot=rot,
                      color=color, bold=bold))
    return ax.text(x, y, text, ha=ha, va=va, fontsize=fs, style=style, rotation=rot, color=color, zorder=4,
                   fontweight="bold" if bold else "normal")


def seg(points):
    path(points, head=False)


def plus(cx, cy, r=2.0):
    SCENE.append(dict(t="plus", cx=cx, cy=cy, r=r))
    ax.add_patch(Circle((cx, cy), r, fc="white", ec=LINE, lw=0.7, zorder=3))
    ax.add_line(Line2D([cx - r * 0.6, cx + r * 0.6], [cy, cy], color=LINE, lw=0.7, zorder=4))
    ax.add_line(Line2D([cx, cx], [cy - r * 0.6, cy + r * 0.6], color=LINE, lw=0.7, zorder=4))


def panel_frame(x, y, w, h, title):
    SCENE.append(dict(t="frame", x=x, y=y, w=w, h=h))
    ax.add_patch(Rectangle((x, y), w, h, fc="none", ec="#C8C8C8", lw=0.5, zorder=0))
    label(x + 1.5, y + h - 1.5, title, ha="left", va="top", fs=7.6, color="#000000", bold=True)


# ---------------------------------------------------------------- panel (a)
panel_frame(2, 122, 180, 78, "(a) Shared representation and prediction within a cropland analysis unit")

hr = box(5, 175, 33, 11, "High-resolution imagery\n(visual anchor)", "eo")
ts = box(5, 160, 33, 11, "Multi-resolution\nEO time series", "eo")
ax_in = box(5, 145, 33, 11, "Soil, weather, terrain,\nmanagement events", "aux")

gfm = box(48, 160, 34, 26, "GFM-inspired\ngeospatial encoder\n(patch and\ntemporal tokens)", "eo")
menc = box(48, 145, 34, 11, "Modality encoders\n+ context embeddings", "aux")

fus = box(94, 145, 26, 41, "Spatial fusion\nblock\n" + r"$\times\,L_f$" + "\n(panel b)", "att")

dec = box(136, 175, 40, 11, "Spatial decoder\nelement maps", "eo")
pool = box(136, 160, 40, 11, "Parcel pooling\nattribute heads", "eo")
htag = box(136, 145, 40, 11, "Shared features " + r"$H$" + "\nto panel (c)", "lang")

ev = box(48, 128, 128, 10,
         "Evidence records " + r"$E$" + ": observed and predicted values with units, dates, "
         "spatial support and source IDs  (to panel c)", "aux")

path([(hr["r"], hr["cy"]), (gfm["l"], hr["cy"])])
path([(ts["r"], ts["cy"]), (gfm["l"], ts["cy"])])
path([(ax_in["r"], ax_in["cy"]), (menc["l"], ax_in["cy"])])
path([(gfm["r"], 173), (fus["l"], 173)])
label(88, 175.4, r"$S$: $N\times d_g$", fs=5.8)
path([(menc["r"], menc["cy"]), (fus["l"], menc["cy"])])
label(88, 153.0, r"$M$: $N_m\times d_g$", fs=5.8)

bus_x = 128
seg([(fus["r"], 165.5), (bus_x, 165.5)])
seg([(bus_x, htag["cy"]), (bus_x, dec["cy"])])
for tgt in (dec, pool, htag):
    path([(bus_x, tgt["cy"]), (tgt["l"], tgt["cy"])])
label(bus_x + 1.2, 158.0, r"$H$: $N\times d_g$", fs=5.8, ha="left")

path([(gfm["cx"], gfm["t"]), (gfm["cx"], 190.5), (156, 190.5), (156, dec["t"])])
label(107, 192.3, "multiscale skip features", fs=5.8, style="italic")
label(151, pool["t"] + 1.8, r"parcel masks $A$", fs=5.6, style="italic", ha="center")

path([(ax_in["cx"], ax_in["b"]), (ax_in["cx"], ev["cy"]), (ev["l"], ev["cy"])])
label(ax_in["cx"] + 1.2, 140.5, "observed", fs=5.6, ha="left", style="italic")
rb = 179.5
seg([(dec["r"], dec["cy"]), (rb, dec["cy"])])
seg([(pool["r"], pool["cy"]), (rb, pool["cy"])])
path([(rb, dec["cy"]), (rb, ev["cy"]), (ev["r"], ev["cy"])])
label(rb - 1.2, 141.5, "predicted", fs=5.6, ha="right", style="italic")

label(92, 124.6, "Position, time, scale and validity stay attached to every feature and evidence record.",
      fs=5.9, style="italic", color="#444444")

# ---------------------------------------------------------------- panel (b)
panel_frame(2, 9, 86, 110, r"(b) Spatial fusion block ($\times\,L_f$)")
cx = 52
bw = 32


def sbox(yc, h, text, kind):
    return box(cx - bw / 2, yc - h / 2, bw, h, text, kind)


s_tok = sbox(16, 8, r"Spatial tokens $S$", "eo")
p1 = 27
plus(cx, p1)
posb = box(6, p1 - 4, 24, 8, "Position, time,\nscale embeddings", "aux")
path([(posb["r"], p1), (cx - 2.0, p1)])
path([(cx, s_tok["t"]), (cx, p1 - 2.0)])

ln1 = sbox(35, 5.5, "LayerNorm", "aux")
path([(cx, p1 + 2.0), (cx, ln1["b"])])
ca = sbox(46, 8, "Cross-attention", "att")
path([(cx, ln1["t"]), (cx, ca["b"])])
label(cx + 1.5, 40.3, r"$Q$", fs=5.8, ha="left")

kv = box(6, 51, 24, 9, "LayerNorm\n" + r"($M$ + context)", "aux")
path([(kv["r"], kv["cy"]), (33, kv["cy"]), (33, 47.5), (ca["l"], 47.5)])
label(31.5, 57.3, r"$K, V$", fs=5.8, ha="left")
mask = box(6, 39, 24, 7, "Support mask", "out")
path([(mask["r"], mask["cy"]), (ca["l"], 44.0)], dashed=True)

p2 = 56
plus(cx, p2)
path([(cx, ca["t"]), (cx, p2 - 2.0)])
ln2 = sbox(63.5, 5.5, "LayerNorm", "aux")
path([(cx, p2 + 2.0), (cx, ln2["b"])])
sa = sbox(74, 8, "Spatial self-attention", "att")
path([(cx, ln2["t"]), (cx, sa["b"])])
p3 = 84
plus(cx, p3)
path([(cx, sa["t"]), (cx, p3 - 2.0)])
ln3 = sbox(91.5, 5.5, "LayerNorm", "aux")
path([(cx, p3 + 2.0), (cx, ln3["b"])])
ff = sbox(101, 7, "Feed-forward", "att")
path([(cx, ln3["t"]), (cx, ff["b"])])
p4 = 109.5
plus(cx, p4)
path([(cx, ff["t"]), (cx, p4 - 2.0)])
label(cx, 115.3, r"$H$: $N\times d_g$", fs=6.2, ha="center")
path([(cx, p4 + 2.0), (cx, 113.5)])

rx = cx + bw / 2 + 4
for y0, y1 in ((p1 + 2.8, p2), (p2 + 2.8, p3), (p3 + 2.8, p4)):
    seg([(cx, y0), (rx, y0), (rx, y1)])
    path([(rx, y1), (cx + 2.0, y1)])
label(rx + 1.2, 70, "residual", fs=5.6, style="italic", ha="left", rot=90)

# ---------------------------------------------------------------- panel (c)
panel_frame(92, 9, 90, 110, "(c) Vision-language interface")

hbox = box(95, 96, 21, 9, r"$H$: $N\times d_g$" + "\n(from a)", "eo")
qbox = box(119, 96, 20, 9, "Learned queries\n" + r"$K\times d_g$", "lang")
qr = box(95, 78, 44, 9, "Query resampler  " + r"$\times\,L_q$", "att")
path([(hbox["cx"], hbox["b"]), (hbox["cx"], qr["t"])])
label(hbox["cx"] + 1.2, 91.5, r"$K, V$", fs=5.8, ha="left")
path([(qbox["cx"], qbox["b"]), (qbox["cx"], qr["t"])])
label(qbox["cx"] + 1.2, 91.5, r"$Q$", fs=5.8, ha="left")
proj = box(99, 60, 36, 8, "MLP projector", "lang")
path([(qr["cx"], qr["b"]), (qr["cx"], proj["t"])])
label(qr["cx"] + 1.5, 72.8, r"$Z$: $K\times d_g$", fs=5.8, ha="left")

qq = box(143, 98, 34, 8, "Question, objective,\nassessment criteria", "out")
eb = box(143, 87, 34, 8, "Evidence records " + r"$E$" + "\n(from a)", "aux")
kb = box(143, 76, 34, 8, "Knowledge base\nand retriever", "aux")
ser = box(143, 60, 34, 8, "Serialize + tokenize", "lang")
tb = 180
for b_ in (qq, eb, kb):
    seg([(b_["r"], b_["cy"]), (tb, b_["cy"])])
path([(tb, qq["cy"]), (tb, ser["cy"]), (ser["r"], ser["cy"])])

llm = box(95, 39, 82, 13, "Pretrained language decoder\n(causal self-attention + FFN; optional LoRA adaptation)\n"
          + r"prefix $[V; T]$: $(K+U)\times d_l$", "lang")
path([(proj["cx"], proj["b"]), (proj["cx"], llm["t"])])
label(proj["cx"] + 1.5, 56.0, r"$V$: $K\times d_l$", fs=5.8, ha="left")
path([(ser["cx"], ser["b"]), (ser["cx"], llm["t"])])
label(ser["cx"] + 1.5, 56.0, r"$T$: $U\times d_l$", fs=5.8, ha="left")

chk = box(102, 27, 68, 7, "Evidence check against " + r"$E$" + ": values, units, dates, support", "out")
path([(llm["cx"], llm["b"]), (llm["cx"], chk["t"])])
outb = box(95, 12, 82, 11, "Scoped statements indexed by D1–D6 × L1–L3\nwith source IDs and evidence status",
           "out")
path([(chk["cx"], chk["b"]), (chk["cx"], outb["t"])])

# ---------------------------------------------------------------- legend
items = [("eo", "EO and spatial features"), ("aux", "Auxiliary data and evidence"),
         ("att", "Attention and fusion"), ("lang", "Language modules"), ("out", "Queries, masks and outputs")]
renderer = fig.canvas.get_renderer()
mm_per_px = W_MM / fig.bbox.width
x = 4
for kind, text in items:
    fc, ec = COL[kind]
    SCENE.append(dict(t="swatch", x=x, y=3, w=3.2, h=3.2, kind=kind))
    ax.add_patch(Rectangle((x, 3), 3.2, 3.2, fc=fc, ec=ec, lw=0.6))
    t = label(x + 4.2, 4.6, text, fs=5.8, ha="left", color="#000000")
    x += 4.2 + t.get_window_extent(renderer).width * mm_per_px + 3.5
plus(x + 1.6, 4.6, r=1.6)
t = label(x + 4.2, 4.6, "addition (residual)", fs=5.8, ha="left", color="#000000")
x += 4.2 + t.get_window_extent(renderer).width * mm_per_px + 3.5
path([(x, 4.6), (x + 6, 4.6)], dashed=True, head=False)
label(x + 7, 4.6, "mask", fs=5.8, ha="left", color="#000000")

for ext in ("pdf", "png", "svg"):
    fig.savefig(f"/tmp/v18/FigS1_CroplandGPT_architecture_detailed.{ext}", dpi=600 if ext == "png" else None)
fig.savefig("/tmp/v18/FigS1_CroplandGPT_architecture_detailed_300dpi.png", dpi=300)
fig.savefig("/tmp/v18/FigS1_preview.png", dpi=150)

from visio_writer import write_vsdx

write_vsdx(SCENE, COL, W_MM, H_MM, "/tmp/v18/FigS1_CroplandGPT_architecture_detailed.vsdx", page_name="Fig. S1")
print("ok")

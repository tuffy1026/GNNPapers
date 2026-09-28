import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle, Polygon

plt.rcParams.update({
    "font.family": "Liberation Sans",
    "mathtext.fontset": "custom",
    "mathtext.rm": "Liberation Sans",
    "mathtext.it": "Liberation Sans:italic",
    "mathtext.bf": "Liberation Sans:bold",
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
})

COL = {
    "eo": ("#DCE9F5", "#4A78A8"),
    "aux": ("#DFF0E3", "#4E8A5E"),
    "att": ("#FBEFC7", "#B08A1E"),
    "lang": ("#E8E1F3", "#6E58A0"),
    "out": ("#EEEEEE", "#6B6B6B"),
    "white": ("#FFFFFF", "#6B6B6B"),
}
LINE = "#3C3C3C"
DASH = (0, (2.5, 1.6))
FS = 6.6


class Canvas:
    def __init__(self, w_mm, h_mm):
        self.w, self.h = w_mm, h_mm
        self.fig = plt.figure(figsize=(w_mm / 25.4, h_mm / 25.4))
        ax = self.fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, w_mm)
        ax.set_ylim(0, h_mm)
        ax.set_aspect("equal")
        ax.axis("off")
        self.ax = ax
        self.scene = []

    def box(self, x, y, w, h, text, kind, fs=FS, bold=False, ls="-", align="center", lw=0.7):
        self.scene.append(dict(t="box", x=x, y=y, w=w, h=h, text=text, kind=kind, fs=fs, bold=bold,
                               dashed=ls != "-"))
        fc, ec = COL[kind]
        self.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                                         fc=fc, ec=ec, lw=lw, ls=ls, zorder=2))
        if text:
            tx = x + w / 2 if align == "center" else x + 2
            self.ax.text(tx, y + h / 2, text, ha=align, va="center", fontsize=fs,
                         fontweight="bold" if bold else "normal", zorder=3, linespacing=1.25)
        return dict(l=x, r=x + w, b=y, t=y + h, cx=x + w / 2, cy=y + h / 2)

    def line(self, pts, dashed=False, color=LINE, lw=0.7, z=1):
        self.scene.append(dict(t="path", pts=list(pts), dashed=dashed, head=False, color=color, lw=lw))
        xs, ys = zip(*pts)
        self.ax.add_line(Line2D(xs, ys, color=color, lw=lw, ls=DASH if dashed else "-", zorder=z))

    def path(self, pts, dashed=False, color=LINE):
        self.scene.append(dict(t="path", pts=list(pts), dashed=dashed, head=True, color=color, lw=0.7))
        if len(pts) > 2:
            xs, ys = zip(*pts[:-1])
            self.ax.add_line(Line2D(xs, ys, color=color, lw=0.7, ls=DASH if dashed else "-", zorder=1))
        self.ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle="-|>,head_length=1.6,head_width=0.9",
                                          mutation_scale=1, color=color, lw=0.7,
                                          ls=DASH if dashed else "-", shrinkA=0, shrinkB=0, zorder=1))

    def label(self, x, y, text, fs=6.0, ha="center", va="center", style="normal", rot=0,
              color="#222222", bold=False):
        self.scene.append(dict(t="text", x=x, y=y, text=text, fs=fs, ha=ha, va=va, italic=style == "italic",
                               rot=rot, color=color, bold=bold))
        return self.ax.text(x, y, text, ha=ha, va=va, fontsize=fs, style=style, rotation=rot, color=color,
                            zorder=4, fontweight="bold" if bold else "normal", linespacing=1.25)

    def dot(self, x, y):
        self.ax.add_patch(Circle((x, y), 0.6, fc=LINE, ec=LINE, zorder=4))

    def frame(self, x, y, w, h, title=None, fc="none"):
        self.scene.append(dict(t="frame", x=x, y=y, w=w, h=h))
        self.ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec="#C8C8C8", lw=0.5, zorder=0))
        if title:
            self.label(x + 1.5, y + h - 1.5, title, fs=7.6, ha="left", va="top", color="#000000", bold=True)

    def rect(self, x, y, w, h, fc, ec="none", lw=0.5, z=2):
        self.ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, zorder=z))

    def poly(self, pts, fc, ec="#6B6B6B", lw=0.4, z=2):
        self.ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, lw=lw, zorder=z))

    def legend(self, items, y=4.6, x=4, dashed_label=None):
        renderer = self.fig.canvas.get_renderer()
        mm_per_px = self.w / self.fig.bbox.width
        for kind, text in items:
            fc, ec = COL[kind]
            self.scene.append(dict(t="swatch", x=x, y=y - 1.6, w=3.2, h=3.2, kind=kind))
            self.ax.add_patch(Rectangle((x, y - 1.6), 3.2, 3.2, fc=fc, ec=ec, lw=0.6))
            t = self.label(x + 4.2, y, text, fs=5.8, ha="left", color="#000000")
            x += 4.2 + t.get_window_extent(renderer).width * mm_per_px + 5.0
        if dashed_label:
            self.line([(x, y), (x + 6, y)], dashed=True)
            self.label(x + 7, y, dashed_label, fs=5.8, ha="left", color="#000000")

    def save(self, stem):
        for ext in ("pdf", "svg"):
            self.fig.savefig(f"/tmp/v18/{stem}.{ext}")
        self.fig.savefig(f"/tmp/v18/{stem}.png", dpi=600)
        self.fig.savefig(f"/tmp/v18/{stem}_300dpi.png", dpi=300)
        self.fig.savefig(f"/tmp/v18/{stem}_preview.png", dpi=150)

    def save_vsdx(self, stem, page_name):
        from visio_writer import write_vsdx

        write_vsdx(self.scene, COL, self.w, self.h, f"/tmp/v18/{stem}.vsdx", page_name=page_name)

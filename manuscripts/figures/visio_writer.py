"""Write a recorded figure scene as a native Visio (.vsdx) drawing.

Every box, line, arrow, addition symbol and label becomes an editable Visio shape.
Coordinates are in millimetres with the origin at the bottom-left, as in Visio.
"""
import math
import re
import shutil
import zipfile
from xml.sax.saxutils import escape

import vsdx

TEMPLATE = __import__("os").path.join(__import__("os").path.dirname(vsdx.__file__), "media", "media.vsdx")
NS = ("xmlns='http://schemas.microsoft.com/office/visio/2012/main' "
      "xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships' xml:space='preserve'")
FONT = "Arial"
LINE = "#3C3C3C"
PT = 1 / 72.0
ARROW = 4  # filled triangular arrowhead


def inch(mm):
    return mm / 25.4


def f(v):
    return repr(round(float(v), 6))


def cell(n, v, u=None):
    return f"<Cell N='{n}' V='{v}'" + (f" U='{u}'" if u else "") + "/>"


def math_runs(s, italic=False, bold=False):
    """Convert matplotlib-style text with $...$ math into (text, italic, bold, subscript) runs."""
    runs = []
    parts = s.split("$")
    for k, part in enumerate(parts):
        if k % 2 == 0:
            if part:
                runs.append([part, italic, bold, False])
            continue
        i, out = 0, []
        while i < len(part):
            ch = part[i]
            if part.startswith(r"\times", i):
                prev = out[-1][0][-1:] if out and out[-1][0] else ""
                out.append([" × " if prev.isalnum() or prev == ")" else "×", False, bold, False])
                i += len(r"\times")
                while i < len(part) and part[i] == " ":
                    i += 1
            elif part.startswith(r"\,", i):
                out.append([" ", False, bold, False])
                i += 2
            elif ch == "_":
                if part[i + 1] == "{":
                    j = part.index("}", i)
                    sub = part[i + 2:j]
                    i = j + 1
                else:
                    sub = part[i + 1]
                    i += 2
                out.append([sub, True, bold, True])
            elif ch == "+":
                out.append([" + ", False, bold, False])
                i += 1
            elif ch.isalpha():
                out.append([ch, True, bold, False])
                i += 1
            else:
                out.append([ch, False, bold, False])
                i += 1
        runs.extend(out)
    merged = []
    for r in runs:
        if merged and merged[-1][1:] == r[1:]:
            merged[-1][0] += r[0]
        else:
            merged.append(list(r))
    return merged


def text_xml(runs, size_pt, color, halign=1, valign=1, margins_pt=0.0, spline=-1.2):
    """Character/Paragraph/TextBlock sections and the <Text> element for a list of runs."""
    chars, body = [], []
    for ix, (txt, it, bd, sub) in enumerate(runs):
        style = (1 if bd else 0) | (2 if it else 0)
        chars.append(f"<Row IX='{ix}'>" + cell("Font", FONT) + cell("Size", f(size_pt * PT), "PT")
                     + cell("Color", color) + cell("Style", style) + cell("Pos", 2 if sub else 0) + "</Row>")
        body.append(f"<cp IX='{ix}'/>" + escape(txt))
    m = f(margins_pt * PT)
    tb = ("".join(cell(n, m, "PT") for n in ("LeftMargin", "RightMargin", "TopMargin", "BottomMargin"))
          + cell("VerticalAlign", valign))
    para = f"<Section N='Paragraph'><Row IX='0'>{cell('HorzAlign', halign)}{cell('SpLine', spline)}</Row></Section>"
    return tb, "<Section N='Character'>" + "".join(chars) + "</Section>" + para, "<Text>" + "".join(body) + "</Text>"


class Page:
    def __init__(self):
        self.shapes = []
        self.next_id = 1

    def add(self, name, x, y, w, h, cells, sections="", text="", angle=0.0):
        sid = self.next_id
        self.next_id += 1
        xml = (f"<Shape ID='{sid}' NameU='{name}.{sid}' Name='{name}.{sid}' Type='Shape' LineStyle='3' "
               f"FillStyle='3' TextStyle='3'>"
               + cell("PinX", f(inch(x + w / 2))) + cell("PinY", f(inch(y + h / 2)))
               + cell("Width", f(inch(w))) + cell("Height", f(inch(h)))
               + f"<Cell N='LocPinX' V='{f(inch(w / 2))}' F='Width*0.5'/>"
               + f"<Cell N='LocPinY' V='{f(inch(h / 2))}' F='Height*0.5'/>"
               + cell("Angle", f(angle)) + cells + sections + text + "</Shape>")
        self.shapes.append(xml)


def line_cells(color=LINE, weight_pt=0.7, dashed=False, end_arrow=0, fill=None, rounding_mm=0.0):
    c = (cell("LineWeight", f(weight_pt * PT), "PT") + cell("LineColor", color)
         + cell("LinePattern", 2 if dashed else 1) + cell("LineCap", 0)
         + cell("Rounding", f(inch(rounding_mm)), "MM")
         + cell("BeginArrow", 0) + cell("EndArrow", end_arrow) + cell("EndArrowSize", 0))
    if fill is None:
        c += cell("FillPattern", 0)
    else:
        c += cell("FillForegnd", fill) + cell("FillPattern", 1)
    return c + cell("ShdwPattern", 0)


def rect_geometry(no_fill=False, no_line=False):
    return ("<Section N='Geometry' IX='0'>" + cell("NoFill", int(no_fill)) + cell("NoLine", int(no_line))
            + cell("NoShow", 0) + cell("NoSnap", 0)
            + "<Row T='RelMoveTo' IX='1'><Cell N='X' V='0'/><Cell N='Y' V='0'/></Row>"
            + "<Row T='RelLineTo' IX='2'><Cell N='X' V='1'/><Cell N='Y' V='0'/></Row>"
            + "<Row T='RelLineTo' IX='3'><Cell N='X' V='1'/><Cell N='Y' V='1'/></Row>"
            + "<Row T='RelLineTo' IX='4'><Cell N='X' V='0'/><Cell N='Y' V='1'/></Row>"
            + "<Row T='RelLineTo' IX='5'><Cell N='X' V='0'/><Cell N='Y' V='0'/></Row></Section>")


def est_text_size(runs, fs):
    lines = "".join(r[0] for r in runs).split("\n")
    w = max(len(l) for l in lines) * fs * 0.75 * 25.4 / 72 + 3
    h = len(lines) * fs * 1.25 * 25.4 / 72 + 0.8
    return w, h


def write_vsdx(scene, col, w_mm, h_mm, out):
    page = Page()
    order = {"frame": 0, "path": 1, "box": 2, "swatch": 2, "plus": 3, "text": 4}
    for it in sorted(scene, key=lambda d: order[d["t"]]):
        t = it["t"]
        if t == "frame":
            page.add("Panel frame", it["x"], it["y"], it["w"], it["h"],
                     line_cells("#C8C8C8", 0.5), rect_geometry(no_fill=True))
        elif t in ("box", "swatch"):
            fc, ec = col[it["kind"]]
            if t == "box":
                runs = math_runs(it["text"], bold=it["bold"])
                tb, sec, txt = text_xml(runs, it["fs"], "#000000", margins_pt=1.0)
                page.add("Box", it["x"], it["y"], it["w"], it["h"],
                         line_cells(ec, 0.7, it["dashed"], fill=fc, rounding_mm=1.2) + tb,
                         rect_geometry() + sec, txt)
            else:
                page.add("Legend swatch", it["x"], it["y"], it["w"], it["h"],
                         line_cells(ec, 0.6, fill=fc), rect_geometry())
        elif t == "path":
            pts = it["pts"]
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            x0, y0 = min(xs), min(ys)
            w, h = max(max(xs) - x0, 0.01), max(max(ys) - y0, 0.01)
            rows = []
            for k, (px, py) in enumerate(pts):
                rt = "MoveTo" if k == 0 else "LineTo"
                rows.append(f"<Row T='{rt}' IX='{k + 1}'>" + cell("X", f(inch(px - x0)))
                            + cell("Y", f(inch(py - y0))) + "</Row>")
            geom = ("<Section N='Geometry' IX='0'>" + cell("NoFill", 1) + cell("NoLine", 0) + cell("NoShow", 0)
                    + cell("NoSnap", 0) + "".join(rows) + "</Section>")
            page.add("Arrow" if it["head"] else "Line", x0, y0, w, h,
                     line_cells(LINE, 0.7, it["dashed"], end_arrow=ARROW if it["head"] else 0), geom)
        elif t == "plus":
            r = it["r"]
            d = 2 * r
            geom = ("<Section N='Geometry' IX='0'>" + cell("NoFill", 0) + cell("NoLine", 0) + cell("NoShow", 0)
                    + cell("NoSnap", 0) + "<Row T='Ellipse' IX='1'>"
                    + cell("X", f(inch(r))) + cell("Y", f(inch(r))) + cell("A", f(inch(d))) + cell("B", f(inch(r)))
                    + cell("C", f(inch(r))) + cell("D", f(inch(d))) + "</Row></Section>")
            for gi, (ax_, ay, bx, by) in enumerate(((0.4 * r, r, 1.6 * r, r), (r, 0.4 * r, r, 1.6 * r)), start=1):
                geom += (f"<Section N='Geometry' IX='{gi}'>" + cell("NoFill", 1) + cell("NoLine", 0)
                         + cell("NoShow", 0) + cell("NoSnap", 0)
                         + "<Row T='MoveTo' IX='1'>" + cell("X", f(inch(ax_))) + cell("Y", f(inch(ay))) + "</Row>"
                         + "<Row T='LineTo' IX='2'>" + cell("X", f(inch(bx))) + cell("Y", f(inch(by))) + "</Row>"
                         + "</Section>")
            page.add("Addition", it["cx"] - r, it["cy"] - r, d, d, line_cells(LINE, 0.7, fill="#FFFFFF"), geom)
        elif t == "text":
            runs = math_runs(it["text"], italic=it["italic"], bold=it["bold"])
            fs = it["fs"]
            tw, th = est_text_size(runs, fs)
            halign = {"left": 0, "center": 1, "right": 2}[it["ha"]]
            valign = {"top": 0, "center": 1, "bottom": 2}[it["va"]]
            tb, sec, txt = text_xml(runs, fs, it["color"], halign, valign)
            x, y = it["x"], it["y"]
            if it["rot"]:
                # rotated 90°: the text's left end sits at y - tw/2 after rotation about its centre
                cxm, cym = x + th / 2, y
                page.add("Label", cxm - tw / 2, cym - th / 2, tw, th,
                         line_cells(fill=None) + tb, rect_geometry(True, True) + sec, txt,
                         angle=math.radians(it["rot"]))
                continue
            lx = {"left": x, "center": x - tw / 2, "right": x - tw}[it["ha"]]
            ly = {"top": y - th, "center": y - th / 2, "bottom": y}[it["va"]]
            page.add("Label", lx, ly, tw, th, line_cells(fill=None) + tb, rect_geometry(True, True) + sec, txt)

    work = out + ".dir"
    shutil.rmtree(work, ignore_errors=True)
    with zipfile.ZipFile(TEMPLATE) as z:
        z.extractall(work)
        names = [n for n in z.namelist() if n not in ("docProps/thumbnail.emf", "visio/pages/_rels/page1.xml.rels")]

    with open(f"{work}/visio/pages/page1.xml", "w", encoding="utf-8") as fh:
        fh.write(f"<?xml version='1.0' encoding='utf-8' ?>\n<PageContents {NS}><Shapes>"
                 + "".join(page.shapes) + "</Shapes></PageContents>")

    pw, ph = inch(w_mm), inch(h_mm)
    pages = open(f"{work}/visio/pages/pages.xml", encoding="utf-8").read()
    pages = re.sub(r"<Cell N='PageWidth' V='[^']*'/>", f"<Cell N='PageWidth' V='{f(pw)}'/>", pages)
    pages = re.sub(r"<Cell N='PageHeight' V='[^']*'/>", f"<Cell N='PageHeight' V='{f(ph)}'/>", pages)
    pages = re.sub(r"ViewCenterX='[^']*'", f"ViewCenterX='{f(pw / 2)}'", pages)
    pages = re.sub(r"ViewCenterY='[^']*'", f"ViewCenterY='{f(ph / 2)}'", pages)
    pages = pages.replace("NameU='Page-1' Name='Page-1'", "NameU='Fig. 3' Name='Fig. 3'")
    open(f"{work}/visio/pages/pages.xml", "w", encoding="utf-8").write(pages)

    win = open(f"{work}/visio/windows.xml", encoding="utf-8").read()
    win = re.sub(r"ViewCenterX='[^']*'", f"ViewCenterX='{f(pw / 2)}'", win)
    win = re.sub(r"ViewCenterY='[^']*'", f"ViewCenterY='{f(ph / 2)}'", win)
    open(f"{work}/visio/windows.xml", "w", encoding="utf-8").write(win)

    doc = open(f"{work}/visio/document.xml", encoding="utf-8").read()
    if "NameU='Arial'" not in doc:
        doc = doc.replace("</FaceNames>", "<FaceName NameU='Arial' UnicodeRanges='-536859905 -1073711037 9 0' "
                          "CharSets='1073742335 -65536' Panose='2 11 6 4 2 2 2 2 2 4' Flags='325'/></FaceNames>")
    open(f"{work}/visio/document.xml", "w", encoding="utf-8").write(doc)

    rels = open(f"{work}/_rels/.rels", encoding="utf-8").read()
    rels = re.sub(r"<Relationship Id=\"rId2\" Type=\"[^\"]*thumbnail\" Target=\"docProps/thumbnail.emf\"/>", "", rels)
    open(f"{work}/_rels/.rels", "w", encoding="utf-8").write(rels)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            z.write(f"{work}/{n}", n)
    shutil.rmtree(work)
    print("wrote", out, len(page.shapes), "shapes")

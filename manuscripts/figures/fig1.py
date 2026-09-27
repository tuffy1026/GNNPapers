from figlib import Canvas, COL, LINE

c = Canvas(184, 150)

# Cropland analysis unit with a schematic of fields, infrastructure and samples
unit = c.box(4, 56, 52, 88, "", "white")
c.label(30, 140.2, "Cropland analysis unit", fs=7.0, bold=True)
c.label(30, 136.0, "500 m × 500 m, specified period", fs=5.9, style="italic")
sx, sy, sw, sh = 8, 82, 44, 50
c.rect(sx, sy, sw, sh, "#F4F1E8", ec="#9A9A9A", lw=0.5)
crop = ["#F3E3A6", "#CFE5B4", "#E9D48C", "#BFDDA0", "#F1E9C4", "#D8EABF"]
fields = [
    [(8, 132), (24, 132), (23, 114), (8, 115)],
    [(24, 132), (38, 132), (37.5, 118), (23.3, 118)],
    [(38, 132), (52, 132), (52, 120), (37.6, 119.5)],
    [(8, 112), (22.8, 111.5), (22, 96), (8, 97)],
    [(23.3, 115.5), (37.4, 115.5), (37, 100), (22.5, 100)],
    [(37.8, 117), (52, 117.5), (52, 101), (37.3, 101)],
    [(8, 94.5), (21.8, 93.5), (21.4, 82), (8, 82)],
    [(22.2, 97.5), (36.8, 97.5), (36.5, 82), (21.8, 82)],
    [(37, 98.5), (52, 98.5), (52, 82), (36.8, 82)],
]
for k, f in enumerate(fields):
    c.poly(f, crop[k % len(crop)])
c.line([(8, 113.3), (52, 118.6)], color="#4A78A8", lw=1.2, z=3)
c.line([(8, 95.8), (52, 99.8)], color="#8C8C8C", lw=1.6, z=3)
for x, y in [(15, 124), (31, 125), (45, 108), (16, 104), (29, 89), (44, 90)]:
    c.dot(x, y)
c.rect(45.5, 125.5, 3.5, 3, "#B7B7B7", ec="#6B6B6B", lw=0.4, z=3)
c.label(30, 78.6, "fields  ·  canal  ·  road  ·  soil samples  ·  facility", fs=5.5, style="italic")
c.label(30, 66.5, "Inputs: high-resolution imagery, EO time series,\nsoil, terrain, climate and dated management records",
        fs=5.8)

rep = c.box(64, 96, 36, 30, "Shared geospatial\nrepresentation\n\nGFM-inspired encoder\n+ spatial fusion", "eo")
ev = c.box(64, 58, 36, 20, "Explicit evidence\nobserved and predicted\nvalues with sources", "aux")
c.path([(unit["r"], rep["cy"]), (rep["l"], rep["cy"])])
c.path([(unit["r"], ev["cy"]), (ev["l"], ev["cy"])])

mapb = c.box(110, 114, 30, 22, "Mapping branch\n\nspatial decoder,\nparcel heads", "eo")
vlb = c.box(110, 80, 30, 22, "Vision-language\nbranch\n\nadapter + language\ndecoder", "lang")
kn = c.box(110, 56, 30, 16, "Criteria, knowledge\nand management\nconstraints", "aux")
bus = 105
c.line([(rep["r"], rep["cy"]), (bus, rep["cy"])])
c.line([(bus, vlb["cy"] + 4), (bus, mapb["cy"])])
c.dot(bus, rep["cy"])
c.path([(bus, mapb["cy"]), (mapb["l"], mapb["cy"])])
c.path([(bus, vlb["cy"] + 4), (vlb["l"], vlb["cy"] + 4)])
c.path([(ev["r"], 74), (107, 74), (107, 86), (vlb["l"], 86)])
c.path([(kn["cx"], kn["t"]), (kn["cx"], vlb["b"])])

s1 = c.box(146, 116, 35, 22, "", "out")
c.label(s1["cx"], 132.8, "Stage 1", fs=6.4, bold=True)
c.label(s1["cx"], 124.0, "Agricultural feature\nrepresentation and mapping\nwhat, where, state", fs=5.9)
s2 = c.box(146, 86, 35, 22, "", "out")
c.label(s2["cx"], 102.8, "Stage 2", fs=6.4, bold=True)
c.label(s2["cx"], 94.0, "Integrated cropland\nassessment\nagainst use and criteria", fs=5.9)
s3 = c.box(146, 56, 35, 22, "", "out")
c.label(s3["cx"], 72.8, "Stage 3", fs=6.4, bold=True)
c.label(s3["cx"], 64.0, "Management decision\nsupport\noptions under constraints", fs=5.9)
c.path([(mapb["r"], mapb["cy"]), (s1["l"], mapb["cy"])])
c.path([(vlb["r"], 97), (s2["l"], 97)])
c.path([(vlb["r"], 84), (143, 84), (143, 67), (s3["l"], 67)])
c.path([(s1["cx"], s1["b"]), (s1["cx"], s2["t"])])
c.path([(s2["cx"], s2["b"]), (s2["cx"], s3["t"])])

# Common assessment specification
c.frame(4, 9, 177, 41)
c.label(6, 46.5, "Common assessment specification", fs=7.0, bold=True, ha="left")
c.label(6, 30.5,
        "Content: six assessment\ndimensions (D1–D6)\n\nScope: three reasoning\nlevels (L1–L3)\n\n"
        "Each statement records its\nobject, period, sources,\nstatement type and\nevidence status.",
        fs=5.7, ha="left")
dims = ["D1 Resources and soil", "D2 Field and infrastructure", "D3 Crops and management",
        "D4 Crop growth", "D5 Yield and stability", "D6 Capacity and potential"]
levels = ["L1 State description", "L2 Cross-dimensional\ninterpretation", "L3 Conditional scenarios"]
shade = ["#EEF3F8", "#DCE6F1", "#C8D8EA"]
mx, rowlab_w, colw, top, hh, rh = 44, 40, 28, 43, 6.4, 4.5
for j, lv in enumerate(levels):
    x0 = mx + rowlab_w + j * colw
    c.rect(x0, top - hh, colw, hh, "#FFFFFF", ec="#9A9A9A")
    c.label(x0 + colw / 2, top - hh / 2, lv, fs=5.7, bold=True)
for i, d in enumerate(dims):
    y0 = top - hh - (i + 1) * rh
    c.rect(mx, y0, rowlab_w, rh, "#FFFFFF", ec="#9A9A9A")
    c.label(mx + 1.5, y0 + rh / 2, d, fs=5.7, ha="left")
    for j in range(3):
        c.rect(mx + rowlab_w + j * colw, y0, colw, rh, shade[j], ec="#9A9A9A")
c.label(mx + rowlab_w + 1.5 * colw, 45.6, "increasing synthesis and evidence requirements  →", fs=5.6,
        style="italic")
c.label(175, 27, "applies to\nexpert\nannotations\nand model\noutputs", fs=5.6, style="italic")
c.path([(125, 50), (125, 56)], dashed=True)
c.path([(163.5, 50), (163.5, 56)], dashed=True)

c.legend([("eo", "Spatial representation and mapping"), ("aux", "Evidence and knowledge"),
          ("lang", "Language branch"), ("out", "Functional stages")], y=4.4,
         dashed_label="structures annotation and output")
c.save("Fig1_CroplandGPT_framework")
print("ok")

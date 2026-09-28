from figlib import Canvas

c = Canvas(184, 118)

# Lane backgrounds
c.frame(4, 70, 177, 42, fc="#FAFAFA")
c.frame(4, 12, 177, 40, fc="#FAFAFA")
c.label(6, 109.5, "Dataset development", fs=7.4, bold=True, ha="left", va="top")
c.label(6, 49.5, "Query-time assessment", fs=7.4, bold=True, ha="left", va="top")

a1 = c.box(8, 76, 30, 22, "Source records\n\nimagery, soil,\nmanagement, yield,\nliterature", "eo")
a2 = c.box(44, 76, 28, 22, "Screening and\nquality control\n\nunits, dates,\nsupport, validity", "aux")
a3 = c.box(78, 76, 32, 22, "Spatial, object and\ntemporal linking\n\nshared CRS, field IDs,\nobservation periods", "aux")
a4 = c.box(116, 76, 32, 22, "Reviewed expert\nannotations\n\ncommon definitions\nD1–D6 × L1–L3", "out")
ev = c.box(154, 76, 24, 22, "Independent\nevaluation\nevidence\n\nheld out", "white", ls=(0, (2.5, 1.6)))
for s, t in ((a1, a2), (a2, a3), (a3, a4)):
    c.path([(s["r"], s["cy"]), (t["l"], t["cy"])])

model = c.box(48, 54, 100, 12, "Shared representations\ngeospatial encoder and fusion  ·  mapping branch  ·  "
              "vision-language branch", "lang")
c.path([(a3["cx"], a3["b"]), (a3["cx"], model["t"])])
c.label(a3["cx"] + 1.2, 71.0, "curated records", fs=5.6, style="italic", ha="left")
c.path([(a4["cx"], a4["b"]), (a4["cx"], model["t"])])
c.label(a4["cx"] + 1.2, 71.0, "training targets", fs=5.6, style="italic", ha="left")

b1 = c.box(8, 18, 30, 22, "Query\n\nobject, period,\nobjective, requested\njudgment", "out")
b2 = c.box(44, 18, 30, 22, "Select applicable\ninputs\n\nobservations and\npermitted knowledge", "aux")
b3 = c.box(82, 18, 32, 22, "Outputs indexed by\ndimension and level\n\nmaps, attributes,\nscoped statements", "eo")
b4 = c.box(120, 18, 30, 22, "Evidence check\nand scoped\nresponse\n\nunassessed when\nunsupported", "out")
c.path([(b1["r"], b1["cy"]), (b2["l"], b2["cy"])])
c.path([(b2["cx"], b2["t"]), (b2["cx"], model["b"])])
c.path([(b3["cx"], model["b"]), (b3["cx"], b3["t"])])
c.path([(b3["r"], b3["cy"]), (b4["l"], b4["cy"])])

c.path([(ev["cx"], ev["b"]), (ev["cx"], b4["cy"]), (b4["r"], b4["cy"])], dashed=True)
c.label(ev["cx"] + 1.2, 45.0, "evaluation\nonly", fs=5.6, style="italic", ha="left")

c.label(92, 7.5, "Training targets, model-input knowledge and independent evaluation evidence are kept separate; "
        "target-bearing records never enter the query-time inputs.", fs=5.9, style="italic", color="#444444")
c.legend([("eo", "Spatial data and outputs"), ("aux", "Preparation and input selection"),
          ("lang", "Shared model"), ("out", "Queries, annotations and checks")], y=2.8,
         dashed_label="evaluation path")
c.save("Fig2_CroplandGPT_pathways")
print("ok")

from figlib import Canvas

c = Canvas(184, 100)

eo = c.box(4, 68, 30, 18, "Remote sensing\nimagery and\ntime series", "eo")
aux = c.box(4, 44, 30, 18, "Soil, climate,\nterrain and\nmanagement records", "aux")

enc = c.box(42, 44, 32, 48, "", "eo")
c.label(enc["cx"], 81.5, "Shared geospatial\nencoder\n+ spatial fusion", fs=6.6)
c.label(enc["cx"], 58.0, "cross-attention\nself-attention\nfeed-forward\n" + r"($\times\,L$)", fs=5.7,
        style="italic", color="#444444")

ad = c.box(82, 72, 30, 16, "Query adapter\n(resampler +\nprojector)", "att")
mp = c.box(82, 44, 30, 16, "Mapping branch\nelement maps,\nparcel attributes", "eo")
llm = c.box(120, 44, 30, 48, "Pretrained\nlanguage\ndecoder", "lang")
out = c.box(158, 44, 23, 48, "Scoped\nassessment\n\nmaps, attributes\nand statements\n\nD1–D6 × L1–L3\nwith sources",
            "out", fs=6.0)

ev = c.box(42, 16, 70, 14, "Evidence records: observed and predicted values\nwith units, dates, spatial support and sources",
           "aux", fs=6.2)
kb = c.box(120, 16, 30, 14, "Knowledge retrieval\ncriteria and\napplicability", "aux", fs=6.2)

c.path([(eo["r"], eo["cy"]), (enc["l"], eo["cy"])])
c.label(38, eo["cy"] + 2.0, r"$S$", fs=6.0)
c.path([(aux["r"], aux["cy"]), (enc["l"], aux["cy"])])
c.label(38, aux["cy"] + 2.0, r"$M$", fs=6.0)

c.path([(enc["r"], ad["cy"]), (ad["l"], ad["cy"])])
c.label(78, ad["cy"] + 2.0, r"$H$", fs=6.0)
c.path([(enc["r"], mp["cy"]), (mp["l"], mp["cy"])])
c.label(78, mp["cy"] + 2.0, r"$H$", fs=6.0)

c.path([(ad["r"], ad["cy"]), (llm["l"], ad["cy"])])
c.label(116, ad["cy"] + 2.0, r"$V$", fs=6.0)

c.path([(aux["cx"], aux["b"]), (aux["cx"], ev["cy"]), (ev["l"], ev["cy"])])
c.label(aux["cx"] + 1.2, 37.0, "observed", fs=5.6, style="italic", ha="left")
c.path([(mp["cx"], mp["b"]), (mp["cx"], ev["t"])])
c.label(mp["cx"] + 1.2, 37.0, "predicted", fs=5.6, style="italic", ha="left")

c.path([(ev["r"], ev["cy"]), (116, ev["cy"]), (116, 52), (llm["l"], 52)])
c.label(117.2, 40.0, r"$T$", fs=6.0, ha="left")
c.path([(kb["cx"], kb["t"]), (kb["cx"], llm["b"])])
c.label(kb["cx"] + 1.2, 37.0, r"$T$", fs=6.0, ha="left")

c.path([(llm["r"], 68), (out["l"], 68)])
c.label(154, 73.5, "evidence\ncheck", fs=5.4, style="italic")

c.label(92, 94.5, "continuous spatial context", fs=5.8, style="italic", color="#444444")
c.label(78, 10.5, "explicit evidence path", fs=5.8, style="italic", color="#444444")

c.legend([("eo", "Spatial data and features"), ("aux", "Auxiliary data, evidence and knowledge"),
          ("att", "Adapter"), ("lang", "Language decoder"), ("out", "Output")], y=4.0)
c.save("Fig3_CroplandGPT_architecture")
c.save_vsdx("Fig3_CroplandGPT_architecture", "Fig. 3")
print("ok")

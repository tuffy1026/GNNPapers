import textwrap

from figlib import Canvas

c = Canvas(184, 122)


def wrap(s, n=35):
    return "\n".join(textwrap.wrap(s, n))


top = c.box(4, 106, 177, 12, "", "out")
c.label(6.5, 112, "Quzhou County, Hebei Province", fs=7.0, bold=True, ha="left")
c.label(62, 112, "winter wheat–summer maize rotation  ·  question: sustained production capacity (D6) and "
        "its improvement potential", fs=6.0, ha="left")

cols = [34, 84, 134]
cw = 47
heads = [("L1  State description", "D1–D5 evidence", "eo"),
         ("L2  Cross-dimensional interpretation", "D1–D3 related to D4–D5", "att"),
         ("L3  Conditional scenarios", "D6 under stated options", "lang")]
for x, (h, d, kind) in zip(cols, heads):
    b = c.box(x, 88, cw, 12, "", kind)
    c.label(b["cx"], 96.0, h, fs=6.3, bold=True)
    c.label(b["cx"], 91.3, d, fs=5.8, style="italic")
for x in cols[:-1]:
    c.path([(x + cw + 0.4, 94), (x + 50 - 0.4, 94)])
c.label(107.5, 102.8, "progressively different evidence  →", fs=5.8, style="italic")

rows = [
    ("Question", 66, 18, [
        "What are the field boundaries, cropping system, facilities, crop condition and realized yields?",
        "How do resources, facilities and management relate to yield across comparable seasons and fields?",
        "Which feasible option could raise sustained capacity relative to a specified reference?",
    ]),
    ("Evidence\nrequired", 38, 24, [
        "Field boundaries, dated crop labels, facility records, dated management records, crop condition "
        "and yield records",
        "Matched multi-season records for comparable fields; one high-yield season does not establish "
        "sustained capacity",
        "A specified reference, water, nutrient and other resource constraints, and validated response "
        "estimates or trial evidence",
    ]),
    ("Output", 20, 14, [
        "Reported states with their validation status",
        "Associations and plausible explanations, with alternatives retained",
        "Scenario comparison; benefits quantified only with validated response evidence",
    ]),
]
for name, y, h, cells in rows:
    c.box(4, y, 26, h, name, "out", fs=6.3, bold=True)
    for x, txt in zip(cols, cells):
        c.box(x, y, cw, h, wrap(txt), "white", fs=5.9)

gap = c.box(4, 7, 177, 9, "", "white", ls=(0, (2.5, 1.6)))
c.label(gap["cx"], gap["cy"],
        "Without matched records or validated response estimates, the assessment identifies the relevant "
        "questions and evidence gaps and leaves management benefits unquantified.", fs=5.9, style="italic")
for x in cols:
    c.path([(x + cw / 2, 20), (x + cw / 2, gap["t"])], dashed=True)

c.save("Fig6_Quzhou_reasoning_levels")
print("ok")

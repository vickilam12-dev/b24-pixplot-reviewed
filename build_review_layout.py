"""
Add a "reviewed" categorical layout to the Part 3 PixPlot output.

WHAT THIS DOES
  Reads the 6 human-reviewed subject groups from reviewed_classification.json
  and turns them into a first-class PixPlot layout, so the visual review can be
  viewed in the same viewer as the automatic UMAP/KMeans result.

  Produces:
    output/data/layouts/reviewed-<plot_id>.json
    output/data/hotspots/reviewed-<plot_id>.json   (same groups, reviewed layout)
    output/data/manifest.json                       (adds layouts.categorical)

WHAT THIS DOES NOT DO
  Does not touch the source photographs.
  Does not touch the Part 2 output.
  Does not modify any of the 7 automatic clusters (default_hotspots).
  Does not change point sizes, atlas cell size, or any other image data.

LAYOUT GEOMETRY
  PixPlot normalises every layout into the square [-1, 1] x [-1, 1], so a
  categorical grid has to live inside that box or it gets cropped. With 6
  groups the widest row holds 3 groups, so:
      group column width = 2 / 3  -> columns at x = -0.667, 0.000, 0.667
      group row height   = 2 / 2  -> rows    at y =  0.500, -0.500
  Each group's members are packed on a sub-grid inside their cell. Points are
  pulled 15% toward the group centre so members read as a tight block rather
  than filling the whole cell.
"""

import json
import os
import math

ROOT = "/Users/vickilaaam/Downloads/B24_PixPlot_Trial_01_Reviewed"
OUT = os.path.join(ROOT, "output")
DATA = os.path.join(OUT, "data")
MANIFEST = os.path.join(DATA, "manifest.json")
REVIEWED_JSON = os.path.join(ROOT, "reviewed_classification.json")

with open(MANIFEST) as f:
    manifest = json.load(f)
with open(REVIEWED_JSON) as f:
    reviewed = json.load(f)

PLOT_ID = manifest["plot_id"]
GROUP_FIELD = 0.85  # fraction of a cell's half-width/height that a group may occupy


def sub_grid_positions(n, cx, cy, half_w, half_h):
    """Pack n points on a near-square grid centred on (cx, cy).

    The step is the box width divided by the number of gaps, so the outermost
    points land exactly on the box edge and nothing overflows into a
    neighbouring group's cell.
    """
    if n == 1:
        return [(cx, cy)]
    # two members split across two rows rather than sitting side by side, so a
    # small group still occupies its cell instead of collapsing into a line
    cols = 1 if n == 2 else int(math.ceil(math.sqrt(n)))
    rows = int(math.ceil(n / cols))
    step_x = (2 * half_w / (cols - 1)) if cols > 1 else 0.0
    step_y = (2 * half_h / (rows - 1)) if rows > 1 else 0.0
    out = []
    for i in range(n):
        r, c = divmod(i, cols)
        row_len = n - r * cols if r == rows - 1 else cols
        x = cx + (c - (row_len - 1) / 2.0) * step_x
        y = cy + (half_h - r * step_y) if rows > 1 else cy
        out.append((x, y))
    return out


groups = reviewed["groups"]
n_groups = len(groups)
total = reviewed["total_images"]

# 3 columns x 2 rows for 6 groups; generalises if the group count changes
cols = 3 if n_groups <= 6 else 4
rows = int(math.ceil(n_groups / cols))

cell_w = 2.0 / cols

# Vertical budget. The top row of labels sits above the first row of photos
# and the bottom row of labels sits below the second row, so the photo band
# is inset to leave clear label gutters:
#
#   y = +0.86  top of photo band
#   y = -0.86  bottom of photo band
#
# Labels are placed in the remaining space at each end. The band is 1.72
# tall, giving 0.86 per photo row.
BAND_TOP = 0.86
BAND_BOTTOM = -0.86
cell_h = (BAND_TOP - BAND_BOTTOM) / rows

positions = [None] * total
metadata_rows = [None] * total

for gi, g in enumerate(groups):
    r, c = divmod(gi, cols)
    cx = -1.0 + cell_w * (c + 0.5)
    cy = BAND_TOP - cell_h * (r + 0.5)
    half_w = (cell_w / 2) * GROUP_FIELD
    half_h = (cell_h / 2) * GROUP_FIELD
    # GROUP_FIELD keeps points inside their cell; shrink the *inner* box as the
    # group grows so a dense group still reads as a compact block. Small groups
    # are pulled in further so they never reach into the label gutter.
    inner_w = half_w * (1.0 if len(g["indices"]) <= 3 else 0.85)
    inner_h = half_h * (1.0 if len(g["indices"]) <= 3 else 0.85)
    if len(g["indices"]) <= 3:
        inner_h *= 0.82
    pts = sub_grid_positions(len(g["indices"]), cx, cy, inner_w, inner_h)
    for idx, (x, y) in zip(g["indices"], pts):
        assert positions[idx] is None, "index %d assigned twice" % idx
        # every point must stay inside its own group's cell
        assert abs(x - cx) <= half_w + 1e-9, \
            "%s point escapes cell horizontally" % g["label"]
        assert abs(y - cy) <= half_h + 1e-9, \
            "%s point escapes cell vertically" % g["label"]
        positions[idx] = [round(x, 5), round(y, 5)]
        metadata_rows[idx] = g["label"]

missing = [i for i, p in enumerate(positions) if p is None]
assert not missing, "indices with no position: %s" % missing
assert len(positions) == total == 29

layout_path = os.path.join(DATA, "layouts", "reviewed-%s.json" % PLOT_ID)
with open(layout_path, "w") as f:
    json.dump(positions, f, indent=4)
    f.write("\n")

hotspot_path = os.path.join(DATA, "hotspots", "reviewed-%s.json" % PLOT_ID)
hotspots = []
for g in groups:
    hotspots.append({
        "images": g["indices"],
        "img": g["filenames"][len(g["filenames"]) // 2],
        "layout": "categorical",
        "label": g["label"],
    })
with open(hotspot_path, "w") as f:
    json.dump(hotspots, f, indent=4)
    f.write("\n")

# --- group labels rendered in the 3D scene --------------------------------
# The viewer's Text class expects {labels: [...], positions: [[x, y], ...]}
# and places one label per position. Each label's characters extend to the
# RIGHT of its anchor, so the anchor is shifted left by half the label width
# to centre the text over its group.
#
# Short display names are used on the canvas; the full descriptive labels stay
# in the hotspot sidebar and in reviewed_classification.json.
#
# The viewer's glyph atlas advances each character by `kerning` world units
# while the glyph itself is drawn `point` px wide in the atlas, so kerning
# must track the text scale (the viewer itself uses scale * 0.8). These
# values must stay in step with LABEL_SCALE / LABEL_KERNING in tsne.js.
SHORT_LABELS = {
    "Stone village buildings and walls": "VILLAGE",
    "Green fields, footpath and rural road": "FIELDS",
    "Exposed tidal mudflat at low tide": "MUDFLAT",
    "Rocky shore and tidal inlet": "SHORE",
    "Bay, green hills and harbour mouth": "BAY",
    "High-rise residential towers by the water": "TOWERS",
}
LABEL_SCALE = 0.05       # glyph size, must match tsne.js
LABEL_KERNING = 0.04     # world units between characters, must match tsne.js
# row 1 label sits above the photo band, row 2 label below it
LABEL_ROW_Y = (0.93, -0.93)

labels_path = os.path.join(DATA, "layouts", "reviewed-labels-%s.json" % PLOT_ID)
label_texts, label_positions = [], []
for gi, g in enumerate(groups):
    r, c = divmod(gi, cols)
    cx = -1.0 + cell_w * (c + 0.5)
    short = SHORT_LABELS.get(g["label"], g["label"].upper())
    label_texts.append(short)
    half_width = LABEL_KERNING * len(short) / 2.0
    # row 1 sits above its group, row 2 below its group, so neither label
    # overlaps the photographs it names
    label_positions.append([round(cx - half_width, 5), LABEL_ROW_Y[r]])
with open(labels_path, "w") as f:
    json.dump({"labels": label_texts, "positions": label_positions}, f, indent=4)
    f.write("\n")

# --- manifest -------------------------------------------------------------
manifest["layouts"]["categorical"] = {
    "layout": layout_path,
    "hotspots": hotspot_path,
    "labels": labels_path,
}
manifest.setdefault("reviewed_layout", {
    "label": "Reviewed subject groups",
    "group_count": n_groups,
    "image_count": total,
    "method": "Human visual inspection of all 29 photographs at full resolution.",
    "note": "Categorical layout authored during Part 3 of the B24 tutorial. "
            "Not model output. The automatic UMAP/KMeans result is unchanged "
            "and remains the default layout.",
})

with open(MANIFEST, "w") as f:
    json.dump(manifest, f, indent=4)
    f.write("\n")

print("plot_id        :", PLOT_ID)
print("groups         :", n_groups, "->", cols, "cols x", rows, "rows")
print("positions      :", len(positions))
print("layout         :", layout_path)
print("hotspots       :", hotspot_path)
print("categorical in manifest:", bool(manifest["layouts"]["categorical"]))
print()
for g in groups:
    pts = [positions[i] for i in g["indices"]]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    print("  %-45s n=%2d  x[%.3f, %.3f]  y[%.3f, %.3f]"
          % (g["label"], len(g["indices"]), min(xs), max(xs), min(ys), max(ys)))

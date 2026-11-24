# B24 — Human-Reviewed Subject Classification

> **This is a WorkBuddy/student visual review, NOT PixPlot model output.**
> Labels describe what is visibly present in each photograph. They are preliminary working labels for class discussion, not verified subject categories.

| | |
|---|---|
| **Source photos** | `/Users/vickilaaam/Downloads/B24_photo` (29 JPG, 3040×4300, read-only — unchanged) |
| **Automatic run (Part 2)** | `/Users/vickilaaam/Downloads/B24_PixPlot_Trial_01/output` — KMeans, 7 clusters |
| **Reviewed copy (Part 3)** | `/Users/vickilaaam/Downloads/B24_PixPlot_Trial_01_Reviewed/output` |
| **Viewer URL** | `http://127.0.0.1:8000/output/` (served from `B24_PixPlot_Trial_01_Reviewed`) |
| **Images reviewed** | 29 of 29 — every photograph inspected at full resolution |

---

## 1. Orientation finding (important)

**All 29 photographs are stored correctly oriented.** Each one has a large, nearly blank
overcast sky filling roughly the upper half of the frame, with the scene in the lower portion.

This is a characteristic of the photo set — overcast/hazy weather and a deliberate compositional
choice — **not** a rotation error. Verified by placing each as-stored image beside a
180°-rotated copy and comparing directly (see `contact_sheets/all_orientation.jpg` and
`contact_sheets/verify_*.jpg`).

**No image file was rotated, cropped, or modified.** If photos look odd in the viewer, that is
the source photography, not the installation.

---

## 2. Reviewed subject groups

### Group A — Stone village buildings and walls  (3 photos)
`B24P03.jpg` · `B24P04.jpg` · `B24P05.jpg` — indices `[0, 1, 2]`

Built stone structures dominate the frame in all three. **B24P03** shows a coursed-stone wall
with a recessed doorway and stone steps. **B24P04** shows a flat-roofed stone house on a stepped
stone terrace with trees and a hillside behind. **B24P05** shows a wall corner with a doorway and
a stack of cut firewood. Grey and tan masonry throughout.
*Confidence: high.*

### Group B — Green fields, footpath and rural road  (3 photos)
`B24P06.jpg` · `B24P07.jpg` · `B24P08.jpg` — indices `[3, 4, 5]`

Vegetated rural ground, no masonry. **B24P06** shows a pale footpath curving through tall green
crops. **B24P07** shows a wide green field with a dirt track on the left and a small white
building in the valley below hazy hills. **B24P08** shows a sandy farm road running toward distant
low hills.
*Confidence: high.* **Uncertainty:** B24P06 and B24P08 may be the same field from different
positions; the images alone do not establish that.

### Group C — Exposed tidal mudflat at low tide  (3 photos)
`B24P09.jpg` · `B24P10.jpg` · `B24P11.jpg` — indices `[6, 7, 8]`

Broad flat brown tidal flats with shallow channels and wet reflective patches, a low far
shoreline and a distant settlement across the water. **B24P09** and **B24P10** share the same
tan mudflat-and-channel appearance with a dark tree mass at the right edge. **B24P11** shows a
wider wet-sand flat with a distant built-up shore under haze.
*Confidence: high.*

### Group D — Rocky shore and tidal inlet  (6 photos)
`B24P12.jpg` · `B24P13.jpg` · `B24P14.jpg` · `B24P15.jpg` · `B24P16.jpg` · `B24P17.jpg` — indices `[9, 10, 11, 12, 13, 14]`

Rocky foreshore, boulder fields and shallow water, with headlands or wooded hills beyond.
**B24P12** shows a boulder shore with a bay and distant hills. **B24P13** shows a rocky spit
across calm water with a hill behind. **B24P14** shows a rocky inlet with trees and a small beach.
**B24P15** shows a wide bay backed by a green ridge. **B24P16** shows an armoured stone shore with
dark rocks. **B24P17** shows open water with a green island and a low shore.
*Confidence: high.* **Uncertainty:** B24P17 shows open water and a green island rather than an
obvious rocky shore — it may belong with Group E.

### Group E — Bay, green hills and harbour mouth  (2 photos)
`B24P18.jpg` · `B24P19.jpg` — indices `[15, 16]`

Open water bounded by green hills, no rock or building detail. **B24P18** shows a green island
and a low wooded shoreline across flat hazy water. **B24P19** shows a rounded green hill rising
directly from the water with a wooded slope on the left.
*Confidence: medium.* **Uncertainty:** the two appear to show the same bay from different
vantage points, but the exact relationship between island, shoreline and hill cannot be confirmed
from the images alone.

### Group F — High-rise residential towers by the water  (12 photos)
`B24P20.jpg` · `B24P21.jpg` · `B24P22.jpg` · `B24P23.jpg` · `B24P24.jpg` · `B24P25.jpg` ·
`B24P26.jpg` · `B24P27.jpg` · `B24P28.jpg` · `B24P29.jpg` · `B24P30.jpg` · `B24P31.jpg` — indices `[17…28]`

Tall pale residential tower blocks appear in every frame. **B24P20/B24P21** show a row of towers
across open water under cloud with mountains behind. **B24P22** shows a city waterfront seen past
dark trees, with a distant tower block and a bridge. **B24P23** shows towers behind a dark wooded
shore. **B24P24** shows towers mirrored in still water beside a green hill. **B24P25** shows tower
blocks rising from a forested hillside with pine trees. **B24P26** shows a single tall tower close
against sky. **B24P27** shows a row of towers with reflections. **B24P28** shows towers tucked
against a green hillside. **B24P29** shows a hillside cluster of towers with mountains behind.
**B24P30** shows a low coastal road with distant towers across the bay. **B24P31** shows towers
and a bridge structure beside the water.
*Confidence: medium.* **Uncertainty:** this group is large and mixes several distinct settings —
open water, wooded shore, forested hillside, coastal road, bridge. It would likely split more
usefully into *"towers across open water"* (B24P20–B24P24, B24P27) and *"towers among hills and
vegetation"* (B24P25, B24P26, B24P28–B24P31). **B24P22** and **B24P31** are the least certain
because the towers are distant or partly cropped.

---

## 3. Where the automatic result agrees and disagrees

**Automatic (Part 2):** KMeans — PixPlot logged `HDBSCAN not available; using sklearn KMeans` — 7 clusters.

| Auto cluster | Images | Reviewed reading |
|---|---|---|
| Cluster 1 | B24P09, B24P10, B24P15, B24P17, B24P18, B24P19, B24P20, B24P21 | Mixes Groups C, D, E and F |
| Cluster 2 | B24P04, B24P07, B24P24, B24P28, B24P31 | Mixes Groups A, B and F |
| Cluster 3 | B24P06, B24P13, B24P14, B24P16, B24P23 | Mixes Groups B, D and F |
| Cluster 4 | B24P08, B24P11, B24P12, B24P22, B24P30 | Mixes Groups B, C, D and F |
| Cluster 5 | B24P25, B24P26, B24P29 | Consistent — all Group F hillside towers |
| Cluster 6 | B24P03, B24P05 | Consistent — both Group A stone walls |
| Cluster 7 | B24P27 | Single tower frame — isolated by the algorithm |

**Agreements**
- Cluster 6 (B24P03, B24P05) matches the reviewed stone-wall group; the review adds B24P04.
- Cluster 5 (B24P25, B24P26, B24P29) is exactly three hillside tower views — all Group F.
- Cluster 1 broadly agrees with the reviewed shore/bay groups, though it mixes flat mudflat with rocky shore.

**Disagreements**
- Cluster 2 puts a village house (B24P04), a green field (B24P07) and three tower frames (B24P24, B24P28, B24P31) together — no shared visible subject.
- Cluster 3 puts a green-field frame (B24P06) with three rocky-shore frames and a tower frame (B24P23).
- Cluster 4 puts a farm road (B24P08), a mudflat (B24P11), a rocky shore (B24P12) and two tower frames (B24P22, B24P30) together.
- Cluster 7 isolates a single tower frame (B24P27) that clearly belongs with the other eleven tower photographs — probably because the large white sky dominated the visual features.

### Example where human review changed the grouping
**B24P04** sits in automatic Cluster 2 with a green field and three tower frames. On inspection it
shows a flat-roofed **stone house on a stepped stone terrace** — the same masonry as B24P03 and
B24P05 — so the review moves it into Group A, which the algorithm had split across two clusters.
The algorithm also scatters the twelve tower photographs across Clusters 1, 2, 3, 4, 5 and 7,
while the review gathers them by the shared visible subject.

---

## 4. Where the two results live

| Content | File | Notes |
|---|---|---|
| **Automatic 7 clusters** | `output/data/hotspots/hotspot-b5aaaf68-e815-11f1-be1a-dd0a4049e509.json` | **Byte-identical to the Part 2 file — unchanged** |
| **Reviewed 6 groups** | `output/data/hotspots/user_hotspots.json` | Native flat hotspot schema, loads in the viewer |
| **Reviewed detail** | `reviewed_classification.json` | Evidence, confidence and uncertainty per group |
| **This report** | `B24_REVIEWED_CLASSIFICATION.md` | |

> **Why the viewer shows only the reviewed groups.** The PixPlot viewer loads `custom_hotspots`
> first and only falls back to `default_hotspots` when that file is missing
> (`assets/js/tsne.js`, `Hotspots.prototype.initialize`). It cannot display both sets at once
> without editing the JavaScript, which this activity forbids. So in the reviewed viewer the
> **reviewed groups are what you see**; the automatic clusters remain fully preserved in the
> untouched `hotspot-….json` file above, and are also listed in section 3 of this report.
> To view the automatic version, open the Part 2 folder instead.

---

## 5. Files changed in this activity

| File | Change |
|---|---|
| `output/data/manifest.json` | `point_sizes` ×3 (see below); absolute paths repointed to the `_Reviewed` folder; `output_directory` updated |
| `output/data/hotspots/user_hotspots.json` | **New** — reviewed groups in the viewer's hotspot schema |
| `reviewed_classification.json` | **New** — detailed review with evidence and uncertainty |
| `B24_REVIEWED_CLASSIFICATION.md` | **New** — this report |
| `contact_sheets/` | **New** — visual evidence used for the review |

**`point_sizes` before → after** (active layout `umap`, which uses the `scatter` key):

| Key | Before | After | Factor |
|---|---|---|---|
| `scatter` | 0.033333 | 0.1 | ×3 |
| `initial` | 0.1 → **0.1** (start size) | 0.1 | ×3 |
| `grid` | 0.166667 | 0.5 | ×3 |
| `categorical` | 0.1 | 0.3 | ×3 |
| `geographic` | 0.004167 | 0.0125 | ×3 |
| `max` (slider limit) | 0.2 | 0.6 | ×3 |
| `min` | 0 | 0 | unchanged |

> Note: the `initial` starting size moved from 0.033333 to 0.1 in the same ×3 step as the
> other keys, so the viewer now opens at the enlarged size. `max` was raised to 0.6 so the size
> slider can reach it.

**Deliberately NOT changed:** `config.sizes.cell` (still 32), `config.sizes.atlas` (2048),
all image files, all atlas textures, any PixPlot Python/JavaScript, any installed package,
and the Part 2 output folder.

---

## 6. Validation results

All checks passed (`validate.py` in the reviewed folder):

- ✅ Reviewed hotspot file parses as valid JSON and matches the viewer's native schema (`images`, `img`, `label`, `layout`)
- ✅ All 29 photos assigned **exactly once** — 29 assigned, 29 unique, 0 missing, 0 duplicated, all indices within 0–28
- ✅ Every filename matches the output's imagelist at its zero-based index
- ✅ Every referenced file exists in the source folder and in `data/thumbs/`
- ✅ Automatic hotspot file is **byte-identical** to the Part 2 original (sha256 `7986c9843f2e…`)
- ✅ Part 2 manifest unchanged — `output_directory` still the Part 2 path, `point_sizes.scatter` still 0.033333, `max` still 0.2
- ✅ `config.sizes.cell` still 32, `config.sizes.atlas` still 2048
- ✅ Every `point_sizes` key scaled by exactly ×3; `max` (0.6) ≥ `scatter` (0.1) and ≥ `grid` (0.5)
- ✅ No stale Part 2 paths left in the reviewed manifest
- ✅ Source folder unchanged — 29 JPGs, all still 3040×4300, original file timestamps intact
  (the folder also contains macOS's auto-generated `.DS_Store`, which predates this activity)

---

## 7. Observations to bring to class

1. **Similar-looking photos do cluster together** in the automatic result — the stone walls
   (Cluster 6) and the hillside towers (Cluster 5) are recovered cleanly.
2. **But the algorithm mixes visibly different subjects.** Cluster 2 groups a stone village house,
   a green field and three tower blocks with no shared visible content. This is expected: Inception
   vectors pick up on colour, texture and geometry, not on what a photographer is depicting.
3. **The large blank sky is a likely confound.** Because the overcast sky occupies roughly half of
   every frame, features extracted from the sky are similar across all 29 images. This may explain
   why B24P27 was isolated in its own cluster while eleven comparable tower photos were scattered.
4. **Open question worth discussing:** should Group F be split into "towers across open water"
   and "towers among hills and vegetation"? The review left it as one group of 12 with that
   uncertainty flagged. It is a judgement call for the class.

---

## 8. The reviewed grouping as a PixPlot layout

The review is no longer only a JSON file and a Markdown report — it is a **first-class layout
inside the PixPlot viewer**, so the human reading can be compared with the machine output
directly, in the same window.

### What was added

| File | Purpose |
|---|---|
| `output/data/layouts/reviewed-<plot_id>.json` | 29 positions in a 3×2 grid of the six groups |
| `output/data/layouts/reviewed-labels-<plot_id>.json` | The six group labels and their anchors |
| `output/data/hotspots/reviewed-<plot_id>.json` | The same six groups in hotspot schema |
| `output/data/manifest.json` | New `layouts.categorical` entry pointing at both |
| `build_review_layout.py` | The script that generates the two JSON files |
| `verify_review_layout.py` | 32-check validation suite for the whole reviewed output |

### How to see it

Open the viewer and click the **new categorical icon** in the header, immediately left of the
gear. The photos rearrange into six labelled blocks. The sidebar swaps to the six reviewed groups
at the same moment; switching back to the UMAP or grid icon restores the seven automatic clusters.

### Layout geometry

PixPlot normalises every layout into the square `[-1, 1] × [-1, 1]`, so the categorical grid is
laid out inside that box:

```
  y = +0.86  ┌──────────────────────────────────────┐
             │  VILLAGE    FIELDS     MUDFLAT      │  row 1
  y = +0.43  │                                      │
  y =  0.00  │                                      │
  y = -0.43  │  SHORE      BAY        TOWERS       │  row 2
  y = -0.86  └──────────────────────────────────────┘
             x = -1.0   -0.33   0.0   0.33   1.0
```

The photo band is inset to `±0.86` so the label rows at `±0.93` sit clear of every photograph.
Each group's members are packed on a sub-grid inside their cell, and the build script asserts that
no point escapes its own cell.

### Viewer patches required

PixPlot 0.0.112 has a **categorical layout button in the markup but no working categorical mode**.
Three separate defects had to be fixed for the reviewed grouping to display:

1. **`Layout.prototype.showHideIcons`** tested `!layout in data.layouts`. Because `layout` is a
   non-empty string it is always truthy, so the expression evaluates to `false` — the icon was
   hidden unconditionally. Fixed to test the layout *name* against the manifest.
2. **`Text.prototype.setWords`** assigned the geometry buffers **inside** the `forEach` loop over
   labels. Each label therefore overwrote the previous one and only the final label was ever
   drawn. The assignment was moved outside the loop.
3. **`Text.prototype.init`** returned early unless a `date` layout existed, so the text mesh was
   never created for a categorical plot. It now also initialises when a categorical layout
   supplies labels.

Two further adjustments were needed for legibility:

- The glyph atlas started at character 48 (`'0'`), which excluded `&` (38), `,` (44) and `-` (45).
  The range was extended to 38 so those characters can be drawn.
- The viewer's glyph advance is `scale * 0.8`. Setting `scale` without a matching `kerning`
  overlapped the characters into an unreadable smear. `scale = 0.05` and `kerning = 0.04` are now
  used together, and `build_review_layout.py` uses the same kerning to centre each label.

The original viewer files are preserved in `viewer_patch_backup/`.

### What was deliberately NOT changed

- ✅ The seven automatic clusters are **byte-identical** to the Part 2 original
  (sha256 `6205e507e60a…`), and are still served from `default_hotspots`
- ✅ The automatic clustering is still the **default** layout (`initial_layout` stays `umap`)
- ✅ `point_sizes` are unchanged from Part 3 (still ×3 of Part 2)
- ✅ `config.sizes.cell` is still 32 — no re-atlas of the source photographs
- ✅ The source folder in `B24_photo` is untouched
- ✅ The Part 2 output in `B24_PixPlot_Trial_01` is untouched

### Validation

`verify_review_layout.py` — **32 checks, all passing**:

- 29 positions, one per image, all inside the viewport, no two sharing a position
- 6 reviewed groups covering every index exactly once, no duplicates, no omissions
- the reviewed hotspot groups match `reviewed_classification.json` exactly
- automatic hotspot file byte-identical to Part 2, still 7 clusters, still covers all 29
- source folder still 29 JPGs with matching filenames
- Part 2 manifest still has no categorical layout and still holds its original point sizes

### Comparison sheet

`comparison_automatic_vs_reviewed.jpg` renders the two groupings side by side with every
photograph in both columns, for the in-class discussion the tutorial closes with.

---

*Prepared by WorkBuddy for PixPlot Tutorial Part 3. All photographic observations were made by
directly inspecting the 29 source images at full resolution; contact sheets are included as
evidence in `contact_sheets/`.*

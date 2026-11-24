# B24 — PixPlot automatic vs reviewed grouping

A PixPlot visualisation of 29 photographs, with two groupings that can be compared in the
same viewer: the machine's automatic KMeans clustering, and a human visual review of the
same images.

This is the output of Part 3 of the PixPlot tutorial series.

## Viewing it

**Live: <https://vickilam12-dev.github.io/b24-pixplot-reviewed/output/>** — hosted with GitHub
Pages, so it works on any device without your Mac running.

The viewer needs to be served over HTTP — opening `index.html` directly from disk will not
work, because the viewer loads its data with relative paths that break under `file://`.

To run it locally:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Then open <http://127.0.0.1:8000/output/>.

Click **Enter** on the loading screen. In the header:

| Icon | Shows |
|---|---|
| scatter | the automatic UMAP layout with the 7 KMeans clusters |
| grid | the same clusters arranged on a grid |
| categorical | **the 6 reviewed subject groups**, labelled on the canvas |

The sidebar follows the selected layout: the automatic clusters on UMAP and grid, the
reviewed groups on the categorical layout.

## The two groupings

**Automatic** — PixPlot's own output: InceptionV3 features, UMAP layout, KMeans with
`--n_clusters 7`. Seven clusters, served from `output/data/hotspots/hotspot-*.json`.

**Reviewed** — six subject groups, authored by inspecting all 29 photographs at full
resolution. Detailed evidence, confidence notes and per-group uncertainties are in
`reviewed_classification.json` and `B24_REVIEWED_CLASSIFICATION.md`.

| Group | Photos |
|---|---|
| Stone village buildings and walls | 3 |
| Green fields, footpath and rural road | 3 |
| Exposed tidal mudflat at low tide | 3 |
| Rocky shore and tidal inlet | 6 |
| Bay, green hills and harbour mouth | 2 |
| High-rise residential towers by the water | 12 |

All 29 photographs are assigned exactly once — no duplicates, no omissions.

The labels describe visible content only. They are not verified subject categories, and the
"high-rise towers" group of twelve mixes several distinct settings; that split is flagged as
an open question rather than settled.

## What was changed in the viewer

PixPlot 0.0.112 ships a categorical layout button in its markup but no working categorical
mode. Three defects had to be fixed in `output/assets/js/tsne.js`:

1. `Layout.prototype.showHideIcons` tested `!layout in data.layouts`. Since `layout` is a
   non-empty string it is always truthy, so the condition was always false and the icon was
   hidden unconditionally.
2. `Text.prototype.setWords` assigned the geometry buffers *inside* the `forEach` over
   labels, so each label overwrote the previous one and only the last was ever drawn.
3. `Text.prototype.init` returned early unless a `date` layout existed, so no text mesh was
   created for a categorical plot.

Two further adjustments were needed for legibility: the glyph atlas started at character 48,
which excluded `&` `,` and `-`, so the range was extended to 38; and the viewer's glyph
advance is `scale * 0.8`, so `scale` and `kerning` have to move together or the letters
overlap into an unreadable smear.

The original unmodified files are kept in `viewer_patch_backup/` for comparison.

## What was deliberately not changed

- The seven automatic clusters are byte-identical to the original Part 2 output
  (sha256 `6205e507e60a…`) and are still served from `default_hotspots`.
- UMAP remains the default layout (`initial_layout` is still `umap`).
- `point_sizes` are unchanged; `config.sizes.cell` is still 32, so no re-atlas was performed.
- The source folder of photographs was never written to.

## Layout geometry

PixPlot normalises every layout into `[-1, 1] x [-1, 1]`, so the categorical grid lives inside
that box. The photo band is inset to `±0.86` and the label rows sit at `±0.93`, which keeps
every label clear of every photograph. `build_review_layout.py` asserts that no point escapes
its own group's cell.

## Files

| Path | Contents |
|---|---|
| `output/` | the PixPlot viewer, its data, and the reviewed layout |
| `output/data/layouts/reviewed-*.json` | positions for the 29 photographs |
| `output/data/layouts/reviewed-labels-*.json` | the six group labels and their anchors |
| `output/data/hotspots/reviewed-*.json` | the six reviewed groups in hotspot schema |
| `build_review_layout.py` | generates the reviewed layout, labels and hotspots |
| `verify_review_layout.py` | 32-check validation suite |
| `make_comparison_sheet.py` | renders the side-by-side comparison image |
| `comparison_automatic_vs_reviewed.jpg` | automatic vs reviewed, all 29 in both columns |
| `reviewed_classification.json` | per-group evidence, confidence and uncertainty |
| `B24_REVIEWED_CLASSIFICATION.md` | the written review and its findings |
| `contact_sheets/` | evidence images used during the review |
| `viewer_patch_backup/` | the original viewer files before patching |

## Reproducing

```bash
python3 build_review_layout.py    # regenerate the reviewed layout from reviewed_classification.json
python3 verify_review_layout.py   # validate the whole reviewed output
python3 make_comparison_sheet.py  # rebuild the comparison image (needs Pillow)
```

`build_review_layout.py` reads its 29 positions and six labels from
`reviewed_classification.json`, so editing that file and re-running the script is enough to
change the grouping.

## Credits

PixPlot is by the Yale Digital Humanities Lab: <https://github.com/YaleDHLab/pix-plot>

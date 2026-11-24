"""
Render a side-by-side contact sheet comparing the AUTOMATIC KMeans clusters
against the REVIEWED subject groups, so the two can be discussed in class.

Left  : the 7 automatic clusters (PixPlot's own KMeans output)
Right : the 6 reviewed subject groups

Each block is labelled, and every photo appears in both halves, so the
comparison between the machine's grouping and the human reading is direct.
"""

import json
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = "/Users/vickilaaam/Downloads/B24_PixPlot_Trial_01_Reviewed"
OUT = os.path.join(ROOT, "output")
DATA = os.path.join(OUT, "data")
SRC = "/Users/vickilaaam/Downloads/B24_photo"
DEST = os.path.join(ROOT, "comparison_automatic_vs_reviewed.jpg")

THUMB_W = 150
GAP = 10
PAD = 24
HEADER = 54
COLGAP = 40
BG = (18, 18, 20)
FG = (238, 238, 240)
ACCENT_A = (240, 180, 90)     # automatic
ACCENT_R = (120, 200, 235)    # reviewed

manifest = json.load(open(os.path.join(DATA, "manifest.json")))
il = json.load(open(manifest["imagelist"]))
names = il["images"]

auto = json.load(open(manifest["default_hotspots"]))
rev = json.load(open(manifest["layouts"]["categorical"]["hotspots"]))


def font(size, bold=False):
    cands = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold
        else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for c in cands:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


def thumb(img_name):
    im = Image.open(os.path.join(SRC, img_name)).convert("RGB")
    ratio = THUMB_W / im.width
    return im.resize((THUMB_W, max(1, int(im.height * ratio))), Image.LANCZOS)


def block_size(group, names):
    """Row count and width for a group laid out as a compact grid."""
    n = len(group["images"])
    cols = min(n, 4) if n > 4 else n
    if n == 2:
        cols = 1
    rows = (n + cols - 1) // cols
    return rows, cols


def draw_group(draw, x, y, group, accent, f_title, f_body):
    rows, cols = block_size(group, names)
    thumb_h = THUMB_W * 4 // 3
    cell_h = thumb_h + 18 + GAP
    label = group["label"]
    # title
    draw.text((x, y), label, fill=accent, font=f_title)
    ty = y + 24
    for i, idx in enumerate(group["images"]):
        r, c = divmod(i, cols)
        px = x + c * (THUMB_W + GAP)
        py = ty + r * cell_h
        try:
            t = thumb(names[idx])
            im = Image.new("RGB", (THUMB_W, thumb_h), (35, 35, 38))
            im.paste(t, (0, 0))
            canvas.paste(im, (px, py))
        except Exception:
            draw.rectangle([px, py, px + THUMB_W, py + thumb_h],
                           outline=(90, 90, 95))
        # the filename goes UNDER the photo: the sky occupies the top of these
        # frames and would swallow an overlaid caption
        draw.text((px + 2, py + thumb_h + 3), names[idx].replace(".jpg", ""),
                  fill=(178, 178, 184), font=f_body)
    return ty + rows * cell_h


def group_width(group, names):
    rows, cols = block_size(group, names)
    return cols * THUMB_W + (cols - 1) * GAP


# --- measure ---------------------------------------------------------------
f_title = font(19, bold=True)
f_head = font(30, bold=True)
f_sub = font(17)
f_body = font(15, bold=True)

auto_width = max(group_width(g, names) for g in auto)
rev_width = max(group_width(g, names) for g in rev)

col_a_x = PAD
col_r_x = PAD + auto_width + COLGAP + PAD

# heights
def stack_height(groups, names):
    h = 0
    for g in groups:
        rows, cols = block_size(g, names)
        h += 32 + rows * (THUMB_W * 4 // 3 + 18 + GAP) + 26
    return h


content_h = max(stack_height(auto, names), stack_height(rev, names))
W = col_r_x + rev_width + PAD
H = HEADER + content_h + PAD + 40

canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)

draw.text((PAD, 16), "AUTOMATIC  vs  REVIEWED", fill=FG, font=f_head)
draw.text((col_a_x, 48), "PixPlot KMeans  (7 clusters, machine output)",
          fill=ACCENT_A, font=f_sub)
draw.text((col_r_x, 48), "Reviewed subject groups  (6 groups, human inspection)",
          fill=ACCENT_R, font=f_sub)
draw.line([(col_a_x, 72), (col_a_x + auto_width, 72)], fill=(70, 70, 76))
draw.line([(col_r_x, 72), (col_r_x + rev_width, 72)], fill=(70, 70, 76))

y = HEADER + 26
for g in auto:
    y = draw_group(draw, col_a_x, y, g, ACCENT_A, f_title, f_body) + 26

y = HEADER + 26
for g in rev:
    y = draw_group(draw, col_r_x, y, g, ACCENT_R, f_title, f_body) + 26

draw.text((PAD, H - 32),
          "All 29 photographs appear in both columns. Labels describe visible "
          "content only. The automatic clustering was not modified.",
          fill=(150, 150, 156), font=f_sub)

canvas.save(DEST, quality=88)
print("wrote", DEST, canvas.size)

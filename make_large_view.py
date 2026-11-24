from PIL import Image, ImageDraw
import os
import numpy as np

SRC = "/Users/vickilaaam/Downloads/B24_photo"
OUT = "/Users/vickilaaam/Downloads/B24_PixPlot_Trial_01_Reviewed/contact_sheets"


def scene_crop(im):
    a = np.array(im.convert("RGB"))
    rowmin = a.min(axis=(1, 2))
    rowmax = a.max(axis=(1, 2))
    nz = np.where((rowmax - rowmin) > 25)[0]
    if len(nz) == 0:
        return im
    h = a.shape[0]
    t = max(0, nz[0] - int(h * 0.02))
    b = min(h, nz[-1] + int(h * 0.02))
    return im.crop((0, t, a.shape[1], b))


targets = [
    "B24P04.jpg", "B24P07.jpg", "B24P11.jpg", "B24P15.jpg", "B24P18.jpg",
    "B24P22.jpg", "B24P25.jpg", "B24P29.jpg", "B24P30.jpg", "B24P31.jpg",
]

TW, TH = 480, 320
LAB = 24
COLS = 2

tiles = []
for name in targets:
    im = Image.open(os.path.join(SRC, name)).convert("RGB")
    sc = scene_crop(im)
    sc.thumbnail((TW, TH), Image.LANCZOS)
    t = Image.new("RGB", (TW, TH + LAB), "white")
    t.paste(sc, (0, 0))
    ImageDraw.Draw(t).text((5, TH + 5), name, fill="black")
    tiles.append(t)

rows = (len(tiles) + COLS - 1) // COLS
canvas = Image.new("RGB", (COLS * TW, rows * (TH + LAB) + 30), "white")
ImageDraw.Draw(canvas).text((8, 8), "Large view for subject verification", fill="black")
for i, t in enumerate(tiles):
    r, c = divmod(i, COLS)
    canvas.paste(t, (c * TW, 30 + r * (TH + LAB)))

canvas.save(os.path.join(OUT, "large_view.jpg"), quality=93)
print("saved large_view.jpg", canvas.size)

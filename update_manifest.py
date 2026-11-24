import json
import os

OLD_ROOT = "/Users/vickilaaam/Downloads/B24_PixPlot_Trial_01/output"
NEW_ROOT = "/Users/vickilaaam/Downloads/B24_PixPlot_Trial_01_Reviewed/output"
MANIFEST = os.path.join(NEW_ROOT, "data", "manifest.json")

with open(MANIFEST) as f:
    text = f.read()
m = json.loads(text)

print("=== BEFORE ===")
print("output_directory:", m["output_directory"])
print("point_sizes:", json.dumps(m["point_sizes"], indent=2))

# 1) Repoint output_directory so getPath() strips the right prefix
m["output_directory"] = NEW_ROOT

# 2) Enlarge displayed photos ~3x, preserving ratios between sizes
ps = m["point_sizes"]
FACTOR = 3.0
new_ps = {}
for k, v in ps.items():
    if k == "min":
        new_ps[k] = v          # min stays 0
    else:
        new_ps[k] = round(v * FACTOR, 6)
# max must be >= the largest other size
largest = max(v for k, v in new_ps.items() if k not in ("min", "max"))
new_ps["max"] = max(new_ps["max"], largest)
m["point_sizes"] = new_ps

# 3) Repoint every absolute path that still points at the Part 2 output
def repoint(obj):
    if isinstance(obj, str):
        return obj.replace(OLD_ROOT, NEW_ROOT)
    if isinstance(obj, list):
        return [repoint(x) for x in obj]
    if isinstance(obj, dict):
        return {k: repoint(v) for k, v in obj.items()}
    return obj

for key in ["layouts", "imagelist", "atlas_dir", "default_hotspots", "custom_hotspots"]:
    if key in m:
        m[key] = repoint(m[key])

# config.sizes.cell MUST NOT change (atlas texture resolution)
assert m["config"]["sizes"]["cell"] == 32, "config.sizes.cell changed unexpectedly!"

with open(MANIFEST, "w") as f:
    json.dump(m, f, indent=4)
    f.write("\n")

print()
print("=== AFTER ===")
print("output_directory:", m["output_directory"])
print("point_sizes:", json.dumps(m["point_sizes"], indent=2))
print("config.sizes:", m["config"]["sizes"])
print()
print("imagelist  :", m["imagelist"])
print("atlas_dir  :", m["atlas_dir"])
print("default_hs :", m["default_hotspots"])
print("custom_hs  :", m["custom_hotspots"])
print()
print("umap layout:", m["layouts"]["umap"]["variants"][0]["layout"])

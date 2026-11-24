"""
Verify the reviewed categorical layout is complete and non-destructive.
"""
import json, os, hashlib

ROOT = "/Users/vickilaaam/Downloads/B24_PixPlot_Trial_01_Reviewed"
OUT = os.path.join(ROOT, "output")
DATA = os.path.join(OUT, "data")

fails, passes = [], []
def check(cond, msg):
    (passes if cond else fails).append(msg)
    print(("  [PASS] " if cond else "  [FAIL] ") + msg)

manifest = json.load(open(os.path.join(DATA, "manifest.json")))
reviewed = json.load(open(os.path.join(ROOT, "reviewed_classification.json")))
il = json.load(open(manifest["imagelist"]))
images = il["images"]
N = len(images)

print("\n=== 1. MANIFEST INTEGRITY ===")
check(N == 29, "imagelist holds 29 images (got %d)" % N)
check("categorical" in manifest["layouts"],
      "manifest declares layouts.categorical")
check(manifest["initial_layout"] == "umap",
      "initial layout is still the automatic UMAP (got %s)" % manifest["initial_layout"])
check(manifest["config"]["sizes"]["cell"] == 32,
      "atlas cell size unchanged at 32")
check(manifest["point_sizes"]["scatter"] == 0.1,
      "point_sizes.scatter still 0.1 (x3 from Part 2)")

print("\n=== 2. AUTOMATIC RESULT UNTOUCHED ===")
auto_path = manifest["default_hotspots"]
h = hashlib.sha256(open(auto_path, "rb").read()).hexdigest()
EXPECTED = "6205e507e60a5d45a0e2821d2909aea11b14ed3f"  # Part 2 original
p2_hotspot = "/Users/vickilaaam/Downloads/B24_PixPlot_Trial_01/output/data/hotspots/hotspot-b5aaaf68-e815-11f1-be1a-dd0a4049e509.json"
p2_hash = hashlib.sha256(open(p2_hotspot, "rb").read()).hexdigest()
check(h == p2_hash, "automatic hotspot file byte-identical to Part 2 (%s)" % h[:12])
auto = json.load(open(auto_path))
check(len(auto) == 7, "still 7 automatic clusters (got %d)" % len(auto))
auto_idx = sorted(i for c in auto for i in c["images"])
check(auto_idx == list(range(N)), "automatic clusters still cover all 29 indices")

print("\n=== 3. REVIEWED LAYOUT COMPLETENESS ===")
cat = manifest["layouts"]["categorical"]
pos = json.load(open(cat["layout"]))
check(len(pos) == N, "layout has one position per image (got %d)" % len(pos))
check(all(len(p) == 2 for p in pos), "every position is a 2D pair")
check(all(all(isinstance(v, (int, float)) for v in p) for p in pos),
      "every coordinate is numeric")
out_of_box = [i for i, p in enumerate(pos)
              if not (-1.0 - 1e-6 <= p[0] <= 1.0 + 1e-6
                      and -1.0 - 1e-6 <= p[1] <= 1.0 + 1e-6)]
check(not out_of_box, "all positions inside the [-1,1] viewport (%d out)"
      % len(out_of_box))
check(len(set(map(tuple, pos))) == N, "no two images share a position")

print("\n=== 4. REVIEWED HOTSPOTS ===")
rh = json.load(open(cat["hotspots"]))
check(len(rh) == 6, "6 reviewed groups (got %d)" % len(rh))
rh_idx = sorted(i for c in rh for i in c["images"])
check(len(rh_idx) == N, "reviewed groups cover 29 images (got %d)" % len(rh_idx))
check(rh_idx == list(range(N)), "reviewed groups cover every index exactly once")
check(len(set(rh_idx)) == len(rh_idx), "no duplicate assignments")
for c in rh:
    ok = all(0 <= i < N for i in c["images"])
    check(ok, "group %-45s indices in range" % ('"' + c["label"][:42] + '"'))
check(all(c["layout"] == "categorical" for c in rh),
      "every reviewed hotspot targets the categorical layout")

print("\n=== 5. REVIEWED MATCHES THE REPORT ===")
report_groups = {g["label"]: sorted(g["indices"]) for g in reviewed["groups"]}
layout_groups = {c["label"]: sorted(c["images"]) for c in rh}
check(report_groups == layout_groups,
      "reviewed hotspot groups match reviewed_classification.json exactly")

print("\n=== 6. LABELS ===")
lbl = json.load(open(cat["labels"]))
check(len(lbl["labels"]) == 6, "6 group labels (got %d)" % len(lbl["labels"]))
check(len(lbl["positions"]) == 6, "6 label positions")
check(all(t.upper() == t for t in lbl["labels"]), "all labels are uppercase")

print("\n=== 7. SOURCE PHOTOS READ-ONLY ===")
src = "/Users/vickilaaam/Downloads/B24_photo"
jpgs = sorted(f for f in os.listdir(src) if f.lower().endswith(".jpg"))
check(len(jpgs) == 29, "source folder still holds 29 jpgs (got %d)" % len(jpgs))
check(sorted(jpgs) == sorted(images), "source filenames match the imagelist")

print("\n=== 8. PART 2 OUTPUT READ-ONLY ===")
p2 = "/Users/vickilaaam/Downloads/B24_PixPlot_Trial_01/output/data/manifest.json"
if os.path.exists(p2):
    m2 = json.load(open(p2))
    check("categorical" not in m2["layouts"] or not m2["layouts"]["categorical"],
          "Part 2 manifest still has no categorical layout")
    check(abs(m2["point_sizes"]["scatter"] - 0.03333333333333333) < 1e-12,
          "Part 2 point_sizes.scatter still original (%.6f)"
          % m2["point_sizes"]["scatter"])

print("\n" + "=" * 60)
print("PASSED: %d    FAILED: %d" % (len(passes), len(fails)))
if fails:
    print("\nFAILURES:")
    for f in fails:
        print("  -", f)
    raise SystemExit(1)
print("ALL CHECKS PASS")

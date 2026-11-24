import json
import os
import hashlib

REVIEWED = "/Users/vickilaaam/Downloads/B24_PixPlot_Trial_01_Reviewed/output"
PART2 = "/Users/vickilaaam/Downloads/B24_PixPlot_Trial_01/output"
REVIEW_ROOT = "/Users/vickilaaam/Downloads/B24_PixPlot_Trial_01_Reviewed"
SRC = "/Users/vickilaaam/Downloads/B24_photo"

ok = True


def check(label, cond, detail=""):
    global ok
    if not cond:
        ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {label}" + (f"  -- {detail}" if detail else ""))


il = json.load(open(f"{REVIEWED}/data/imagelists/imagelist-b5aaaf68-e815-11f1-be1a-dd0a4049e509.json"))
names = il["images"]

print("=== 1. JSON validity ===")
for p in [
    f"{REVIEWED}/data/manifest.json",
    f"{REVIEWED}/data/hotspots/user_hotspots.json",
    f"{REVIEW_ROOT}/reviewed_classification.json",
    f"{PART2}/data/manifest.json",
    f"{PART2}/data/hotspots/hotspot-b5aaaf68-e815-11f1-be1a-dd0a4049e509.json",
]:
    try:
        json.load(open(p))
        check(os.path.relpath(p, "/Users/vickilaaam/Downloads"), True)
    except Exception as e:
        check(os.path.relpath(p, "/Users/vickilaaam/Downloads"), False, str(e))

print()
print("=== 2. user_hotspots matches the viewer's native flat schema ===")
uh = json.load(open(f"{REVIEWED}/data/hotspots/user_hotspots.json"))
check("is a flat list", isinstance(uh, list), type(uh).__name__)
auto = json.load(open(f"{PART2}/data/hotspots/hotspot-b5aaaf68-e815-11f1-be1a-dd0a4049e509.json"))
auto_keys = set(auto[0].keys())
check("automatic schema keys == 'images','img','label','layout'", auto_keys == {"images", "img", "label", "layout"}, str(auto_keys))
for h in uh:
    check(f"'{h['label'][:38]}' has all automatic keys", set(h.keys()) == auto_keys, str(sorted(h.keys())))
    check(f"'{h['label'][:38]}' img file exists in data/thumbs",
          os.path.isfile(f"{REVIEWED}/data/thumbs/{h['img']}"), h["img"])

print()
print("=== 3. Coverage: all 29 exactly once ===")
idx = [i for h in uh for i in h["images"]]
check("total assigned == 29", len(idx) == 29, f"got {len(idx)}")
check("no duplicates", len(set(idx)) == len(idx),
      str([i for i in set(idx) if idx.count(i) > 1]))
check("no missing", not (set(range(29)) - set(idx)), str(sorted(set(range(29)) - set(idx))))
check("all indices in 0..28", all(0 <= i < 29 for i in idx))

print()
print("=== 4. Cross-check: detailed report matches hotspot file ===")
rc = json.load(open(f"{REVIEW_ROOT}/reviewed_classification.json"))
check("group counts match", len(rc["groups"]) == len(uh), f"{len(rc['groups'])} vs {len(uh)}")
for g, h in zip(rc["groups"], uh):
    check(f"'{g['label'][:38]}' indices match", g["indices"] == h["images"], f"{g['indices']} vs {h['images']}")
    check(f"'{g['label'][:38]}' label matches", g["label"] == h["label"])
    check(f"'{g['label'][:38]}' filenames match imagelist",
          [names[i] for i in g["indices"]] == g["filenames"])
    check(f"'{g['label'][:38]}' filenames exist in source",
          all(os.path.isfile(os.path.join(SRC, f)) for f in g["filenames"]))
check("report total == 29", rc["total_images"] == 29)
check("report sum(counts) == 29", sum(rc["counts"].values()) == 29)
check("report unassigned empty", rc["unassigned"] == [])

print()
print("=== 5. Automatic grouping preserved (byte-identical) ===")
h1 = hashlib.sha256(open(f"{PART2}/data/hotspots/hotspot-b5aaaf68-e815-11f1-be1a-dd0a4049e509.json", "rb").read()).hexdigest()
h2 = hashlib.sha256(open(f"{REVIEWED}/data/hotspots/hotspot-b5aaaf68-e815-11f1-be1a-dd0a4049e509.json", "rb").read()).hexdigest()
check("automatic hotspot file unchanged", h1 == h2)

print()
print("=== 6. Part 2 output untouched ===")
p2 = json.load(open(f"{PART2}/data/manifest.json"))
check("part2 output_directory", p2["output_directory"] == PART2, p2["output_directory"])
check("part2 point_sizes.scatter == 0.03333", abs(p2["point_sizes"]["scatter"] - 0.03333333333333333) < 1e-12)
check("part2 point_sizes.max == 0.2", abs(p2["point_sizes"]["max"] - 0.2) < 1e-9)
check("part2 has 29 originals", len(os.listdir(f"{PART2}/data/originals")) == 29)

print()
print("=== 7. Reviewed manifest: sizes 3x, cell untouched, paths repointed ===")
rm = json.load(open(f"{REVIEWED}/data/manifest.json"))
old, new = p2["point_sizes"], rm["point_sizes"]
for k in ["scatter", "initial", "grid", "categorical", "geographic", "max"]:
    ratio = new[k] / old[k]
    check(f"{k}: {old[k]:.6g} -> {new[k]:.6g}  (x{ratio:.2f})", abs(ratio - 3.0) < 0.01)
check("new max >= new scatter", new["max"] >= new["scatter"])
check("new max >= new grid", new["max"] >= new["grid"])
check("config.sizes.cell still 32", rm["config"]["sizes"]["cell"] == 32)
check("config.sizes.atlas still 2048", rm["config"]["sizes"]["atlas"] == 2048)
check("output_directory repointed", rm["output_directory"] == REVIEWED, rm["output_directory"])
for key in ["imagelist", "atlas_dir", "default_hotspots", "custom_hotspots"]:
    check(f"{key} points into Reviewed folder", rm[key].startswith(REVIEWED), rm[key])
check("umap layout repointed",
      rm["layouts"]["umap"]["variants"][0]["layout"].startswith(REVIEWED))
check("no stale Part2 paths in manifest", PART2 not in json.dumps(rm))

print()
print("=== 8. Source photos untouched ===")
src = sorted(f for f in os.listdir(SRC) if f.lower().endswith(".jpg"))
check("source still has 29 jpgs", len(src) == 29, f"got {len(src)}")
check("source filenames identical to imagelist", src == names)
check("no files added to source", len(os.listdir(SRC)) == 29)

print()
print("=" * 62)
print("OVERALL:", "ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")
print("=" * 62)
print()
print("REVIEWED GROUPS (WorkBuddy/student visual review, not PixPlot output):")
for h in uh:
    print(f"  {len(h['images']):2d}  {h['label']}")
    print(f"      {', '.join(names[i] for i in h['images'])}")
print(f"  --  TOTAL: {sum(len(h['images']) for h in uh)}")

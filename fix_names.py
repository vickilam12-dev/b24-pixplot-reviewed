import os
import re

ROOT = "/Users/vickilaaam/Downloads/B24_PixPlot_Trial_01_Reviewed/output"

# rsync temp names look like ".realname.XXXXXX" -> "realname"
pattern = re.compile(r"^\.(.+)\.([A-Za-z0-9]{6})$")

renamed = 0
skipped = 0

for dirpath, dirnames, filenames in os.walk(ROOT):
    for name in filenames:
        m = pattern.match(name)
        if not m:
            continue
        real = m.group(1)
        src = os.path.join(dirpath, name)
        dst = os.path.join(dirpath, real)
        if os.path.exists(dst):
            # target already correct, remove the temp duplicate
            try:
                os.remove(src)
                skipped += 1
            except Exception as e:
                print("could not remove", src, e)
            continue
        try:
            os.rename(src, dst)
            renamed += 1
        except Exception as e:
            print("could not rename", src, "->", dst, e)

print("renamed:", renamed)
print("removed duplicates:", skipped)

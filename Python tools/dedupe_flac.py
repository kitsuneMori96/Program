import hashlib
import os
from collections import defaultdict

TARGET_DIR = r"D:\Download"   # ← 改成你的目录
EXT = ".flac"

def sha1(path, buf_size=1024 * 1024):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        while chunk := f.read(buf_size):
            h.update(chunk)
    return h.hexdigest()

files = [
    os.path.join(TARGET_DIR, f)
    for f in os.listdir(TARGET_DIR)
    if f.lower().endswith(EXT)
]

hash_map = defaultdict(list)

print("正在计算 hash...")
for f in files:
    try:
        h = sha1(f)
        hash_map[h].append(f)
    except Exception as e:
        print("跳过:", f, e)

deleted = 0

print("\n开始去重：")
for h, group in hash_map.items():
    if len(group) <= 1:
        continue

    # 按创建时间排序，保留最早的
    group.sort(key=lambda x: os.path.getctime(x))
    keep = group[0]
    print(f"\n保留: {os.path.basename(keep)}")

    for dup in group[1:]:
        print("  删除:", os.path.basename(dup))
        os.remove(dup)
        deleted += 1

print(f"\n完成，共删除 {deleted} 个重复文件")

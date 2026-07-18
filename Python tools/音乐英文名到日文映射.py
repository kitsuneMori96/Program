#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量重命名音频文件，按序号匹配日文曲目名。
默认处理脚本所在目录，也可通过命令行参数指定其他目录。
适用场景：Disc 1（25首）
支持格式：.flac .mp3 .wav .ogg .m4a .ape
"""

import os
import re
import sys

# ====== Disc 1 曲目映射 (序号 -> 日文名称) ======
TRACK_MAP = {
    1:  "大切なものは見えないんだよ",
    2:  "Only your angel",
    3:  "静寂のかこい",
    4:  "娘はドタドータ",
    5:  "放課後GOGO!",
    6:  "午後はお茶して",
    7:  "初夏のひととき",
    8:  "ゆきなちゃん危機一髪",
    9:  "聖峰の庭で",
    10: "召使いのご奉仕",
    11: "融心",
    12: "背後に迫る",
    13: "慟哭の少女",
    14: "届かないメール",
    15: "切ないけど今だけは",
    16: "夏の終わる日",
    17: "こころのおと",
    18: "絆",
    19: "Only your angel(MarchArrange)",
    20: "Mint Kiss",
    21: "Only your angel(PianoArrange)",
    22: "BonusTrack 1",
    23: "BonusTrack 2",
    24: "BonusTrack 3",
    25: "BonusTrack 4",
}

AUDIO_EXTENSIONS = {".flac", ".mp3", ".wav", ".ogg", ".m4a", ".ape"}


def get_script_directory():
    """获取脚本自身所在的目录"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的exe，使用exe所在目录
        return os.path.dirname(sys.executable)
    else:
        # 普通Python脚本，使用__file__
        return os.path.dirname(os.path.abspath(__file__))


def extract_track_number(filename):
    """从文件名中提取两位数字序号（如 01, 02 ... 25）"""
    match = re.search(r'(\d{2})', filename)
    if match:
        return int(match.group(1))
    return None


def main(target_dir=None):
    if target_dir is None:
        target_dir = get_script_directory()

    if not os.path.isdir(target_dir):
        print(f"错误：目录不存在或无法访问 -> {target_dir}")
        input("按回车键退出...")
        return

    print(f"正在处理目录：{target_dir}\n")

    files_to_process = []
    for fname in os.listdir(target_dir):
        ext = os.path.splitext(fname)[1].lower()
        if ext in AUDIO_EXTENSIONS:
            track_num = extract_track_number(fname)
            if track_num and track_num in TRACK_MAP:
                files_to_process.append((track_num, fname))

    if not files_to_process:
        print("未找到任何可匹配序号的音频文件。")
        input("按回车键退出...")
        return

    files_to_process.sort(key=lambda x: x[0])

    print("\n=== 重命名预览 ===")
    rename_pairs = []
    for num, old_name in files_to_process:
        new_name = f"{num:02d} {TRACK_MAP[num]}{os.path.splitext(old_name)[1]}"
        rename_pairs.append((old_name, new_name))
        print(f"  {old_name}  ->  {new_name}")

    existing_names = set(os.listdir(target_dir))
    conflicts = [new for _, new in rename_pairs if new in existing_names]
    if conflicts:
        print("\n⚠️  警告：以下新文件名已存在于目录中，将被跳过：")
        for c in conflicts:
            print(f"  {c}")

    confirm = input("\n是否执行以上重命名？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消。")
        input("按回车键退出...")
        return

    success_count = 0
    skip_count = 0
    for old_name, new_name in rename_pairs:
        old_path = os.path.join(target_dir, old_name)
        new_path = os.path.join(target_dir, new_name)
        if os.path.exists(new_path):
            print(f"跳过（已存在）：{new_name}")
            skip_count += 1
            continue
        try:
            os.rename(old_path, new_path)
            print(f"成功：{old_name} -> {new_name}")
            success_count += 1
        except Exception as e:
            print(f"失败：{old_name} -> {e}")

    print(f"\n完成！成功 {success_count} 个，跳过 {skip_count} 个。")
    input("按回车键退出...")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
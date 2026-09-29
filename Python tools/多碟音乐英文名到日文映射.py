#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义多碟音乐目录重命名脚本
文件名格式：碟号-序号.扩展名  例如 1-01.flac , 2-10.flac
支持格式: .flac .mp3 .wav .ogg .m4a .ape
"""

import os
import re
import sys

# ====== 全局碟片曲目映射（碟号 -> {序号: 曲名}） ======
# 新增碟片只需在此字典添加条目即可
DISCS_MAP = {
    1: {
        1:  "想いのカナタ <夏空カナタ 主題歌>",
        2:  "想いのカナタ ～Piano Version～",
        3:  "想いのカナタ (Game Size)",
        4:  "島人",
        5:  "リゾートアイランド",
        6:  "ちょ、ま",
        7:  "日々の営み",
        8:  "夕暮れの風",
        9:  "朝の光に包まれて",
        10: "観察してみよう",
        11: "星空を見上げて",
        12: "告白",
        13: "緊迫",
        14: "芽生えた不安",
        15: "心の闇",
        16: "悲しい決意",
        17: "切ない想い",
        18: "憂鬱",
        19: "明日への一歩",
    },
    2: {
        1:  "想いのカナタ ～MusicBox Version～",
        2:  "昏い真実",
        3:  "絶望の淵で",
        4:  "塔弦島",
        5:  "二人の絆",
        6:  "最後の望み",
        7:  "激流",
        8:  "蠢動",
        9:  "抗うもの",
        10: "儚い願い",
        11: "あの頃のように",
        12: "灯と幻",
        13: "リフレイン (Game Size)",
        14: "リフレイン ～Piano Version～",
        15: "リフレイン <夏空カナタ エンディングテーマ>",
        16: "想いのカナタ (Karaoke Version)",
        17: "リフレイン (Karaoke Version)",
    },
}

AUDIO_EXTENSIONS = {".flac", ".mp3", ".wav", ".ogg", ".m4a", ".ape"}


def get_script_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def parse_disc_and_track(filename):
    """
    从文件名中提取碟号和序号。
    默认格式：碟号-序号  （如 1-01, 2-10）
    返回 (disc_num, track_num) 或 None
    """
    name_no_ext = os.path.splitext(filename)[0]
    m = re.match(r'(\d+)[-–—](\d+)', name_no_ext)
    if m:
        disc = int(m.group(1))
        track = int(m.group(2))
        return disc, track
    return None


def main(target_dir=None):
    if target_dir is None:
        target_dir = get_script_directory()

    if not os.path.isdir(target_dir):
        print(f"错误：目录不存在 -> {target_dir}")
        input("按回车键退出...")
        return

    print(f"处理目录：{target_dir}\n")

    files_to_process = []

    for fname in os.listdir(target_dir):
        ext = os.path.splitext(fname)[1].lower()
        if ext not in AUDIO_EXTENSIONS:
            continue
        parsed = parse_disc_and_track(fname)
        if parsed is None:
            continue
        disc, track = parsed
        if disc in DISCS_MAP and track in DISCS_MAP[disc]:
            files_to_process.append((disc, track, fname))
        else:
            print(f"忽略（碟{disc}无序号{track}）：{fname}")

    if not files_to_process:
        print("未找到任何符合格式的音频文件（格式应为 碟号-序号.扩展名）。")
        input("按回车键退出...")
        return

    files_to_process.sort(key=lambda x: (x[0], x[1]))

    print("=== 重命名预览 ===")
    rename_pairs = []
    for disc, track, old in files_to_process:
        jp_name = DISCS_MAP[disc][track]
        ext = os.path.splitext(old)[1]
        new = f"{disc}-{track:02d} {jp_name}{ext}"
        rename_pairs.append((old, new))
        print(f"  {old}  ->  {new}")

    existing = set(os.listdir(target_dir))
    conflicts = [n for _, n in rename_pairs if n in existing]
    if conflicts:
        print(f"\n⚠ 以下新文件名已存在，将被跳过：")
        for c in conflicts:
            print(f"  {c}")

    confirm = input("\n执行以上重命名？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消。")
        input("按回车键退出...")
        return

    ok = skip = 0
    for old, new in rename_pairs:
        old_path = os.path.join(target_dir, old)
        new_path = os.path.join(target_dir, new)
        if os.path.exists(new_path):
            print(f"跳过（已存在）：{new}")
            skip += 1
            continue
        try:
            os.rename(old_path, new_path)
            print(f"成功：{old} -> {new}")
            ok += 1
        except Exception as e:
            print(f"失败：{old} -> {e}")

    print(f"\n完成！成功 {ok} 个，跳过 {skip} 个。")
    input("按回车键退出...")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    main(target)
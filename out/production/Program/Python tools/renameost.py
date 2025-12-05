import os
import re
import glob

def rename_music_files():
    # 完整的曲目列表（24首）
    tracklist = [
        "01 みずいろ",
        "02 降る雪", 
        "03 ひなたより",
        "04 遠くへ",
        "05 静道と交差点",
        "06 いっしょに",
        "07 POP'n UP",
        "08 Sweet・Sweet",
        "09 みずいろ (アレンジバージョン)",
        "10 雨やどり",
        "11 あの海へと続く道",
        "12 シグナルブルー",
        "13 じゃあね",
        "14 POP'n UP",
        "15 ピアノの時間",
        "16 ごめんね... (アレンジバージョン)",
        "17 スカーレット",
        "18 みずいろ (オーゴール)",
        "19 あの日へ",
        "20 勝る高架線",
        "21 HAPPY・HAPPY",
        "22 ごめんね...",
        "23 みずいろ (カラオケ)",
        "24 ごめんね... (カラオケ)"
    ]
    
    # 获取当前目录或指定目录
    print("当前目录:", os.getcwd())
    folder_path = input("请输入音乐文件所在文件夹路径 (直接回车使用当前目录): ").strip()
    
    if not folder_path:
        folder_path = "."
    
    if not os.path.exists(folder_path):
        print(f"错误：文件夹路径不存在: {folder_path}")
        return
    
    # 获取所有音频文件
    audio_extensions = ['*.flac', '*.mp3', '*.wav', '*.m4a', '*.aac']
    audio_files = []
    for ext in audio_extensions:
        audio_files.extend(glob.glob(os.path.join(folder_path, ext)))
    
    # 只获取文件名（不包含路径）
    audio_files = [os.path.basename(f) for f in audio_files]
    
    if not audio_files:
        print("在指定文件夹中未找到音频文件")
        return
    
    print(f"\n找到 {len(audio_files)} 个音频文件:")
    for i, file in enumerate(audio_files, 1):
        print(f"{i:2d}. {file}")
    
    # 智能文件排序
    def get_sort_key(filename):
        # 提取文件名中的数字
        numbers = re.findall(r'\d+', filename)
        if numbers:
            return int(numbers[0])
        return filename
    
    audio_files.sort(key=get_sort_key)
    
    print("\n排序后的文件列表:")
    for i, file in enumerate(audio_files, 1):
        print(f"{i:2d}. {file}")
    
    # 确认是否继续
    if len(audio_files) != len(tracklist):
        print(f"\n警告: 找到 {len(audio_files)} 个文件，但曲目列表有 {len(tracklist)} 首")
        response = input("是否继续? (y/n): ").lower()
        if response != 'y':
            return
    
    print("\n重命名预览:")
    print("=" * 60)
    
    # 预览重命名效果
    rename_map = []
    for i, (old_filename, track_info) in enumerate(zip(audio_files, tracklist)):
        match = re.match(r'(\d+)\s+(.+)', track_info)
        if not match:
            continue
        
        track_num = match.group(1).zfill(2)
        track_name = match.group(2)
        
        file_ext = os.path.splitext(old_filename)[1]
        safe_track_name = re.sub(r'[<>:"/\\|?*]', '', track_name)
        new_filename = f"{track_num} {safe_track_name}{file_ext}"
        
        rename_map.append((old_filename, new_filename))
        print(f"{old_filename}")
        print(f"  → {new_filename}")
        print()
    
    print("=" * 60)
    
    # 确认执行重命名
    confirm = input("确认执行重命名? (y/n): ").lower()
    if confirm != 'y':
        print("取消重命名")
        return
    
    # 执行重命名
    success_count = 0
    for old_filename, new_filename in rename_map:
        old_path = os.path.join(folder_path, old_filename)
        new_path = os.path.join(folder_path, new_filename)
        
        try:
            # 检查目标文件是否已存在
            if os.path.exists(new_path):
                print(f"跳过: {new_filename} 已存在")
                continue
            
            os.rename(old_path, new_path)
            print(f"✓ {old_filename} → {new_filename}")
            success_count += 1
        except Exception as e:
            print(f"✗ 重命名失败: {old_filename} → {e}")
    
    print(f"\n重命名完成! 成功重命名 {success_count} 个文件")

def quick_rename():
    """快速重命名模式 - 直接按顺序重命名"""
    tracklist = [
        "01 みずいろ", "02 降る雪", "03 ひなたより", "04 遠くへ", 
        "05 静道と交差点", "06 いっしょに", "07 POP'n UP", "08 Sweet・Sweet",
        "09 みずいろ (アレンジバージョン)", "10 雨やどり", "11 あの海へと続く道",
        "12 シグナルブルー", "13 じゃあね", "14 POP'n UP", "15 ピアノの時間",
        "16 ごめんね... (アレンジバージョン)", "17 スカーレット", "18 みずいろ (オーゴール)",
        "19 あの日へ", "20 勝る高架線", "21 HAPPY・HAPPY", "22 ごめんね...",
        "23 みずいろ (カラオケ)", "24 ごめんね... (カラオケ)"
    ]
    
    folder_path = "."  # 当前目录
    audio_files = [f for f in os.listdir(folder_path) 
                  if f.lower().endswith(('.flac', '.mp3', '.wav', '.m4a'))]
    
    if not audio_files:
        print("当前目录下未找到音频文件")
        return
    
    # 按文件名排序
    audio_files.sort()
    
    print(f"找到 {len(audio_files)} 个文件，开始快速重命名...")
    
    for i, (old_file, track_info) in enumerate(zip(audio_files, tracklist)):
        if i >= len(tracklist):
            break
            
        match = re.match(r'(\d+)\s+(.+)', track_info)
        if match:
            track_num = match.group(1).zfill(2)
            track_name = match.group(2)
            file_ext = os.path.splitext(old_file)[1]
            safe_name = re.sub(r'[<>:"/\\|?*]', '', track_name)
            new_file = f"{track_num} {safe_name}{file_ext}"
            
            old_path = os.path.join(folder_path, old_file)
            new_path = os.path.join(folder_path, new_file)
            
            try:
                os.rename(old_path, new_path)
                print(f"✓ {old_file} → {new_file}")
            except Exception as e:
                print(f"✗ {old_file} → 失败: {e}")

if __name__ == "__main__":
    print("音乐文件重命名程序 - Python直接版")
    print("=" * 50)
    
    print("选择模式:")
    print("1. 标准模式（预览后确认）")
    print("2. 快速模式（直接重命名）")
    
    choice = input("请选择 (1 或 2): ").strip()
    
    if choice == "1":
        rename_music_files()
    elif choice == "2":
        quick_rename()
    else:
        print("无效选择")
import os
import glob
from mutagen import File
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TPE2, TRCK, TYER

def update_audio_tags():
    """更新音频文件的元数据标签"""
    
    # 完整的曲目列表
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
    
    # 专辑信息
    album_info = {
        'title': 'みずいろ オリジナル・サウンドトラック',  # 专辑标题
        'artist': 'Various Artists',  # 专辑艺术家
        'year': '2001',  # 发行年份
        'genre': 'Game Music'  # 流派
    }
    
    # 获取文件夹路径
    folder_path = input("请输入音频文件所在文件夹路径 (直接回车使用当前目录): ").strip()
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
    
    audio_files = [os.path.basename(f) for f in audio_files]
    
    if not audio_files:
        print("在指定文件夹中未找到音频文件")
        return
    
    print(f"找到 {len(audio_files)} 个音频文件")
    
    # 按文件名中的数字排序
    import re
    def extract_number(filename):
        numbers = re.findall(r'\d+', filename)
        return int(numbers[0]) if numbers else 0
    
    audio_files.sort(key=extract_number)
    
    print("\n文件列表:")
    for i, file in enumerate(audio_files, 1):
        print(f"{i:2d}. {file}")
    
    # 预览标签修改
    print("\n标签修改预览:")
    print("=" * 70)
    
    for i, (filename, track_info) in enumerate(zip(audio_files, tracklist)):
        if i >= len(tracklist):
            break
            
        match = re.match(r'(\d+)\s+(.+)', track_info)
        if match:
            track_num = match.group(1)
            track_title = match.group(2)
            
            print(f"{filename}")
            print(f"  → 标题: {track_title}")
            print(f"  → 音轨: {track_num}/{len(tracklist)}")
            print(f"  → 专辑: {album_info['title']}")
            print()
    
    print("=" * 70)
    
    # 确认执行
    confirm = input("确认修改标签? (y/n): ").lower()
    if confirm != 'y':
        print("取消修改")
        return
    
    # 执行标签修改
    success_count = 0
    for i, (filename, track_info) in enumerate(zip(audio_files, tracklist)):
        if i >= len(tracklist):
            break
            
        match = re.match(r'(\d+)\s+(.+)', track_info)
        if not match:
            continue
            
        track_num = match.group(1)
        track_title = match.group(2)
        
        file_path = os.path.join(folder_path, filename)
        
        try:
            # 根据文件类型处理
            if filename.lower().endswith('.flac'):
                success = update_flac_tags(file_path, track_title, track_num, album_info, i+1, len(tracklist))
            elif filename.lower().endswith('.mp3'):
                success = update_mp3_tags(file_path, track_title, track_num, album_info, i+1, len(tracklist))
            else:
                success = update_generic_tags(file_path, track_title, track_num, album_info, i+1, len(tracklist))
            
            if success:
                print(f"✓ {filename} - 标签更新成功")
                success_count += 1
            else:
                print(f"✗ {filename} - 标签更新失败")
                
        except Exception as e:
            print(f"✗ {filename} - 错误: {e}")
    
    print(f"\n标签修改完成! 成功更新 {success_count} 个文件的标签")

def update_flac_tags(file_path, title, track_num, album_info, track, total_tracks):
    """更新FLAC文件标签"""
    try:
        audio = FLAC(file_path)
        
        # 清除所有现有标签
        audio.delete()
        
        # 设置新标签
        audio['title'] = [title]
        audio['artist'] = [get_artist_from_title(title)]  # 从标题推测艺术家
        audio['album'] = [album_info['title']]
        audio['tracknumber'] = [str(track)]
        audio['tracktotal'] = [str(total_tracks)]
        audio['date'] = [album_info['year']]
        audio['genre'] = [album_info['genre']]
        
        audio.save()
        return True
    except Exception as e:
        print(f"FLAC标签更新错误: {e}")
        return False

def update_mp3_tags(file_path, title, track_num, album_info, track, total_tracks):
    """更新MP3文件标签"""
    try:
        # 尝试读取现有标签，如果没有则创建
        try:
            audio = ID3(file_path)
        except:
            audio = ID3()
        
        # 更新ID3标签
        audio.delall('TIT2')  # 标题
        audio.delall('TPE1')  # 艺术家
        audio.delall('TALB')  # 专辑
        audio.delall('TRCK')  # 音轨号
        audio.delall('TYER')  # 年份
        
        audio.add(TIT2(encoding=3, text=title))
        audio.add(TPE1(encoding=3, text=get_artist_from_title(title)))
        audio.add(TALB(encoding=3, text=album_info['title']))
        audio.add(TRCK(encoding=3, text=f"{track}/{total_tracks}"))
        audio.add(TYER(encoding=3, text=album_info['year']))
        
        audio.save(file_path)
        return True
    except Exception as e:
        print(f"MP3标签更新错误: {e}")
        return False

def update_generic_tags(file_path, title, track_num, album_info, track, total_tracks):
    """更新其他格式的音频文件标签"""
    try:
        audio = File(file_path, easy=True)
        if audio is not None:
            audio['title'] = title
            audio['artist'] = get_artist_from_title(title)
            audio['album'] = album_info['title']
            audio['tracknumber'] = f"{track}/{total_tracks}"
            audio['date'] = album_info['year']
            audio['genre'] = album_info['genre']
            audio.save()
            return True
        return False
    except Exception as e:
        print(f"通用标签更新错误: {e}")
        return False

def get_artist_from_title(title):
    """从标题中提取艺术家信息（简单实现）"""
    # 这里可以根据需要自定义艺术家映射
    artist_mapping = {
        "みずいろ": "下川直哉",
        "降る雪": "下川直哉", 
        "ひなたより": "下川直哉",
        # 可以继续添加其他映射
    }
    
    # 尝试匹配已知的标题
    for key, artist in artist_mapping.items():
        if key in title:
            return artist
    
    # 默认返回
    return "Various Artists"

def show_current_tags():
    """显示当前文件的标签信息"""
    folder_path = input("请输入音频文件所在文件夹路径 (直接回车使用当前目录): ").strip()
    if not folder_path:
        folder_path = "."
    
    audio_files = [f for f in os.listdir(folder_path) 
                  if f.lower().endswith(('.flac', '.mp3', '.wav', '.m4a'))]
    
    if not audio_files:
        print("未找到音频文件")
        return
    
    print("\n当前文件标签信息:")
    print("=" * 70)
    
    for filename in audio_files[:5]:  # 只显示前5个文件
        file_path = os.path.join(folder_path, filename)
        try:
            audio = File(file_path, easy=True)
            if audio:
                title = audio.get('title', ['未知'])[0]
                artist = audio.get('artist', ['未知'])[0]
                album = audio.get('album', ['未知'])[0]
                print(f"{filename}")
                print(f"  标题: {title}")
                print(f"  艺术家: {artist}")
                print(f"  专辑: {album}")
                print()
        except:
            print(f"{filename} - 无法读取标签")
    
    print("=" * 70)

if __name__ == "__main__":
    print("音频文件标签编辑器")
    print("=" * 50)
    
    # 检查是否安装了mutagen
    try:
        import mutagen
        print("mutagen库已安装")
    except ImportError:
        print("错误: 需要安装mutagen库")
        print("请运行: pip install mutagen")
        exit(1)
    
    print("\n选择操作:")
    print("1. 更新音频文件标签")
    print("2. 查看当前标签信息")
    print("3. 同时重命名文件和更新标签")
    
    choice = input("请选择 (1/2/3): ").strip()
    
    if choice == "1":
        update_audio_tags()
    elif choice == "2":
        show_current_tags()
    elif choice == "3":
        # 这里可以组合文件重命名和标签更新
        print("此功能需要先实现文件重命名")
        update_audio_tags()
    else:
        print("无效选择")
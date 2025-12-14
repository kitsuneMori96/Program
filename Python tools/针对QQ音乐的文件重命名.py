import os
import re
import tkinter as tk
from tkinter import filedialog
from rapidfuzz import fuzz, process
import shutil
import tempfile

def select_directory():
    """
    弹出图形对话框让用户选择文件夹
    """
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    folder_selected = filedialog.askdirectory(title="请选择包含音乐文件的文件夹")
    root.destroy()
    return folder_selected

def extract_song_name(filename, file_type):
    """
    从文件名中提取标准化的歌名
    file_type: '.ogg' 或 '.wav'
    """
    base_name = os.path.splitext(filename)[0]
    
    if file_type == '.ogg':
        # OGG格式: "艺术家 - 歌名 [mqms2]"
        if ' - ' in base_name:
            parts = base_name.split(' - ', 1)
            if len(parts) > 1:
                song_name = re.sub(r'\[mqms2\]', '', parts[1]).strip()
                return song_name
        return base_name
    
    elif file_type == '.wav':
        # WAV格式: "序号 歌名" - 移除序号
        song_name = re.sub(r'^\d+\s*', '', base_name).strip()
        return song_name
    
    return base_name

def normalize_title(title):
    """
    标准化歌名用于匹配，处理变体差异
    """
    if not title:
        return ""
    
    # 转换为小写
    title = title.lower()
    
    # 处理常见的变体符号
    title = re.sub(r'[～~]', ' ', title)
    title = re.sub(r'[・･]', ' ', title)
    title = re.sub(r'[\(（].*?[\)）]', '', title)  # 移除括号内容
    title = re.sub(r'[\[［].*?[\]］]', '', title)  # 移除方括号内容
    
    # 处理特定变体
    title = re.sub(r'\s*arrange\s*', ' ', title)
    title = re.sub(r'\s*ver\.?\s*', ' ', title)
    title = re.sub(r'\s*orgel\s*', ' ', title)
    
    # 标准化标点和空格
    title = re.sub(r'[^\w\s]', ' ', title)  # 移除非字母数字字符
    title = re.sub(r'\s+', ' ', title).strip()  # 合并多余空格
    
    return title

def find_best_matches(ogg_files, wav_files, similarity_threshold=75):
    """
    为每个WAV文件找到最匹配的OGG文件
    返回匹配列表和未匹配的文件
    """
    matches = []
    used_ogg_files = set()
    used_wav_files = set()
    
    # 预处理所有文件
    ogg_data = []
    for ogg_file in ogg_files:
        song_name = extract_song_name(ogg_file, '.ogg')
        normalized = normalize_title(song_name)
        ogg_data.append({
            'file': ogg_file,
            'song_name': song_name,
            'normalized': normalized
        })
    
    wav_data = []
    for wav_file in wav_files:
        song_name = extract_song_name(wav_file, '.wav')
        normalized = normalize_title(song_name)
        wav_data.append({
            'file': wav_file,
            'song_name': song_name,
            'normalized': normalized
        })
    
    # 为每个WAV文件寻找最佳匹配
    for wav_item in wav_data:
        best_match = None
        best_score = 0
        
        for ogg_item in ogg_data:
            if ogg_item['file'] in used_ogg_files:
                continue
                
            # 计算相似度
            score = fuzz.ratio(wav_item['normalized'], ogg_item['normalized'])
            
            # 如果找到更好的匹配
            if score > best_score and score >= similarity_threshold:
                best_match = ogg_item['file']
                best_score = score
        
        if best_match:
            matches.append((wav_item['file'], best_match, best_score))
            used_ogg_files.add(best_match)
            used_wav_files.add(wav_item['file'])
    
    # 找出未匹配的文件
    unmatched_ogg = [ogg for ogg in ogg_files if ogg not in used_ogg_files]
    unmatched_wav = [wav for wav in wav_files if wav not in used_wav_files]
    
    return matches, unmatched_ogg, unmatched_wav

def safe_file_operation(wav_path, ogg_path, new_path, backup_dir):
    """
    安全执行文件操作：先删除OGG文件，再重命名WAV文件
    """
    try:
        # 1. 备份原始OGG文件
        ogg_backup_path = os.path.join(backup_dir, os.path.basename(ogg_path))
        if os.path.exists(ogg_path):
            shutil.copy2(ogg_path, ogg_backup_path)
        
        # 2. 备份原始WAV文件
        wav_backup_path = os.path.join(backup_dir, os.path.basename(wav_path))
        if os.path.exists(wav_path):
            shutil.copy2(wav_path, wav_backup_path)
        
        # 3. 删除OGG文件
        if os.path.exists(ogg_path):
            os.remove(ogg_path)
            print(f"    ✓ 已删除OGG文件: {os.path.basename(ogg_path)}")
        
        # 4. 检查目标路径是否已存在
        if os.path.exists(new_path):
            # 如果存在，先删除（可能是之前操作失败留下的）
            os.remove(new_path)
            print(f"    ! 清理了已存在的目标文件: {os.path.basename(new_path)}")
        
        # 5. 重命名WAV文件
        os.rename(wav_path, new_path)
        print(f"    ✓ 已重命名WAV文件: {os.path.basename(wav_path)} -> {os.path.basename(new_path)}")
        
        return True, "操作成功"
        
    except Exception as e:
        # 尝试恢复备份（如果操作失败）
        try:
            if os.path.exists(ogg_backup_path) and not os.path.exists(ogg_path):
                shutil.copy2(ogg_backup_path, ogg_path)
            if os.path.exists(wav_backup_path) and not os.path.exists(wav_path):
                shutil.copy2(wav_backup_path, wav_path)
        except Exception as restore_error:
            print(f"    恢复备份失败: {restore_error}")
            
        return False, f"操作失败: {e}"

def process_music_files(directory, dry_run=True):
    """
    主处理函数
    dry_run: True=只显示将要执行的操作，False=实际执行
    """
    if not os.path.isdir(directory):
        print(f"错误：目录 '{directory}' 不存在")
        return None, None, None
    
    # 获取所有文件
    all_files = os.listdir(directory)
    ogg_files = [f for f in all_files if f.lower().endswith('.ogg')]
    wav_files = [f for f in all_files if f.lower().endswith('.wav')]
    
    print(f"找到 {len(ogg_files)} 个OGG文件")
    print(f"找到 {len(wav_files)} 个WAV文件")
    print("=" * 60)
    
    # 查找匹配和未匹配的文件
    matches, unmatched_ogg, unmatched_wav = find_best_matches(ogg_files, wav_files)
    
    # 输出匹配结果
    if matches:
        print(f"找到 {len(matches)} 个匹配的文件对：")
        print("=" * 60)
        
        for i, (wav_file, ogg_file, similarity) in enumerate(matches, 1):
            new_name = ogg_file  # 使用OGG文件的完整名称
            print(f"{i:2d}. 相似度: {similarity}%")
            print(f"    WAV: {wav_file}")
            print(f"    OGG: {ogg_file}")
            print(f"    → 将执行:")
            print(f"       1. 删除OGG文件: {ogg_file}")
            print(f"       2. 将WAV文件重命名为: {new_name}")
            print()
    else:
        print("未找到匹配的文件对")
    
    # 输出未匹配成功的文件
    if unmatched_ogg:
        print(f"未匹配的OGG文件 ({len(unmatched_ogg)}个):")
        print("-" * 40)
        for ogg_file in unmatched_ogg:
            print(f"  - {ogg_file}")
        print()
    
    if unmatched_wav:
        print(f"未匹配的WAV文件 ({len(unmatched_wav)}个):")
        print("-" * 40)
        for wav_file in unmatched_wav:
            print(f"  - {wav_file}")
        print()
    
    if dry_run:
        print("这是预览模式，未执行实际操作。")
        return matches, unmatched_ogg, unmatched_wav
    
    # 实际执行操作
    print("开始执行文件操作...")
    print("=" * 60)
    
    # 创建备份目录
    backup_dir = tempfile.mkdtemp(prefix="music_backup_")
    print(f"已创建备份目录: {backup_dir}")
    
    success_count = 0
    error_count = 0
    error_details = []
    
    for wav_file, ogg_file, similarity in matches:
        wav_path = os.path.join(directory, wav_file)
        ogg_path = os.path.join(directory, ogg_file)
        new_path = os.path.join(directory, ogg_file)  # 新文件路径
        
        print(f"处理: {wav_file} ↔ {ogg_file} (相似度: {similarity}%)")
        
        success, message = safe_file_operation(wav_path, ogg_path, new_path, backup_dir)
        
        if success:
            success_count += 1
            print(f"  ✓ 处理成功")
        else:
            error_count += 1
            error_details.append(f"{wav_file}/{ogg_file}: {message}")
            print(f"  ✗ 处理失败: {message}")
        
        print()
    
    print("=" * 60)
    print(f"操作完成: 成功 {success_count}, 失败 {error_count}")
    print(f"备份文件保存在: {backup_dir}")
    
    if error_details:
        print("失败详情:")
        for detail in error_details:
            print(f"  - {detail}")
    
    return matches, unmatched_ogg, unmatched_wav

def main():
    """
    主函数 - 使用图形化界面选择文件夹并处理文件
    """
    print("=" * 60)
    print("           安全音乐文件处理程序")
    print(" 操作逻辑: 1.保存OGG名→2.删除OGG→3.重命名WAV")
    print("=" * 60)
    
    print("请选择包含音乐文件的文件夹...")
    directory = select_directory()
    
    if not directory:
        print("未选择文件夹，程序退出。")
        return
    
    print(f"已选择文件夹: {directory}")
    print()
    
    # 先进行预览
    matches, unmatched_ogg, unmatched_wav = process_music_files(directory, dry_run=True)
    
    if not matches:
        print("没有找到匹配的文件对，程序退出。")
        return
    
    # 询问用户是否执行实际操作
    response = input("\n是否执行以上操作？(y/N): ").strip().lower()
    if response == 'y' or response == 'yes':
        print()
        process_music_files(directory, dry_run=False)
        print("所有操作已完成！")
        
        # 显示最终状态报告
        print("\n" + "=" * 60)
        print("最终状态报告:")
        print(f"  - 成功处理: {len(matches)} 个文件对")
        if unmatched_ogg:
            print(f"  - 未匹配的OGG文件: {len(unmatched_ogg)} 个")
        if unmatched_wav:
            print(f"  - 未匹配的WAV文件: {len(unmatched_wav)} 个")
        print("=" * 60)
    else:
        print("操作已取消。")

if __name__ == "__main__":
    main()
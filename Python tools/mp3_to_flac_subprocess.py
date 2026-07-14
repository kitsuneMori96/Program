import os
import sys
import subprocess

def check_ffmpeg():
    """检查 ffmpeg 是否可用"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def convert_mp3_to_flac(input_path):
    """使用 ffmpeg 将单个 MP3 转换为同目录下的 FLAC"""
    base_name = os.path.splitext(input_path)[0]
    output_path = base_name + ".flac"

    # 如果目标 FLAC 已存在，跳过
    if os.path.exists(output_path):
        print(f"⏭️ 跳过 (已存在): {os.path.basename(input_path)}")
        return

    print(f"🔄 正在转换: {os.path.basename(input_path)} ...", end="", flush=True)

    # 调用 ffmpeg 命令：-i 输入 -vn 忽略视频 -c:a flac 音频编码为 flac -y 覆盖输出
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-vn",               # 忽略视频流（如果有）
        "-c:a", "flac",
        "-compression_level", "5",  # 默认压缩等级 5，平衡速度和大小
        "-y",                # 覆盖已有文件
        output_path
    ]

    try:
        # 运行 ffmpeg，捕获标准输出和错误，避免打印大量日志
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(" ✅ 完成")
        else:
            print(f" ❌ ffmpeg 返回错误:\n{result.stderr}")
    except Exception as e:
        print(f" ❌ 异常: {e}")

def batch_convert_in_current_folder():
    """扫描脚本所在目录，批量转换所有 MP3"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"--- 正在扫描目录: {script_dir} ---")

    # 列出所有 mp3 文件（不区分大小写）
    mp3_files = [f for f in os.listdir(script_dir) if f.lower().endswith('.mp3')]

    if not mp3_files:
        print("❌ 当前文件夹中没有找到 MP3 文件。")
        print("请将此脚本放在含有 MP3 文件的文件夹中再运行。")
        return

    print(f"📂 找到了 {len(mp3_files)} 个 MP3 文件，准备开始转换...")
    print("-" * 60)

    for mp3_file in mp3_files:
        full_path = os.path.join(script_dir, mp3_file)
        convert_mp3_to_flac(full_path)

    print("-" * 60)
    print(f"🎉 全部转换结束！输出文件已保存在当前文件夹。")

if __name__ == "__main__":
    # 首先检查 ffmpeg 是否可用
    if not check_ffmpeg():
        print("❌ 错误：未检测到 ffmpeg。")
        print("请从 https://ffmpeg.org/download.html 下载并安装。")
        print("安装后务必将其 bin 目录添加到系统 PATH 环境变量中。")
        print("\n按 Enter 键退出...")
        input()
        sys.exit(1)

    batch_convert_in_current_folder()

    print("\n✅ 按 Enter 键退出本窗口...")
    input()
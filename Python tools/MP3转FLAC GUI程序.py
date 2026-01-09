import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import threading

# 检查pydub是否安装
try:
    from pydub import AudioSegment
except ImportError:
    print("错误：未找到pydub库。请通过 'pip install pydub' 安装。")
    sys.exit(1)

def convert_mp3_to_flac(input_folder, output_folder):
    """
    将输入文件夹中的所有MP3文件转换为FLAC格式，保存到输出文件夹。
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except PermissionError:
            print(f"错误：无法创建输出文件夹 {output_folder}，请检查权限。")
            return
        except Exception as e:
            print(f"创建输出文件夹时出错: {e}")
            return
    
    # 遍历文件夹中的mp3文件
    mp3_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".mp3")]
    if not mp3_files:
        print("未找到MP3文件。")
        return
    
    for filename in mp3_files:
        mp3_path = os.path.join(input_folder, filename)
        flac_filename = os.path.splitext(filename)[0] + ".flac"
        flac_path = os.path.join(output_folder, flac_filename)
        
        try:
            # 加载mp3文件并转换为flac
            audio = AudioSegment.from_mp3(mp3_path)
            audio.export(flac_path, format="flac")
            print(f"转换成功: {filename} -> {flac_filename}")
        except FileNotFoundError:
            print(f"文件不存在: {mp3_path}")
        except Exception as e:
            print(f"转换失败 {filename}: {e}")

def select_folder():
    """
    打开文件夹选择对话框，并启动转换线程。
    """
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        # 在同一个文件夹中新建输出文件夹
        output_folder = os.path.join(folder_selected, "flac_output")
        # 在后台线程中运行转换，避免GUI冻结
        thread = threading.Thread(target=convert_mp3_to_flac, args=(folder_selected, output_folder))
        thread.daemon = True  # 设置为守护线程，主程序退出时线程也会退出
        thread.start()
        messagebox.showinfo("开始转换", f"转换已开始，输出文件夹: {output_folder}\n请查看控制台输出以获取详细信息。")

def main():
    root = tk.Tk()
    root.title("MP3 转 FLAC 转换器")
    root.geometry("400x200")
    
    label = tk.Label(root, text="选择包含MP3文件的文件夹", font=("Arial", 12))
    label.pack(pady=20)
    
    button = tk.Button(root, text="选择文件夹", command=select_folder, font=("Arial", 12), height=2, width=20)
    button.pack(pady=20)
    
    # 添加退出按钮
    exit_button = tk.Button(root, text="退出", command=root.quit, font=("Arial", 10))
    exit_button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()

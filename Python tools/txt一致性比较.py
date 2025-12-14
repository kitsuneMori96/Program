import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import hashlib
import os
from difflib import Differ, unified_diff

class FileComparator:
    def __init__(self, root):
        self.root = root
        self.root.title("文本文件比较工具")
        self.root.geometry("800x600")
        
        # 初始化文件路径
        self.file1_path = ""
        self.file2_path = ""
        
        # 设置界面
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = tk.Label(main_frame, text="文本文件比较工具", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 文件选择区域
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        # 文件1选择
        file1_frame = tk.Frame(file_frame)
        file1_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(file1_frame, text="文件1:", width=8, anchor="w").pack(side=tk.LEFT)
        self.file1_label = tk.Label(file1_frame, text="未选择文件", 
                                   bg="#f0f0f0", relief=tk.SUNKEN, 
                                   anchor="w", padx=5, pady=2)
        self.file1_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        tk.Button(file1_frame, text="选择文件", 
                 command=self.select_file1).pack(side=tk.LEFT, padx=(5, 0))
        
        # 文件2选择
        file2_frame = tk.Frame(file_frame)
        file2_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(file2_frame, text="文件2:", width=8, anchor="w").pack(side=tk.LEFT)
        self.file2_label = tk.Label(file2_frame, text="未选择文件", 
                                   bg="#f0f0f0", relief=tk.SUNKEN, 
                                   anchor="w", padx=5, pady=2)
        self.file2_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        tk.Button(file2_frame, text="选择文件", 
                 command=self.select_file2).pack(side=tk.LEFT, padx=(5, 0))
        
        # 比较选项
        options_frame = tk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        # 比较模式选择
        mode_frame = tk.Frame(options_frame)
        mode_frame.pack(anchor="w", pady=5)
        
        tk.Label(mode_frame, text="比较模式:").pack(side=tk.LEFT)
        
        self.compare_mode = tk.StringVar(value="hash")
        tk.Radiobutton(mode_frame, text="哈希值比较", variable=self.compare_mode, 
                      value="hash").pack(side=tk.LEFT, padx=(10, 0))
        tk.Radiobutton(mode_frame, text="逐行比较", variable=self.compare_mode, 
                      value="line").pack(side=tk.LEFT, padx=(10, 0))
        tk.Radiobutton(mode_frame, text="差异对比", variable=self.compare_mode, 
                      value="diff").pack(side=tk.LEFT, padx=(10, 0))
        
        # 比较按钮
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="开始比较", 
                 command=self.compare_files, bg="#4CAF50", fg="white",
                 font=("Arial", 10, "bold"), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="清空结果", 
                 command=self.clear_results, bg="#f44336", fg="white",
                 font=("Arial", 10), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="退出程序", 
                 command=self.root.quit, bg="#607D8B", fg="white",
                 font=("Arial", 10), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        # 结果显示区域
        result_frame = tk.LabelFrame(main_frame, text="比较结果", padx=10, pady=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # 滚动文本框用于显示详细结果
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, 
                                                    font=("Courier", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status_bar = tk.Label(main_frame, text="就绪", bd=1, relief=tk.SUNKEN, 
                                  anchor=tk.W, padx=5)
        self.status_bar.pack(fill=tk.X, pady=(5, 0))
        
    def select_file1(self):
        """选择第一个文件"""
        filename = filedialog.askopenfilename(
            title="选择第一个文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filename:
            self.file1_path = filename
            self.file1_label.config(text=os.path.basename(filename))
            self.update_status(f"已选择文件1: {filename}")
            
    def select_file2(self):
        """选择第二个文件"""
        filename = filedialog.askopenfilename(
            title="选择第二个文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filename:
            self.file2_path = filename
            self.file2_label.config(text=os.path.basename(filename))
            self.update_status(f"已选择文件2: {filename}")
            
    def update_status(self, message):
        """更新状态栏"""
        self.status_bar.config(text=message)
        self.root.update()
            
    def calculate_file_hash(self, filepath, algorithm='sha256'):
        """计算文件的哈希值"""
        hash_func = hashlib.new(algorithm)
        try:
            with open(filepath, 'rb') as f:
                # 分块读取大文件，避免内存不足
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            return f"计算哈希值时出错: {e}"
            
    def read_file_lines(self, filepath):
        """读取文件的所有行"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.readlines()
        except UnicodeDecodeError:
            # 如果utf-8失败，尝试其他编码
            try:
                with open(filepath, 'r', encoding='gbk') as f:
                    return f.readlines()
            except Exception as e:
                return f"读取文件时出错: {e}"
        except Exception as e:
            return f"读取文件时出错: {e}"
            
    def compare_files(self):
        """比较两个文件"""
        # 清空结果区域
        self.result_text.delete(1.0, tk.END)
        
        # 检查是否选择了两个文件
        if not self.file1_path or not self.file2_path:
            messagebox.showwarning("警告", "请先选择两个文件进行比较")
            return
            
        # 检查文件是否存在
        if not os.path.exists(self.file1_path):
            messagebox.showerror("错误", f"文件不存在: {self.file1_path}")
            return
            
        if not os.path.exists(self.file2_path):
            messagebox.showerror("错误", f"文件不存在: {self.file2_path}")
            return
            
        self.update_status("正在比较文件...")
        
        # 获取比较模式
        mode = self.compare_mode.get()
        
        # 显示基本信息
        self.result_text.insert(tk.END, "="*60 + "\n")
        self.result_text.insert(tk.END, "文件比较报告\n")
        self.result_text.insert(tk.END, "="*60 + "\n\n")
        
        file1_size = os.path.getsize(self.file1_path)
        file2_size = os.path.getsize(self.file2_path)
        
        self.result_text.insert(tk.END, f"文件1: {self.file1_path}\n")
        self.result_text.insert(tk.END, f"大小: {file1_size} 字节\n\n")
        
        self.result_text.insert(tk.END, f"文件2: {self.file2_path}\n")
        self.result_text.insert(tk.END, f"大小: {file2_size} 字节\n\n")
        
        self.result_text.insert(tk.END, "-"*60 + "\n")
        
        # 根据选择的模式进行比较
        if mode == "hash":
            self.compare_by_hash()
        elif mode == "line":
            self.compare_line_by_line()
        else:  # diff mode
            self.show_differences()
            
        self.update_status("比较完成")
        
    def compare_by_hash(self):
        """通过哈希值比较文件"""
        self.result_text.insert(tk.END, "哈希值比较结果:\n")
        self.result_text.insert(tk.END, "-"*40 + "\n")
        
        # 计算SHA256哈希值
        hash1 = self.calculate_file_hash(self.file1_path, 'sha256')
        hash2 = self.calculate_file_hash(self.file2_path, 'sha256')
        
        self.result_text.insert(tk.END, f"文件1 SHA256: {hash1}\n")
        self.result_text.insert(tk.END, f"文件2 SHA256: {hash2}\n\n")
        
        if hash1 == hash2:
            self.result_text.insert(tk.END, "✅ 结果: 两个文件完全相同\n")
        else:
            self.result_text.insert(tk.END, "❌ 结果: 两个文件不同\n")
            
        # 计算MD5哈希值
        hash1_md5 = self.calculate_file_hash(self.file1_path, 'md5')
        hash2_md5 = self.calculate_file_hash(self.file2_path, 'md5')
        
        self.result_text.insert(tk.END, "\n")
        self.result_text.insert(tk.END, f"文件1 MD5: {hash1_md5}\n")
        self.result_text.insert(tk.END, f"文件2 MD5: {hash2_md5}\n")
        
    def compare_line_by_line(self):
        """逐行比较文件内容"""
        self.result_text.insert(tk.END, "逐行比较结果:\n")
        self.result_text.insert(tk.END, "-"*40 + "\n")
        
        lines1 = self.read_file_lines(self.file1_path)
        lines2 = self.read_file_lines(self.file2_path)
        
        if isinstance(lines1, str) and lines1.startswith("读取文件时出错"):
            self.result_text.insert(tk.END, f"错误: {lines1}\n")
            return
            
        if isinstance(lines2, str) and lines2.startswith("读取文件时出错"):
            self.result_text.insert(tk.END, f"错误: {lines2}\n")
            return
            
        len1 = len(lines1)
        len2 = len(lines2)
        
        self.result_text.insert(tk.END, f"文件1行数: {len1}\n")
        self.result_text.insert(tk.END, f"文件2行数: {len2}\n\n")
        
        if len1 != len2:
            self.result_text.insert(tk.END, f"❌ 行数不同: 文件1有{len1}行, 文件2有{len2}行\n\n")
        
        # 比较每一行
        max_lines = max(len1, len2)
        differences = []
        
        for i in range(max_lines):
            line1 = lines1[i] if i < len1 else ""
            line2 = lines2[i] if i < len2 else ""
            
            # 去除行尾换行符进行比较
            if line1.rstrip('\n') != line2.rstrip('\n'):
                differences.append(i + 1)  # 行号从1开始
                self.result_text.insert(tk.END, f"第{i+1}行不同:\n")
                self.result_text.insert(tk.END, f"  文件1: {line1.rstrip()}\n")
                self.result_text.insert(tk.END, f"  文件2: {line2.rstrip()}\n\n")
        
        if differences:
            self.result_text.insert(tk.END, f"❌ 共发现 {len(differences)} 处不同\n")
            self.result_text.insert(tk.END, f"   不同行号: {differences}\n")
        else:
            if len1 == len2:
                self.result_text.insert(tk.END, "✅ 所有行都完全相同\n")
            else:
                self.result_text.insert(tk.END, "⚠️ 行数不同但现有行内容相同\n")
                
    def show_differences(self):
        """显示文件差异（类似diff工具）"""
        self.result_text.insert(tk.END, "差异对比结果:\n")
        self.result_text.insert(tk.END, "-"*40 + "\n")
        
        lines1 = self.read_file_lines(self.file1_path)
        lines2 = self.read_file_lines(self.file2_path)
        
        if isinstance(lines1, str) and lines1.startswith("读取文件时出错"):
            self.result_text.insert(tk.END, f"错误: {lines1}\n")
            return
            
        if isinstance(lines2, str) and lines2.startswith("读取文件时出错"):
            self.result_text.insert(tk.END, f"错误: {lines2}\n")
            return
            
        # 使用difflib生成差异
        d = Differ()
        diff = list(d.compare(lines1, lines2))
        
        # 统计差异
        added = 0
        removed = 0
        changed = 0
        
        for line in diff:
            if line.startswith('+ '):
                added += 1
                self.result_text.insert(tk.END, f"  + {line[2:]}", 'added')
            elif line.startswith('- '):
                removed += 1
                self.result_text.insert(tk.END, f"  - {line[2:]}", 'removed')
            elif line.startswith('? '):
                # 这是difflib的上下文行，我们跳过
                continue
            else:
                # 无变化的行
                self.result_text.insert(tk.END, f"    {line[2:]}")
        
        # 配置文本标签颜色
        self.result_text.tag_config('added', foreground='green')
        self.result_text.tag_config('removed', foreground='red')
        
        self.result_text.insert(tk.END, "\n" + "-"*40 + "\n")
        self.result_text.insert(tk.END, "差异统计:\n")
        self.result_text.insert(tk.END, f"  新增行: {added}\n")
        self.result_text.insert(tk.END, f"  删除行: {removed}\n")
        
        if added == 0 and removed == 0:
            self.result_text.insert(tk.END, "✅ 文件内容完全相同\n")
        else:
            self.result_text.insert(tk.END, "❌ 文件内容不同\n")
            
    def clear_results(self):
        """清空结果区域"""
        self.result_text.delete(1.0, tk.END)
        self.update_status("结果已清空")
        
    def run(self):
        """运行程序"""
        self.root.mainloop()

def main():
    """主函数"""
    root = tk.Tk()
    app = FileComparator(root)
    app.run()

if __name__ == "__main__":
    main()
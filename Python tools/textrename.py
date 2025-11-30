import os
import re

def replace_words_in_file(file_path, replacements):
    """
    在文件中替换指定的词语
    
    参数:
        file_path: 文件路径
        replacements: 字典，键为要替换的词语，值为替换后的词语
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 执行替换操作
        replace_count = 0
        for old_word, new_word in replacements.items():
            # 使用正则表达式进行不区分大小写的全局替换
            pattern = re.escape(old_word)  # 转义特殊字符
            content, count = re.subn(pattern, new_word, content, flags=re.IGNORECASE)
            replace_count += count
            print(f"替换 '{old_word}' -> '{new_word}': {count} 处")
        
        # 写入修改后的内容
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"\n总共完成 {replace_count} 处替换")
        return True
        
    except FileNotFoundError:
        print(f"错误：找不到文件 '{file_path}'")
        return False
    except Exception as e:
        print(f"发生错误：{e}")
        return False

def main():
    print("=== 文本文件词语替换工具 ===")
    print("输入格式: 原词 新词 (使用空格分隔)")
    print("输入空行开始执行替换")
    print("=" * 40)
    
    # 获取文件路径
    file_path = input("请输入文本文件路径（默认: text.txt）: ").strip()
    if not file_path:
        file_path = "text.txt"
    
    if not os.path.exists(file_path):
        print(f"错误：文件 '{file_path}' 不存在")
        return
    
    # 获取替换规则
    replacements = {}
    print("\n请输入替换规则 (原词 新词):")
    
    line_num = 1
    while True:
        try:
            user_input = input(f"[{line_num}]> ").strip()
            line_num += 1
            
            if not user_input:
                break  # 空行结束输入
            
            # 分割输入，支持多个空格
            parts = user_input.split()
            if len(parts) < 2:
                print("格式错误，请使用: 原词 新词")
                continue
            
            old_word = parts[0]
            new_word = ' '.join(parts[1:])  # 新词可能包含空格
            
            replacements[old_word] = new_word
            print(f"  已添加: '{old_word}' -> '{new_word}'")
            
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\n操作已取消")
            return
    
    if not replacements:
        print("未提供任何替换规则")
        return
    
    # 显示替换摘要
    print(f"\n=== 替换摘要 ===")
    print(f"文件: {file_path}")
    print(f"替换规则数量: {len(replacements)}")
    for i, (old_word, new_word) in enumerate(replacements.items(), 1):
        print(f"{i}. '{old_word}' -> '{new_word}'")
    
    # 确认执行
    confirm = input("\n确认执行替换？(y/n): ").strip().lower()
    if confirm in ['y', 'yes', '是']:
        success = replace_words_in_file(file_path, replacements)
        if success:
            print("替换完成！")
    else:
        print("已取消替换操作")

if __name__ == "__main__":
    main()
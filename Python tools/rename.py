import os
import re
from datetime import datetime

def batch_rename_images(folder_path, prefix):
    """
    智能批量重命名图片文件
    :param folder_path: 需要处理的文件夹路径
    :param prefix: 要添加的统一前缀
    """
    # 校验输入参数
    if not os.path.exists(folder_path):
        print(f"⛔ 错误：目录 '{folder_path}' 不存在")
        return

    # 初始化计数器
    success_count = 0
    skip_count = 0
    error_count = 0
    conflict_files = []

    # 创建安全日志
    log_file = os.path.join(folder_path, f"rename_log_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
    
    # 匹配纯数字文件名模式（支持.jpg和.jpeg）
    pattern = re.compile(r'^(\d+)\.jpe?g$', re.IGNORECASE)

    # 遍历目录中的文件
    for filename in os.listdir(folder_path):
        # 忽略子目录
        if not os.path.isfile(os.path.join(folder_path, filename)):
            continue

        # 匹配数字文件名
        match = pattern.match(filename)
        if not match:
            continue

        # 提取数字部分
        file_num = match.group(1)
        old_path = os.path.join(folder_path, filename)
        
        # 构建新文件名
        new_filename = f"{prefix} {file_num}.jpg"
        new_path = os.path.join(folder_path, new_filename)

        # 冲突检测：检查目标文件是否已存在
        if os.path.exists(new_path):
            conflict_files.append((filename, new_filename))
            skip_count += 1
            continue

        try:
            # 执行重命名操作
            os.rename(old_path, new_path)
            success_count += 1
            # 记录日志
            with open(log_file, 'a') as log:
                log.write(f"重命名成功：{filename} -> {new_filename}\n")
        except Exception as e:
            error_count += 1
            print(f"⚠ 重命名失败：{filename} | 错误：{str(e)}")
            with open(log_file, 'a') as log:
                log.write(f"重命名失败：{filename} | 错误：{str(e)}\n")

    # 处理命名冲突
    if conflict_files:
        print("\n⚠ 检测到文件名冲突：")
        for _, new_filename in conflict_files:
            print(f" - 目标文件已存在：{new_filename}")
        print("已跳过这些文件，请手动处理")

    # 输出统计报告
    print("\n操作完成，统计报告：")
    print(f"✅ 成功重命名：{success_count} 个文件")
    print(f"⚠ 跳过冲突文件：{skip_count} 个")
    print(f"⛔ 操作失败：{error_count} 次")
    print(f"📝 操作日志：{log_file}")

if __name__ == "__main__":
    # 配置参数（根据实际需要修改）
    target_folder = r"F:\vscode\downloaded_images"
    new_prefix = "いろとりどりのセカイ"

    # 二次确认
    print("将要执行批量重命名操作：")
    print(f"目录位置：{target_folder}")
    print(f"新文件名格式：'{new_prefix} X.jpg'")
    confirmation = input("是否继续？(y/n) ").lower()

    if confirmation == 'y':
        batch_rename_images(target_folder, new_prefix)
    else:
        print("操作已取消")

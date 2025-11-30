import requests
import time
import os
import random
import urllib3

# 禁用SSL证书验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_max_number(save_dir):
    """智能获取目录中最大图片编号（支持不连续编号）"""
    max_num = 0
    if os.path.exists(save_dir):
        for filename in os.listdir(save_dir):
            if filename.endswith('.jpg'):
                try:
                    num = int(os.path.splitext(filename)[0])
                    max_num = max(max_num, num)
                except ValueError:
                    continue
    return max_num

def download_images(save_dir='images', max_retries=5):
    # 请求头设置（模拟最新版Edge浏览器）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Referer': 'https://www.google.com/'
    }

    # 构建URL模板
    base_url = "https://tsundora.com/image/2015/09/irotoridori_no_sekai_"
    url_template = f"{base_url}/{{}}.jpg"

    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)
    
    # 初始化下载参数
    num = get_max_number(save_dir) + 1
    retry_count = 0
    success_count = 0

    while retry_count < max_retries:
        file_path = os.path.join(save_dir, f'{num}.jpg')
        
        # 跳过已存在文件
        if os.path.exists(file_path):
            print(f'⏩ 跳过已存在文件：{num}.jpg')
            num += 1
            success_count += 1
            continue

        try:
            # 发送请求（包含动态超时）
            response = requests.get(
                url_template.format(num),
                headers=headers,
                verify=False,
                timeout=random.uniform(5, 10)  # 动态超时设置
            )

            # 处理响应
            if response.status_code == 200:
                # 保存图片
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f'✅ 成功下载 [{num}.jpg] | 大小：{len(response.content)//1024}KB')
                num += 1
                success_count += 1
                retry_count = 0
            elif response.status_code == 404:
                print(f'⛔ 终止下载：{num}.jpg 不存在')
                break
            else:
                print(f'⚠ 异常状态码 [{response.status_code}]，正在重试...')
                retry_count += 1

        except requests.exceptions.RequestException as e:
            print(f'⚠ 网络异常：{type(e).__name__}，正在重试...')
            retry_count += 1

        # 动态等待时间（0.5-2.5秒随机间隔）
        sleep_time = random.uniform(0.5, 1.5)
        time.sleep(sleep_time)

    print('\n============== 下载报告 ==============')
    print(f'✅ 成功下载数量：{success_count}')
    print(f'⏩ 跳过已存在文件：{num - get_max_number(save_dir) - 1}')
    print(f'📁 存储路径：{os.path.abspath(save_dir)}')

if __name__ == '__main__':
    download_images(save_dir='downloaded_images')

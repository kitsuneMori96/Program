import requests
import os
import random
import time
import json
from tqdm import tqdm
from pathlib import Path

class SmartImageSpider:
    def __init__(self, base_url, output_dir='downloaded', config_file='.spider_config'):
        """
        初始化智能爬虫
        :param base_url: 基础URL格式（必须包含{}数字占位符）
        :param output_dir: 图片保存目录
        :param config_file: 配置文件路径（记录进度和失败项）
        """
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.config_file = Path(config_file)
        self.state = {
            'current_num': 1,
            'success_count': 0,
            'failed_items': [],
            'downloaded': []
        }
        
        # 初始化目录和配置文件
        self.output_dir.mkdir(exist_ok=True)
        self._load_config()

    def _load_config(self):
        """加载或创建配置文件"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.state = json.load(f)
            print(f"加载历史进度：已下载 {self.state['success_count']} 张图片")

    def _save_config(self):
        """保存配置文件"""
        with open(self.config_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def _generate_filename(self, num):
        """生成标准化的文件名"""
        return f"image_{num:d}.jpg"  # 示例格式：image_00001.jpg

    def _download_image(self, num):
        """执行单个图片下载"""
        url = self.base_url.format(num)
        filename = self._generate_filename(num)
        filepath = self.output_dir / filename
        
        # 跳过已下载文件
        if filename in self.state['downloaded']:
            return 'skipped', None
        
        try:
            # 随机下载延迟（0.5-1.5秒）
            time.sleep(random.uniform(0.5, 1.5))
            
            response = requests.get(url, stream=True, timeout=15)
            
            if response.status_code == 200:
                # 分块写入文件
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                self.state['downloaded'].append(filename)
                return 'success', None
                
            elif response.status_code == 404:
                return 'fail', f"HTTP 404 - 资源不存在"
                
            else:
                return 'fail', f"HTTP {response.status_code}"
                
        except Exception as e:
            return 'fail', str(e)

    def run(self, max_consecutive_fails=3):
        """启动爬虫"""
        print(f"启动智能爬虫，存储目录：{self.output_dir.resolve()}")
        
        with tqdm(desc="智能探测进度", unit="个") as pbar:
            consecutive_fails = 0
            
            while consecutive_fails < max_consecutive_fails:
                result, error = self._download_image(self.state['current_num'])
                
                # 更新进度显示
                status_msg = f"当前：{self.state['current_num']} "
                if result == 'success':
                    self.state['success_count'] += 1
                    consecutive_fails = 0
                    status_msg += "✅ 下载成功"
                elif result == 'fail':
                    consecutive_fails += 1
                    self.state['failed_items'].append({
                        'num': self.state['current_num'],
                        'url': self.base_url.format(self.state['current_num']),
                        'error': error,
                        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                    status_msg += f"⛔ 失败（{consecutive_fails}/{max_consecutive_fails}）"
                else:
                    status_msg += "⏩ 已跳过"
                
                pbar.set_description(status_msg)
                pbar.update(1)
                self.state['current_num'] += 1
                
                # 保存进度
                if result in ('success', 'fail'):
                    self._save_config()
                
                # 连续失败控制
                if result == 'fail' and consecutive_fails >= max_consecutive_fails:
                    break

        # 生成最终报告
        print("\n" + "="*40)
        print(f"任务完成！共处理 {self.state['current_num'] - 1} 个资源")
        print(f"成功下载：{self.state['success_count']} 张")
        print(f"失败项目：{len(self.state['failed_items'])} 个")
        
        # 保存失败日志
        if self.state['failed_items']:
            log_file = self.output_dir / "failed_items.log"
            with open(log_file, 'w') as f:
                f.write("失败项目清单：\n")
                for item in self.state['failed_items']:
                    f.write(f"[{item['timestamp']}] {item['url']}\n错误：{item['error']}\n\n")
            print(f"失败日志已保存至：{log_file.resolve()}")

if __name__ == "__main__":
    # 示例配置
    spider = SmartImageSpider(
        base_url="https://tsundora.com/image/2015/09/irotoridori_no_sekai_{}.jpg",
        output_dir="downloaded_images",
        config_file=".spider_config"
    )
    
    # 启动爬虫（设置最大连续失败次数为3）
    spider.run(max_consecutive_fails=4)

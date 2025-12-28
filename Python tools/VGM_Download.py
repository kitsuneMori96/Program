from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from msedge.selenium_tools import Edge, EdgeOptions
import time
import os


def setup_edge_driver(download_path):
    """
    配置Edge浏览器选项，设置下载路径和参数
    """
    from selenium.webdriver.edge.options import Options as EdgeOptions
    
    options = EdgeOptions()
    
    # 设置Edge浏览器下载参数
    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,  # 禁止弹出下载确认框
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_setting_values.automatic_downloads": 1  # 允许自动下载
    }
    
    options.add_experimental_option("prefs", prefs)
    
    # 添加一些参数使自动化更自然
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--start-maximized")  # 最大化窗口
    
    # 初始化Edge浏览器驱动
    # 确保Microsoft Edge WebDriver已安装并与Edge浏览器版本匹配
    driver = Edge(options=options)
    
    return driver

def find_and_download_all_songs(album_url, download_path):
    """
    主函数：从专辑页面开始，找到所有歌曲并下载FLAC版本
    """
    # 创建下载目录
    os.makedirs(download_path, exist_ok=True)
    
    # 初始化Edge浏览器
    driver = setup_edge_driver(download_path)
    wait = WebDriverWait(driver, 15)  # 设置显式等待时间
    
    try:
        print(f"正在打开专辑页面: {album_url}")
        driver.get(album_url)
        time.sleep(3)  # 等待页面加载
        
        total_downloaded = 0
        page_count = 1
        
        # 主循环：处理所有分页
        while True:
            print(f"\n{'='*60}")
            print(f"处理第 {page_count} 页")
            print(f"当前页面URL: {driver.current_url}")
            
            # 1. 获取当前页面的所有歌曲链接
            song_links = extract_song_links(driver)
            
            if not song_links:
                print("未找到任何歌曲链接，尝试备用查找方法...")
                song_links = extract_song_links_alternative(driver)
            
            if not song_links:
                print("未找到任何歌曲，程序结束")
                break
            
            print(f"本页找到 {len(song_links)} 首歌曲")
            
            # 2. 遍历当前页的每首歌曲
            for i, song in enumerate(song_links, 1):
                try:
                    print(f"\n[{total_downloaded + i}] 处理: {song.get('name', f'歌曲 {i}')}")
                    
                    # 获取歌曲详情页URL
                    song_url = song.get('url')
                    if not song_url:
                        print("  跳过：没有有效的歌曲URL")
                        continue
                    
                    # 3. 下载FLAC文件
                    success = download_flac_from_song_page(driver, song_url, wait)
                    
                    if success:
                        print(f"  ✓ 下载成功")
                        total_downloaded += 1
                    else:
                        print(f"  ✗ 下载失败")
                    
                    # 4. 返回专辑列表页
                    driver.back()
                    time.sleep(2)  # 等待返回
                    
                    # 每下载5首歌后暂停一下
                    if i % 5 == 0:
                        print("  暂停3秒，避免请求过快...")
                        time.sleep(3)
                        
                except Exception as e:
                    print(f"  处理歌曲时出错: {e}")
                    continue
            
            # 5. 检查是否有下一页
            next_page_exists, next_page_url = find_next_page(driver)
            
            if next_page_exists and next_page_url:
                print(f"\n发现下一页，跳转到: {next_page_url}")
                page_count += 1
                driver.get(next_page_url)
                time.sleep(3)  # 等待下一页加载
            else:
                print("\n已到达最后一页")
                break
                
    except Exception as e:
        print(f"\n程序执行过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print(f"\n{'='*60}")
        print(f"程序执行完成！")
        print(f"总共处理了 {total_downloaded} 首歌曲")
        print(f"文件保存在: {os.path.abspath(download_path)}")
        
        # 等待最后几个下载完成
        print("等待15秒让最后几个下载完成...")
        time.sleep(15)
        
        driver.quit()
        print("Edge浏览器已关闭")

def extract_song_links(driver):
    """
    从专辑页面提取歌曲链接
    根据第二张图片的歌曲列表结构
    """
    song_links = []
    
    try:
        # 根据图片中的表格结构查找歌曲
        # 歌曲列表通常在表格中，每行包含序号、歌曲名、时长、文件大小
        song_rows = driver.find_elements(By.XPATH, "//table//tr[td[1][contains(text(), '.')]]")
        
        for row in song_rows:
            try:
                # 提取歌曲序号
                index_elem = row.find_element(By.XPATH, "./td[1]")
                song_index = index_elem.text.strip()
                
                # 提取歌曲名和链接（通常在第二列）
                song_name_elem = row.find_element(By.XPATH, "./td[2]/a")
                song_name = song_name_elem.text.strip()
                song_url = song_name_elem.get_attribute("href")
                
                if song_url:
                    song_links.append({
                        'index': song_index,
                        'name': song_name,
                        'url': song_url
                    })
                    
            except NoSuchElementException:
                continue
                
    except Exception as e:
        print(f"提取歌曲链接时出错: {e}")
    
    return song_links

def extract_song_links_alternative(driver):
    """
    备用方法：查找所有可能的歌曲链接
    """
    song_links = []
    
    try:
        # 查找所有指向歌曲详情页的链接
        all_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/game-soundtracks/album/')]")
        
        for link in all_links:
            link_text = link.text.strip()
            link_url = link.get_attribute("href")
            
            # 过滤掉无效链接
            if (link_text and 
                len(link_text) > 1 and 
                not link_text.startswith('http') and
                link_url and
                link_url != driver.current_url):
                
                song_links.append({
                    'name': link_text,
                    'url': link_url
                })
                
    except Exception as e:
        print(f"备用方法提取链接时出错: {e}")
    
    return song_links

def download_flac_from_song_page(driver, song_url, wait):
    """
    从歌曲详情页下载FLAC文件
    根据第一张图片的页面结构
    """
    try:
        # 打开歌曲详情页
        driver.get(song_url)
        time.sleep(2)  # 等待页面加载
        
        # 方法1：查找FLAC下载链接（根据第一张图片）
        flac_link = None
        
        # 尝试多种定位策略
        selectors = [
            "//a[contains(@href, '.flac')]",  # 通过文件扩展名
            "//a[contains(text(), 'FLAC')]",  # 通过文本内容
            "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'flac')]",  # 不区分大小写
            "//a[contains(text(), 'download as') and contains(text(), 'FLAC')]",  # 完整下载文本
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if elements:
                    flac_link = elements[0]
                    print(f"  使用选择器找到FLAC链接: {selector}")
                    break
            except:
                continue
        
        # 如果没找到，尝试查找所有链接并筛选
        if not flac_link:
            print("  未找到标准FLAC链接，尝试查找所有链接...")
            all_links = driver.find_elements(By.TAG_NAME, "a")
            for link in all_links:
                href = link.get_attribute("href")
                if href and ".flac" in href.lower():
                    flac_link = link
                    break
        
        if flac_link:
            # 获取下载链接
            download_url = flac_link.get_attribute("href")
            print(f"  找到FLAC下载链接: {download_url[:80]}...")
            
            # 使用JavaScript点击，避免元素不可点击的问题
            driver.execute_script("arguments[0].scrollIntoView(true);", flac_link)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", flac_link)
            
            # 等待下载开始
            print("  开始下载，等待5秒...")
            time.sleep(5)
            
            return True
        else:
            print("  ⚠️ 未找到FLAC下载链接")
            return False
            
    except Exception as e:
        print(f"  下载FLAC时出错: {e}")
        return False

def find_next_page(driver):
    """
    检查是否有下一页，并返回下一页链接
    """
    try:
        # 查找"Next"、"下一页"或箭头符号
        next_selectors = [
            "//a[contains(text(), 'Next')]",
            "//a[contains(text(), '»')]",  # 右箭头
            "//a[contains(text(), '>')]",  # 大于号
            "//a[contains(text(), '下一页')]",  # 中文
        ]
        
        for selector in next_selectors:
            try:
                next_links = driver.find_elements(By.XPATH, selector)
                for link in next_links:
                    next_url = link.get_attribute("href")
                    if next_url and next_url != driver.current_url:
                        return True, next_url
            except:
                continue
        
        return False, None
        
    except Exception as e:
        print(f"查找下一页时出错: {e}")
        return False, None

# ============================
# 主程序入口
# ============================
if __name__ == "__main__":
    # 配置信息 - 请根据您的需求修改
    
    # 专辑页面URL（第二张图片的网址）
    ALBUM_URL = "https://downloads.khinsider.com/game-soundtracks/album/oniuta-original-soundtrack"
    
    # 下载保存路径
    # Windows示例: "D:\\Music\\oniuta"
    # Mac/Linux示例: "/Users/你的用户名/Music/oniuta"
    DOWNLOAD_PATH = "D:\\Music\\oniuta"
    
    # 运行下载程序
    print("=" * 60)
    print("Edge浏览器自动下载FLAC音乐程序")
    print("=" * 60)
    
    find_and_download_all_songs(ALBUM_URL, DOWNLOAD_PATH)
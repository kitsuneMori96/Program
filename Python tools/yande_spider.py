"""
yande.re 通用爬虫
=================
基于 JSON API，支持：
  - pool/show/{id}  : 爬取画集(pool)中的所有图片
  - post.json       : 按标签搜索帖子
  - post/show/{id}  : 单个帖子详情

使用方式：
    python yande_spider.py pool 99363
    python yande_spider.py search "lump_of_sugar" --limit 20
    python yande_spider.py post 1260686
    python yande_spider.py pool 99363 --mode jpeg  # 下载 JPEG 版（保留元数据/EXIF）
    #如果有些文件因网络问题失败，重试
    python yande_spider.py retry-failed D:/储存/图片/pool_99363_Lump_of_Sugar_...
    # 下载画集 99363 中所有包含标签 mito_mashiro 的图片
    python yande_spider.py pool-filter 99363 "mito_mashiro"
"""

import argparse
import json
import os
import random
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from tqdm import tqdm

# ── UTF-8 终端输出 ────────────────────────────────────
# 修复 Windows GBK 终端下中文显示为乱码的问题
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


class YandeSpider:
    """yande.re 通用爬虫"""

    BASE_URL = "https://yande.re"
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/html, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://yande.re/",
    }

    def __init__(
        self,
        output_dir="downloads",
        delay_range=(0.1, 0.9),
        resume_file=None,
        mode="file_url",
    ):
        """
        :param output_dir:         图片保存目录
        :param delay_range:        请求间隔范围(秒)，默认 1~2s 防封
        :param resume_file:        断点续传记录文件，默认存在 output_dir 下
        :param mode:               下载模式 file_url|jpeg_url|sample_url
        """
        self.output_dir = Path(output_dir)
        self.delay_range = delay_range
        self.resume_file = Path(resume_file or self.output_dir / ".yande_resume.json")
        self.mode = mode

        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

        # 状态
        self.state = {"downloaded": [], "failed": [], "total": 0, "success": 0}
        self._load_resume()

        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ── 节流 ──────────────────────────────────────────

    def _throttle(self):
        """随机延迟，降低被封概率"""
        time.sleep(random.uniform(*self.delay_range))

    # ── 请求 ──────────────────────────────────────────

    def _get_json(self, path, params=None, max_retries=3):
        """请求 JSON API，带重试"""
        url = f"{self.BASE_URL}{path}"
        for attempt in range(1, max_retries + 1):
            try:
                resp = self.session.get(url, params=params, timeout=30)
                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 404:
                    print(f"  [404] 资源不存在: {url}")
                    return None
                elif resp.status_code == 429:
                    wait = 10 * attempt
                    print(f"  [429] 被限流，等待 {wait}s...")
                    time.sleep(wait)
                    continue
                else:
                    print(f"  [HTTP {resp.status_code}] {url}")
            except requests.RequestException as e:
                print(f"  [{type(e).__name__}] 重试 {attempt}/{max_retries}")
            if attempt < max_retries:
                self._throttle()
        return None

    def _download_file(self, url, filepath, max_retries=5):
        """下载单个文件，流式写入（带自动重试）"""
        for attempt in range(1, max_retries + 1):
            self._throttle()
            try:
                # 连接超时 30s，读取超时 180s（大图需要更长时间）
                resp = self.session.get(url, stream=True, timeout=(30, 180))
                if resp.status_code != 200:
                    if attempt < max_retries:
                        wait = 5 * attempt
                        print(f"  [HTTP {resp.status_code}] 重试 {attempt}/{max_retries}，{wait}s...")
                        time.sleep(wait)
                        continue
                    return False, f"HTTP {resp.status_code}"

                # 删除可能存在的部分文件（上次下载中断残留）
                filepath.unlink(missing_ok=True)

                with open(filepath, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=65536):
                        if chunk:
                            f.write(chunk)
                return True, None

            except (requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError) as e:
                filepath.unlink(missing_ok=True)
                if attempt < max_retries:
                    wait = 10 * attempt
                    print(f"  [{type(e).__name__}] 重试 {attempt}/{max_retries}，{wait}s...")
                    time.sleep(wait)
                    continue
                return False, str(e)

            except Exception as e:
                filepath.unlink(missing_ok=True)
                if attempt < max_retries:
                    wait = 5 * attempt
                    print(f"  [{type(e).__name__}] 重试 {attempt}/{max_retries}，{wait}s...")
                    time.sleep(wait)
                    continue
                return False, str(e)

    # ── 续传 ──────────────────────────────────────────

    def _load_resume(self):
        if self.resume_file.exists():
            try:
                with open(self.resume_file) as f:
                    self.state = json.load(f)
                print(f"[续传] 已有 {self.state['success']} 张，失败 {len(self.state['failed'])} 张")
            except Exception:
                self.state = {"downloaded": [], "failed": [], "total": 0, "success": 0}

    def _save_resume(self):
        try:
            with open(self.resume_file, "w") as f:
                json.dump(self.state, f, indent=2)
        except Exception:
            pass

    # ── 图片下载核心 ──────────────────────────────────

    def _safe_filename(self, post):
        """生成安全文件名: {post_id}.{tags_prefix}.{ext}"""
        ext = Path(post["file_url"].split("?")[0]).suffix or ".jpg"
        tags = post.get("tags", "untagged")[:80]
        # 清理非法文件名字符
        safe_tags = "".join(c if c.isalnum() or c in "-_." else "_" for c in tags)
        return f"{post['id']}_{safe_tags}{ext}"

    def _pick_url(self, post):
        """按 mode 选择下载链接"""
        mode = post.get("mode", self.mode)
        if mode == "jpeg_url":
            url = post.get("jpeg_url") or post.get("file_url")
        elif mode == "sample_url":
            url = post.get("sample_url") or post.get("file_url")
        else:  # file_url (原图)
            url = post.get("file_url")
        return url

    def download_posts(self, posts, description=""):
        """下载帖子列表"""
        total = len(posts)
        self.state["total"] = total
        print(f"\n{'─'*40}")
        print(f"{description} — 共 {total} 个资源")
        print(f"{'─'*40}")

        for post in tqdm(posts, desc="下载进度", unit="张"):
            pid = post["id"]
            # 跳过已下载
            if str(pid) in self.state["downloaded"]:
                continue

            url = self._pick_url(post)
            if not url:
                self.state["failed"].append({"id": pid, "reason": "无可用下载链接"})
                continue

            filename = self._safe_filename(post)
            filepath = self.output_dir / filename

            ok, err = self._download_file(url, filepath)
            if ok:
                self.state["success"] += 1
                self.state["downloaded"].append(str(pid))
            else:
                self.state["failed"].append({"id": pid, "url": url, "reason": err})
                tqdm.write(f"  [失败] [{pid}] {err}")

            # 每张下载后保存一次续传状态
            self._save_resume()

        self._print_report()

    def _print_report(self):
        print(f"\n{'─'*40}")
        print(f"完成  成功: {self.state['success']}/{self.state['total']}")
        if self.state["failed"]:
            print(f"失败: {len(self.state['failed'])} 张")
            log_path = self.output_dir / "failed.log"
            with open(log_path, "w") as f:
                for item in self.state["failed"]:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")
            print(f"日志: {log_path}")
        print(f"{'─'*40}\n")

    # ── 业务方法 ──────────────────────────────────────

    def scrape_pool(self, pool_id, mode=None):
        """
        爬取画集(pool)中的所有图片
        API: /pool/show/{id}.json
        """
        print(f"\n爬取画集: pool/show/{pool_id}")
        data = self._get_json(f"/pool/show/{pool_id}.json")
        if not data:
            print("画集不存在或请求失败")
            return

        posts = data.get("posts", [])
        if mode:
            for p in posts:
                p["mode"] = mode

        pool_name = data.get("name", str(pool_id))
        save_dir = self.output_dir / f"pool_{pool_id}_{pool_name[:40]}"
        save_dir.mkdir(parents=True, exist_ok=True)

        # 保存元数据
        meta_path = save_dir / "_pool_meta.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(
                {k: v for k, v in data.items() if k != "posts"},
                f, indent=2, ensure_ascii=False,
            )

        spider = YandeSpider(
            output_dir=str(save_dir),
            delay_range=self.delay_range,
            mode=mode or self.mode,
        )
        spider.download_posts(posts, description=data.get("name", f"Pool {pool_id}"))

    def scrape_pool_with_filter(self, pool_id, filter_tags, mode=None):
        """
        混合搜索：在画集中按标签过滤图片
        1. 获取画集所有帖子
        2. 按标签关键词过滤（大小写不敏感，所有关键词都要匹配）
        3. 下载匹配的帖子
        """
        print(f"\n混合搜索: pool {pool_id} 中过滤标签 '{filter_tags}'")
        data = self._get_json(f"/pool/show/{pool_id}.json")
        if not data:
            print("画集不存在或请求失败")
            return

        all_posts = data.get("posts", [])
        if not all_posts:
            print("画集为空")
            return

        keywords = [k.lower() for k in filter_tags.split()]

        filtered = []
        for p in all_posts:
            post_tags = p.get("tags", "").lower()
            if all(k in post_tags for k in keywords):
                filtered.append(p)

        if not filtered:
            print(f"未找到包含 '{filter_tags}' 的帖子 (共 {len(all_posts)} 张，均不匹配)")
            return

        print(f"匹配 {len(filtered)}/{len(all_posts)} 张")

        if mode:
            for p in filtered:
                p["mode"] = mode

        pool_name = data.get("name", str(pool_id))
        tag_slug = filter_tags.replace(" ", "_")[:30]
        save_dir = self.output_dir / f"pool_{pool_id}_{pool_name[:30]}_filter_{tag_slug}"
        save_dir.mkdir(parents=True, exist_ok=True)

        spider = YandeSpider(
            output_dir=str(save_dir),
            delay_range=self.delay_range,
            mode=mode or self.mode,
        )
        spider.download_posts(
            filtered,
            description=f"Pool {pool_id}「{pool_name}」↳ '{filter_tags}' ({len(filtered)} 张)",
        )

    def search_posts(self, tags, limit=50, page=1, mode=None):
        """
        按标签搜索帖子
        API: /post.json?tags=xxx&page=n&limit=n
        """
        print(f"\n搜索标签: {tags}  (limit={limit})")
        per_page = min(limit, 100)
        collected = []
        current_page = page

        while len(collected) < limit:
            params = {"tags": tags, "page": current_page, "limit": per_page}
            posts = self._get_json("/post.json", params=params)
            if not posts:
                break
            collected.extend(posts)
            if len(posts) < per_page:
                break
            current_page += 1
            self._throttle()

        collected = collected[:limit]
        if not collected:
            print("未找到匹配的帖子")
            return

        if mode:
            for p in collected:
                p["mode"] = mode

        tag_slug = tags.replace(" ", "_")[:40]
        save_dir = self.output_dir / f"search_{tag_slug}"
        save_dir.mkdir(parents=True, exist_ok=True)

        spider = YandeSpider(
            output_dir=str(save_dir),
            delay_range=self.delay_range,
            mode=mode or self.mode,
        )
        spider.download_posts(collected, description=f"标签搜索: {tags} ({len(collected)} 张)")

    def scrape_post(self, post_id, mode=None):
        """
        爬取单个帖子详情
        API: /post/show/{id}.json
        """
        print(f"\n爬取帖子: post/show/{post_id}")
        post = self._get_json(f"/post/show/{post_id}.json")
        if not post:
            print("帖子不存在或请求失败")
            return

        if mode:
            post["mode"] = mode

        save_dir = self.output_dir / f"post_{post_id}"
        save_dir.mkdir(parents=True, exist_ok=True)

        spider = YandeSpider(
            output_dir=str(save_dir),
            delay_range=self.delay_range,
            mode=mode or self.mode,
        )
        spider.download_posts([post], description=f"帖子 #{post_id}")

    def retry_failed(self, fail_dir):
        """
        重试 failed.log 中下载失败的图片
        failed.log 格式: JSON Lines，每行包含 {"id", "url", "reason"}
        """
        fail_dir = Path(fail_dir)
        log_path = fail_dir / "failed.log"
        if not log_path.exists():
            print("未找到 failed.log")
            return

        failed_items = []
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    failed_items.append(json.loads(line))

        if not failed_items:
            print("failed.log 为空，没有需要重试的项")
            return

        print(f"\n找到 {len(failed_items)} 个失败项，开始重试...")
        success_count = 0

        for item in tqdm(failed_items, desc="重试下载", unit="张"):
            pid = item["id"]
            url = item["url"]

            # 从 URL 提取扩展名，用 id 作为文件名（兼容原 _safe_filename 命名）
            ext = Path(url.split("?")[0]).suffix or ".jpg"
            filename = f"{pid}{ext}"
            filepath = fail_dir / filename

            ok, err = self._download_file(url, filepath)
            if ok:
                success_count += 1
                tqdm.write(f"  [成功] [{pid}] 下载完成")
            else:
                tqdm.write(f"  [失败] [{pid}] {err}")

        print(f"\n重试完成: 成功 {success_count}/{len(failed_items)}")
        print(f"{'─'*40}\n")


# ── CLI ────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="yande.re 通用爬虫 —— 支持画集/搜索/单帖下载",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  python yande_spider.py pool 99363\n"
            "  python yande_spider.py pool 99363 --mode jpeg\n"
            "  python yande_spider.py search \"lump_of_sugar\" -l 50\n"
            "  python yande_spider.py post 1260686\n"
            "  python yande_spider.py pool-filter 99363 \"mito_mashiro\"\n"
            "  python yande_spider.py pool-filter 99363 \"mito_mashiro kagamine_len\" -m jpeg\n"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # pool
    p_pool = sub.add_parser("pool", help="爬取画集")
    p_pool.add_argument("pool_id", type=int, help="画集 ID")
    p_pool.add_argument("-o", "--output", default=r"D:\储存\图片", help="输出目录")
    p_pool.add_argument(
        "-m", "--mode", choices=["file_url", "jpeg_url", "sample_url"],
        default="file_url", help="下载模式: 原图/JPEG版/预览图",
    )
    p_pool.add_argument("--delay", type=float, nargs=2, default=[1.5, 3.0],
                        help="请求延迟范围(秒) 默认 1.5 3.0")

    # search
    p_search = sub.add_parser("search", help="按标签搜索帖子")
    p_search.add_argument("tags", help="搜索标签 (空格分隔用引号包裹)")
    p_search.add_argument("-l", "--limit", type=int, default=50, help="下载数量")
    p_search.add_argument("-o", "--output", default=r"D:\储存\图片", help="输出目录")
    p_search.add_argument(
        "-m", "--mode", choices=["file_url", "jpeg_url", "sample_url"],
        default="file_url",
    )
    p_search.add_argument("--delay", type=float, nargs=2, default=[1.5, 3.0])

    # post
    p_post = sub.add_parser("post", help="爬取单个帖子")
    p_post.add_argument("post_id", type=int, help="帖子 ID")
    p_post.add_argument("-o", "--output", default=r"D:\储存\图片", help="输出目录")
    p_post.add_argument(
        "-m", "--mode", choices=["file_url", "jpeg_url", "sample_url"],
        default="file_url",
    )
    p_post.add_argument("--delay", type=float, nargs=2, default=[1.5, 3.0])

    # retry-failed
    p_retry = sub.add_parser("retry-failed", help="重试 failed.log 中失败的下载")
    p_retry.add_argument("dir", help="包含 failed.log 的下载目录")
    p_retry.add_argument(
        "-m", "--mode", choices=["file_url", "jpeg_url", "sample_url"],
        default="file_url",
    )
    p_retry.add_argument("--delay", type=float, nargs=2, default=[1.5, 3.0])

    # pool-filter (混合搜索)
    p_pf = sub.add_parser("pool-filter", help="画集中按标签过滤图片（混合搜索）")
    p_pf.add_argument("pool_id", type=int, help="画集 ID")
    p_pf.add_argument("tags", help="过滤标签（空格分隔，全部匹配才下载）")
    p_pf.add_argument("-o", "--output", default=r"D:\储存\图片", help="输出目录")
    p_pf.add_argument(
        "-m", "--mode", choices=["file_url", "jpeg_url", "sample_url"],
        default="file_url",
    )
    p_pf.add_argument("--delay", type=float, nargs=2, default=[1.5, 3.0])

    args = parser.parse_args()

    if args.command == "pool":
        spider = YandeSpider(
            output_dir=args.output,
            delay_range=tuple(args.delay),
            mode=args.mode,
        )
        spider.scrape_pool(args.pool_id, mode=args.mode)
    elif args.command == "search":
        spider = YandeSpider(
            output_dir=args.output,
            delay_range=tuple(args.delay),
            mode=args.mode,
        )
        spider.search_posts(args.tags, limit=args.limit, mode=args.mode)
    elif args.command == "post":
        spider = YandeSpider(
            output_dir=args.output,
            delay_range=tuple(args.delay),
            mode=args.mode,
        )
        spider.scrape_post(args.post_id, mode=args.mode)
    elif args.command == "retry-failed":
        spider = YandeSpider(
            output_dir=args.dir,
            delay_range=tuple(args.delay),
            mode=args.mode,
        )
        spider.retry_failed(args.dir)
    elif args.command == "pool-filter":
        spider = YandeSpider(
            output_dir=args.output,
            delay_range=tuple(args.delay),
            mode=args.mode,
        )
        spider.scrape_pool_with_filter(args.pool_id, args.tags, mode=args.mode)


if __name__ == "__main__":
    main()
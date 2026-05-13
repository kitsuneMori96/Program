"""LRU 缓存工具模块"""
import time
import threading
from typing import Any, Callable, Dict, Optional, Tuple


class LRUCache:
    """线程安全的LRU缓存，支持TTL过期"""

    def __init__(self, capacity: int = 128, ttl: float = 300.0):
        self.capacity = capacity
        self.ttl = ttl
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                return None
            value, expires_at = self._cache[key]
            if time.time() > expires_at:
                del self._cache[key]
                return None
            # 刷新过期时间（LRU风格）
            self._cache[key] = (value, time.time() + self.ttl)
            return value

    def set(self, key: str, value: Any):
        with self._lock:
            if len(self._cache) >= self.capacity:
                # 删除最旧的条目
                oldest = min(self._cache.keys(),
                             key=lambda k: self._cache[k][1])
                del self._cache[oldest]
            self._cache[key] = (value, time.time() + self.ttl)

    def invalidate(self, key: str):
        with self._lock:
            self._cache.pop(key, None)

    def clear(self):
        with self._lock:
            self._cache.clear()


# 全局缓存实例
formula_cache = LRUCache(capacity=256, ttl=600.0)
plot_cache = LRUCache(capacity=64, ttl=300.0)
ocr_cache = LRUCache(capacity=32, ttl=3600.0)


def cached(cache: LRUCache):
    """装饰器：缓存函数返回值"""
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            # 构建缓存键
            key = f"{func.__name__}:{repr(args)}:{repr(sorted(kwargs.items()))}"
            result = cache.get(key)
            if result is not None:
                return result
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        return wrapper
    return decorator
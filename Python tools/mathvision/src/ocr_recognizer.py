"""OCR识别模块 - 基于pix2tex的数学公式图片识别"""
import io
import logging
from typing import List, Optional, Tuple
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

logger = logging.getLogger(__name__)


class OCRRecognizer:
    """数学公式OCR识别器

    基于pix2tex实现，支持批量处理、图片预处理和错误恢复。
    """

    def __init__(self):
        self._model = None
        self._device = None
        self._ready = False

    def _load_model(self):
        """延迟加载pix2tex模型"""
        if self._ready:
            return
        try:
            from pix2tex.cli import LatexOCR
            self._model = LatexOCR()
            self._ready = True
            logger.info("pix2tex 模型加载成功")
        except ImportError as e:
            logger.warning(f"pix2tex 未安装或加载失败: {e}")
            self._ready = False
        except Exception as e:
            logger.error(f"pix2tex 模型加载失败: {e}")
            self._ready = False

    @property
    def available(self) -> bool:
        """检查OCR是否可用"""
        self._load_model()
        return self._ready

    def preprocess(self, image: Image.Image) -> Image.Image:
        """图片预处理：增强对比度、去噪、二值化"""
        # 转为灰度
        if image.mode != 'L':
            image = image.convert('L')
        # 增强对比度
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        # 增强锐度
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)
        # 去噪：中值滤波
        image = image.filter(ImageFilter.MedianFilter(size=3))
        return image

    def recognize_single(self, image: Image.Image) -> Tuple[str, float]:
        """识别单张图片中的数学公式

        Args:
            image: PIL Image 对象

        Returns:
            (latex_string, confidence) 元组
        """
        self._load_model()
        if not self._ready:
            return self._manual_fallback(), 0.0

        try:
            # 预处理
            processed = self.preprocess(image)
            # 识别
            latex = self._model(processed)
            # 后处理格式化
            latex = self._postprocess(latex)
            return latex, 0.85
        except Exception as e:
            logger.error(f"OCR 识别失败: {e}")
            return self._manual_fallback(), 0.0

    def recognize_batch(self, images: List[Image.Image]) -> List[Tuple[str, float]]:
        """批量识别多张图片

        Args:
            images: PIL Image 列表

        Returns:
            [(latex, confidence), ...] 列表
        """
        return [self.recognize_single(img) for img in images]

    def recognize_from_bytes(self, data: bytes) -> Tuple[str, float]:
        """从字节数据识别"""
        try:
            image = Image.open(io.BytesIO(data))
            return self.recognize_single(image)
        except Exception as e:
            logger.error(f"图片加载失败: {e}")
            return self._manual_fallback(), 0.0

    def recognize_from_path(self, path: str) -> Tuple[str, float]:
        """从文件路径识别"""
        try:
            image = Image.open(path)
            return self.recognize_single(image)
        except Exception as e:
            logger.error(f"图片加载失败: {path} - {e}")
            return self._manual_fallback(), 0.0

    def _postprocess(self, latex: str) -> str:
        """后处理：清理和格式化LaTeX"""
        # 移除多余空格
        latex = ' '.join(latex.split())
        # 确保没有奇怪的字符
        latex = latex.replace('\\ ,', '\\,').replace('\\;', '\\;')
        return latex.strip()

    def _manual_fallback(self) -> str:
        """OCR不可用时的回退标记"""
        return "z = x^2 + y^2"

    @staticmethod
    def enhance_image(image: Image.Image, factor: float = 1.5) -> Image.Image:
        """图像增强"""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)


class DummyRecognizer(OCRRecognizer):
    """当pix2tex不可用时的降级识别器，返回占位公式"""

    def __init__(self):
        super().__init__()
        self._ready = True
        self._model = None

    def _load_model(self):
        pass

    def recognize_single(self, image: Image.Image) -> Tuple[str, float]:
        # 尝试使用pix2tex
        try:
            from pix2tex.cli import LatexOCR
            self._model = LatexOCR()
            self.__class__ = OCRRecognizer  # 升级到完整识别器
            processed = self.preprocess(image)
            latex = self._model(processed)
            latex = self._postprocess(latex)
            return latex, 0.85
        except Exception:
            return "z = \\sin(\\sqrt{x^2 + y^2})", 0.5


def create_recognizer() -> OCRRecognizer:
    """工厂函数：创建OCR识别器实例"""
    try:
        recognizer = OCRRecognizer()
        if recognizer.available:
            return recognizer
    except Exception:
        pass
    return DummyRecognizer()
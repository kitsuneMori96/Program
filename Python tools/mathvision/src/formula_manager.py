"""公式管理模块 - 多公式生命周期管理"""
import uuid
import logging
from typing import Any, Callable, Dict, List, Optional

from .utils.cache import formula_cache
from .formula_parser import FormulaParser
from .ocr_recognizer import OCRRecognizer

logger = logging.getLogger(__name__)


class FormulaItem:
    """单个公式的数据模型"""

    def __init__(
        self,
        latex: str,
        formula_type: str = 'explicit',
        label: str = '',
        color: str = None,
        visible: bool = True,
        opacity: float = 0.8,
    ):
        self.id = str(uuid.uuid4())[:8]
        self.latex = latex
        self.formula_type = formula_type
        self.label = label or f"公式 {self.id}"
        self.color = color or self._default_color()
        self.visible = visible
        self.opacity = opacity
        self.parsed = None
        self.numeric_func = None
        self.error = None

    def _default_color(self) -> str:
        """根据类型返回默认颜色"""
        colors = {
            'explicit': '#636EFA',
            'implicit': '#EF553B',
            'parametric': '#00CC96',
        }
        return colors.get(self.formula_type, '#636EFA')

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'latex': self.latex,
            'type': self.formula_type,
            'label': self.label,
            'color': self.color,
            'visible': self.visible,
            'opacity': self.opacity,
            'error': self.error,
        }


class FormulaManager:
    """多公式管理器

    管理公式的增删改查、排序、可见性和缓存。
    """

    def __init__(self):
        self._formulas: List[FormulaItem] = []
        self._parser = FormulaParser()
        self._recognizer = OCRRecognizer()
        self._change_callbacks: List[Callable] = []

    # ---- 公式增删改 ----

    def add_formula(
        self,
        latex: str,
        formula_type: Optional[str] = None,
        label: str = '',
        color: str = None,
    ) -> FormulaItem:
        """添加新公式"""
        item = FormulaItem(
            latex=latex,
            formula_type=formula_type or self._detect_type(latex),
            label=label,
            color=color,
        )
        self._parse_and_cache(item)
        self._formulas.append(item)
        self._notify_changed()
        return item

    def add_from_ocr(self, image_data: Any) -> Optional[FormulaItem]:
        """从OCR识别结果添加公式"""
        latex, confidence = self._recognizer.recognize_single(image_data)
        if confidence > 0.3:
            return self.add_formula(latex, label=f"OCR ({confidence:.0%})")
        return None

    def remove_formula(self, formula_id: str) -> bool:
        """删除公式"""
        for i, f in enumerate(self._formulas):
            if f.id == formula_id:
                self._formulas.pop(i)
                formula_cache.invalidate(f.id)
                self._notify_changed()
                return True
        return False

    def update_formula(self, formula_id: str, **kwargs) -> bool:
        """更新公式属性"""
        for f in self._formulas:
            if f.id == formula_id:
                for key, value in kwargs.items():
                    if hasattr(f, key):
                        setattr(f, key, value)
                # 如果LaTeX变更，重新解析
                if 'latex' in kwargs:
                    self._parse_and_cache(f)
                self._notify_changed()
                return True
        return False

    def reorder_formulas(self, new_order: List[str]):
        """重新排序公式列表 (按ID列表)"""
        id_to_formula = {f.id: f for f in self._formulas}
        self._formulas = [
            id_to_formula[fid] for fid in new_order if fid in id_to_formula
        ]
        self._notify_changed()

    # ---- 解析与缓存 ----

    def _parse_and_cache(self, item: FormulaItem):
        """解析公式并缓存结果"""
        cache_key = f"parsed:{item.latex}"
        cached = formula_cache.get(cache_key)
        if cached:
            item.parsed = cached['parsed']
            item.numeric_func = cached['func']
            item.error = None
            return

        parsed = self._parser.parse(item.latex, item.formula_type)
        if parsed['valid']:
            try:
                func = self._parser.get_numeric_function(parsed)
                formula_cache.set(cache_key, {
                    'parsed': parsed,
                    'func': func,
                })
                item.parsed = parsed
                item.numeric_func = func
                item.error = None
            except Exception as e:
                item.error = str(e)
                item.parsed = parsed
                item.numeric_func = None
        else:
            item.error = parsed.get('error', '解析失败')
            item.parsed = parsed
            item.numeric_func = None

    def _detect_type(self, latex: str) -> str:
        """检测LaTeX对应的函数类型"""
        from .utils.validators import detect_function_type
        return detect_function_type(latex)

    # ---- 查询 ----

    @property
    def formulas(self) -> List[FormulaItem]:
        return list(self._formulas)

    @property
    def count(self) -> int:
        return len(self._formulas)

    def get_visible_formulas(self) -> List[FormulaItem]:
        return [f for f in self._formulas if f.visible and f.parsed and f.parsed['valid']]

    def get_by_id(self, formula_id: str) -> Optional[FormulaItem]:
        for f in self._formulas:
            if f.id == formula_id:
                return f
        return None

    def get_by_type(self, ftype: str) -> List[FormulaItem]:
        return [f for f in self._formulas if f.formula_type == ftype]

    # ---- 事件 ----

    def on_change(self, callback: Callable):
        """注册变更回调"""
        self._change_callbacks.append(callback)

    def _notify_changed(self):
        for cb in self._change_callbacks:
            try:
                cb(self)
            except Exception as e:
                logger.error(f"变更回调失败: {e}")

    def clear(self):
        """清空所有公式"""
        self._formulas.clear()
        formula_cache.clear()
        self._notify_changed()
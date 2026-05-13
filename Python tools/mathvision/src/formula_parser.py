"""公式解析模块 - LaTeX转SymPy表达式"""
import re
import logging
from typing import Any, Dict, List, Optional, Tuple

import sympy as sp
from sympy import symbols, sympify, simplify, lambdify

from .utils.validators import (
    detect_function_type,
    normalize_latex,
    validate_expression,
    validate_latex,
)

logger = logging.getLogger(__name__)


class FormulaParseError(Exception):
    """公式解析异常"""
    pass


class FormulaParser:
    """LaTeX数学公式解析器

    支持三种函数类型：
    - 显函数: z = f(x, y)
    - 隐函数: f(x, y, z) = 0
    - 参数方程: x=f(u,v), y=g(u,v), z=h(u,v)
    """

    def __init__(self):
        self._symbols = {
            'x': sp.Symbol('x'),
            'y': sp.Symbol('y'),
            'z': sp.Symbol('z'),
            'u': sp.Symbol('u'),
            'v': sp.Symbol('v'),
        }
        # 常用函数映射
        self._function_map = {
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
            'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
            'exp': sp.exp, 'log': sp.log, 'ln': sp.log,
            'sqrt': sp.sqrt, 'abs': sp.Abs,
            'pi': sp.pi, 'Pi': sp.pi,
        }

    def parse(self, latex_str: str, formula_type: Optional[str] = None) -> Dict[str, Any]:
        """解析LaTeX公式为SymPy表达式

        Args:
            latex_str: LaTeX格式的公式字符串
            formula_type: 指定函数类型 (explicit/implicit/parametric)，None则自动检测

        Returns:
            {
                'type': str,          # 函数类型
                'expr': sympy.Expr,   # SymPy表达式
                'latex': str,         # 标准化后的LaTeX
                'variables': list,    # 变量列表
                'raw': str,           # 原始LaTeX
                'valid': bool,        # 是否有效
                'error': str or None, # 错误信息
            }
        """
        # 标准化
        latex = normalize_latex(latex_str)
        # 验证LaTeX合法性
        valid, error = validate_latex(latex)
        if not valid:
            return {
                'type': 'unknown',
                'expr': None,
                'latex': latex,
                'variables': [],
                'raw': latex_str,
                'valid': False,
                'error': error,
            }

        # 检测类型
        ftype = formula_type or detect_function_type(latex)

        try:
            if ftype == 'explicit':
                result = self._parse_explicit(latex)
            elif ftype == 'implicit':
                result = self._parse_implicit(latex)
            elif ftype == 'parametric':
                result = self._parse_parametric(latex)
            else:
                result = self._parse_explicit(latex)
                result['type'] = 'unknown'

            result.update({
                'latex': latex,
                'raw': latex_str,
                'valid': True,
                'error': None,
            })
            return result

        except Exception as e:
            return {
                'type': ftype,
                'expr': None,
                'latex': latex,
                'variables': [],
                'raw': latex_str,
                'valid': False,
                'error': str(e),
            }

    def _latex_to_sympy(self, latex: str) -> sp.Expr:
        """将LaTeX转换为SymPy表达式"""
        try:
            from latex2sympy2 import latex2sympy
            expr = latex2sympy(latex)
            if expr is None:
                raise FormulaParseError("LaTeX转换结果为 None")
            return sp.simplify(expr)
        except ImportError:
            logger.warning("latex2sympy2 未安装，使用回退解析器")
            return self._fallback_parse(latex)
        except Exception as e:
            raise FormulaParseError(f"LaTeX转换失败: {e}")

    def _fallback_parse(self, latex: str) -> sp.Expr:
        """latex2sympy2不可用时的回退解析"""
        # 移除 LaTeX 标记
        text = latex
        text = text.replace('\\left', '').replace('\\right', '')
        text = text.replace('\\{', '').replace('\\}', '')
        return sp.sympify(text, locals=self._function_map)

    def _parse_explicit(self, latex: str) -> Dict[str, Any]:
        """解析显函数: z = f(x, y)"""
        # 去掉 "z = " 前缀
        text = latex
        text = re.sub(r'^z\s*=', '', text).strip()
        if not text:
            text = latex  # 没有前缀则使用整个表达式

        expr = self._latex_to_sympy(text)
        # 验证变量合法性
        valid, error = validate_expression(str(expr), ['x', 'y'])
        if not valid:
            raise FormulaParseError(error)

        return {
            'type': 'explicit',
            'expr': expr,
            'variables': ['x', 'y'],
        }

    def _parse_implicit(self, latex: str) -> Dict[str, Any]:
        """解析隐函数: f(x, y, z) = 0"""
        # 分割等号两边
        parts = latex.split('=')
        if len(parts) != 2:
            raise FormulaParseError("隐函数需包含一个等号")

        left = parts[0].strip()
        right = parts[1].strip()

        # 去除两端为零的情况
        if right == '0':
            expr_str = left
        else:
            right_expr = self._latex_to_sympy(right)
            left_expr = self._latex_to_sympy(left)
            expr = left_expr - right_expr
            expr_str = str(expr)

        expr = self._latex_to_sympy(expr_str)
        valid, error = validate_expression(str(expr), ['x', 'y', 'z'])
        if not valid:
            raise FormulaParseError(error)

        return {
            'type': 'implicit',
            'expr': expr,
            'variables': ['x', 'y', 'z'],
        }

    def _parse_parametric(self, latex: str) -> Dict[str, Any]:
        """解析参数方程: x=f(u,v), y=g(u,v), z=h(u,v)"""
        # 分割逗号分隔的三个表达式
        parts = [p.strip() for p in latex.split(',')]
        if len(parts) < 3:
            raise FormulaParseError("参数方程需要三个表达式: x, y, z")

        results = {}
        for part in parts[:3]:
            # 匹配 x=..., y=..., z=...
            m = re.match(r'^\s*([xyz])\s*=\s*(.+)$', part)
            if m:
                var = m.group(1)
                expr_str = m.group(2)
                results[var] = self._latex_to_sympy(expr_str)

        if not all(k in results for k in ('x', 'y', 'z')):
            raise FormulaParseError(
                "参数方程需要定义 x, y, z 三个分量")

        for var, expr in results.items():
            valid, error = validate_expression(str(expr), ['u', 'v'])
            if not valid:
                raise FormulaParseError(f"{var} 分量错误: {error}")

        return {
            'type': 'parametric',
            'expr': results,  # {'x': expr_x, 'y': expr_y, 'z': expr_z}
            'variables': ['u', 'v'],
        }

    def get_numeric_function(self, parsed: Dict[str, Any]):
        """将解析后的公式转换为可调用的数值函数

        Args:
            parsed: parse() 返回的结果字典

        Returns:
            可调用的函数，根据类型不同签名不同
        """
        if not parsed['valid'] or parsed['expr'] is None:
            raise FormulaParseError("无效的公式，无法生成数值函数")

        ftype = parsed['type']
        expr = parsed['expr']

        if ftype == 'explicit':
            x, y = self._symbols['x'], self._symbols['y']
            f = lambdify((x, y), expr, modules='numpy')
            return lambda X, Y: f(X, Y)

        elif ftype == 'implicit':
            x, y, z = self._symbols['x'], self._symbols['y'], self._symbols['z']
            f = lambdify((x, y, z), expr, modules='numpy')
            return lambda X, Y, Z: f(X, Y, Z)

        elif ftype == 'parametric':
            u, v = self._symbols['u'], self._symbols['v']
            fx = lambdify((u, v), expr['x'], modules='numpy')
            fy = lambdify((u, v), expr['y'], modules='numpy')
            fz = lambdify((u, v), expr['z'], modules='numpy')
            return lambda U, V: (fx(U, V), fy(U, V), fz(U, V))

        else:
            raise FormulaParseError(f"不支持的函数类型: {ftype}")

    def simplify(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """简化表达式"""
        if not parsed['valid'] or parsed['expr'] is None:
            return parsed

        result = parsed.copy()
        if parsed['type'] == 'parametric':
            result['expr'] = {
                k: sp.simplify(v) for k, v in parsed['expr'].items()
            }
        else:
            result['expr'] = sp.simplify(parsed['expr'])
        return result
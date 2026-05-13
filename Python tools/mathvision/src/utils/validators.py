"""数学表达式验证工具模块"""
import re
from typing import Optional, Tuple
import sympy as sp


def validate_latex(latex_str: str) -> Tuple[bool, Optional[str]]:
    """验证LaTeX字符串的基本合法性"""
    if not latex_str or not latex_str.strip():
        return False, "LaTeX 表达式为空"

    # 检查括号匹配
    stack = []
    for ch in latex_str:
        if ch in '({[':
            stack.append(ch)
        elif ch in ')}]':
            if not stack:
                return False, f"括号不匹配: 多余的 '{ch}'"
            opening = stack.pop()
            if (ch == ')' and opening != '(') or \
               (ch == '}' and opening != '{') or \
               (ch == ']' and opening != '['):
                return False, f"括号类型不匹配: '{opening}' vs '{ch}'"
    if stack:
        return False, f"括号未关闭: 缺少 {len(stack)} 个右括号"

    return True, None


def validate_expression(expr_str: str, variables: list) -> Tuple[bool, Optional[str]]:
    """验证数学表达式是否可被SymPy解析"""
    try:
        expr = sp.sympify(expr_str)
        if expr is None:
            return False, "表达式解析结果为 None"
        # 检查未定义的符号
        free_syms = expr.free_symbols
        allowed = set(sp.Symbol(v) for v in variables)
        undefined = free_syms - allowed
        if undefined:
            names = ', '.join(str(s) for s in undefined)
            return False, f"表达式包含未定义的变量: {names}"
        return True, None
    except sp.SympifyError as e:
        return False, f"表达式语法错误: {str(e)}"
    except Exception as e:
        return False, f"表达式验证失败: {str(e)}"


def detect_function_type(latex_str: str) -> str:
    """
    检测LaTeX表达式的函数类型。
    返回: 'explicit' | 'implicit' | 'parametric' | 'unknown'
    """
    text = latex_str.strip()

    # 参数方程检测：包含逗号分隔的多个表达式，有参数标记
    # 如: x = u*cos(v), y = u*sin(v), z = u
    param_patterns = [
        r'x\s*[=:].*?,\s*y\s*[=:].*?,\s*z\s*[=:]',
        r'\b(u|v|s|t)\b.*\b(u|v|s|t)\b',  # 两个参数
    ]
    for pat in param_patterns:
        if re.search(pat, text, re.IGNORECASE):
            return 'parametric'

    # 隐函数检测：包含等号但没有 z = 形式
    if '=' in text:
        # 检查是否为显函数 z = ...
        explicit_pattern = r'^z\s*='  # 以 z = 开头
        if re.match(explicit_pattern, text.strip(), re.IGNORECASE):
            return 'explicit'
        return 'implicit'

    # 默认简单表达式视为显函数
    return 'explicit'


def normalize_latex(latex_str: str) -> str:
    """标准化LaTeX字符串"""
    # 移除多余空格
    text = re.sub(r'\s+', ' ', latex_str.strip())
    # 统一括号
    text = text.replace('{', '{').replace('}', '}')
    return text


def sanity_check_range(x_range, y_range, z_range=None):
    """检查绘图范围是否合理"""
    if x_range and len(x_range) == 2:
        if abs(x_range[1] - x_range[0]) < 0.1:
            return False, "X 范围太小"
    if y_range and len(y_range) == 2:
        if abs(y_range[1] - y_range[0]) < 0.1:
            return False, "Y 范围太小"
    if z_range and len(z_range) == 2:
        if abs(z_range[1] - z_range[0]) < 0.1:
            return False, "Z 范围太小"
    return True, None
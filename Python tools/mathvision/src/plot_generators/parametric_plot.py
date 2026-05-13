"""参数方程3D渲染: x=f(u,v), y=g(u,v), z=h(u,v)"""
import numpy as np
import plotly.graph_objects as go
from typing import Callable, Tuple, Optional


def generate_parametric_plot(
    func: Callable,
    u_range: Tuple[float, float] = (-np.pi, np.pi),
    v_range: Tuple[float, float] = (-np.pi, np.pi),
    u_resolution: int = 60,
    v_resolution: int = 60,
    color: str = '#00CC96',
    opacity: float = 0.8,
    name: str = 'Parametric',
) -> go.Surface:
    """生成参数方程 3D 曲面

    func 签名: (U, V) -> (X, Y, Z)

    Args:
        func: 可调用函数 f(u, v) -> (x, y, z)
        u_range: u 参数范围
        v_range: v 参数范围
        u_resolution: u 方向分辨率
        v_resolution: v 方向分辨率
        color: 曲面颜色
        opacity: 透明度
        name: 图例名称

    Returns:
        plotly.graph_objects.Surface
    """
    u = np.linspace(u_range[0], u_range[1], u_resolution)
    v = np.linspace(v_range[0], v_range[1], v_resolution)
    U, V = np.meshgrid(u, v)

    with np.errstate(all='ignore'):
        X, Y, Z = func(U, V)

    X = np.nan_to_num(X, nan=0.0)
    Y = np.nan_to_num(Y, nan=0.0)
    Z = np.nan_to_num(Z, nan=0.0)

    return go.Surface(
        x=X, y=Y, z=Z,
        name=name,
        showscale=False,
        colorscale=[[0, color], [1, color]],
        opacity=opacity,
        hovertemplate=(
            f'<b>{name}</b><br>'
            'x: %{x:.3f}<br>'
            'y: %{y:.3f}<br>'
            'z: %{z:.3f}<br>'
            '<extra></extra>'
        ),
    )


def generate_parametric_wireframe(
    func: Callable,
    u_range: Tuple[float, float] = (-np.pi, np.pi),
    v_range: Tuple[float, float] = (-np.pi, np.pi),
    u_resolution: int = 20,
    v_resolution: int = 20,
    color: str = '#00CC96',
    name: str = 'Wireframe',
) -> go.Scatter3d:
    """生成参数方程的线框"""
    u = np.linspace(u_range[0], u_range[1], u_resolution)
    v = np.linspace(v_range[0], v_range[1], v_resolution)
    U, V = np.meshgrid(u, v)

    with np.errstate(all='ignore'):
        X, Y, Z = func(U, V)

    X = np.nan_to_num(X, nan=0.0)
    Y = np.nan_to_num(Y, nan=0.0)
    Z = np.nan_to_num(Z, nan=0.0)

    return go.Scatter3d(
        x=X.ravel(), y=Y.ravel(), z=Z.ravel(),
        mode='markers+lines',
        marker=dict(size=2, color=color, opacity=0.6),
        line=dict(color=color, width=1, opacity=0.3),
        name=name,
        hovertemplate=(
            f'<b>{name}</b><br>'
            'x: %{x:.3f}<br>'
            'y: %{y:.3f}<br>'
            'z: %{z:.3f}<br>'
            '<extra></extra>'
        ),
    )
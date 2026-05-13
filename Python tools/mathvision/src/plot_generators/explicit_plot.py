"""显函数3D渲染: z = f(x, y)"""
import numpy as np
import plotly.graph_objects as go
from typing import Callable, Optional, Tuple


def generate_explicit_plot(
    func: Callable,
    x_range: Tuple[float, float] = (-5, 5),
    y_range: Tuple[float, float] = (-5, 5),
    resolution: int = 80,
    color: str = '#636EFA',
    opacity: float = 0.8,
    show_contours: bool = False,
    name: str = 'z = f(x, y)',
) -> go.Surface:
    """生成显函数 3D 曲面图

    Args:
        func: 可调用函数 f(x, y) -> z
        x_range: X 轴范围 (min, max)
        y_range: Y 轴范围 (min, max)
        resolution: 网格分辨率
        color: 曲面颜色
        opacity: 透明度 (0-1)
        show_contours: 是否显示等高线投影
        name: 图例名称

    Returns:
        plotly.graph_objects.Surface
    """
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)

    with np.errstate(all='ignore'):
        Z = func(X, Y)

    # 处理无穷大和NaN
    Z = np.nan_to_num(Z, nan=0.0, posinf=1e6, neginf=-1e6)

    # 自动裁剪极值
    z_std = np.nanstd(Z)
    z_mean = np.nanmean(Z)
    if z_std > 0 and z_std < 1e6:
        lower = z_mean - 3 * z_std
        upper = z_mean + 3 * z_std
        Z = np.clip(Z, lower, upper)

    surface = go.Surface(
        x=x, y=y, z=Z,
        name=name,
        showscale=True,
        colorscale=[[0, color], [1, color]],
        opacity=opacity,
        contours=dict(
            x=dict(show=show_contours, highlight=False, width=1),
            y=dict(show=show_contours, highlight=False, width=1),
            z=dict(show=show_contours, highlight=False, width=1),
        ) if show_contours else None,
        hovertemplate=(
            f'<b>{name}</b><br>'
            'x: %{x:.3f}<br>'
            'y: %{y:.3f}<br>'
            'z: %{z:.3f}<br>'
            '<extra></extra>'
        ),
    )

    return surface


def generate_explicit_contour(
    func: Callable,
    x_range: Tuple[float, float] = (-5, 5),
    y_range: Tuple[float, float] = (-5, 5),
    resolution: int = 100,
    colorscale: str = 'Viridis',
    name: str = 'Contour',
) -> go.Contour:
    """生成显函数的等高线图（2D投影）"""
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)

    with np.errstate(all='ignore'):
        Z = func(X, Y)
    Z = np.nan_to_num(Z, nan=0.0)

    return go.Contour(
        x=x, y=y, z=Z,
        name=name,
        colorscale=colorscale,
        contours=dict(
            coloring='heatmap',
            showlabels=True,
        ),
        colorbar=dict(title='z'),
        hovertemplate=(
            f'<b>{name}</b><br>'
            'x: %{x:.3f}<br>'
            'y: %{y:.3f}<br>'
            'z: %{z:.3f}<br>'
            '<extra></extra>'
        ),
    )
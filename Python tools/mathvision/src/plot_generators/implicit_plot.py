"""隐函数3D渲染: f(x, y, z) = 0

使用 marching cubes 算法提取等值面。
"""
import numpy as np
import plotly.graph_objects as go
from typing import Callable, Optional, Tuple, List


def generate_implicit_plot(
    func: Callable,
    x_range: Tuple[float, float] = (-5, 5),
    y_range: Tuple[float, float] = (-5, 5),
    z_range: Tuple[float, float] = (-5, 5),
    resolution: int = 50,
    color: str = '#EF553B',
    opacity: float = 0.7,
    name: str = 'f(x,y,z) = 0',
) -> go.Mesh3d:
    """使用 marching cubes 生成隐函数等值面

    Args:
        func: 可调用函数 f(x, y, z) -> float
        x_range: X 轴范围
        y_range: Y 轴范围
        z_range: Z 轴范围
        resolution: 网格分辨率
        color: 等值面颜色
        opacity: 透明度
        name: 图例名称

    Returns:
        plotly.graph_objects.Mesh3d
    """
    # 生成三维网格
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    z = np.linspace(z_range[0], z_range[1], resolution)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    # 计算标量场
    with np.errstate(all='ignore'):
        V = func(X, Y, Z)
    V = np.nan_to_num(V, nan=1.0)

    try:
        from skimage.measure import marching_cubes
        verts, faces, _, _ = marching_cubes(
            V, level=0.0,
            spacing=(
                (x_range[1] - x_range[0]) / (resolution - 1),
                (y_range[1] - y_range[0]) / (resolution - 1),
                (z_range[1] - z_range[0]) / (resolution - 1),
            ),
        )
        # 偏移到实际坐标
        verts[:, 0] += x_range[0]
        verts[:, 1] += y_range[0]
        verts[:, 2] += z_range[0]

        if len(verts) == 0 or len(faces) == 0:
            return _empty_mesh(name=name)

        return go.Mesh3d(
            x=verts[:, 0],
            y=verts[:, 1],
            z=verts[:, 2],
            i=faces[:, 0],
            j=faces[:, 1],
            k=faces[:, 2],
            name=name,
            color=color,
            opacity=opacity,
            flatshading=True,
            hovertemplate=(
                f'<b>{name}</b><br>'
                'x: %{x:.3f}<br>'
                'y: %{y:.3f}<br>'
                'z: %{z:.3f}<br>'
                '<extra></extra>'
            ),
        )

    except ImportError:
        return _fallback_implicit(func, x_range, y_range, z_range,
                                  resolution, color, opacity, name)
    except Exception as e:
        print(f"Marching cubes 失败: {e}")
        return _empty_mesh(name=name)


def _fallback_implicit(
    func: Callable,
    x_range, y_range, z_range,
    resolution: int, color: str, opacity: float, name: str,
) -> go.Scatter3d:
    """scikit-image 不可用时的回退：用散点采样近似"""
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    z = np.linspace(z_range[0], z_range[1], resolution)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    with np.errstate(all='ignore'):
        V = func(X, Y, Z)

    # 找到靠近零点的点
    mask = np.abs(V) < 0.15
    pts = np.column_stack([
        X[mask].ravel(),
        Y[mask].ravel(),
        Z[mask].ravel(),
    ])

    if len(pts) == 0:
        return _empty_mesh(name=name)

    # 随机采样控制点数
    max_pts = 20000
    if len(pts) > max_pts:
        idx = np.random.choice(len(pts), max_pts, replace=False)
        pts = pts[idx]

    return go.Scatter3d(
        x=pts[:, 0], y=pts[:, 1], z=pts[:, 2],
        mode='markers',
        marker=dict(
            size=2,
            color=color,
            opacity=opacity,
        ),
        name=name,
        hovertemplate=(
            f'<b>{name}</b><br>'
            'x: %{x:.3f}<br>'
            'y: %{y:.3f}<br>'
            'z: %{z:.3f}<br>'
            '<extra></extra>'
        ),
    )


def _empty_mesh(name: str = '') -> go.Scatter3d:
    """返回空的占位对象"""
    return go.Scatter3d(
        x=[], y=[], z=[],
        mode='markers',
        name=name,
        showlegend=True,
    )
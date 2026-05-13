"""
MathVision 3D - 数学公式识别与3D可视化Web应用

基于 Streamlit 的交互式数学公式 OCR 识别与 3D 可视化工具。
支持显函数、隐函数、参数方程的识别与渲染。
"""
import io
import logging
from typing import Any, Dict, List, Optional

import streamlit as st
import plotly.graph_objects as go
import numpy as np
from PIL import Image

from src.formula_manager import FormulaManager, FormulaItem
from src.formula_parser import FormulaParser
from src.ocr_recognizer import create_recognizer
from src.utils.validators import detect_function_type

# ── 页面配置 ───────────────────────────────────────
st.set_page_config(
    page_title="MathVision 3D",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 日志 ───────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── 会话状态初始化 ────────────────────────────────
if "manager" not in st.session_state:
    st.session_state.manager = FormulaManager()
if "recognizer" not in st.session_state:
    st.session_state.recognizer = create_recognizer()
if "parser" not in st.session_state:
    st.session_state.parser = FormulaParser()
if "page" not in st.session_state:
    st.session_state.page = "3D 可视化"
if "view_camera" not in st.session_state:
    st.session_state.view_camera = dict(
        eye=dict(x=1.5, y=1.5, z=1.5),
        center=dict(x=0, y=0, z=0),
        up=dict(x=0, y=0, z=1),
    )

manager: FormulaManager = st.session_state.manager


# ── 辅助函数 ──────────────────────────────────────

def get_scene_layout(formulas: List[FormulaItem]) -> Dict:
    """根据公式列表自动计算合适的场景范围"""
    return dict(
        xaxis=dict(title='X', range=[-6, 6]),
        yaxis=dict(title='Y', range=[-6, 6]),
        zaxis=dict(title='Z', range=[-6, 6]),
        aspectmode='cube',
        camera=st.session_state.view_camera,
    )


def build_figure() -> go.Figure:
    """构建包含所有可见公式的 Plotly 图表"""
    fig = go.Figure()
    visible = manager.get_visible_formulas()

    if not visible:
        fig.add_annotation(
            text="添加公式以开始可视化",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20, color="gray"),
        )
        fig.update_layout(
            scene=get_scene_layout([]),
            height=700,
        )
        return fig

    for item in visible:
        if not item.numeric_func or not item.parsed:
            continue
        try:
            trace = _generate_trace(item)
            if trace is not None:
                fig.add_trace(trace)
        except Exception as e:
            logger.error(f"生成图表失败 [{item.label}]: {e}")

    fig.update_layout(
        scene=get_scene_layout(visible),
        height=700,
        hovermode='closest',
        showlegend=True,
        legend=dict(
            x=0.01, y=0.99,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='gray',
            borderwidth=1,
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def _generate_trace(item: FormulaItem) -> Optional[go.Trace]:
    """根据公式类型生成对应的 Plotly trace"""
    ftype = item.parsed['type']
    func = item.numeric_func

    if ftype == 'explicit':
        from src.plot_generators.explicit_plot import generate_explicit_plot
        return generate_explicit_plot(
            func=func,
            color=item.color,
            opacity=item.opacity,
            name=item.label,
        )

    elif ftype == 'implicit':
        from src.plot_generators.implicit_plot import generate_implicit_plot
        return generate_implicit_plot(
            func=func,
            color=item.color,
            opacity=item.opacity,
            name=item.label,
        )

    elif ftype == 'parametric':
        from src.plot_generators.parametric_plot import generate_parametric_plot
        return generate_parametric_plot(
            func=func,
            color=item.color,
            opacity=item.opacity,
            name=item.label,
        )

    return None


# ── 侧边栏 ─────────────────────────────────────────

with st.sidebar:

    # ── 页头 ──
    st.title("🧮 MathVision 3D")
    st.caption("数学公式识别与 3D 可视化")

    # ── Tab 导航 ──
    tab_names = ["OCR 识别", "3D 可视化", "多公式对比", "分析工具"]
    current_tab_idx = tab_names.index(st.session_state.page) if st.session_state.page in tab_names else 1
    selected_tab = st.radio("功能导航", tab_names, index=current_tab_idx, label_visibility="collapsed")
    st.session_state.page = selected_tab
    st.divider()

    # ── 文件上传（始终可见） ──
    st.subheader("📤 上传图片")
    uploaded_files = st.file_uploader(
        "支持 PNG/JPG 格式",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files:
        ocr_btn = st.button("🔍 OCR 识别上传的图片", use_container_width=True, type="primary")
        if ocr_btn:
            with st.spinner("正在识别图片中的数学公式..."):
                for uploaded_file in uploaded_files:
                    image = Image.open(uploaded_file)
                    latex, confidence = st.session_state.recognizer.recognize_single(image)
                    formula_type = detect_function_type(latex)
                    label = f"OCR {manager.count + 1} ({confidence:.0%})"
                    item = manager.add_formula(latex, formula_type=formula_type, label=label)
                    st.success(f"✅ 识别成功: ${latex}$")

    # ── 手动输入公式 ──
    with st.expander("✏️ 手动输入公式", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            latex_input = st.text_input(
                "LaTeX 公式",
                placeholder="例如: z = sin(sqrt(x^2 + y^2))",
                label_visibility="collapsed",
            )
        with col2:
            add_btn = st.button("添加", use_container_width=True)

        if add_btn and latex_input.strip():
            formula_type = detect_function_type(latex_input)
            manager.add_formula(latex_input, formula_type=formula_type)
            st.rerun()

    # ── 示例公式 ──
    with st.expander("📚 示例公式"):
        examples = {
            "显函数 - 双曲抛物面": "z = x^2 - y^2",
            "显函数 - 正弦波": "z = sin(sqrt(x^2 + y^2))",
            "显函数 - 高斯曲面": "z = exp(-(x^2 + y^2)/4)",
            "隐函数 - 球体": "x^2 + y^2 + z^2 = 4",
            "隐函数 - 环面": "(sqrt(x^2 + y^2) - 2)^2 + z^2 = 1",
            "参数方程 - 螺旋面": "x = u*cos(v), y = u*sin(v), z = v/2",
            "参数方程 - 球面": "x = sin(u)*cos(v), y = sin(u)*sin(v), z = cos(u)",
        }
        for label, example in examples.items():
            if st.button(label, key=f"ex_{label}", use_container_width=True):
                ftype = detect_function_type(example)
                manager.add_formula(example, formula_type=ftype, label=label)
                st.rerun()

    st.divider()

    # ── 公式列表管理 ──
    st.subheader("📋 公式列表")

    if manager.count == 0:
        st.info("暂无公式，请上传图片或手动输入")
    else:
        for i, item in enumerate(manager.formulas):
            with st.container(border=True):
                cols = st.columns([1, 4, 1, 1])
                with cols[0]:
                    visible = st.checkbox(
                        "显示", value=item.visible,
                        key=f"vis_{item.id}",
                        label_visibility="collapsed",
                    )
                    if visible != item.visible:
                        manager.update_formula(item.id, visible=visible)
                        st.rerun()
                with cols[1]:
                    st.caption(f"**{item.label}**")
                    if item.error:
                        st.error(item.error, icon="⚠️")
                    else:
                        st.text(item.latex[:50] + ("..." if len(item.latex) > 50 else ""))
                with cols[2]:
                    st.caption(
                        {"explicit": "显函数", "implicit": "隐函数", "parametric": "参数"}.get(
                            item.formula_type, item.formula_type
                        )
                    )
                with cols[3]:
                    if st.button("✕", key=f"del_{item.id}"):
                        manager.remove_formula(item.id)
                        st.rerun()

                # 样式控制
                with st.expander("样式", key=f"style_{item.id}"):
                    new_color = st.color_picker(
                        "颜色", value=item.color,
                        key=f"color_{item.id}",
                        label_visibility="collapsed",
                    )
                    new_opacity = st.slider(
                        "透明度", 0.0, 1.0, item.opacity,
                        key=f"opacity_{item.id}",
                        label_visibility="collapsed",
                    )
                    if new_color != item.color or new_opacity != item.opacity:
                        manager.update_formula(
                            item.id, color=new_color, opacity=new_opacity,
                        )

        if st.button("🗑️ 清空所有公式", use_container_width=True):
            manager.clear()
            st.rerun()


# ── 主区域 ─────────────────────────────────────────

current_page = st.session_state.page

# ── Tab 1: OCR 识别界面 ──────────────────────────
if current_page == "OCR 识别":
    st.header("🔍 OCR 数学公式识别")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("图片上传")
        ocr_file = st.file_uploader(
            "选择图片",
            type=['png', 'jpg', 'jpeg'],
            key="ocr_uploader",
        )
        if ocr_file:
            image = Image.open(ocr_file)
            st.image(image, caption="原图", use_container_width=True)

            if st.button("开始识别", type="primary", use_container_width=True):
                with st.spinner("正在识别..."):
                    # 显示预处理效果
                    processed = st.session_state.recognizer.preprocess(image)
                    st.image(processed, caption="预处理后", use_container_width=True)

                    latex, confidence = st.session_state.recognizer.recognize_single(image)
                    formula_type = detect_function_type(latex)

                    st.session_state.last_ocr = {
                        'latex': latex,
                        'confidence': confidence,
                        'type': formula_type,
                    }

    with col2:
        st.subheader("识别结果")
        if 'last_ocr' in st.session_state:
            result = st.session_state.last_ocr
            st.success(f"**识别置信度**: {result['confidence']:.0%}")
            st.info(f"**函数类型**: {result['type']}")
            st.latex(result['latex'])
            st.code(result['latex'], language='latex')

            type_map = {
                'explicit': '显函数',
                'implicit': '隐函数',
                'parametric': '参数方程',
            }
            selected_type = st.selectbox(
                "函数类型（可修改）",
                options=['explicit', 'implicit', 'parametric'],
                format_func=lambda x: type_map.get(x, x),
                index=['explicit', 'implicit', 'parametric'].index(result['type']),
            )
            label = st.text_input("标签", value=f"OCR 公式")

            if st.button("✅ 确认添加到可视化", type="primary", use_container_width=True):
                manager.add_formula(
                    result['latex'],
                    formula_type=selected_type,
                    label=label,
                )
                st.success("已添加！切换到 3D 可视化查看")
                del st.session_state.last_ocr
                st.rerun()
        else:
            st.info("请上传图片并点击识别")

# ── Tab 2: 3D 可视化 ─────────────────────────────
elif current_page == "3D 可视化":
    st.header("🌐 3D 可视化")

    # 工具栏
    toolbar = st.container()
    with toolbar:
        tool_cols = st.columns([2, 1, 1, 1, 1])
        with tool_cols[0]:
            st.caption(f"当前公式数: {manager.count} | 可见: {len(manager.get_visible_formulas())}")
        with tool_cols[1]:
            if st.button("🔄 重置视角", use_container_width=True):
                st.session_state.view_camera = dict(
                    eye=dict(x=1.5, y=1.5, z=1.5),
                    center=dict(x=0, y=0, z=0),
                    up=dict(x=0, y=0, z=1),
                )
                st.rerun()
        with tool_cols[2]:
            top_view = st.button("🔝 俯视", use_container_width=True)
            if top_view:
                st.session_state.view_camera = dict(
                    eye=dict(x=0, y=0, z=5),
                    center=dict(x=0, y=0, z=0),
                    up=dict(x=0, y=1, z=0),
                )
                st.rerun()
        with tool_cols[3]:
            side_view = st.button("↔️ 侧视", use_container_width=True)
            if side_view:
                st.session_state.view_camera = dict(
                    eye=dict(x=5, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    up=dict(x=0, y=0, z=1),
                )
                st.rerun()
        with tool_cols[4]:
            front_view = st.button("👁️ 正视", use_container_width=True)
            if front_view:
                st.session_state.view_camera = dict(
                    eye=dict(x=0, y=5, z=1),
                    center=dict(x=0, y=0, z=0),
                    up=dict(x=0, y=0, z=1),
                )
                st.rerun()

    # 3D 图表
    fig = build_figure()
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'modeBarButtonsToAdd': [
            'drawline', 'drawopenpath', 'drawclosedpath',
            'eraseshape',
        ],
        'modeBarButtonsToRemove': ['sendDataToCloud'],
        'displaylogo': False,
        'scrollZoom': True,
    })

    # 当前视角信息
    with st.expander("📐 当前视角信息"):
        st.json(st.session_state.view_camera)

# ── Tab 3: 多公式对比 ────────────────────────────
elif current_page == "多公式对比":
    st.header("📊 多公式对比")

    visible = manager.get_visible_formulas()

    if len(visible) < 2:
        st.warning("请至少添加 2 个可见公式以进行对比")
        if st.button("📚 加载示例公式进行对比"):
            manager.add_formula("z = sin(sqrt(x^2 + y^2))", label="正弦波")
            manager.add_formula("z = x^2 - y^2", label="双曲抛物面")
            st.rerun()
    else:
        # 创建对比布局
        n = len(visible)
        cols = st.columns(min(n, 3))

        for idx, item in enumerate(visible):
            col_idx = idx % len(cols)
            with cols[col_idx]:
                st.subheader(item.label)
                st.latex(item.latex)
                st.caption(f"类型: {item.formula_type} | 透明度: {item.opacity:.2f}")
                st.color_picker("颜色", value=item.color,
                                key=f"compare_color_{item.id}",
                                disabled=True, label_visibility="collapsed")

        # 叠加显示
        st.subheader("叠加对比视图")
        fig = build_figure()
        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False,
            'scrollZoom': True,
        })

        # 公式数据表格
        st.subheader("公式参数对比")
        data = []
        for item in visible:
            data.append({
                "标签": item.label,
                "类型": item.formula_type,
                "表达式": item.latex[:40],
            })
        st.table(data)

# ── Tab 4: 分析工具 ──────────────────────────────
elif current_page == "分析工具":
    st.header("🔬 分析工具")

    visible = manager.get_visible_formulas()

    if not visible:
        st.info("请先添加公式")
    else:
        formula_names = [f"{f.label} - {f.latex[:30]}" for f in visible]
        selected_name = st.selectbox("选择公式分析", formula_names)
        selected_idx = formula_names.index(selected_name)
        selected = visible[selected_idx]

        st.subheader(selected.label)
        st.latex(selected.latex)

        tabs = st.tabs(["属性", "数值采样", "断面"])

        with tabs[0]:
            st.json(selected.to_dict())

        with tabs[1]:
            if selected.parsed and selected.parsed['valid'] and selected.numeric_func:
                st.caption("在 X, Y 网格上采样 Z 值")

                sample_x = st.slider("X 采样范围", -10.0, 10.0, (-3.0, 3.0))
                sample_y = st.slider("Y 采样范围", -10.0, 10.0, (-3.0, 3.0))
                sample_res = st.slider("分辨率", 10, 100, 30)

                if st.button("采样", use_container_width=True):
                    try:
                        xs = np.linspace(sample_x[0], sample_x[1], sample_res)
                        ys = np.linspace(sample_y[0], sample_y[1], sample_res)
                        Xs, Ys = np.meshgrid(xs, ys)
                        Zs = selected.numeric_func(Xs, Ys)
                        Zs = np.nan_to_num(Zs, nan=0.0)

                        st.write(f"**统计**")
                        st.write(f"- Z 范围: [{Zs.min():.4f}, {Zs.max():.4f}]")
                        st.write(f"- Z 均值: {Zs.mean():.4f}")
                        st.write(f"- Z 标准差: {Zs.std():.4f}")

                        # 简单热度图
                        import plotly.express as px
                        heat_fig = px.imshow(
                            Zs, x=xs, y=ys,
                            color_continuous_scale='Viridis',
                            title=f"Z 值热度图 - {selected.label}",
                            labels=dict(x="X", y="Y", color="Z"),
                        )
                        heat_fig.update_layout(height=500)
                        st.plotly_chart(heat_fig, use_container_width=True)

                    except Exception as e:
                        st.error(f"采样失败: {e}")
            else:
                st.warning("该公式不可用于数值采样")

        with tabs[2]:
            st.info("断面分析功能开发中")

# ── 页脚 ──────────────────────────────────────────
st.markdown("---")
st.caption("MathVision 3D v1.0 | 基于 Streamlit + SymPy + Plotly")
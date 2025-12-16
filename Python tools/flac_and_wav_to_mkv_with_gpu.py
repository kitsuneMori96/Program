#!/usr/bin/env python3
"""
flac_and_wav_to_mkv_with_gpu.py

GUI tool: single image + folder of .flac/.wav -> for each audio file:
  1) resample/re-encode FLAC/WAV -> FLAC @ 48kHz, 24-bit
  2) generate a static H.264/H.265 video from image with duration == audio duration (GPU accelerated)
  3) mux video + FLAC into .mkv
  4) set audio track disposition default so players auto-play it

Requirements:
- Python 3.8+
- PyQt5
- ffmpeg & ffprobe (with GPU support)
- NVIDIA: requires NVIDIA drivers and CUDA support
- AMD: requires AMD drivers and AMF support
- Intel: requires Intel Media SDK
"""
import sys
import os
import json
import shutil
import tempfile
import subprocess
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QTextEdit, QProgressBar, QMessageBox,
    QGroupBox, QCheckBox, QComboBox, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

CONFIG_PATH = Path.home() / ".flac_to_mkv_config.json"

# -------------------------
# Utilities
# -------------------------
def which_bin(name: str):
    return shutil.which(name)

def load_config():
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_config(cfg: dict):
    try:
        CONFIG_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

def run_quiet(cmd, capture=False, timeout=None, ffmpeg_safe=True):
    """
    Run a subprocess safely:
    - By default redirect stdout/stderr to DEVNULL (avoids Windows text-reader crashes).
    - If capture=True, capture stderr as bytes and return (returncode, stdout_bytes, stderr_bytes).
    """
    if capture:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, timeout=timeout, text=False)
        return p.returncode, p.stdout, p.stderr
    else:
        # suppress outputs to avoid encoding/reader issues on Windows
        p = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, timeout=timeout)
        return p.returncode, None, None

def ffprobe_duration_seconds(path: Path, ffprobe_bin=None):
    ffprobe = ffprobe_bin or which_bin('ffprobe') or 'ffprobe'
    cmd = [ffprobe, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(path)]
    rc, outb, errb = run_quiet(cmd, capture=True)
    if rc != 0:
        stderr = errb.decode('utf-8', errors='ignore') if errb else ''
        raise RuntimeError(f"ffprobe failed: {stderr.strip()}")
    out = outb.decode('utf-8', errors='ignore') if outb else ''
    try:
        return float(out.strip())
    except Exception:
        raise RuntimeError(f"ffprobe returned unparsable duration: {out!r}")

def ffprobe_has_audio(path: Path, ffprobe_bin=None):
    ffprobe = ffprobe_bin or which_bin('ffprobe') or 'ffprobe'
    cmd = [ffprobe, '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'default=noprint_wrappers=1:nokey=1', str(path)]
    rc, outb, errb = run_quiet(cmd, capture=True)
    if rc != 0:
        return False
    out = outb.decode('utf-8', errors='ignore') if outb else ''
    return bool(out.strip())

# -------------------------
# GPU Encoder Settings
# -------------------------
GPU_ENCODERS = {
    "cpu": {
        "h264": "libx264",
        "h265": "libx265",
        "presets": ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"]
    },
    "nvidia": {
        "h264": "h264_nvenc",
        "h265": "hevc_nvenc",
        "presets": ["p1", "p2", "p3", "p4", "p5", "p6", "p7"],  # p1=fastest, p7=slowest
        "tune": ["hq", "ll", "ull", "lossless", "losslesshp"],
        "requires": ["-hwaccel", "cuda", "-hwaccel_output_format", "cuda"]
    },
    "amd": {
        "h264": "h264_amf",
        "h265": "hevc_amf",
        "presets": ["speed", "balanced", "quality"],
        "requires": []
    },
    "intel": {
        "h264": "h264_qsv",
        "h265": "hevc_qsv",
        "presets": ["veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"],
        "requires": ["-hwaccel", "qsv", "-hwaccel_output_format", "qsv"]
    }
}

def detect_gpu_capabilities(ffmpeg_path=None):
    """检测系统可用的GPU编码器"""
    ffmpeg = ffmpeg_path or which_bin('ffmpeg') or 'ffmpeg'
    capabilities = {
        "nvidia": False,
        "amd": False,
        "intel": False,
        "cpu": True
    }
    
    # 运行 ffmpeg -encoders 检查可用编码器
    cmd = [ffmpeg, '-encoders']
    rc, outb, errb = run_quiet(cmd, capture=True)
    
    if rc == 0:
        output = (outb or b'').decode('utf-8', errors='ignore') + (errb or b'').decode('utf-8', errors='ignore')
        
        # 检查NVIDIA编码器
        if 'h264_nvenc' in output or 'hevc_nvenc' in output:
            capabilities["nvidia"] = True
            
        # 检查AMD编码器
        if 'h264_amf' in output or 'hevc_amf' in output:
            capabilities["amd"] = True
            
        # 检查Intel编码器
        if 'h264_qsv' in output or 'hevc_qsv' in output:
            capabilities["intel"] = True
    
    return capabilities

# -------------------------
# Worker
# -------------------------
class Worker(QThread):
    log = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal(int, int)

    def __init__(self, image_path, folder_path, output_dir, file_types, 
                 ffmpeg_path=None, ffprobe_path=None, fps=24, 
                 sample_rate=48000, bit_depth=24,
                 gpu_type="cpu", video_codec="h264", preset="medium"):
        super().__init__()
        self.image_path = Path(image_path).resolve()
        self.folder_path = Path(folder_path).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.ffmpeg = ffmpeg_path or which_bin('ffmpeg') or 'ffmpeg'
        self.ffprobe = ffprobe_path or which_bin('ffprobe') or 'ffprobe'
        self.fps = fps
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
        self.file_types = file_types
        self.gpu_type = gpu_type
        self.video_codec = video_codec
        self.preset = preset
        
    def _log(self, s):
        self.log.emit(s)
        
    def _get_audio_files(self):
        """根据选择的文件类型获取音频文件列表"""
        files = []
        
        for file_type in self.file_types:
            if file_type == "flac":
                files.extend(self.folder_path.rglob("*.flac"))
            elif file_type == "wav":
                files.extend(self.folder_path.rglob("*.wav"))
                
        return sorted(set(files))  # 去重并排序
        
    def _get_sample_format(self, bit_depth):
        """根据位深度返回对应的ffmpeg采样格式"""
        if bit_depth == 16:
            return "s16"
        elif bit_depth == 24:
            return "s32"  # ffmpeg使用s32表示24-bit
        elif bit_depth == 32:
            return "s32"
        else:
            return "s32"  # 默认
    
    def _get_gpu_encoder_settings(self):
        """获取GPU编码器设置"""
        gpu_info = GPU_ENCODERS.get(self.gpu_type, GPU_ENCODERS["cpu"])
        encoder = gpu_info.get(self.video_codec, gpu_info.get("h264"))
        extra_params = gpu_info.get("requires", [])
        return encoder, extra_params
    
    def _build_video_command(self, image_path, temp_video, duration, encoder, extra_params):
        """构建视频生成命令"""
        cmd = [
            self.ffmpeg, '-y',
            '-hide_banner', '-loglevel', 'error',
        ]
        
        # 添加GPU加速参数
        if self.gpu_type != "cpu" and extra_params:
            cmd.extend(extra_params)
        
        # 添加输入参数
        cmd.extend([
            '-loop', '1',
            '-framerate', str(self.fps),
            '-i', str(image_path),
        ])
        
        # 添加编码参数
        cmd.extend([
            '-c:v', encoder,
            '-preset', self.preset,
            '-pix_fmt', 'yuv420p',
            '-t', str(duration),
        ])
        
        # 添加特定GPU的优化参数
        if self.gpu_type == "nvidia":
            # NVIDIA 特定参数
            if self.video_codec == "h264":
                cmd.extend(['-rc', 'vbr', '-cq', '23', '-b:v', '0'])
            elif self.video_codec == "h265":
                cmd.extend(['-rc', 'vbr', '-cq', '28', '-b:v', '0'])
        elif self.gpu_type == "amd":
            # AMD 特定参数
            if self.video_codec == "h264":
                cmd.extend(['-usage', 'transcoding', '-quality', 'balanced'])
            elif self.video_codec == "h265":
                cmd.extend(['-usage', 'transcoding', '-quality', 'balanced'])
        elif self.gpu_type == "intel":
            # Intel 特定参数
            cmd.extend(['-look_ahead', '0'])
        
        # 输出文件
        cmd.append(str(temp_video))
        
        return cmd

    def run(self):
        files = self._get_audio_files()
        
        if not files:
            self._log("未找到 .flac 或 .wav 文件。")
            self.finished.emit(0, 0)
            return

        self.output_dir.mkdir(parents=True, exist_ok=True)
        total = len(files)
        succ = 0
        
        # 获取编码器设置
        encoder, extra_params = self._get_gpu_encoder_settings()
        self._log(f"使用编码器: {encoder} ({self.gpu_type.upper()})")
        self._log(f"预设: {self.preset}")
        
        sample_fmt = self._get_sample_format(self.bit_depth)
        
        for idx, audio_file in enumerate(files, start=1):
            try:
                self._log(f"[{idx}/{total}] 处理：{audio_file.name} ({audio_file.suffix})")
                
                # 获取文件时长
                try:
                    duration = ffprobe_duration_seconds(audio_file, ffprobe_bin=self.ffprobe)
                except Exception as e:
                    self._log(f"  无法读取时长，跳过：{e}")
                    continue

                if duration <= 0:
                    self._log("  时长 <=0，跳过")
                    continue

                if not ffprobe_has_audio(audio_file, ffprobe_bin=self.ffprobe):
                    self._log("  未检测到音频流，跳过")
                    continue

                self._log(f"  时长：{duration:.2f}s")

                # 准备临时文件
                with tempfile.TemporaryDirectory() as td:
                    td = Path(td)
                    # 重采样后的FLAC路径
                    resampled = td / (audio_file.stem + f"_{self.sample_rate}k{self.bit_depth}bit.flac")
                    # 临时视频
                    temp_video = td / (audio_file.stem + "_video.mp4")
                    out_mkv = self.output_dir / (audio_file.stem + ".mkv")

                    # 1) 重采样音频 -> 指定采样率和位深的FLAC
                    self._log(f"  正在重采样音频 -> {self.sample_rate}kHz {self.bit_depth}-bit FLAC ...")
                    
                    # 构建ffmpeg命令
                    cmd_resample = [
                        self.ffmpeg, '-y',
                        '-hide_banner', '-loglevel', 'error',
                        '-i', str(audio_file),
                    ]
                    
                    # 添加音频过滤器
                    cmd_resample.extend([
                        '-af', f'aresample={self.sample_rate}',
                        '-sample_fmt', sample_fmt,
                        '-bits_per_raw_sample', str(self.bit_depth),
                        str(resampled)
                    ])
                    
                    rc, _, _ = run_quiet(cmd_resample, capture=False)
                    if rc != 0 or not resampled.exists():
                        # 捕获错误信息用于诊断
                        self._log("  重采样失败，尝试捕获错误信息...")
                        rc2, outb2, errb2 = run_quiet(cmd_resample, capture=True)
                        err = errb2.decode('utf-8', errors='ignore') if errb2 else "(no stderr)"
                        self._log(f"  重采样失败 stderr 摘要:\n{err.strip()[:2000]}")
                        continue
                    self._log("  重采样成功")

                    # 2) 从图片生成静态视频（使用GPU加速）
                    cmd_video = self._build_video_command(
                        self.image_path, temp_video, duration, encoder, extra_params
                    )
                    
                    self._log(f"  正在生成静态视频轨（{self.video_codec.upper()}，使用{self.gpu_type.upper()} GPU加速）...")
                    rc, _, _ = run_quiet(cmd_video, capture=False)
                    if rc != 0 or not temp_video.exists():
                        self._log("  生成视频失败，尝试捕获错误信息...")
                        rc2, outb2, errb2 = run_quiet(cmd_video, capture=True)
                        err = errb2.decode('utf-8', errors='ignore') if errb2 else "(no stderr)"
                        self._log(f"  生成视频失败 stderr 摘要:\n{err.strip()[:2000]}")
                        
                        # 如果GPU编码失败，尝试回退到CPU编码
                        if self.gpu_type != "cpu":
                            self._log("  GPU编码失败，尝试回退到CPU编码...")
                            cpu_encoder, _ = self._get_gpu_encoder_settings()
                            cpu_encoder = GPU_ENCODERS["cpu"].get(self.video_codec, "libx264")
                            cmd_video_cpu = self._build_video_command(
                                self.image_path, temp_video, duration, cpu_encoder, []
                            )
                            rc2, _, _ = run_quiet(cmd_video_cpu, capture=False)
                            if rc2 == 0 and temp_video.exists():
                                self._log("  CPU编码成功")
                            else:
                                continue
                        else:
                            continue
                    self._log("  静态视频生成成功")

                    # 3) 混合视频 + 音频到MKV
                    cmd_mux = [
                        self.ffmpeg, '-y',
                        '-hide_banner', '-loglevel', 'error',
                        '-i', str(temp_video),
                        '-i', str(resampled),
                        '-map', '0:v',
                        '-map', '1:a',
                        '-c:v', 'copy',
                        '-c:a', 'copy',
                        '-disposition:a:0', 'default',
                        str(out_mkv)
                    ]
                    self._log("  正在封装到 MKV（不转码音频，直接 copy FLAC）...")
                    rc, _, _ = run_quiet(cmd_mux, capture=False)
                    if rc != 0 or not out_mkv.exists():
                        self._log("  封装失败，尝试捕获错误信息...")
                        rc2, outb2, errb2 = run_quiet(cmd_mux, capture=True)
                        err = errb2.decode('utf-8', errors='ignore') if errb2 else "(no stderr)"
                        self._log(f"  封装失败 stderr 摘要:\n{err.strip()[:2000]}")
                        continue

                    # 成功
                    self._log(f"  ✓ 已生成：{out_mkv.name}")
                    succ += 1

                # 更新进度
                self.progress.emit(int(idx / total * 100))

            except Exception as e:
                self._log(f"  处理异常: {e}")
                import traceback
                self._log(f"  异常详情: {traceback.format_exc()}")

        self.finished.emit(succ, total)

# -------------------------
# GUI
# -------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FLAC/WAV -> MKV (GPU加速版)")
        self.resize(900, 800)

        cfg = load_config()
        self.user_ffmpeg = cfg.get('ffmpeg_path', '') or ''
        self.user_ffprobe = cfg.get('ffprobe_path', '') or ''
        self.file_types = cfg.get('file_types', ['flac', 'wav'])
        self.gpu_type = cfg.get('gpu_type', 'cpu')
        self.video_codec = cfg.get('video_codec', 'h264')
        self.preset = cfg.get('preset', 'medium')

        self.image_path = ""
        self.folder_path = ""
        self.output_dir = ""
        self.gpu_capabilities = {"cpu": True}  # 默认只有CPU可用

        self.init_ui()
        self.detect_gpu_capabilities()

    def init_ui(self):
        w = QWidget()
        self.setCentralWidget(w)
        v = QVBoxLayout(w)

        # ffmpeg choose
        gb_ff = QGroupBox("FFmpeg / FFprobe (可选，设置会保存)")
        gff = QHBoxLayout()
        btn_ff = QPushButton("选择 ffmpeg.exe")
        btn_ff.clicked.connect(self.choose_ffmpeg)
        self.lbl_ff = QLabel(self.user_ffmpeg or "(未指定，使用 PATH)")
        btn_fp = QPushButton("选择 ffprobe.exe")
        btn_fp.clicked.connect(self.choose_ffprobe)
        self.lbl_fp = QLabel(self.user_ffprobe or "(未指定, 使用 PATH)")
        gff.addWidget(btn_ff); gff.addWidget(self.lbl_ff)
        gff.addSpacing(8)
        gff.addWidget(btn_fp); gff.addWidget(self.lbl_fp)
        gb_ff.setLayout(gff)
        v.addWidget(gb_ff)

        # GPU检测结果
        self.gpu_status_label = QLabel("正在检测GPU加速能力...")
        v.addWidget(self.gpu_status_label)

        # 视频编码设置
        gb_video = QGroupBox("视频编码设置 (GPU加速)")
        gv = QVBoxLayout()
        
        # GPU类型选择
        h1 = QHBoxLayout()
        h1.addWidget(QLabel("GPU加速类型:"))
        
        self.gpu_button_group = QButtonGroup()
        self.cpu_radio = QRadioButton("CPU (软件编码)")
        self.nvidia_radio = QRadioButton("NVIDIA GPU")
        self.amd_radio = QRadioButton("AMD GPU")
        self.intel_radio = QRadioButton("Intel GPU")
        
        self.gpu_button_group.addButton(self.cpu_radio, 0)
        self.gpu_button_group.addButton(self.nvidia_radio, 1)
        self.gpu_button_group.addButton(self.amd_radio, 2)
        self.gpu_button_group.addButton(self.intel_radio, 3)
        
        h1.addWidget(self.cpu_radio)
        h1.addWidget(self.nvidia_radio)
        h1.addWidget(self.amd_radio)
        h1.addWidget(self.intel_radio)
        h1.addStretch()
        
        gv.addLayout(h1)
        
        # 视频编码器和预设
        h2 = QHBoxLayout()
        h2.addWidget(QLabel("视频编码:"))
        self.video_codec_combo = QComboBox()
        self.video_codec_combo.addItems(["h264", "h265"])
        self.video_codec_combo.setCurrentText(self.video_codec)
        h2.addWidget(self.video_codec_combo)
        
        h2.addSpacing(20)
        h2.addWidget(QLabel("预设:"))
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(GPU_ENCODERS["cpu"]["presets"])
        self.preset_combo.setCurrentText(self.preset)
        h2.addWidget(self.preset_combo)
        
        h2.addStretch()
        gv.addLayout(h2)
        
        # 帧率
        h3 = QHBoxLayout()
        h3.addWidget(QLabel("视频帧率:"))
        self.fps_spin = QComboBox()
        self.fps_spin.addItems(["1", "5", "10", "15", "24", "25", "30", "50", "60"])
        self.fps_spin.setCurrentText("24")
        h3.addWidget(self.fps_spin)
        h3.addStretch()
        gv.addLayout(h3)
        
        gb_video.setLayout(gv)
        v.addWidget(gb_video)
        
        # 连接信号
        self.cpu_radio.toggled.connect(lambda: self.on_gpu_type_changed("cpu"))
        self.nvidia_radio.toggled.connect(lambda: self.on_gpu_type_changed("nvidia"))
        self.amd_radio.toggled.connect(lambda: self.on_gpu_type_changed("amd"))
        self.intel_radio.toggled.connect(lambda: self.on_gpu_type_changed("intel"))
        self.video_codec_combo.currentTextChanged.connect(self.on_video_codec_changed)

        # 音频设置
        gb_audio = QGroupBox("音频设置")
        ga = QHBoxLayout()
        ga.addWidget(QLabel("采样率:"))
        self.sample_rate_combo = QComboBox()
        self.sample_rate_combo.addItems(["44100", "48000", "96000", "192000"])
        self.sample_rate_combo.setCurrentText("48000")
        ga.addWidget(self.sample_rate_combo)
        
        ga.addSpacing(20)
        ga.addWidget(QLabel("位深度:"))
        self.bit_depth_combo = QComboBox()
        self.bit_depth_combo.addItems(["16", "24", "32"])
        self.bit_depth_combo.setCurrentText("24")
        ga.addWidget(self.bit_depth_combo)
        
        ga.addSpacing(20)
        ga.addWidget(QLabel("处理文件类型:"))
        
        # 文件类型复选框
        self.flac_check = QCheckBox("FLAC")
        self.flac_check.setChecked("flac" in self.file_types)
        ga.addWidget(self.flac_check)
        
        self.wav_check = QCheckBox("WAV")
        self.wav_check.setChecked("wav" in self.file_types)
        ga.addWidget(self.wav_check)
        
        ga.addStretch()
        gb_audio.setLayout(ga)
        v.addWidget(gb_audio)

        # image
        gb_img = QGroupBox("1) 选择图片（用于所有视频）")
        gli = QHBoxLayout()
        btn_img = QPushButton("选择图片")
        btn_img.clicked.connect(self.choose_image)
        self.lbl_img = QLabel("未选择")
        gli.addWidget(btn_img); gli.addWidget(self.lbl_img); gli.addStretch()
        gb_img.setLayout(gli)
        v.addWidget(gb_img)
        
        self.preview = QLabel()
        self.preview.setFixedSize(360, 220)
        self.preview.setStyleSheet("border:1px solid #ccc;")
        v.addWidget(self.preview)

        # folder
        gb_folder = QGroupBox("2) 选择包含音频文件的文件夹（递归搜索）")
        glf = QHBoxLayout()
        btn_folder = QPushButton("选择文件夹")
        btn_folder.clicked.connect(self.choose_folder)
        self.lbl_folder = QLabel("未选择")
        glf.addWidget(btn_folder); glf.addWidget(self.lbl_folder); glf.addStretch()
        gb_folder.setLayout(glf)
        v.addWidget(gb_folder)

        # output
        gb_out = QGroupBox("3) 输出目录")
        glo = QHBoxLayout()
        btn_out = QPushButton("选择输出目录")
        btn_out.clicked.connect(self.choose_output)
        self.lbl_out = QLabel("未选择（默认：./output）")
        glo.addWidget(btn_out); glo.addWidget(self.lbl_out); glo.addStretch()
        gb_out.setLayout(glo)
        v.addWidget(gb_out)

        # start
        hstart = QHBoxLayout()
        self.btn_start = QPushButton("开始批量生成 MKV (GPU加速)")
        self.btn_start.clicked.connect(self.start)
        self.progress = QProgressBar()
        self.progress.setValue(0)
        hstart.addWidget(self.btn_start); hstart.addWidget(self.progress)
        v.addLayout(hstart)

        # log
        self.logbox = QTextEdit()
        self.logbox.setReadOnly(True)
        v.addWidget(self.logbox)
        
    def detect_gpu_capabilities(self):
        """检测GPU加速能力"""
        ffmpeg_bin = self.user_ffmpeg or which_bin('ffmpeg')
        if not ffmpeg_bin:
            self.gpu_status_label.setText("未找到ffmpeg，无法检测GPU加速能力")
            return
            
        try:
            self.gpu_capabilities = detect_gpu_capabilities(ffmpeg_bin)
            
            # 更新界面状态
            status_text = "检测到GPU加速能力: "
            available_gpus = []
            for gpu_type, available in self.gpu_capabilities.items():
                if available and gpu_type != "cpu":
                    available_gpus.append(gpu_type.upper())
            
            if available_gpus:
                status_text += ", ".join(available_gpus)
            else:
                status_text += "无 (将使用CPU编码)"
                
            self.gpu_status_label.setText(status_text)
            
            # 设置默认选择的GPU类型
            if self.gpu_capabilities.get("nvidia", False):
                self.nvidia_radio.setChecked(True)
                self.on_gpu_type_changed("nvidia")
            elif self.gpu_capabilities.get("amd", False):
                self.amd_radio.setChecked(True)
                self.on_gpu_type_changed("amd")
            elif self.gpu_capabilities.get("intel", False):
                self.intel_radio.setChecked(True)
                self.on_gpu_type_changed("intel")
            else:
                self.cpu_radio.setChecked(True)
                self.on_gpu_type_changed("cpu")
                
        except Exception as e:
            self.gpu_status_label.setText(f"GPU检测失败: {str(e)}")
            self.cpu_radio.setChecked(True)
            self.on_gpu_type_changed("cpu")
    
    def on_gpu_type_changed(self, gpu_type):
        """GPU类型改变时更新预设列表"""
        self.gpu_type = gpu_type
        self.preset_combo.clear()
        
        if gpu_type in GPU_ENCODERS:
            presets = GPU_ENCODERS[gpu_type].get("presets", GPU_ENCODERS["cpu"]["presets"])
            self.preset_combo.addItems(presets)
            
            # 设置默认预设
            if gpu_type == "nvidia":
                self.preset_combo.setCurrentText("p4")  # NVIDIA默认平衡预设
            elif gpu_type == "amd":
                self.preset_combo.setCurrentText("balanced")
            elif gpu_type == "intel":
                self.preset_combo.setCurrentText("medium")
            else:
                self.preset_combo.setCurrentText("medium")
    
    def on_video_codec_changed(self, codec):
        """视频编码器改变时更新预设"""
        self.video_codec = codec
        # 重新加载当前GPU类型的预设
        self.on_gpu_type_changed(self.gpu_type)
        
    def get_selected_file_types(self):
        """获取选择的文件类型"""
        file_types = []
        if self.flac_check.isChecked():
            file_types.append("flac")
        if self.wav_check.isChecked():
            file_types.append("wav")
        return file_types

    def log(self, s: str):
        self.logbox.append(s)
        QApplication.processEvents()

    def choose_ffmpeg(self):
        f, _ = QFileDialog.getOpenFileName(self, "选择 ffmpeg 可执行文件", "", "Executables (*.exe);;All files (*)")
        if f:
            self.user_ffmpeg = str(Path(f).resolve())
            cfg = load_config()
            cfg['ffmpeg_path'] = self.user_ffmpeg
            save_config(cfg)
            self.lbl_ff.setText(self.user_ffmpeg)
            self.log(f"已指定 ffmpeg: {self.user_ffmpeg}")
            # 重新检测GPU能力
            self.detect_gpu_capabilities()

    def choose_ffprobe(self):
        f, _ = QFileDialog.getOpenFileName(self, "选择 ffprobe 可执行文件", "", "Executables (*.exe);;All files (*)")
        if f:
            self.user_ffprobe = str(Path(f).resolve())
            cfg = load_config()
            cfg['ffprobe_path'] = self.user_ffprobe
            save_config(cfg)
            self.lbl_fp.setText(self.user_ffprobe)
            self.log(f"已指定 ffprobe: {self.user_ffprobe}")

    def choose_image(self):
        f, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "图片 (*.png *.jpg *.jpeg *.bmp *.webp)")
        if f:
            self.image_path = str(Path(f).resolve())
            self.lbl_img.setText(Path(self.image_path).name)
            pix = QPixmap(self.image_path)
            if not pix.isNull():
                pix = pix.scaled(self.preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.preview.setPixmap(pix)

    def choose_folder(self):
        d = QFileDialog.getExistingDirectory(self, "选择包含音频文件的文件夹")
        if d:
            self.folder_path = str(Path(d).resolve())
            self.lbl_folder.setText(self.folder_path)

    def choose_output(self):
        d = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if d:
            self.output_dir = str(Path(d).resolve())
            self.lbl_out.setText(self.output_dir)

    def start(self):
        if not getattr(self, 'image_path', ''):
            QMessageBox.warning(self, "提示", "请先选择一张图片")
            return
        if not getattr(self, 'folder_path', ''):
            QMessageBox.warning(self, "提示", "请先选择包含音频文件的文件夹")
            return
            
        # 检查是否选择了文件类型
        file_types = self.get_selected_file_types()
        if not file_types:
            QMessageBox.warning(self, "提示", "请至少选择一种音频文件类型（FLAC 或 WAV）")
            return
            
        if not getattr(self, 'output_dir', ''):
            self.output_dir = str(Path.cwd() / "output")
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)
            self.lbl_out.setText(self.output_dir)

        ffmpeg_bin = self.user_ffmpeg or which_bin('ffmpeg')
        ffprobe_bin = self.user_ffprobe or which_bin('ffprobe')
        if not ffmpeg_bin or not ffprobe_bin:
            QMessageBox.warning(self, "提示", "未找到 ffmpeg/ffprobe。请指定可执行文件或确保已安装并在 PATH 中。")
            return

        # 保存设置
        cfg = load_config()
        cfg['file_types'] = file_types
        cfg['gpu_type'] = self.gpu_type
        cfg['video_codec'] = self.video_codec
        cfg['preset'] = self.preset_combo.currentText()
        save_config(cfg)
        
        # 显示处理信息
        file_types_str = " 和 ".join([f".{ft.upper()}" for ft in file_types])
        self.log(f"开始处理 {file_types_str} 文件...")
        self.log(f"GPU加速: {self.gpu_type.upper()}")
        self.log(f"视频编码: {self.video_codec.upper()}")
        self.log(f"编码预设: {self.preset_combo.currentText()}")
        self.log(f"采样率: {self.sample_rate_combo.currentText()} Hz")
        self.log(f"位深度: {self.bit_depth_combo.currentText()} bit")
        self.log(f"帧率: {self.fps_spin.currentText()} fps")

        # 禁用开始按钮
        self.btn_start.setEnabled(False)
        self.log("开始批量处理...")

        self.worker = Worker(
            self.image_path, 
            self.folder_path, 
            self.output_dir, 
            file_types,
            ffmpeg_path=ffmpeg_bin, 
            ffprobe_path=ffprobe_bin, 
            fps=int(self.fps_spin.currentText()),
            sample_rate=int(self.sample_rate_combo.currentText()),
            bit_depth=int(self.bit_depth_combo.currentText()),
            gpu_type=self.gpu_type,
            video_codec=self.video_codec,
            preset=self.preset_combo.currentText()
        )
        self.worker.log.connect(self.log)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, succ, total):
        self.log(f"全部完成：成功 {succ} / {total}")
        QMessageBox.information(self, "完成", f"处理完成：成功 {succ} / {total}")
        self.btn_start.setEnabled(True)
        self.progress.setValue(100)

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
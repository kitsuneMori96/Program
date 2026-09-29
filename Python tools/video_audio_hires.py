#!/usr/bin/env python3
"""
video_audio_hires.py

GUI tool: Extract audio from video -> resample to 48kHz 24bit FLAC -> mux back to MKV

Requirements:
- Python 3.8+
- PyQt5
- ffmpeg & ffprobe
"""
import sys
import os
import json
import shutil
import tempfile
import subprocess
import concurrent.futures
import traceback
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QTextEdit, QProgressBar, QMessageBox,
    QGroupBox, QCheckBox, QComboBox, QRadioButton, QButtonGroup, QListWidget,
    QListWidgetItem, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

CONFIG_PATH = Path.home() / ".video_audio_hires_config.json"
DEFAULT_OUTPUT_DIR = Path(r"D:\Video\目标文件夹")

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm", ".m4v", ".ts", ".mpg", ".mpeg"}

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

def run_quiet(cmd, capture=False, timeout=None):
    if capture:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, timeout=timeout, text=False)
        return p.returncode, p.stdout, p.stderr
    else:
        p = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, timeout=timeout)
        return p.returncode, None, None

def ffprobe_video_info(path: Path, ffprobe_bin=None):
    """Get video info including audio streams"""
    ffprobe = ffprobe_bin or which_bin('ffprobe') or 'ffprobe'
    cmd = [
        ffprobe, '-v', 'error',
        '-show_entries', 'format=duration',
        '-show_streams',
        '-of', 'json',
        str(path)
    ]
    rc, outb, errb = run_quiet(cmd, capture=True)
    if rc != 0 or not outb:
        stderr = errb.decode('utf-8', errors='ignore') if errb else ''
        raise RuntimeError(f"ffprobe failed: {stderr.strip()[:200]}")
    data = json.loads(outb.decode('utf-8', errors='ignore'))
    duration = float(data.get('format', {}).get('duration', 0))
    
    video_stream = None
    audio_streams = []
    for st in data.get('streams', []):
        if st.get('codec_type') == 'video' and not video_stream:
            video_stream = st
        elif st.get('codec_type') == 'audio':
            audio_streams.append(st)
    
    return {
        'duration': duration,
        'has_video': video_stream is not None,
        'video_codec': video_stream.get('codec_name', '') if video_stream else '',
        'audio_streams': audio_streams,
        'audio_count': len(audio_streams),
    }

# -------------------------
# Worker
# -------------------------
class Worker(QThread):
    log = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal(int, int)

    def __init__(self, input_files, output_dir, 
                 ffmpeg_path=None, ffprobe_path=None, 
                 sample_rate=48000, bit_depth=24,
                 audio_track_index=0, max_workers=2):
        super().__init__()
        self.input_files = [Path(f) for f in input_files]
        self.output_dir = Path(output_dir).resolve()
        self.ffmpeg = ffmpeg_path or which_bin('ffmpeg') or 'ffmpeg'
        self.ffprobe = ffprobe_path or which_bin('ffprobe') or 'ffprobe'
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
        self.audio_track_index = audio_track_index
        self.max_workers = max_workers
        self._temp_dir = None

    def _log(self, s):
        self.log.emit(s)

    def _get_video_info(self, path):
        return ffprobe_video_info(path, ffprobe_bin=self.ffprobe)

    def _extract_audio(self, video_path, output_path, track_index=0):
        """Extract audio track from video"""
        cmd = [
            self.ffmpeg, '-y',
            '-hide_banner', '-loglevel', 'error',
            '-i', str(video_path),
            '-map', f'0:a:{track_index}',
            '-vn',
            '-c:a', 'flac',
            '-compression_level', '5',
            str(output_path)
        ]
        self._log(f"  正在提取音轨 {track_index} ...")
        rc, _, _ = run_quiet(cmd, capture=False)
        if rc != 0 or not output_path.exists():
            rc2, outb2, errb2 = run_quiet(cmd, capture=True)
            err = errb2.decode('utf-8', errors='ignore') if errb2 else "(no stderr)"
            self._log(f"  提取失败: {err.strip()[:500]}")
            return False
        self._log("  音频提取成功")
        return True

    def _resample_audio(self, audio_input, output_path):
        """Resample audio to target format"""
        cmd = [
            self.ffmpeg, '-y',
            '-hide_banner', '-loglevel', 'error',
            '-i', str(audio_input),
            '-af', f'aresample={self.sample_rate}',
            '-sample_fmt', 's32' if self.bit_depth >= 24 else 's16',
            '-bits_per_raw_sample', str(self.bit_depth),
            '-c:a', 'flac',
            str(output_path)
        ]
        self._log(f"  正在重采样音频 -> {self.sample_rate}kHz {self.bit_depth}bit ...")
        rc, _, _ = run_quiet(cmd, capture=False)
        if rc != 0 or not output_path.exists():
            rc2, outb2, errb2 = run_quiet(cmd, capture=True)
            err = errb2.decode('utf-8', errors='ignore') if errb2 else "(no stderr)"
            self._log(f"  重采样失败: {err.strip()[:500]}")
            return False
        self._log("  重采样成功")
        return True

    def _mux_video_audio(self, video_path, audio_path, output_path):
        """Mux video + processed audio into MKV"""
        cmd = [
            self.ffmpeg, '-y',
            '-hide_banner', '-loglevel', 'error',
            '-i', str(video_path),
            '-i', str(audio_path),
            '-map', '0:v',
            '-map', '1:a',
            '-c:v', 'copy',
            '-c:a', 'copy',
            '-shortest',
            '-disposition:a:0', 'default',
            str(output_path)
        ]
        self._log("  正在封装到 MKV ...")
        rc, _, _ = run_quiet(cmd, capture=False)
        if rc != 0 or not output_path.exists():
            rc2, outb2, errb2 = run_quiet(cmd, capture=True)
            err = errb2.decode('utf-8', errors='ignore') if errb2 else "(no stderr)"
            self._log(f"  封装失败: {err.strip()[:500]}")
            return False
        self._log(f"  ✓ 已生成：{output_path.name}")
        return True

    def _process_one_file(self, video_file):
        self._log(f"\n处理：{video_file.name}")
        try:
            # Get video info
            info = self._get_video_info(video_file)
            if not info['has_video']:
                self._log(f"  跳过（无视频流）：{video_file.name}")
                return False
            
            if info['audio_count'] == 0:
                self._log(f"  跳过（无音频流）：{video_file.name}")
                return False
            
            # Check if requested track index exists
            if self.audio_track_index >= info['audio_count']:
                self._log(f"  警告：请求的音轨索引 {self.audio_track_index} 不存在，使用音轨 0")
                track_index = 0
            else:
                track_index = self.audio_track_index
            
            self._log(f"  视频时长: {info['duration']:.1f}s, 音轨数: {info['audio_count']}")
            
            # Step 1: Extract audio
            extracted_audio = self._temp_dir / (video_file.stem + "_extracted.flac")
            if not self._extract_audio(video_file, extracted_audio, track_index):
                return False
            
            # Step 2: Resample audio
            resampled_audio = self._temp_dir / (video_file.stem + "_resampled.flac")
            if not self._resample_audio(extracted_audio, resampled_audio):
                return False
            
            # Step 3: Mux back
            output_file = self.output_dir / (video_file.stem + ".mkv")
            if not self._mux_video_audio(video_file, resampled_audio, output_file):
                return False
            
            return True
            
        except Exception as e:
            self._log(f"  {video_file.name} 异常: {e}")
            self._log(f"  {traceback.format_exc()[:500]}")
            return False

    def run(self):
        if not self.input_files:
            self._log("没有选择输入文件。")
            self.finished.emit(0, 0)
            return

        self.output_dir.mkdir(parents=True, exist_ok=True)
        total = len(self.input_files)

        self._temp_dir = Path(tempfile.mkdtemp(prefix="video_hires_"))

        self._log(f"=== 开始处理 {total} 个视频文件 ===")
        self._log(f"目标格式: {self.sample_rate}kHz / {self.bit_depth}bit FLAC")
        self._log(f"音轨索引: {self.audio_track_index}")
        self._log("")

        completed = 0
        succ = 0
        
        # Process sequentially for now (parallel processing of videos can be complex)
        for i, video_file in enumerate(self.input_files):
            if self._process_one_file(video_file):
                succ += 1
            completed += 1
            self.progress.emit(int(completed / total * 100))

        self._cleanup()
        self._log(f"\n全部完成：成功 {succ} / {total}")
        self.finished.emit(succ, total)

    def _cleanup(self):
        if self._temp_dir and self._temp_dir.exists():
            shutil.rmtree(self._temp_dir, ignore_errors=True)
            self._temp_dir = None

class DroppableListWidget(QListWidget):
    """支持拖拽文件/文件夹的列表控件"""

    def __init__(self, on_files_dropped, parent=None):
        super().__init__(parent)
        self._on_files_dropped = on_files_dropped
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if not event.mimeData().hasUrls():
            event.ignore()
            return
        paths = []
        for url in event.mimeData().urls():
            local = url.toLocalFile()
            if local:
                paths.append(local)
        event.acceptProposedAction()
        if paths:
            self._on_files_dropped(paths)

# -------------------------
# GUI
# -------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("视频音频Hi-Res处理工具")
        self.resize(950, 850)

        cfg = load_config()
        self.user_ffmpeg = cfg.get('ffmpeg_path', '') or ''
        self.user_ffprobe = cfg.get('ffprobe_path', '') or ''
        self.sample_rate = cfg.get('sample_rate', 48000)
        self.bit_depth = cfg.get('bit_depth', 24)
        self.audio_track_index = cfg.get('audio_track_index', 0)
        self.max_workers = cfg.get('max_workers', 2)

        self.input_files = []
        self.output_dir = str(DEFAULT_OUTPUT_DIR)

        self.init_ui()

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

        # 音频设置
        gb_audio = QGroupBox("音频设置")
        ga = QVBoxLayout()

        h_audio_top = QHBoxLayout()
        h_audio_top.addWidget(QLabel("采样率:"))
        self.sample_rate_combo = QComboBox()
        self.sample_rate_combo.addItems(["44100", "48000", "96000", "192000"])
        self.sample_rate_combo.setCurrentText(str(self.sample_rate))
        h_audio_top.addWidget(self.sample_rate_combo)

        h_audio_top.addSpacing(20)
        h_audio_top.addWidget(QLabel("位深度:"))
        self.bit_depth_combo = QComboBox()
        self.bit_depth_combo.addItems(["16", "24", "32"])
        self.bit_depth_combo.setCurrentText(str(self.bit_depth))
        h_audio_top.addWidget(self.bit_depth_combo)
        
        h_audio_top.addSpacing(20)
        h_audio_top.addWidget(QLabel("音轨索引:"))
        self.track_index_combo = QComboBox()
        self.track_index_combo.addItems(["0", "1", "2", "3", "4"])
        self.track_index_combo.setCurrentText(str(self.audio_track_index))
        h_audio_top.addWidget(self.track_index_combo)
        
        h_audio_top.addStretch()
        ga.addLayout(h_audio_top)

        gb_audio.setLayout(ga)
        v.addWidget(gb_audio)

        # input files
        gb_input = QGroupBox("1) 选择视频文件（支持多选 / 拖拽添加）")
        gli = QVBoxLayout()
        self.drop_hint = QLabel("拖拽视频文件或文件夹到下方列表（文件夹会自动递归搜索），或点击按钮选择")
        gli.addWidget(self.drop_hint)
        self.file_list = DroppableListWidget(self.add_dropped_paths)
        self.file_list.setMinimumHeight(150)
        gli.addWidget(self.file_list)
        h_btns = QHBoxLayout()
        btn_input = QPushButton("选择视频文件")
        btn_input.clicked.connect(self.choose_input_files)
        btn_remove = QPushButton("移除选中")
        btn_remove.clicked.connect(self.remove_selected)
        btn_clear = QPushButton("清空列表")
        btn_clear.clicked.connect(self.clear_files)
        h_btns.addWidget(btn_input)
        h_btns.addWidget(btn_remove)
        h_btns.addWidget(btn_clear)
        h_btns.addStretch()
        gli.addLayout(h_btns)
        gb_input.setLayout(gli)
        v.addWidget(gb_input)

        # output
        gb_out = QGroupBox("2) 输出目录")
        glo = QHBoxLayout()
        btn_out = QPushButton("选择输出目录")
        btn_out.clicked.connect(self.choose_output)
        self.lbl_out = QLabel(self.output_dir)
        glo.addWidget(btn_out); glo.addWidget(self.lbl_out); glo.addStretch()
        gb_out.setLayout(glo)
        v.addWidget(gb_out)

        # start
        hstart = QHBoxLayout()
        self.btn_start = QPushButton("开始处理")
        self.btn_start.clicked.connect(self.start)
        self.progress = QProgressBar()
        self.progress.setValue(0)
        hstart.addWidget(self.btn_start); hstart.addWidget(self.progress)
        v.addLayout(hstart)

        # log
        self.logbox = QTextEdit()
        self.logbox.setReadOnly(True)
        v.addWidget(self.logbox)

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

    def choose_ffprobe(self):
        f, _ = QFileDialog.getOpenFileName(self, "选择 ffprobe 可执行文件", "", "Executables (*.exe);;All files (*)")
        if f:
            self.user_ffprobe = str(Path(f).resolve())
            cfg = load_config()
            cfg['ffprobe_path'] = self.user_ffprobe
            save_config(cfg)
            self.lbl_fp.setText(self.user_ffprobe)
            self.log(f"已指定 ffprobe: {self.user_ffprobe}")

    def choose_input_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择视频文件", "",
            "视频文件 (*.mp4 *.mkv *.avi *.mov *.flv *.wmv *.webm *.m4v *.ts *.mpg *.mpeg);;All files (*)"
        )
        if files:
            self.add_dropped_paths(files)

    def add_dropped_paths(self, paths):
        existing = set(self.input_files)
        added = 0
        skipped = 0
        for raw in paths:
            p = Path(raw)
            if not p.exists():
                continue
            candidates = []
            if p.is_dir():
                candidates = [str(x) for x in p.rglob("*") if x.is_file() and x.suffix.lower() in VIDEO_EXTENSIONS]
                if not candidates:
                    self.log(f"文件夹无视频文件，已跳过：{p}")
                    continue
            else:
                if p.suffix.lower() not in VIDEO_EXTENSIONS:
                    skipped += 1
                    self.log(f"跳过非视频文件：{p.name}")
                    continue
                candidates = [str(p.resolve())]
            for c in candidates:
                if c in existing:
                    continue
                existing.add(c)
                self.input_files.append(c)
                self.file_list.addItem(Path(c).name)
                added += 1
        if added:
            self.log(f"已添加 {added} 个视频文件，当前共 {len(self.input_files)} 个")
        if skipped and not added:
            self.log(f"未添加任何文件，跳过 {skipped} 个非视频文件")

    def remove_selected(self):
        rows = sorted({item.row() for item in self.file_list.selectedItems()}, reverse=True)
        if not rows:
            return
        for row in rows:
            self.file_list.takeItem(row)
            del self.input_files[row]
        self.log(f"已移除 {len(rows)} 个，剩余 {len(self.input_files)} 个")

    def clear_files(self):
        self.input_files = []
        self.file_list.clear()
        self.log("已清空文件列表")

    def choose_output(self):
        d = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if d:
            self.output_dir = str(Path(d).resolve())
            self.lbl_out.setText(self.output_dir)

    def start(self):
        if not self.input_files:
            QMessageBox.warning(self, "提示", "请先选择视频文件")
            return
            
        if not getattr(self, 'output_dir', ''):
            self.output_dir = str(DEFAULT_OUTPUT_DIR)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        self.lbl_out.setText(self.output_dir)

        ffmpeg_bin = self.user_ffmpeg or which_bin('ffmpeg')
        ffprobe_bin = self.user_ffprobe or which_bin('ffprobe')
        if not ffmpeg_bin or not ffprobe_bin:
            QMessageBox.warning(self, "提示", "未找到 ffmpeg/ffprobe。请指定可执行文件或确保已安装并在 PATH 中。")
            return

        # Save settings
        cfg = load_config()
        cfg['sample_rate'] = int(self.sample_rate_combo.currentText())
        cfg['bit_depth'] = int(self.bit_depth_combo.currentText())
        cfg['audio_track_index'] = int(self.track_index_combo.currentText())
        cfg['max_workers'] = self.max_workers
        save_config(cfg)
        
        self.log(f"开始处理 {len(self.input_files)} 个视频文件...")
        self.log(f"目标格式: {self.sample_rate_combo.currentText()}kHz / {self.bit_depth_combo.currentText()}bit FLAC")
        self.log(f"音轨索引: {self.track_index_combo.currentText()}")

        self.btn_start.setEnabled(False)
        self.progress.setValue(0)

        self.worker = Worker(
            self.input_files, 
            self.output_dir, 
            ffmpeg_path=ffmpeg_bin, 
            ffprobe_path=ffprobe_bin, 
            sample_rate=int(self.sample_rate_combo.currentText()),
            bit_depth=int(self.bit_depth_combo.currentText()),
            audio_track_index=int(self.track_index_combo.currentText()),
            max_workers=self.max_workers
        )
        self.worker.log.connect(self.log)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, succ, total):
        self.log(f"\n全部完成：成功 {succ} / {total}")
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

#!/usr/bin/env python3
"""
flac_to_mkv_final.py

GUI tool: single image + folder of .flac -> for each FLAC:
  1) resample/re-encode FLAC -> FLAC @ 48kHz, 24-bit (s32 sample format, ffmpeg produces 24-bit FLAC)
  2) generate a static H.264 video from image with duration == audio duration
  3) mux video + FLAC into .mkv (copy audio, copy video or use copy for video)
  4) set audio track disposition default so players auto-play it

Requirements:
- Python 3.8+
- PyQt5
- ffmpeg & ffprobe (or choose executables manually)
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
    QGroupBox, QCheckBox
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
# Worker
# -------------------------
class Worker(QThread):
    log = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal(int, int)

    def __init__(self, image_path, folder_path, output_dir, ffmpeg_path=None, ffprobe_path=None, fps=24):
        super().__init__()
        self.image_path = Path(image_path).resolve()
        self.folder_path = Path(folder_path).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.ffmpeg = ffmpeg_path or which_bin('ffmpeg') or 'ffmpeg'
        self.ffprobe = ffprobe_path or which_bin('ffprobe') or 'ffprobe'
        self.fps = fps

    def _log(self, s):
        self.log.emit(s)

    def run(self):
        files = sorted(self.folder_path.rglob("*.flac"))
        if not files:
            self._log("未找到 .flac 文件。")
            self.finished.emit(0, 0)
            return

        self.output_dir.mkdir(parents=True, exist_ok=True)
        total = len(files)
        succ = 0

        for idx, flac in enumerate(files, start=1):
            try:
                self._log(f"[{idx}/{total}] 处理：{flac.name}")
                # duration
                try:
                    duration = ffprobe_duration_seconds(flac, ffprobe_bin=self.ffprobe)
                except Exception as e:
                    self._log(f"  无法读取时长，跳过：{e}")
                    continue

                if duration <= 0:
                    self._log("  时长 <=0，跳过")
                    continue

                if not ffprobe_has_audio(flac, ffprobe_bin=self.ffprobe):
                    self._log("  未检测到音频流，跳过")
                    continue

                self._log(f"  时长：{duration:.2f}s")

                # prepare temp files
                with tempfile.TemporaryDirectory() as td:
                    td = Path(td)
                    # resampled FLAC path
                    resampled = td / (flac.stem + "_48k24.flac")
                    # temp video
                    temp_video = td / (flac.stem + "_video.mp4")
                    out_mkv = self.output_dir / (flac.stem + ".mkv")

                    # 1) resample FLAC -> 48k 24-bit FLAC (sample_fmt s32 maps to 24-bit in FFmpeg for FLAC)
                    cmd_resample = [
                        self.ffmpeg, '-y',
                        '-hide_banner', '-loglevel', 'error',
                        '-i', str(flac),
                        '-sample_fmt', 's32',  # s32 used to produce 24-bit FLAC in ffmpeg
                        '-ar', '48000',
                        str(resampled)
                    ]
                    self._log("  正在重采样 FLAC -> 48kHz 24-bit FLAC ...")
                    rc, _, _ = run_quiet(cmd_resample, capture=False)
                    if rc != 0 or not resampled.exists():
                        # capture stderr for diagnosis
                        self._log("  重采样失败，尝试捕获错误信息...")
                        rc2, outb2, errb2 = run_quiet(cmd_resample, capture=True)
                        err = errb2.decode('utf-8', errors='ignore') if errb2 else "(no stderr)"
                        self._log(f"  重采样失败 stderr 摘要:\n{err.strip()[:2000]}")
                        continue
                    self._log("  重采样成功")

                    # 2) generate static video from image with exact duration
                    # Use -t duration to ensure video ends when audio ends.
                    cmd_video = [
                        self.ffmpeg, '-y',
                        '-hide_banner', '-loglevel', 'error',
                        '-loop', '1',
                        '-framerate', str(self.fps),
                        '-i', str(self.image_path),
                        '-c:v', 'libx264',
                        '-preset', 'veryfast',
                        '-tune', 'stillimage',
                        '-pix_fmt', 'yuv420p',
                        '-t', str(duration),
                        str(temp_video)
                    ]
                    self._log("  正在生成静态视频轨（H.264）...")
                    rc, _, _ = run_quiet(cmd_video, capture=False)
                    if rc != 0 or not temp_video.exists():
                        self._log("  生成视频失败，尝试捕获错误信息...")
                        rc2, outb2, errb2 = run_quiet(cmd_video, capture=True)
                        err = errb2.decode('utf-8', errors='ignore') if errb2 else "(no stderr)"
                        self._log(f"  生成视频失败 stderr 摘要:\n{err.strip()[:2000]}")
                        continue
                    self._log("  静态视频生成成功")

                    # 3) mux video + resampled flac into MKV, copy streams, set audio disposition default
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

                    # success
                    self._log(f"  ✓ 已生成：{out_mkv.name}")
                    succ += 1

                # update progress
                self.progress.emit(int(idx / total * 100))

            except Exception as e:
                self._log(f"  处理异常: {e}")

        self.finished.emit(succ, total)

# -------------------------
# GUI
# -------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FLAC -> MKV (no PCM; FLAC->FLAC 48k/24bit)")
        self.resize(900, 640)

        cfg = load_config()
        self.user_ffmpeg = cfg.get('ffmpeg_path', '') or ''
        self.user_ffprobe = cfg.get('ffprobe_path', '') or ''

        self.image_path = ""
        self.folder_path = ""
        self.output_dir = ""

        self.init_ui()

    def init_ui(self):
        w = QWidget()
        self.setCentralWidget(w)
        v = QVBoxLayout(w)

        # ffmpeg choose
        gb_ff = QGroupBox("FFmpeg / FFprobe (optional, saved)")
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
        gb_folder = QGroupBox("2) 选择包含 FLAC 的文件夹（递归）")
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
        self.btn_start = QPushButton("开始批量生成 MKV（FLAC->FLAC 48k/24bit）")
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
        d = QFileDialog.getExistingDirectory(self, "选择包含 FLAC 的文件夹")
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
            QMessageBox.warning(self, "提示", "请先选择包含 FLAC 的文件夹")
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

        # disable start button
        self.btn_start.setEnabled(False)
        self.log("开始批量处理...")

        self.worker = Worker(self.image_path, self.folder_path, self.output_dir, ffmpeg_path=ffmpeg_bin, ffprobe_path=ffprobe_bin, fps=24)
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

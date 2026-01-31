import os
import random
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QGraphicsDropShadowEffect, QHBoxLayout
)
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QPointF
from PyQt5.QtGui import QFont, QPainter, QColor
import pyqtgraph as pg
import subprocess

# ---------------- Worker Thread for Non-blocking Execution ----------------
class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd

    def run(self):
        subprocess.run(self.cmd, shell=True)
        self.finished.emit()

# ---------------- Particle Background ----------------
class ParticleBackground(QWidget):
    def __init__(self, parent=None, num_particles=80):
        super().__init__(parent)
        self.num_particles = num_particles
        self.particles = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)  # ~33 FPS
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

        # Initialize after widget has size
        QTimer.singleShot(0, self.init_particles)

    def init_particles(self):
        w, h = self.width(), self.height()
        if w == 0 or h == 0:
            # fallback: retry in 50ms
            QTimer.singleShot(50, self.init_particles)
            return
        self.particles = [
            {
                "x": random.uniform(0, w),
                "y": random.uniform(0, h),
                "size": random.uniform(4, 12),
                "z": random.uniform(0.5, 1.5),  # depth for pseudo-3D
                "color": QColor(
                    random.randint(50, 255),
                    random.randint(50, 255),
                    random.randint(50, 255),
                    random.randint(40, 120)
                ),
                "speed": random.uniform(0.5, 2),
                "dx": random.uniform(-0.5, 0.5)
            }
            for _ in range(self.num_particles)
        ]

    def animate(self):
        w, h = self.width(), self.height()
        for p in self.particles:
            # Float motion
            p["x"] += p["dx"] * p["z"]
            p["y"] += p["speed"] * p["z"]

            # Wrap around edges
            if p["y"] > h:
                p["y"] = 0
                p["x"] = random.uniform(0, w)
            if p["x"] < 0:
                p["x"] = w
            elif p["x"] > w:
                p["x"] = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        for p in self.particles:
            # Size and opacity scaled by depth for 3D effect
            size = p["size"] * p["z"]
            color = QColor(p["color"])
            color.setAlphaF(min(1.0, p["color"].alphaF() * p["z"]))
            painter.setBrush(color)
            painter.drawEllipse(int(p["x"]), int(p["y"]), int(size), int(size))

# ---------------- Dashboard ----------------
class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TRUESIGHT-AI Dashboard")
        self.setFixedSize(900, 600)

        # Neon dark background with particle widget
        self.background = ParticleBackground(self)
        self.background.setGeometry(0, 0, 900, 600)
        self.background.lower()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # --- Title ---
        title = QLabel("TRUESIGHT-AI Control Panel")
        title.setAlignment(Qt.AlignCenter)
        self.load_fonts()
        title.setFont(QFont("Orbitron", 28, QFont.Bold))
        title.setStyleSheet("color: #1e90ff;")
        main_layout.addWidget(title)

        # --- Confidence Chart ---
        self.conf_plot = pg.PlotWidget(title="Detection Confidence (Last 20)")
        self.conf_plot.setBackground(None)
        self.conf_plot.showGrid(x=True, y=True, alpha=0.3)
        self.conf_plot.setYRange(0, 1)
        self.conf_plot.setLabel('left', 'Confidence')
        self.conf_plot.setLabel('bottom', 'Detections')
        self.conf_curve = self.conf_plot.plot(pen=pg.mkPen(color=(0,255,255), width=3))
        main_layout.addWidget(self.conf_plot)
        self.conf_list = []

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        self.btn_image = self.create_button("Run Image Detection", "#00ffcc", "#00b3a6")
        self.btn_webcam = self.create_button("Run Webcam Detection", "#ff9933", "#ff6600")
        self.btn_exit = self.create_button("Exit", "#ff1a1a", "#cc0000")

        self.btn_image.clicked.connect(lambda: self.run_cmd("python detect.py"))
        self.btn_webcam.clicked.connect(lambda: self.run_cmd("python webcam.py"))
        self.btn_exit.clicked.connect(self.close)

        for btn in [self.btn_image, self.btn_webcam, self.btn_exit]:
            btn_layout.addWidget(btn)

        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        # Timer to simulate updating confidence chart (replace with real detections)
        self.chart_timer = QTimer()
        self.chart_timer.timeout.connect(self.update_chart)
        self.chart_timer.start(1000)  # update every second

    # ---------------- Helpers ----------------
    def load_fonts(self):
        font_dir = os.path.join(os.path.dirname(__file__), "assets/fonts")
        for f in os.listdir(font_dir):
            if f.lower().endswith((".ttf", ".otf")):
                QFontDatabase.addApplicationFont(os.path.join(font_dir, f))

    def create_button(self, text, color_start, color_end):
        btn = QPushButton(text)
        btn.setFont(QFont("Audiowide", 14, QFont.Bold))
        btn.setStyleSheet(f"""
            QPushButton {{
                color: black;
                padding: 12px;
                border-radius: 10px;
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color_start}, stop:1 {color_end}
                );
            }}
            QPushButton:hover {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color_end}, stop:1 {color_start}
                );
            }}
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0,255,255))
        shadow.setOffset(0)
        btn.setGraphicsEffect(shadow)
        return btn

    def run_cmd(self, cmd):
        self.thread = WorkerThread(cmd)
        self.thread.start()

    def update_chart(self):
        # demo simulation: random confidence, replace with real YOLO results
        self.conf_list.append(random.uniform(0.4, 1.0))
        if len(self.conf_list) > 20:
            self.conf_list.pop(0)
        self.conf_curve.setData(self.conf_list)

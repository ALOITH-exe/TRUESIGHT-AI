import sys
import random
import os
from PyQt5.QtGui import QFontDatabase, QFont, QPainter, QColor
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QProgressBar, QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPointF

# ---------------- Particle Background ----------------
class ParticleBackground(QWidget):
    def __init__(self, parent=None, num_particles=60):
        super().__init__(parent)
        self.num_particles = num_particles
        self.particles = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)
        QTimer.singleShot(0, self.init_particles)

    def init_particles(self):
        w, h = self.width(), self.height()
        if w == 0 or h == 0:
            QTimer.singleShot(50, self.init_particles)
            return
        self.particles = [
            {
                "x": random.uniform(0, w),
                "y": random.uniform(0, h),
                "size": random.uniform(6, 14),
                "z": random.uniform(0.5, 1.5),
                "color": QColor(
                    random.randint(100, 255),
                    random.randint(100, 255),
                    random.randint(100, 255),
                    random.randint(100, 200)
                ),
                "speed": random.uniform(0.5, 2),
                "dx": random.uniform(-0.3, 0.3)
            }
            for _ in range(self.num_particles)
        ]

    def animate(self):
        w, h = self.width(), self.height()
        for p in self.particles:
            p["x"] += p["dx"] * p["z"]
            p["y"] += p["speed"] * p["z"]
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
            size = p["size"] * (0.8 + p["z"])
            color = QColor(p["color"])
            color.setAlphaF(min(1.0, p["color"].alphaF() * p["z"]))
            painter.setBrush(color)
            painter.drawEllipse(int(p["x"]), int(p["y"]), int(size), int(size))


# ---------------- Loading Screen ----------------
class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TRUESIGHT-AI")
        self.setFixedSize(900, 600)
        self.setStyleSheet("background-color:#f5f5f5;")  # light theme

        # ---------------- Background ----------------
        self.bg = ParticleBackground(self)
        self.bg.setGeometry(0, 0, 900, 600)
        self.bg.lower()

        # ---------------- Layout ----------------
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)


        # --- Load fonts ---
        font_dir = os.path.join(os.path.dirname(__file__), "assets/fonts")
        for f in os.listdir(font_dir):
            if f.lower().endswith((".ttf", ".otf")):
                QFontDatabase.addApplicationFont(os.path.join(font_dir, f))
                
        # --- Title ---
        self.title = QLabel("TRUESIGHT-AI")
        self.title.setAlignment(Qt.AlignCenter)
        font_path = "./assets/fonts/Orbitron-Bold.otf"
        QFontDatabase.addApplicationFont(font_path)
        self.title.setFont(QFont("Orbitron", 36, QFont.Bold))
        self.title.setStyleSheet("color: #1e90ff; background: transparent;")
        layout.addWidget(self.title)

        # --- Status Label ---
        self.status = QLabel("Initializing...")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setFont(QFont("Orbitron", 18))
        colors = ["#00ffff", "#ff69b4", "#39ff14", "#ff9900"]
        self.status.setStyleSheet(f"color: {random.choice(colors)}; background: transparent;")

        layout.addWidget(self.status)

        # --- Progress Bar ---
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(24)  # make height consistent
        self.progress.setFixedWidth(800) 
        # Base progress bar style
        self.progress.setStyleSheet("""
QProgressBar {
    background-color: #111;      
    border: 0px solid #111;
    border-radius: 12px;          /* round edges */
    text-align: center;
}

QProgressBar::chunk {
    border-radius: 12px;          /* round fill edges */
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #00ffcc,
        stop:0.25 #33ff99,
        stop:0.5 #ff33ff,
        stop:0.75 #ff9933,
        stop:1 #00ccff
    );
    margin: 0px;                  /* removes blocky effect */
}
""")
        layout.addWidget(self.progress)

        self.setLayout(layout)

        # ---------------- Opacity Animation ----------------
        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(1000)
        self.opacity_anim.setStartValue(0)
        self.opacity_anim.setEndValue(1)
        self.opacity_anim.start()

        # ---------------- Progress Timer ----------------
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_progress)
        self.timer.start(50)
        self.value = 0

        self.messages = [
            "Initializing Instance...",
            "Loading Modules...",
            "Starting Vision Engine...",
            "Setting Up Dashboard...",
            "Almost Ready..."
        ]
        self.msg_index = 0

    def load_progress(self):
        self.value += 1
        self.progress.setValue(self.value)

        # Update status message every 15 units
        if self.value % 15 == 0:
            self.status.setText(self.messages[self.msg_index])
            self.msg_index = (self.msg_index + 1) % len(self.messages)

        if self.value >= 100:
            self.timer.stop()
            from dashboard import Dashboard
            self.dashboard = Dashboard()
            self.dashboard.show()
            self.close()

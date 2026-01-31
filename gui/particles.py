from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QWidget
import random

# ---------------- Particle Widget ----------------
class ParticleWidget(QWidget):
    def __init__(self, parent=None, num_particles=60):
        super().__init__(parent)
        self.num_particles = num_particles
        self.particles = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(100)  # slower refresh = slower particle motion
        self.init_particles()

    def init_particles(self):
        self.particles = [{
            "pos": QPointF(random.randint(0, self.width()), random.randint(0, self.height())),
            "size": random.randint(4, 10),
            "color": QColor(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255), 90)
        } for _ in range(self.num_particles)]

    def animate(self):
        for p in self.particles:
            p["pos"].setY(p["pos"].y() + random.uniform(0.2, 1.0))  # slower
            if p["pos"].y() > self.height():
                p["pos"].setY(0)
                p["pos"].setX(random.randint(0, self.width()))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        for p in self.particles:
            painter.setBrush(p["color"])
            painter.drawEllipse(p["pos"], p["size"], p["size"])

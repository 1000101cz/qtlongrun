import math
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtWidgets import QWidget


class LoadingSpinner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_spinner)
        self.timer.start(7)
        self._dot_radius = 4
        self._num_dots = 12

    def rotate_spinner(self):
        self.angle = (self.angle + 2) % 360
        self.update()

    def resizeEvent(self, event):
        """Update internal parameters when the widget is resized."""
        self._dot_radius = min(self.width(), self.height()) / 15  # Adjust dot size relative to widget size
        self.update()  # Trigger a repaint when resizing
        super().resizeEvent(event)

    def paintEvent(self, event):
        """Draw the spinning dots."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center = self.rect().center()
        radius = min(self.width(), self.height()) / 3  # Adjust radius relative to the widget size

        for i in range(self._num_dots):
            radius_const = (i) / self._num_dots

            color = QColor(0, 0, 0)
            color.setAlphaF((i + 1) / self._num_dots)
            painter.setBrush(QBrush(color))

            # Calculate the position of each dot
            angle_rad = math.radians(self.angle + (360 / self._num_dots) * i)
            x = int(center.x() + radius * math.cos(angle_rad))
            y = int(center.y() + radius * math.sin(angle_rad))
            painter.drawEllipse(QPoint(x, y), radius_const * self._dot_radius, radius_const * self._dot_radius)

        painter.end()
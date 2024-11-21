import math
from typing import Optional
from PyQt5.QtCore import QTimer, QPoint, Qt
from PyQt5.QtGui import QPainter, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QWidget

from ._settings import qtlongrun_settings
from ._settings.settings import SpinnerStyle

USE_DEF = '_*/USE_DEFAULT/_*'


def blend_colors(color1: QColor, color2: QColor, weight: float = 0.5) -> QColor:
    """
    Blend two QColors into one color by adjusting the weight between them

    :param color1:      first color
    :param color2:      second color
    :param weight:      blending weight

    :return:            blended color
    """
    # Clamp weight between 0 and 1
    weight = max(0, min(1, weight))

    # Extract RGB components
    r1, g1, b1, a1 = color1.red(), color1.green(), color1.blue(), color1.alpha()
    r2, g2, b2, a2 = color2.red(), color2.green(), color2.blue(), color2.alpha()

    # Compute blended color
    r_blend = int(r1 * (1 - weight) + r2 * weight)
    g_blend = int(g1 * (1 - weight) + g2 * weight)
    b_blend = int(b1 * (1 - weight) + b2 * weight)
    a_blend = int(a1 * (1 - weight) + a2 * weight)

    # Return blended QColor
    return QColor(r_blend, g_blend, b_blend, a_blend)


class LoadingSpinner(QWidget):
    """ Animated dot-spinning animation used for Loading window by loruf decorator """
    def __init__(self, parent: Optional[QWidget] = USE_DEF, style: SpinnerStyle = USE_DEF):
        """
        :param parent:      PyQt object to be used as LoadingSpinner parent
        :param style:       graphic style settings for LoadingSpinner
        """
        parent = parent if (parent != USE_DEF) else qtlongrun_settings.default.parent
        style = style if (style != USE_DEF) else qtlongrun_settings.default.spinner_style

        super().__init__(parent)
        self._style = style
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_spinner)
        self.timer.start(style.speed)
        self._dot_radius = style.dot_radius
        self._num_dots = style.n_dots
        self.fill_image = None
        if self._style.fill_image is not None:
            self.fill_image = QPixmap(str(self._style.fill_image))
            self._resize_image()

    def rotate_spinner(self):
        self.angle = (self.angle + self._style.angle_inc) % 360
        self.update()

    def _resize_image(self):
        """Resize the original image to fit within the dot size."""
        if self.fill_image is None:
            return

        self.fill_image = self.fill_image.scaled(
            self.width(), self.height(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        )

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
            radius_const = i / self._num_dots

            angle_rad = math.radians(self.angle + (360 / self._num_dots) * i)
            x = int(center.x() + radius * math.cos(angle_rad))
            y = int(center.y() + radius * math.sin(angle_rad))

            if self._style.style in [SpinnerStyle.plain_fade, SpinnerStyle.plain, SpinnerStyle.plain_transition]:
                color = self._style.prim_color
                if self._style.style == SpinnerStyle.plain_fade:
                    color.setAlphaF((i + 1) / self._num_dots)
                elif self._style.style == SpinnerStyle.plain_transition:
                    color = blend_colors(color1=color, color2=self._style.sec_color,
                                         weight=((i + 1) / self._num_dots) * self._style.transition_weight)
                painter.setBrush(QBrush(color))
            elif self._style.style == SpinnerStyle.image:
                assert self.fill_image is not None, "fill_image is not defined"
                brush = QBrush(self.fill_image)
                painter.setBrush(brush)
            painter.drawEllipse(QPoint(x, y), radius_const * self._dot_radius, radius_const * self._dot_radius)

        painter.end()

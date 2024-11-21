from PyQt5.QtGui import QColor as _QColor
from PyQt5.QtCore import Qt as _Qt
import pathlib as pl

from .settings import QtLongRunSettings, SpinnerStyle


_spinner_style = SpinnerStyle(style=SpinnerStyle.plain_transition,
                              primary=_QColor(255, 0, 0),
                              secondary=_QColor(0, 255, 0),
                              transition_weight=0.55,
                              fill_image=pl.Path(__file__).parent.parent / '_data' / 'banner2.png',
                              speed=7,
                              n_dots=12,
                              dot_radius=4,
                              angle_inc=2
                              )

_window_sheet = """
    QDialog {
        border: 2px solid #2c3e50;
    }
"""

_window_flags = ~_Qt.WindowContextHelpButtonHint & _Qt.FramelessWindowHint | _Qt.Dialog

qtlongrun_settings = QtLongRunSettings(on_finish=None,
                                       on_fail=None,
                                       window=True,
                                       parent=None,
                                       window_title='Long Running Task',
                                       enable_kill=True,
                                       window_description='Task is running',
                                       window_sheet=_window_sheet,
                                       window_flags=_window_flags,
                                       spinner_style=_spinner_style
                                       )
""" Settings of default values for loruf decorator and LoadingSpinner style """

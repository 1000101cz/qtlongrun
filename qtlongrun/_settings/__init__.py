from PyQt5.QtGui import QColor

from .settings import QtLongRunSettings, SpinnerStyle


_spinner_style = SpinnerStyle(style=SpinnerStyle.image,
                              primary=QColor(255, 0, 0),
                              secondary=QColor(0, 255, 0),
                              transition_weight=0.55,
                              fill_image=None,
                              speed=7,
                              n_dots=12,
                              dot_radius=4,
                              angle_inc=2
                              )

qtlongrun_settings = QtLongRunSettings(on_finish=None,
                                       on_fail=None,
                                       window=True,
                                       parent=None,
                                       window_title='Long Running Task',
                                       enable_kill=True,
                                       window_description='Task is running',
                                       spinner_style=_spinner_style
                                       )
import pathlib as pl
from typing import Optional, Callable
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt


class SpinnerStyle:
    """ Settings of LoadingSpinner visuals """

    plain = 'plain'
    plain_fade = 'plain_fade'
    plain_transition = 'plain_transition'
    image = 'fill_image'

    def __init__(self,
                 style: str,
                 primary: QColor,
                 secondary: QColor,
                 transition_weight: float,
                 fill_image: Optional[pl.Path | str],
                 speed: int,
                 n_dots: int,
                 dot_radius: int,
                 angle_inc: int):
        """

        :param style:               color fill style (plain/plain_fade/plain_transition/image)
        :param primary:             primary color (used for plain/plain_fade/plain_transition)
        :param secondary:           secondary color (used for plain_transition)
        :param transition_weight:   transition wight between primary and secondary color
        :param fill_image:          path to image used for image style color fill
        :param speed:               time for one animation frame (ms)
        :param n_dots:              number of dots in animation
        :param dot_radius:          radius between dots
        :param angle_inc:           angle increment (rotation) for each frame
        """
        self.style = style
        self.prim_color = primary
        self.sec_color = secondary
        self.transition_weight = transition_weight
        self.fill_image = fill_image
        self.speed = speed
        self.n_dots = n_dots
        self.dot_radius = dot_radius
        self.angle_inc = angle_inc


class _DefParams:
    def __init__(self,
                 on_finish: Optional[Callable],
                 on_fail: Optional[Callable],
                 window: bool,
                 parent: Optional[QWidget],
                 window_title: str,
                 enable_kill: bool,
                 window_description: Optional[str],
                 window_sheet: str,
                 window_flags: Qt.WindowFlags,
                 spinner_style: SpinnerStyle):
        self.on_finish = on_finish
        self.on_fail = on_fail
        self.window = window
        self.parent = parent
        self.window_title = window_title
        self.enable_kill = enable_kill
        self.window_description = window_description
        self.window_sheet = window_sheet
        self.window_flags = window_flags
        self.spinner_style = spinner_style


class QtLongRunSettings:
    """ Global settings for whole qtlongrun package """

    def __init__(self,
                 on_finish: Optional[Callable],
                 on_fail: Optional[Callable],
                 window: bool,
                 parent: Optional[QWidget],
                 window_title: str,
                 enable_kill: bool,
                 window_description: Optional[str],
                 window_sheet: str,
                 window_flags: Qt.WindowFlags,
                 spinner_style: SpinnerStyle
                 ):

        self.default = _DefParams(on_finish=on_finish,
                                  on_fail=on_fail,
                                  window=window,
                                  parent=parent,
                                  window_title=window_title,
                                  enable_kill=enable_kill,
                                  window_description=window_description,
                                  window_sheet=window_sheet,
                                  window_flags=window_flags,
                                  spinner_style=spinner_style)
        """ Default values used throughout the package """

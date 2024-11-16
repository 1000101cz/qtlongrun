from typing import Optional, Callable
from PyQt5.QtWidgets import QWidget


class _DefParams:
    def __init__(self,
                 on_finish: Optional[Callable],
                 on_fail: Optional[Callable],
                 window: bool,
                 parent: Optional[QWidget],
                 window_title: str,
                 enable_kill: bool,
                 window_description: Optional[str]):
        self.on_finish = on_finish
        self.on_fail = on_fail
        self.window = window
        self.parent = parent
        self.window_title = window_title
        self.enable_kill = enable_kill
        self.window_description = window_description



class QtLongRunSettings:
    def __init__(self,
                 on_finish: Optional[Callable],
                 on_fail: Optional[Callable],
                 window: bool,
                 parent: Optional[QWidget],
                 window_title: str,
                 enable_kill: bool,
                 window_description: Optional[str]
                 ):

        self.default = _DefParams(on_finish=on_finish,
                                  on_fail=on_fail,
                                  window=window,
                                  parent=parent,
                                  window_title=window_title,
                                  enable_kill=enable_kill,
                                  window_description=window_description)

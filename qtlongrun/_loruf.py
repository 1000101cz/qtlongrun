import time
import pathlib as pl
from loguru import logger
from typing import Optional, Callable

from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, QSize, Qt
from PyQt5.QtWidgets import QWidget, QDialog

from ._settings import qtlongrun_settings as qlrs
from ._settings import SpinnerStyle
from ._loading_animation import LoadingSpinner

_ui_path = pl.Path(__file__).parent / '_loruf.ui'
_loruf_dialog = uic.loadUiType(str(_ui_path))[0]

USE_DEF = '_*/USE_DEFAULT/_*'


class _LFRLoadingWindow(QDialog, _loruf_dialog):
    def __init__(self, title, parent=None, on_kill: Optional[Callable] = None, enable_kill: bool = True, description: Optional[str] = None, style=None):
        super().__init__(parent)
        QDialog.__init__(self, parent)
        if style is None:
            style = qlrs.default.spinner_style
        self.spinner = LoadingSpinner(parent=parent, style=style)
        self.setupUi(self)
        self.setWindowTitle(title)
        self._set_spinner()
        if isinstance(description, str):
            self.label_desc.setText(description)
        else:
            self.label_desc.hide()

        if enable_kill:
            if on_kill is not None:
                self.pushButton_kill.clicked.connect(on_kill)
            else:
                logger.warning("enable_kill parameter is turned on, but no on_kill function is provided!")
                self.widget_kill.hide()
        else:
            self.widget_kill.hide()
            if on_kill is not None:
                logger.warning("on_kill function is provided, but enable_kill parameter is turned off!")

        self.setWindowFlags(~Qt.WindowContextHelpButtonHint & Qt.FramelessWindowHint | Qt.Dialog)
        self.setFixedSize(self.sizeHint())

        self.progressBar.hide()

    def closeEvent(self, event):
        # Prevent the dialog from closing when the 'X' button is clicked
        event.ignore()  # This stops the close event from proceeding
        # Optionally, you can show a message or take some other action here

    def _set_spinner(self):
        layout = self.widget_2.layout()
        index = layout.indexOf(self.label)  # Get the index of the QLabel

        # Step 2: Remove the existing QLabel from the layout
        layout.removeWidget(self.label)
        self.label.deleteLater()  # Remove it from memory
        self.label = None
        layout.insertWidget(index, self.spinner)

        self.spinner.setFixedSize(QSize(self.size().width(), 250))

        layout.setStretch(1, 0)

    def update_progress(self, prog: int):
        if self.progressBar.isHidden():
            self.progressBar.show()

        self.progressBar.setValue(prog)

    def change_description(self, desc: str):
        if self.label_desc.isHidden():
            self.label_desc.show()

        self.label_desc.setText(desc)



class WorkerThread(QThread):
    progress = pyqtSignal(int)
    change_description = pyqtSignal(str)
    finished = pyqtSignal()
    failed = pyqtSignal(Exception)

    def __init__(self, fnc, fnc_args=None, fnc_kwargs=None):
        super().__init__()
        self.fnc = fnc
        self.fnc_args = fnc_args
        self.fnc_kwargs = fnc_kwargs

    # Overriding the run method of QThread
    def run(self) -> None:
        try:
            self.fnc(*self.fnc_args, **self.fnc_kwargs, prog_sig=self.progress, change_desc=self.change_description)
        except Exception as e:
            self.failed.emit(e)
            return
        self.finished.emit()


def loruf(on_finish: Optional[Callable] = USE_DEF,
          on_fail: Optional[Callable] = USE_DEF,
          window: bool = USE_DEF,
          parent: Optional[QWidget] = USE_DEF,
          window_title: str = USE_DEF,
          enable_kill: bool = USE_DEF,
          window_description: Optional[str] = USE_DEF,
          spinner_style: Optional[SpinnerStyle] = USE_DEF):
    """
    LOng-RUnning Function decorator

    Decorated function can accept any args or kwargs, but must also accept 'prog_sig' and 'change_desc' parameters.

    prog_sig - is pyqtSignal for emitting the long-running task progress (accepts int values 0-100)
    change_desc - is pyqtSignal for changing the loading window description label (accepts str)


    :param on_finish:           function to be called after task finishes successfully (returns no arguments)
    :param on_fail:             function to be called after tasks fails or is terminated by user (returns exception)
    :param window:              whether to show loading window or not
    :param parent:              PyQt parent widget
    :param window_title:        title of loading window
    :param enable_kill:         whether to allow user to terminate the task
    :param window_description:  initial description showed in the loading window
    :param spinner_style:       graphic style to be used for LoadingSpinner
    :return:
    """

    on_finish = on_finish if (on_finish != USE_DEF) else qlrs.default.on_finish
    on_fail = on_fail if (on_fail != USE_DEF) else qlrs.default.on_fail
    window = window if (window != USE_DEF) else qlrs.default.window
    parent = parent if (parent != USE_DEF) else qlrs.default.parent
    window_title = window_title if (window_title != USE_DEF) else qlrs.default.window_title
    enable_kill = enable_kill if (enable_kill != USE_DEF) else qlrs.default.enable_kill
    window_description = window_description if (window_description != USE_DEF) else qlrs.default.window_description
    spinner_style = spinner_style if (spinner_style != USE_DEF) else qlrs.default.spinner_style

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            try:
                fnc_args = args
                fnc_kwargs = kwargs
                thread = WorkerThread(func, fnc_args=fnc_args, fnc_kwargs=fnc_kwargs)
                thread.finished.connect(on_finish)  # Connect the signal to a slot
                thread.failed.connect(on_fail)  # Connect the signal to a slot
                if window:
                    def kill_clicked():
                        thread.terminate()
                        thread.wait()
                        thread.failed.emit(RuntimeError("Terminated by user"))
                        return

                    window_dialog = _LFRLoadingWindow(on_kill=kill_clicked, parent=parent, title=window_title, enable_kill=enable_kill, description=window_description, style=spinner_style)

                    thread.finished.connect(window_dialog.accept)
                    thread.failed.connect(window_dialog.accept)
                    thread.progress.connect(window_dialog.update_progress)
                    thread.change_description.connect(window_dialog.change_description)

                thread.start()

                if window:
                    window_dialog.exec_()
            except Exception as e:
                logger.exception(e)
        return wrapper
    return decorator

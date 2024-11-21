from time import sleep
import pathlib as pl

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from loguru import logger
import ctypes

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from qtlongrun import loruf, qtlongrun_settings, LoadingSpinner, SpinnerStyle

myappid = '1000101cz.1000101cz.QTLONGRUNEXAMPLE'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        window_path = pl.Path(__file__).parent / 'data' / 'window.ui'
        uic.loadUi(window_path, self)
        icon = QIcon(str(pl.Path(__file__).parent / 'data' / 'logo.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('Example PyQt Application')

        self.show()

        self.pushButton.clicked.connect(self.button_clicked)
        self.pushButton_en_dis_kill.clicked.connect(self._en_dis_kill)

    def button_clicked(self):
        self._set_default_settings()

        logger.info("start button clicked")

        def on_finish(obj=None):
            logger.success("Long running task finished")

        def on_failure(ex: Exception):
            logger.warning("Long running task failed!")
            logger.debug(ex)

        @loruf(on_finish=on_finish, on_fail=on_failure, parent=self)
        def task(arg1, arg2, arg3, prog_sig: pyqtSignal, change_desc: pyqtSignal):
            loop_lengths = (5, 5, 5)

            change_desc.emit("Executing for loop 1")
            for i in range(loop_lengths[0]):
                sleep(0.5)
                progress = int(100 * ((i + 1) / sum(loop_lengths)))
                prog_sig.emit(progress)
                logger.debug(f"Loop 1 | arg1: {arg1} | Iteration: {i + 1}")

            change_desc.emit("Executing for loop 2")
            for i in range(loop_lengths[1]):
                sleep(1)
                progress = int(100 * ((i + 1 + loop_lengths[0]) / sum(loop_lengths)))
                prog_sig.emit(progress)
                logger.debug(f"Loop 2 | arg1: {arg2} | Iteration: {i + 1}")

            change_desc.emit("Executing for loop 3")
            for i in range(loop_lengths[1]):
                sleep(1.5)
                progress = int(100 * ((i + 1 + loop_lengths[0] + loop_lengths[1]) / sum(loop_lengths)))
                prog_sig.emit(progress)
                logger.debug(f"Loop 3 | arg1: {arg3} | Iteration: {i + 1}")

        task('First argument', arg3='Argument 3', arg2='2. argument')

    @staticmethod
    def _set_default_settings():
        qtlongrun_settings.default.spinner_style.n_dots = 7
        qtlongrun_settings.default.spinner_style.dot_radius = 14
        qtlongrun_settings.default.spinner_style.style = SpinnerStyle.image

    @staticmethod
    def _en_dis_kill():
        qtlongrun_settings.default.enable_kill = not qtlongrun_settings.default.enable_kill
        logger.info(f"'enable_kill' set to {qtlongrun_settings.default.enable_kill}")


if __name__ == '__main__':
    app = QApplication([])
    main = Main()
    app.exec_()

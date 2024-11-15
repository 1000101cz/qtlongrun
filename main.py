from time import sleep
import pathlib as pl

from PyQt5.QtCore import pyqtSignal
from loguru import logger

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from qtlongrun import loruf, qtlongrun_settings

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        window_path = pl.Path(__file__).parent / 'data' / 'window.ui'
        uic.loadUi(window_path, self)

        self.show()

        self.pushButton.clicked.connect(self.button_clicked)
        self.pushButton_en_dis_kill.clicked.connect(self._en_dis_kill)

    def button_clicked(self):
        logger.info("start button clicked")

        def on_finish():
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
    def _en_dis_kill():
        qtlongrun_settings.default.enable_kill = not qtlongrun_settings.default.enable_kill
        logger.info(f"Kill set to {qtlongrun_settings.default.enable_kill}")


if __name__ == '__main__':
    app = QApplication([])
    main = Main()
    app.exec_()

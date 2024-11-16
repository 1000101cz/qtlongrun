from .settings import QtLongRunSettings


qtlongrun_settings = QtLongRunSettings(on_finish=None,
                                       on_fail=None,
                                       window=True,
                                       parent=None,
                                       window_title='Long Running Task',
                                       enable_kill=True,
                                       window_description='Task is running'
                                       )
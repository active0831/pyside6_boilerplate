
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from lib.core.state.functions import bind_state
from ._main import State

class StatusBar(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)
        bind_state([State, "status", 0], self.showMessage)
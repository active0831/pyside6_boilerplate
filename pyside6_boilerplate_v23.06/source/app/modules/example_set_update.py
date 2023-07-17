import time, shutil, os, random, socket, subprocess, uuid

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from functools import partial

from lib.widget import AbstractWidget
from lib.state import AbstractState
from lib.task import Tasks, AbstractTask
from modules._main_state import MainState

from components.basic import TextComponent, LineEditComponent, ButtonComponent


class State(AbstractState):
    def __init__(self):
        super().__init__()
        self.use("max_value",[100])
        self.use("value",[0])

class ToolBar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.addAction("update_status")
        self.addAction("update_widget")
        self.actionTriggered.connect(self.set_some_task)

    def set_some_task(self, action):
        start_update(action.text())

class CenteralWidget(AbstractWidget):
    def render(self, widget):
        TextComponent(id="text", label="Text", layout=widget.layout(),
            model=[State, "value", 0])

class RightWidget(AbstractWidget):
    def render(self, widget):
        LineEditComponent(id="max_value", label="Max Value", layout=widget.layout(),
            onChange=partial(State().setPartial, "max_value", 0),
            model=[State, "max_value", 0])
        ButtonComponent(id="button", label="Update Status", layout=widget.layout(),
            onClick=partial(start_update,"update_status"))
        ButtonComponent(id="button", label="Update Widget", layout=widget.layout(),
            onClick=partial(start_update,"update_widget"))

def start_update(task_name):
    if task_name == "update_status":
        Tasks().set(task_name, UpdateText(State().get("max_value")[0]), 
            func_update=partial(MainState().setPartial, "status", 0),
            func_return=partial(MainState().setPartial, "status", 0))
    elif task_name == "update_widget":
        Tasks().set(task_name, UpdateText(State().get("max_value")[0]), 
            func_update=partial(State().setPartial, "value", 0),
            func_return=partial(State().setPartial, "value", 0))

class UpdateText(AbstractTask):
    def run(self):
        max_value = int(self.args[0])
        for i in range(max_value):

            time.sleep(0.01)

            self.update_value = str(i)
        self.return_value = "finished"
        return None

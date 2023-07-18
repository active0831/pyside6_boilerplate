import time, shutil, os, random, socket, subprocess, uuid
from functools import partial

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from lib.widget import AbstractWidget
from lib.core.state import AbstractState
from lib.core.task import Tasks, AbstractTask
from lib.component import TextComponent, LineEditComponent, TextEditComponent, ButtonComponent
from lib.core.state.functions import bind_state
from modules._main_state import MainState

class State(AbstractState):
    def __init__(self):
        super().__init__()
        self.use("centeral_widget_index",[0])
        self.use("widget_data",["data_1","data_2"])
        self.use("max_value",[100])
        self.use("value",[0])

        
class ToolBar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.addAction("A")
        self.addAction("B")
        self.actionTriggered.connect(self.do_action)

    def do_action(self, action):
        print(action.text(), "is triggered")


class CentralWidget_1(AbstractWidget):
    def render(self, widget):
        TextComponent(id="widget_1_text", label="Widget 1 Text", layout=widget.layout(),
            model=[State, "widget_data",0])

class CentralWidget_2(AbstractWidget):
    def render(self, widget):
        TextEditComponent(id="widget_2_text", label="Widget 2 Text", layout=widget.layout(),
            onChange=partial(State().setPartial, "widget_data", 1),
            model=[State, "widget_data",1])


class CenteralWidget(QDockWidget):
    def __init__(self):
        super().__init__()
        self.widgets = [CentralWidget_1(),CentralWidget_2()]
        self.setWidget(self.widgets[0])
        bind_state([State, "centeral_widget_index",0], self.changeWidget)

    def changeWidget(self, index):
        self.setWidget(self.widgets[index])


class RightWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(RightWidget_1(),"Tab 1")
        self.addTab(RightWidget_2(),"Tab 2")
        self.currentChanged.connect(self.setCurrentTab)
    
    def setCurrentTab(self):
        index = self.currentIndex()
        State().setPartial("centeral_widget_index",0,index)

class RightWidget_1(AbstractWidget):
    def render(self, widget):
        LineEditComponent(id="widget_1_control", label="Widget 1 Control", layout=widget.layout(),
            onChange=partial(State().setPartial, "widget_data", 0),
            model=[State, "widget_data",0])

class RightWidget_2(AbstractWidget):
    def render(self, widget):
        TextComponent(id="widget_2_control", label="Widget 2 Control", layout=widget.layout(),
            model=[State, "widget_data",1])


class LeftWidget(AbstractWidget):
    def render(self, widget):
        LineEditComponent(id="max_value", label="Max Value", layout=widget.layout(),
            onChange=partial(State().setPartial, "max_value", 0),
            model=[State, "max_value", 0])
        ButtonComponent(id="button", label="Update Status", layout=widget.layout(),
            onClick=partial(start_update,"update_status"))

def start_update(task_name):
    if task_name == "update_status":
        Tasks().set(task_name, UpdateText(State().get("max_value")[0]), 
            func_update=partial(MainState().setPartial, "status", 0),
            func_return=partial(MainState().setPartial, "status", 0))

class UpdateText(AbstractTask):
    def run(self):
        max_value = int(self.args[0])
        for i in range(max_value):

            time.sleep(0.01)

            self.update_value = str(i)
        self.return_value = "finished"
        return None


from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from lib.core.state import AbstractState
from lib.core.state.functions import bind_state

from lib.widget import AbstractWidget
from lib.component import TextComponent
from ._example_module import State, run


class GuiState(AbstractState):
    def __init__(self):
        super().__init__()
        self.use("centeral_widget_index",[0])
        #self.use_QItemModel("structure_table_model",[QAbstractItemModel()])
        #self.use_customModel("space_pars_model",[FormModel(default_data=spacePars())])

class ToolBar(QToolBar):    
    def __init__(self, parent):
        super().__init__(parent)
        self.addAction("Run")
        self.actionTriggered.connect(self.do_action)

    def do_action(self, action):
        if action.text() == "Run":
            run()
        else:
            print(action.text(), "is triggered")


class CentralWidget1(AbstractWidget):
    def render(self, widget):
        TextComponent(id="central_widget_1_text", label="Widget 1", layout=widget.layout(),
            text="This is widget 1")

class CentralWidget2(AbstractWidget):
    def render(self, widget):
        TextComponent(id="central_widget_2_text", label="Widget 2", layout=widget.layout(),
            text="This is widget 2")

class CenteralWidget(QDockWidget):
    def __init__(self):
        super().__init__()
        self.widgets = [CentralWidget1(),CentralWidget2()]
        self.setWidget(self.widgets[0])
        bind_state([GuiState, "centeral_widget_index",0], self.changeWidget)

    def changeWidget(self, index):
        self.setWidget(self.widgets[index])


class RightWidget1(AbstractWidget):
    def render(self, widget):
        TextComponent(id="right_widget_1_text", label="Widget 1", layout=widget.layout(),
            text="This is right widget 1")

class RightWidget2(AbstractWidget):
    def render(self, widget):
        TextComponent(id="right_widget_2_text", label="Widget 2", layout=widget.layout(),
            text="This is right widget 2")

class RightWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(RightWidget1(),"1")
        self.addTab(RightWidget2(),"2")
        self.currentChanged.connect(self.setCurrentTab)
    
    def setCurrentTab(self):
        index = self.currentIndex()
        GuiState().setPartial("centeral_widget_index",0,index)

    

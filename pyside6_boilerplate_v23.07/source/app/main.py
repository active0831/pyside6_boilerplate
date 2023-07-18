from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from modules._main_state import MainState
import modules.example.example_module as exm
from lib.core.task import Tasks
from lib.core.state.functions import bind_state

class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        file_menu = QMenu("File", parent)
        file_menu.addAction("file_action_test")
        self.addMenu(file_menu)
        self.triggered.connect(lambda action: self.actionTriggered(action))
    
    
class MainWindow(QMainWindow):
    def __init__(self):    
        super().__init__()

        #Widget 등록        
        self.setMenuBar(MenuBar(self))

        self.addToolBar(exm.ToolBar(self))
        self.setCentralWidget(exm.CenteralWidget())
        self.setSideWidget("Tabs",exm.RightWidget(), Qt.RightDockWidgetArea)
        self.setSideWidget("Text Update",exm.LeftWidget(), Qt.LeftDockWidgetArea)        
        #self.setSideWidget("Bottom",QWidget(), Qt.BottomDockWidgetArea)

        self.setStatusBar(StatusBar(self))
        
        #메인 윈도우 환경 설정
        self.setWindowTitle("PySide Boilerplate Example")
        self.resize(1280,720)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

    def setSideWidget(self, title, widget, area):
        dockwidget = QDockWidget(title, self)
        dockwidget.setWidget(widget)
        self.addDockWidget(area, dockwidget)


class StatusBar(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)
        bind_state([MainState, "status", 0], self.showMessage)


if __name__=="__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.setStyle('Fusion')
    app.exec()
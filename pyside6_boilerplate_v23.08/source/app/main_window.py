import io, time

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

import lib.addon.auth as auth

from modules.main import show_status
from modules.main.gui import StatusBar
import modules.example_module as example_module

class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        file_menu = QMenu("File", parent)
        file_menu.addAction("file_action_test")
        self.addMenu(file_menu)

        module_menu = QMenu("Modules", parent)
        module_menu.addAction("example_module")
        self.addMenu(module_menu)
        
        login_menu = QMenu("Cloud", parent)
        login_menu.addAction("Login")
        login_menu.addAction("Login Info")
        self.addMenu(login_menu)
        
        self.triggered.connect(lambda action: self.actionTriggered(action))

    def actionTriggered(self, action):
        print(action.text())
        if action.text() == "example_module":
            self.parent().loadModule(example_module)
        if action.text() == "Login":
            auth.gui.LoginDialog(self.parent())
        if action.text() == "Login Info":
            auth.gui.LoginInfoDialog(self.parent())


class MainWindow(QMainWindow):
    def __init__(self):    
        super().__init__()

        #메인 윈도우 환경 설정
        self.setWindowTitle("PySide Boilerplate Example")
        self.resize(1280,720)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

        #기본 위젯
        self.setMenuBar(MenuBar(self))
        self.setStatusBar(StatusBar(self))

        #모듈 위젯
        self.toolbar = QToolBar()
        self.central_widget = QWidget()
        self.left_dockWidget = QDockWidget()
        self.right_dockWidget = QDockWidget()
        self.bottom_dockWidget = QDockWidget()

        #시작 모듈
        self.module = example_module
        self.loadModule(self.module)


    def setSideWidget(self, title, widget, area):
        dockwidget = QDockWidget(title, self)
        dockwidget.setWidget(widget)
        self.addDockWidget(area, dockwidget)
        return dockwidget

    def loadModule(self, module):
        self.module = module
        self.setCentralWidget(module.gui.CenteralWidget())

        try:
            self.removeToolBar(self.toolbar)
        except AttributeError:
            pass
        try:
            self.removeDockWidget(self.left_dockWidget)
        except AttributeError:
            pass
        try:
            self.removeDockWidget(self.right_dockWidget)
        except AttributeError:
            pass
        try:
            self.removeDockWidget(self.bottom_dockWidget)
        except AttributeError:
            pass

        try:            
            self.toolbar = module.gui.ToolBar(self)
            self.addToolBar(self.toolbar)
        except AttributeError:
            pass
        try:            
            self.left_dockWidget = self.setSideWidget(
                "Settings",module.gui.LeftWidget(), Qt.LeftDockWidgetArea)
        except AttributeError:
            pass
        try:
            self.right_dockWidget = self.setSideWidget(
                "Settings",module.gui.RightWidget(), Qt.RightDockWidgetArea)
        except AttributeError:
            pass
        try:
            self.bottom_dockWidget = self.setSideWidget(
                "Settings",module.gui.BottomWidget(), Qt.BottomDockWidgetArea)
        except AttributeError:
            pass

    def currentModule(self):
        return self.module

if __name__=="__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.setStyle('Fusion')
    app.exec()

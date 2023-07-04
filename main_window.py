import time, joblib, shutil, os, random, socket, subprocess, uuid

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from functools import partial

from lib.state import State, setStateFunc

from components.basic import TextComponent, ButtonComponent

class MainWindow(QMainWindow):
    def __init__(self):    
        super().__init__()

        #본 프로그램에서 Widget과 Component 들이 공유할 데이터 등록
            #State().use("text","3")
            #State().use("status")

        #Widget 등록        
            #self.setMenuBar(MenuBar(self))
            #self.addToolBar(ToolBar(self))
            #self.setCentralWidget(CentralWidget())
            #self.setSideWidget("Left",LeftWidget(), Qt.LeftDockWidgetArea)
            #self.setSideWidget("Right",QWidget(), Qt.RightDockWidgetArea)
            #self.setSideWidget("Bottom",QWidget(), Qt.BottomDockWidgetArea)
            #self.setStatusBar(StatusBar(self))
        
        #메인 윈도우 환경 설정
            #self.setWindowTitle("test")
            #self.resize(500,500)
            #self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
            #self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

    def setSideWidget(self, title, widget, area):
        dockwidget = QDockWidget(title, self)
        dockwidget.setWidget(widget)
        self.addDockWidget(area, dockwidget)


#class MenuBar(QMenuBar):
#    pass

#class ToolBar(QToolBar):
#    pass

#class StatusBar(QStatusBar):
#    pass

#class CentralWidget(QWidget):
#    pass

#class LeftWidget(QWidget):
#    pass


if __name__=="__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.setStyle('Fusion')
    app.exec()
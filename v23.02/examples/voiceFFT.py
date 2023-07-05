import time, joblib, shutil, os, random, socket, subprocess, uuid

import numpy as np
import matplotlib.pyplot as plt
import librosa.core
import librosa.display

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from PIL.ImageQt import ImageQt
from PIL import Image
import io

from functools import partial

from lib.state import State, setStateFunc

from components.basic import *
from components.image import *

class MainWindow(QMainWindow):
    def __init__(self):    
        super().__init__()

        State().use("dataDict",{})
        State().use("imgDict",{})
        State().use("selectedDataFFTgraph",None)

        self.addToolBar(ToolBar(self))
        self.setCentralWidget(CentralWidget())
        self.setSideWidget("Select Data",DataSelectionWidget(), Qt.LeftDockWidgetArea)

        find_data()
        
    def setSideWidget(self, title, widget, area):
        dockwidget = QDockWidget(title, self)
        dockwidget.setWidget(widget)
        self.addDockWidget(area, dockwidget)


class ToolBar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.addAction("Find Data")
        self.actionTriggered.connect(self.find_data)

    def find_data(self, action):
        if action.text() == "Find Data":
            find_data()

class CentralWidget(QWidget):
    def __init__(self):   
        super().__init__()

        #레이아웃 등록
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        #Component 등록
        ImageComponent(id="selected_data_fft_graph", label="FFT Result" ,layout=mainLayout,
            model_id = "selectedDataFFTgraph")

class DataSelectionWidget(QWidget):
    def __init__(self):   
        super().__init__()

        #레이아웃 등록
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        #Component 등록
        ImageListComponent(id="data_image_list", layout=mainLayout,
            itemSelected=self.setSelectedData,
            model_id = "imgDict")
        
    def setSelectedData(self, id):
        data = State().value("dataDict")[id]
        data_fft = np.abs(librosa.core.stft(data,n_fft=2048))[:,:]

        fig = plt.figure()
        plot = fig.add_subplot(111)
        plot.imshow(data_fft, aspect=0.03, vmin=0, cmap="gist_ncar")
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        pil_img = Image.open(img_buf)
    
        State().set("selectedDataFFTgraph",pil_img)
        plt.clf()


def find_data():
    dataDict = {}
    imgDict = {}
    for fname in os.listdir("./data"):
        data = np.loadtxt("./data/"+fname)        
        dataDict[fname] = data

        fig = plt.figure(1,[1,0.5])
        plot = fig.add_subplot(111)
        plot.plot(range(len(data)),data)
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        pil_img = Image.open(img_buf)

        imgDict[fname] = pil_img

    State().set("dataDict",dataDict)
    State().set("imgDict",imgDict)
    plt.clf()


if __name__=="__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.setStyle('Fusion')
    app.exec()
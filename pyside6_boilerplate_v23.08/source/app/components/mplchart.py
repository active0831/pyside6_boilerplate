from functools import partial

#Component 정의
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PIL.ImageQt import ImageQt
from PIL import Image
import io

from lib.core.state.functions import bind_state
from lib.component import render_component

def MplPlotComponent(id, label, layout, model=None):
    widget = FigureCanvasQTAgg(Figure())
    layout.addWidget(widget)
    plot = widget.figure.add_subplot()

    def setPlot(data_list):
        plot.clear()
        data_np = np.array(data_list).T

        for lindata in data_np[1:]:
            plot.plot(data_np[0], lindata)        
        widget.draw()
    
    if model is not None:
        bind_state(model, setPlot)


def MplSVFSViewerComponent(id, label, layout, model=None):
    widget = FigureCanvasQTAgg(Figure())

    def setValue(svfs_np):
        if type(svfs_np).__name__ =="ndarray":
            widget.figure.clf()
            svfs_abs = (svfs_np**2).mean(0)**0.5

            Ni = svfs_abs.shape[0]
            Nj = svfs_abs.shape[1]
            for i in range(Ni):
                for j in range(Nj):
                    widget.figure.add_subplot(Ni,Nj,1+i*Nj+j).imshow(svfs_abs[i,j,:,:])
            widget.draw()   

    render_component(layout, [widget], model, setValue)
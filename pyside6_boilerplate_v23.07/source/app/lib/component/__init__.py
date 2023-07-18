#Component 정의
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from lib.core.state.functions import bind_state


def render_component(layout, items, model=None, setValue=print, vertical_layout=False):

    itemLayout = QVBoxLayout() if vertical_layout else QHBoxLayout()

    widget = QWidget()
    widget.setLayout(itemLayout)    
    layout.addWidget(widget)

    for item in items:
        itemLayout.addWidget(item)
        itemLayout.addWidget(item)

    if model is not None:
        bind_state(model, setValue)


def TextComponent(id, label, layout, model_id=None, model=None, text=None):

    labelItem = QLabel(label)
    textItem = QLabel(text)

    def setValue(value):
        textItem.setText(str(value))

    render_component(layout, [labelItem, textItem], model, setValue)


def LineEditComponent(id, label, layout, onChange=None, model = None, text=None):

    labelItem = QLabel(label)
    textItem = QLineEdit(text)

    def setValue(value):
        textItem.setText(str(value))

    render_component(layout, [labelItem, textItem], model, setValue)

    if onChange is not None:
        textItem.textChanged.connect(onChange)


def TextEditComponent(id, label, layout, onChange=None, model = None, text=None):
    textItem = QTextEdit(text)
    buttonItem = QPushButton("Submit")
    def setValue(value):
        textItem.setText(str(value))

    render_component(layout, [textItem, buttonItem], model, setValue)

    if onChange is not None:
        def exe_onChange():
            onChange(textItem.toPlainText())
        buttonItem.clicked.connect(exe_onChange)



def ButtonComponent(id, label, layout, onClick=None):

    buttonItem = QPushButton(label)

    render_component(layout, [buttonItem])

    if onClick is not None:
        buttonItem.clicked.connect(onClick)


def SliderComponent(id, label, layout, scale=1, min=0, max=100,
        onChange=None, model=None, value=None):

    labelItem = QLabel(label)
    sliderItem = QSlider(Qt.Horizontal)

    def setValue(v):
        if v != None:
            sliderItem.setValue(int(v/scale))

    render_component(layout, [labelItem, sliderItem], model, setValue)

    if onChange is not None:
        sliderItem.valueChanged.connect(lambda v: onChange(v*scale))
    if value is not None:
        setValue(value)


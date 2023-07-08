#Component 정의
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from lib.state import State, setStateFunc

def TextComponent(id, label, layout, model_id=None, text=None):
    itemLayout = QHBoxLayout()
    layout.addLayout(itemLayout)

    labelItem = QLabel(label)
    itemLayout.addWidget(labelItem)
    textItem = QLabel(text)
    itemLayout.addWidget(textItem)

    if model_id is not None:
        State().bind(model_id, id, textItem.setText)


def LineEditComponent(id, label, layout, onChange=None, model_id=None, text=None):
    itemLayout = QHBoxLayout()
    layout.addLayout(itemLayout)

    labelItem = QLabel(label)
    itemLayout.addWidget(labelItem)
    textItem = QLineEdit(text)
    itemLayout.addWidget(textItem)

    if onChange is not None:
        textItem.textChanged.connect(onChange)

    if model_id is not None:
        State().bind(model_id, id, textItem.setText)


def ButtonComponent(id, label, layout, onClick=None):
    buttonItem = QPushButton(label)
    layout.addWidget(buttonItem)
    if onClick is not None:
        buttonItem.clicked.connect(onClick)
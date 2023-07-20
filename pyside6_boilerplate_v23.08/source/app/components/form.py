#Standard library modules
import sys, os, subprocess, socketserver, time, uuid, shutil, json
from functools import partial
from io import BytesIO

#Third-party modules
import numpy as np
import pandas as pd
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from lib.core.state.functions import bind_state

class FormModel():
    def __init__(self,default_data={}):
        self.update_functions = []
        self.data = default_data

    def bind_data(self,update_function):
        self.update_functions.append(update_function)

    def set_data(self,key,value):
        self.data[key]["value"] = value
        for update_function in self.update_functions:
            update_function(self.data)

    def export_data(self):
        data_dict = {}
        for key in self.data.keys():
            data_dict[key] = self.data[key]["value"]
        return data_dict

    def import_data_values(self,data_dict):
        for key in self.data.keys():
            if key in data_dict.keys():
                self.data[key]["value"] = data_dict[key]

class FormView(QWidget):
    def __init__(self,orientation="vertical",parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setAttribute(Qt.WA_DeleteOnClose)
        if orientation == "vertical":
            self.layout = QVBoxLayout()
        else:
            self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.forms = {}

    def setModel(self,model):
        self.model = model
        self.model.bind_data(self.update_data)
        self.update_data(self.model.data)

    def update_data(self,data):
        self.clear_forms()
        for key in data.keys():
            label = data[key]["label"]
            init_value = data[key]["value"]
            properties = data[key]["properties"]

            self.forms[key] = {}
            self.forms[key]["layout"] = QHBoxLayout()
            self.forms[key]["label"] = QLabel(label)
            if "editor_type" in properties.keys():
                editor_type = properties["editor_type"]
            elif "options" in properties.keys():
                editor_type = "QComboBox"
            else:
                editor_type = "QLineEdit"

            if editor_type == "QComboBox":
                self.forms[key]["editor"] = QComboBox()
                for option in properties["options"]:
                    self.forms[key]["editor"].addItem(option)
                    self.forms[key]["editor"].setCurrentText(str(init_value))
                self.forms[key]["editor"].currentTextChanged.connect(
                    partial(self.modify_value,key))
            elif editor_type == "QCheckBox":
                self.forms[key]["editor"] = QCheckBox()
                self.forms[key]["editor"].setChecked(init_value)
                self.forms[key]["editor"].stateChanged.connect(
                    partial(self.modify_value,key))
            else:
                self.forms[key]["editor"] = QLineEdit(str(init_value))
                self.forms[key]["editor"].editingFinished.connect(
                    partial(self.modify_value,key))

            self.layout.addLayout(self.forms[key]["layout"])
            self.forms[key]["layout"].addWidget(self.forms[key]["label"])
            self.forms[key]["layout"].addWidget(self.forms[key]["editor"])

    def clear_forms(self):
        for key in list(self.forms.keys()):
            self.layout.removeWidget(self.forms[key]["label"])
            self.layout.removeWidget(self.forms[key]["editor"])
            self.layout.removeItem(self.forms[key]["layout"])
            del self.forms[key]

    def modify_value(self,key,text=None):
        editor = self.forms[key]["editor"]
        if type(editor).__name__ in ["QCheckBox"]:            
            value = editor.isChecked()
        else:
            if type(editor).__name__ in ["QComboBox"]:
                text = editor.currentText()
            else:
                text = editor.text()
            try:
                value = float(text)
            except ValueError:
                value = text
        self.model.set_data(key,value)


def FormComponent(id, label, layout, model = None):
    widget = FormView()
    layout.addWidget(widget)

    if model is not None:
        module_cls = model[0]
        model_id = model[1]
        data_index = model[2]
        form_model = module_cls().get(model_id)[data_index]
        widget.setModel(form_model)


def FormTextComponent(id, label, layout, model=None, text=None):
    itemLayout = QVBoxLayout()
    widget = QWidget()
    widget.setLayout(itemLayout)
    layout.addWidget(widget)

    labelItem = QLabel(label)
    itemLayout.addWidget(labelItem)
    textItem = QTextEdit(text)
    itemLayout.addWidget(textItem)

    def setValue(value):
        textItem.setText(str(value.export_data()))

    if model is not None:
        bind_state(model, setValue)
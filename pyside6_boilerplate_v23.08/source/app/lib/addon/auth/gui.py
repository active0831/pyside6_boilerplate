from functools import partial

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from lib.component import LineEditComponent
from ._auth import State, login, logout, check_login_user

class LoginDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.resize(300, 200)

        self.id = QLineEdit()
        self.pw = QLineEdit()
        self.pw.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        layout = QFormLayout()
        LineEditComponent(id="auth_host_input", label="Auth Host", layout=layout,
            onChange=partial(State().setPartial,"auth_host",0),
            model=[State, "auth_host", 0])
        layout.addRow("ID", self.id)
        layout.addRow("PW", self.pw)
        layout.addRow("", self.login_button)
        self.setLayout(layout)

        self.exec()

    def login(self):
        id = self.id.text()
        pw = self.pw.text()
        login({"email":id,"password":pw})
        self.close()

class LoginInfoDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Login Info")
        self.resize(300, 200)

        user_info = check_login_user()
        
        self.info = QLabel()
        self.info.setText(str(user_info))      
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)

        layout = QFormLayout()
        layout.addRow("로그인 정보", self.info)
        layout.addRow("", self.logout_button)
        self.setLayout(layout)
        self.exec()

    def logout(self):
        logout()
        self.close()


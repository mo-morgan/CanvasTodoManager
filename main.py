# -*- coding: utf-8 -*-
import sys
from canvasapi import Canvas
from datetime import datetime, timedelta

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *


class Auth:
    def __init__(self, name, token):
        self._name = name
        self._token = token


class MyAssignment:
    def __init__(self, name, dueDate):
        self._name = name
        self._dueDate = dueDate

    def name(self):
        return self._name

    def due_date(self):
        return self._dueDate


class LoginDialog (QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        self.username = QLineEdit()
        self.accessToken = QLineEdit()
        loginLayout = QFormLayout()
        loginLayout.addRow("Name: ", self.username)
        loginLayout.addRow("Access Token: ", self.accessToken)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.check)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(loginLayout)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def check(self):
        if str(self.accessToken.text()) == "123":  # do actual login check
            self.accept()
        else:
            pass  # or inform the user about bad username/password


class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'Canvas TODO Manager'

        self.left = 600
        self.top = 110
        self.width = 420
        self.height = 700
        self.course_dict = {}

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        Auth._name, Auth._token = self.getInfo()
        App.parse(self)

        self.createStyle()
        self.createLayout()

        self.show()

    def createLayout(self):
        layout = QFormLayout()

        # Combobox for course selection
        self.comboBox = QComboBox()
        self.comboBox.addItem("Course 1")
        self.comboBox.addItem("Course 2")

        # checkBox for each assignment
        self.checkBox = QCheckBox('Assignment 1', self)
        self.checkBox.stateChanged.connect(self.clickBox)

        # adding combo and check to layout
        layout.addWidget(self.comboBox)
        layout.addRow(self.checkBox)

        # set style of assignment checkboxes
        self.checkBox.setStyleSheet("margin: 3px; padding: 30%;"
                                    "background-color: rgb(255, 255, 255);"
                                    "color: rgba(0,0,0,1);"
                                    "border-style: solid;"
                                    "border-radius: 3px; "
                                    "border-width: 0.5px;"
                                    "border-color: rgba(255, 204, 153,30);")
        self.comboBox.setStyleSheet("margin: 10px; padding: 16%;"
                                    "background-color: rgb(255, 255, 255);"
                                    "color: rgba(0,0,0,1);"
                                    "border-style: solid;"
                                    "border-radius: 3px; "
                                    "border-width: 0.5px;"
                                    "border-color: rgba(255, 204, 153,30);")
        self.setLayout(layout)

    def createStyle(self):
        self.setStyleSheet("margin: 1px; padding: 7px;"
                           "background-color: rgba(255, 204, 153,0.8);"
                           "color: rgba(0,0,0,100);"
                           "border-style: solid;"
                           "border-radius: 3px; "
                           "border-width: 0.5px;"
                           "border-color: rgba(255, 204, 153,30);")

    def clickBox(self, state):
        print(state)

    def getInfo(self):
        name, okPressed = QInputDialog.getText(self, "User Login", "Your name:", QLineEdit.Normal, "")
        token, okPressed = QInputDialog.getText(self, "Access Token", "Enter access token:", QLineEdit.Normal, "")
        if okPressed and token != '':
            print(token)
        self.setStyleSheet("margin: 1px; padding: 7px;"
                           "background-color: rgba(255, 204, 153,0.8);"
                           "color: rgba(0,0,0,100);"
                           "border-style: solid;"
                           "border-radius: 3px; "
                           "border-width: 0.5px;"
                           "border-color: rgba(255, 204, 153,30);")
        return name, token

    @staticmethod
    def parse(self):
        courses = []
        # Canvas API URL
        API_URL = "https://canvas.ubc.ca"
        # Canvas API key
        API_KEY = Auth._token
        canvas = Canvas(API_URL, API_KEY)

        for course in canvas.get_courses():
            if course.attributes.get("course_code") is not None:
                courses.append(course)

        for course in courses:
            theirAssignments = course.get_assignments()
            print(course)

            myAssignments = []

            # each course has a list of assignments that are sorted by due date
            for theirAssignment in theirAssignments:
                if theirAssignment.due_at is not None:
                    datetime_object = datetime.strptime(theirAssignment.due_at, '%Y-%m-%dT%H:%M:%SZ')
                    if datetime.now() - timedelta(days=1) < datetime_object:
                        a = MyAssignment(theirAssignment.name, datetime_object)
                        myAssignments.append(a)

            # now sort
            allSorted = sorted(myAssignments, key=lambda assignment: assignment._dueDate)
            for assignment in allSorted:
                print(assignment.name())
                print(assignment.due_date())

            self.course_dict[course] = allSorted




if __name__ == '__main__':
    app = QApplication(sys.argv)

    # login = LoginDialog()
    # if not login.exec_():  # user quit
    #     sys.exit(-1)

    main = App()

    # get Name and token
    # main.setName(login.username.text())
    # main.setToken(login.accessToken.text())
    main.show()
    sys.exit(app.exec_())







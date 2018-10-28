# -*- coding: utf-8 -*-
import sys
import os
import dotenv
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
        if str(self.accessToken.text()) == Auth._token:  # do actual login check
            self.accept()
        else:
            pass  # or inform the user about bad username/password


class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'Canvas TODO Manager'

        self.left = 600
        self.top = 80
        self.width = 600
        self.height = 800
        self.course_dict = {}

        self.comboBox = QComboBox()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        Auth._name = self.getInfo()
        App.parse(self)

        self.createStyle()
        self.createLayout()

        self.show()

    def removeCheckBoxes(self):
        for cnt in reversed(range(self.layout.count())):
            # takeAt does both the jobs of itemAt and removeWidget
            # namely it removes an item and returns it
            widget = self.layout.takeAt(cnt).widget()

            if widget is not self.comboBox:
                # widget will be None if the item is a layout
                widget.deleteLater()

    def handleActivated(self, index):
        self.removeCheckBoxes()

        course_name = self.comboBox.itemText(index)
        assignments = self.course_dict[course_name]

        self.layout.addWidget(self.comboBox)

        self.addAssignments(assignments)

        self.setLayout(self.layout)

    def addAssignments(self, assignments):
        for assignment in assignments:
            # checkBox for each assignment
            print(assignment._name)
            self.checkBox = QCheckBox(assignment._name + "      Due: " + assignment._dueDate.strftime("%Y-%m-%d %H:%M:%S"), self)
            self.layout.addRow(self.checkBox)
            self.checkBox.stateChanged.connect(self.clickBox)
            self.checkBox.setStyleSheet("margin: 3px; padding: 30%;"
                                        "background-color: rgb(255, 255, 255);"
                                        "color: rgba(0,0,0,1);"
                                        "border-style: solid;"
                                        "border-radius: 3px; "
                                        "border-width: 0.5px;"
                                        "border-image: url(FFCC99.png);")

    def createLayout(self):
        self.layout = QFormLayout()

        # Combobox for course selection
        i = 0
        for key in self.course_dict:
            self.comboBox.addItem(key, i)
            i = i + 1

        self.comboBox.activated.connect(self.handleActivated)

        # adding combo and check to layout
        self.layout.addWidget(self.comboBox)
        course_name = self.comboBox.itemText(0)
        self.addAssignments(self.course_dict[course_name])

        # set style of assignment checkboxes
        self.comboBox.setStyleSheet("margin: 10px; padding: 16%;"
                                    "background-color: rgb(255, 255, 255);"
                                    "color: rgba(0,0,0,1);"
                                    "border-style: solid;"
                                    "border-radius: 3px; "
                                    "border-width: 0.5px;"
                                    "border-image: url(FFCC99.png);")
        self.setLayout(self.layout)

    def createStyle(self):
        self.setStyleSheet("margin: 1px; padding: 7px;"
                           "background-color: rgba(255, 204, 153,0.8);"
                           "color: rgba(0,0,0,100);"
                           "border-style: solid;"
                           "border-radius: 3px; "
                           "border-width: 0.5px;"
                           "border-image: url(flower.jpg);")

    def clickBox(self, state):
        print(state)

    def getInfo(self):
        name, okPressed = QInputDialog.getText(self, "User Login", "Your name:", QLineEdit.Normal, "")
        # token, okPressed = QInputDialog.getText(self, "Access Token", "Enter access token:", QLineEdit.Normal, "")
        if okPressed != '':
            print(name)
        self.setStyleSheet("margin: 1px; padding: 7px;"
                           "background-color: rgba(255, 204, 153,0.8);"
                           "color: rgba(0,0,0,100);"
                           "border-style: solid;"
                           "border-radius: 3px; "
                           "border-width: 0.5px;"
                           "border-color: rgba(255, 204, 153,30);")
        return name

    def course_dict(self):
        return self.course_dict

    @staticmethod
    def parse(self):
        dotenv.load_dotenv(dotenv.find_dotenv())

        courses = []
        # Canvas API URL
        API_URL = "https://canvas.ubc.ca"
        # Canvas API key
        API_KEY = os.environ.get('TOKEN')
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

            self.course_dict[course.name] = allSorted




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







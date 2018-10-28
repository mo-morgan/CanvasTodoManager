import sys
# from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'Canvas TODO Manager'

        self.left = 600
        self.top = 110
        self.width = 420
        self.height = 700

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        name, token = self.getInfo()
        print(name)
        print(token)

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
                                    "border-image: url(FFCC99.png);")
        self.comboBox.setStyleSheet("margin: 10px; padding: 16%;"
                                    "background-color: rgb(255, 255, 255);"
                                    "color: rgba(0,0,0,1);"
                                    "border-style: solid;"
                                    "border-radius: 3px; "
                                    "border-width: 0.5px;"
                                    "border-image: url(FFCC99.png);")
        self.setLayout(layout)

    def createStyle(self):
<<<<<<< HEAD
        self.setStyleSheet("border-image: url(flower.jpg);"
                           "margin: 1px; padding: 7px;"
=======
        self.setStyleSheet("margin: 1px; padding: 7px;"
                           "background-color: rgba(255, 204, 153,0.8);"
                           "color: rgba(0,0,0,100);"
>>>>>>> e6893384a4de66afd857b509212fee70d470978e
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
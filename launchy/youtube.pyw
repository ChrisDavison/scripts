#!/usr/bin/env python
import sys
import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets

WIDTH, HEIGHT = 150, 60


class Ui_Search(object):
    def setupUi(self, Search):
        Search.setObjectName("Search")
        Search.setFixedSize(WIDTH, HEIGHT)
        Search.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(Search)
        self.centralwidget.setObjectName("centralwidget")
        self.query = QtWidgets.QLineEdit(self.centralwidget)
        self.query.setGeometry(QtCore.QRect(0, 0, WIDTH, 31))
        self.query.setObjectName("query")
        self.buttonGo = QtWidgets.QPushButton(self.centralwidget)
        self.buttonGo.setGeometry(0, 30, WIDTH, 30)
        self.buttonGo.setFixedSize(QtCore.QSize(WIDTH, 30))
        self.buttonGo.setObjectName("search")
        self.buttonGo.setText("Search")
        Search.setCentralWidget(self.centralwidget)

        self.retranslateUi(Search)
        QtCore.QMetaObject.connectSlotsByName(Search)

    def retranslateUi(self, Search):
        _translate = QtCore.QCoreApplication.translate
        Search.setWindowTitle(_translate("Search", "Search"))


class Search(QtWidgets.QMainWindow):
    def __init__(self):
        super(Search, self).__init__()
        self.ui = Ui_Search()
        self.ui.setupUi(self)
        self.ui.buttonGo.clicked.connect(self.search)

    def search(self):
        txt = self.ui.query.text().replace(' ', '+')
        query = f"https://www.youtube.com/results?search_query={txt}"
        webbrowser.open(query)
        app.quit()


app = QtWidgets.QApplication([])
application = Search()
application.show()
sys.exit(app.exec())
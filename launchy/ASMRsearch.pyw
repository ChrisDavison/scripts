#!/usr/bin/env python
import sys
import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets

F_IN = 'E:\\Dropbox\\automation\\asmr.md'

WIDTH, HEIGHT = 300, 90


class Ui_ASMRSearch(object):
    def setupUi(self, ASMRSearch):
        ASMRSearch.setObjectName("ASMRSearch")
        ASMRSearch.setFixedSize(WIDTH, HEIGHT)
        ASMRSearch.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(ASMRSearch)
        self.centralwidget.setObjectName("centralwidget")
        self.query = QtWidgets.QLineEdit(self.centralwidget)
        self.query.setGeometry(QtCore.QRect(0, 0, WIDTH, 31))
        self.query.setObjectName("query")
        self.dropdown = QtWidgets.QComboBox(self.centralwidget)
        self.dropdown.setGeometry(QtCore.QRect(0, 30, WIDTH, 30))
        self.dropdown.setFixedSize(QtCore.QSize(WIDTH, 30))
        self.dropdown.setObjectName("dropdown")
        self.buttonGo = QtWidgets.QPushButton(self.centralwidget)
        self.buttonGo.setGeometry(0, 60, WIDTH/2, 30)
        self.buttonGo.setFixedSize(QtCore.QSize(WIDTH/2, 30))
        self.buttonGo.setObjectName("open")
        self.buttonGo.setText("Open")
        self.buttonSearch = QtWidgets.QPushButton(self.centralwidget)
        self.buttonSearch.setGeometry(WIDTH/2, 60, WIDTH/2, 30)
        self.buttonSearch.setFixedSize(QtCore.QSize(WIDTH/2, 30))
        self.buttonSearch.setObjectName("dosearch")
        self.buttonSearch.setText("Search")
        ASMRSearch.setCentralWidget(self.centralwidget)

        self.retranslateUi(ASMRSearch)
        QtCore.QMetaObject.connectSlotsByName(ASMRSearch)

    def retranslateUi(self, ASMRSearch):
        _translate = QtCore.QCoreApplication.translate
        ASMRSearch.setWindowTitle(_translate("ASMRSearch", "ASMR Search"))


class ASMRSearch(QtWidgets.QMainWindow):
    def __init__(self):
        super(ASMRSearch, self).__init__()
        self.ui = Ui_ASMRSearch()
        self.ui.setupUi(self)
        self.ui.query.textChanged.connect(self.filter)
        self.ui.buttonSearch.clicked.connect(self.search)
        self.ui.buttonGo.clicked.connect(self.open)
        self.filter()
        self.update_dropdown()

    def get_contents(self):
        """Get the contents of the ASMR file"""
        def tidy(line):
            """Tidy a markdown link into (path, url)"""
            stripped = line.strip()
            no_lead = stripped.strip('- [')
            no_tail = no_lead.strip(')')
            return no_tail.split('](')
        data = open(F_IN, 'r', encoding='utf-8').read().split('\n')
        matching = [line for line in data if line.startswith('- [')]
        return sorted(map(tidy, matching))

    def filter(self):
        self.filtered = self.get_contents()
        if self.ui.query.text():
            self.filtered = [f for f in self.filtered
                             if self.ui.query.text().lower() in f[0].lower()]
        self.update_dropdown()

    def update_dropdown(self):
        self.ui.dropdown.clear()
        for line in self.filtered:
            self.ui.dropdown.addItem(line[0])

    def open(self):
        choice = self.filtered[self.ui.dropdown.currentIndex()][1]
        webbrowser.open(choice)
        app.quit()

    def search(self):
        txt = self.ui.query.text()
        query = f"https://www.youtube.com/results?search_query=asmr+{txt}"
        webbrowser.open(query)
        app.quit()


app = QtWidgets.QApplication([])
application = ASMRSearch()
application.show()
sys.exit(app.exec())
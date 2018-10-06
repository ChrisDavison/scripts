#!/usr/bin/env python
import sys
import webbrowser
import requests
from PyQt5 import QtCore, QtGui, QtWidgets

GIST = "https://gist.githubusercontent.com/ChrisDavison/ffe8159d49b0a9c490375db7fcb9df3f/raw/d0f4b6a025b1d002082e5c0ddd328daa7e7035a9/asmr.md"


WIDTH, HEIGHT = 300, 30  # Element geometry
B_WIDTH, B_HEIGHT = 60, HEIGHT  # Button geometry
W_WIDTH, W_HEIGHT = WIDTH + B_WIDTH, HEIGHT * 2  # Window geometry


class Ui_ASMRSearch(object):
    def setupUi(self, ASMRSearch):
        ASMRSearch.setObjectName("ASMRSearch")
        ASMRSearch.setFixedSize(W_WIDTH, W_HEIGHT)
        ASMRSearch.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(ASMRSearch)
        self.centralwidget.setObjectName("centralwidget")
        # ===== Query and Search button
        self.query = QtWidgets.QLineEdit(self.centralwidget)
        self.query.setGeometry(QtCore.QRect(0, 0, WIDTH, HEIGHT))
        self.query.setObjectName("query")
        # ----------
        self.buttonSearch = QtWidgets.QPushButton(self.centralwidget)
        self.buttonSearch.setGeometry(WIDTH, 0, B_WIDTH, B_HEIGHT)
        self.buttonSearch.setFixedSize(QtCore.QSize(B_WIDTH, B_HEIGHT))
        self.buttonSearch.setObjectName("dosearch")
        self.buttonSearch.setText("Search")
        # ===== Dropdown and Go button
        self.dropdown = QtWidgets.QComboBox(self.centralwidget)
        self.dropdown.setGeometry(QtCore.QRect(0, HEIGHT, WIDTH, HEIGHT))
        self.dropdown.setFixedSize(QtCore.QSize(WIDTH, HEIGHT))
        self.dropdown.setObjectName("dropdown")
        # ----------
        self.buttonGo = QtWidgets.QPushButton(self.centralwidget)
        self.buttonGo.setGeometry(WIDTH, HEIGHT, B_WIDTH, B_HEIGHT)
        self.buttonGo.setFixedSize(QtCore.QSize(B_WIDTH, B_HEIGHT))
        self.buttonGo.setObjectName("open")
        self.buttonGo.setText("Open")
        
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
        self.contents = self.get_contents()
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
        contents = []
        for line in requests.get(GIST).text.split('\n'):
            if not line.startswith('- ['):
                continue
            tidied = tidy(line)
            contents.append({"title": tidied[0], "url": tidied[1]})
        return sorted(contents, key=lambda x: x["title"])

    def filter(self):
        query = self.ui.query.text().lower()
        self.filtered = [f for f in self.contents
                         if query in f["title"].lower()]
        self.update_dropdown()

    def update_dropdown(self):
        self.ui.dropdown.clear()
        self.ui.dropdown.addItems(x["title"] for x in self.filtered)

    def open(self):
        choice = self.filtered[self.ui.dropdown.currentIndex()]["url"]
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
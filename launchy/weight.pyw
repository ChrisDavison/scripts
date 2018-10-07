import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(230,90)
        MainWindow.setWindowTitle("Convert")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.weightEntry_kg = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.weightEntry_kg.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.weightEntry_kg.setFrame(True)
        self.weightEntry_kg.setAlignment(QtCore.Qt.AlignCenter)
        self.weightEntry_kg.setSuffix("kg")
        self.weightEntry_kg.setMinimum(60.0)
        self.weightEntry_kg.setMaximum(120.0)
        self.weightEntry_kg.setSingleStep(0.1)
        self.weightEntry_kg.setProperty("value", 80.0)
        self.weightEntry_kg.setObjectName("weightEntry_kg")
        self.display_lb = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.display_lb.setGeometry(QtCore.QRect(140, 10, 80, 30))
        self.display_lb.setReadOnly(True)
        self.display_lb.setPlainText("10")
        self.display_lb.setObjectName("display_lb")
        self.display_st = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.display_st.setGeometry(QtCore.QRect(140, 50, 80, 30))
        self.display_st.setReadOnly(True)
        self.display_st.setPlainText("15")
        self.display_st.setObjectName("display_st")
        self.label_is = QtWidgets.QLabel(self.centralwidget)
        self.label_is.setGeometry(QtCore.QRect(120, 10, 20, 20))
        self.label_is.setText("is")
        self.label_is.setAlignment(QtCore.Qt.AlignCenter)
        self.label_is.setObjectName("label_is")
        self.label_or = QtWidgets.QLabel(self.centralwidget)
        self.label_or.setGeometry(QtCore.QRect(120, 50, 20, 20))
        self.label_or.setText("or")
        self.label_or.setAlignment(QtCore.Qt.AlignCenter)
        self.label_or.setObjectName("label_or")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass


class Weight(QtWidgets.QMainWindow):
    def __init__(self):
        super(Weight, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.weightEntry_kg.valueChanged.connect(self.update)
        self.update()

    def update(self):
        kg = self.ui.weightEntry_kg.value()
        self.ui.display_lb.setPlainText(f"{kg * 2.2:.2f} lb")
        self.ui.display_st.setPlainText(f"{kg * 2.2 / 14:.2f} st")


app = QtWidgets.QApplication([])
application = Weight()
application.show()
sys.exit(app.exec())
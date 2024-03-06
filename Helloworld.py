import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        btn = QPushButton("Button", self)
        btn.move(10, 10)
        btn.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        print("hi click")

app = QApplication(sys.argv)
win = MyWindow()
win.show()
app.exec_()
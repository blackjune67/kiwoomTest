import sys 
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)
label = QLabel("Hello PyQt")
win = QMainWindow();

win.show();
# label.show()
app.exec_()
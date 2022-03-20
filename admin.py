import sys
import threading
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot,QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QImage
import resource
import time

class Admin(QDialog):

    age = 0

    def __init__(self):
        super(Admin, self).__init__()
        loadUi("./admin.ui", self)
        self.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Admin()
    sys.exit(app.exec_())





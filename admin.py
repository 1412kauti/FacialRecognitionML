import sys
import threading
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot,QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QImage
import resource
import time
import os

class Admin(QDialog):

    age = 0

    def __init__(self):
        super(Admin, self).__init__()
        loadUi("./admin.ui", self)
        self.show()
        self.comboBox.activated[str].connect(self.comboBoxClicked)
        self.Thread_init3 = threading.Thread(target=self.load_qss)
        self.Thread_init3.start()

    def load_qss(self):
        dummy=[]
        qss_path = 'QSS'
        qss_list = os.listdir(qss_path)
        for theme in qss_list:
            dummy.append(os.path.splitext(theme)[0])
            self.comboBox.addItem(os.path.splitext(theme)[0])

    def comboBoxClicked(self,val):
        qss_path = 'QSS/'
        theme_name = self.comboBox.currentText()
        theme_file_name = qss_path + str(theme_name)+(".qss")
        with open(theme_file_name, "r") as fh:
            self.setStyleSheet(fh.read())

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Admin()
    sys.exit(app.exec_())





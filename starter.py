import sys
import threading
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot,QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QImage
import resource
from Facial import Ui_OutputDialog
import time
import configparser

class Attendance(QDialog):
    
    def __init__(self):
        super(Attendance, self).__init__()
        loadUi("outputwindow.ui")
        self.ui = Ui_OutputDialog()
        self.ui.setWindowTitle("Face Recognition")

        self._new_window = None
        self.Videocapture_ = None

        self.Thread1 = Worker1()
        self.Thread1.start()
        self.Thread1.camera_name.connect(self.refresh)

        self.Thread2 = Worker1()
        self.Thread2.start()
        self.Thread2.camera_name.connect(self.func1)

    def refresh(self,val):
        self.Videocapture_ = val
        self._new_window = Ui_OutputDialog()
        self._new_window.show()
        print("showing")
    
    def func1(self,val):
        self._new_window.startVideo(val)
        print("starting video")

    def func2(self,val):
        self._new_window.update_frame(val)

class Worker1(QThread):
    config = configparser.RawConfigParser()   
    config.read('camconfig.txt') 
    camcode = config.get('cam-config','camcode')
    
    camera_name = pyqtSignal(str)
    def run(self):
        self.camera_name.emit(str(self.camcode))
    
    def stop(self):
        self.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Attendance()
    sys.exit(app.exec_())
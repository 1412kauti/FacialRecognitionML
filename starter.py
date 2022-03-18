import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
import resource
from Facial import Ui_OutputDialog


class Attendance(QDialog):
    def __init__(self):
        super(Attendance, self).__init__()
        loadUi("outputwindow.ui")
        self._new_window = None
        self.Videocapture_ = None
        self.runSlot()

    def refreshAll(self):
        """
        Set the text of lineEdit once it's valid
        """
        self.Videocapture_ = "0"

    def runSlot(self):
        """
        Called when the user presses the Run button
        """
        self.refreshAll()
        self.outputWindow_()  # Create and open new output window

    def outputWindow_(self):
        """
        Created new window for vidual output of the video in GUI
        """
        self._new_window = Ui_OutputDialog()
        self._new_window.show()
        self._new_window.startVideo(self.Videocapture_)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Attendance()
    sys.exit(app.exec_())
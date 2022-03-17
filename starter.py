import sys
from PyQt5.uic import loadUi
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
# import resource
from Facial import Ui_OutputDialog


class Attendance(QDialog):
    def __init__(self):
        super(Attendance, self).__init__()
        loadUi("outputwindow.ui")
        self._new_window = None
        self.video_capture = None
        self.run_slot()

    def refresh_all(self):
        """
        Set the text of lineEdit once it's valid
        """
        self.video_capture = "0"

    def run_slot(self):
        """
        Called when the user presses the Run button
        """
        self.refresh_all()
        self.output_window()  # Create and open new output window

    def output_window(self):
        """
        Created new window for vidual output of the video in GUI
        """
        self._new_window = Ui_OutputDialog()
        self._new_window.show()
        self._new_window.start_video(self.video_capture)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Attendance()
    sys.exit(app.exec_())

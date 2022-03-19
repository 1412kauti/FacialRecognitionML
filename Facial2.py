import threading
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QDialog, QMessageBox
import cv2
import face_recognition
import numpy as np
import datetime
import os
import csv
import sqlite3


class Ui_OutputDialog(QDialog):
    run_once = False

    path = 'ImagesAttendance'
    images = []
    class_names = []
    encode_list = []
    TimeList1 = []
    TimeList2 = []
    attendance_list = os.listdir(path)
    

    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi("./outputwindow.ui", self)

        # Update time
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.Date_Label.setText(current_date)
        self.Time_Label.setText(current_time)
        self.themeComboBox.activated[str].connect(self.comboBoxClicked)
        self.image = None
        x = threading.Thread(target=self.load_qss)
        x.start()

    
    def load_qss(self):
        dummy=[]
        qss_path = 'QSS'
        qss_list = os.listdir(qss_path)
        for theme in qss_list:
            dummy.append(os.path.splitext(theme)[0])
            self.themeComboBox.addItem(os.path.splitext(theme)[0])

    def comboBoxClicked(self,val):
        qss_path = 'QSS/'
        theme_name = self.themeComboBox.currentText()
        theme_file_name = qss_path + str(theme_name)+(".qss")
        with open(theme_file_name, "r") as fh:
            self.setStyleSheet(fh.read())

    @pyqtSlot()
    def startVideo(self, camera_name):
        pass

    def get_class_names(self):
        
        if not os.path.exists(path):
            os.mkdir(path)
        attendance_list = os.listdir(path)
        
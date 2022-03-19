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
        if len(camera_name) == 1:
            self.capture = cv2.VideoCapture(int(camera_name))
        else:
            self.capture = cv2.VideoCapture(camera_name)

    def get_class_names(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.attendance_list = os.listdir(self.path)
        for cl in self.attendance_listattendance_list:
            cur_img = cv2.imread(f'{self.path}/{cl}')
            self.images.append(cur_img)
            self.class_names.append(os.path.splitext(cl)[0])

    def get_encode_list(self):
        for img in self.images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(img)
            encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]
            # encode = face_recognition.face_encodings(img)[0]
            self.encode_list.append(encodes_cur_frame)
        
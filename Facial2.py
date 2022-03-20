from concurrent.futures import thread
from multiprocessing import dummy
import queue
import threading
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt,QThread,pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox
import cv2
import face_recognition
import numpy as np
import datetime
import os
import csv
import sqlite3
import configparser

class Ui_OutputDialog(QDialog):
    run_once = False

    path = 'ImagesAttendance'
    images = []
    class_names = []
    encode_list = []
    TimeList1 = []
    TimeList2 = []
    attendance_list = os.listdir(path)

    config = configparser.RawConfigParser()   
    config.read('camconfig.txt') 
    camcode = config.get('cam-config','camcode')
    

    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi("./outputwindow.ui", self)

        self.Thread_init4 = threading.Thread(target=self.load_dt)
        self.Thread_init3 = threading.Thread(target=self.load_qss)
        self.Thread_init3.start()
        self.Thread_init4.start()
        self.themeComboBox.activated[str].connect(self.comboBoxClicked)
        self.image = None
        

    def load_dt(self):
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.Date_Label.setText(current_date)
        self.Time_Label.setText(current_time)
        

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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(1) 
 

    def get_class_names(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.attendance_list = os.listdir(self.path)
        for cl in self.attendance_list:
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
    
    def update_frame(self):
        ret, self.image = self.capture.read()
        x = threading.Thread(target=self.face_rec_,args=(self.image,self.encode_list,self.class_names))
        y = threading.Thread(target=self.displayImage,args=(self.image, 1))
        x.start()
        x.join()
        y.start()
       

    def face_rec_(self, frame, encode_list_known, class_names):

        """
        :param frame: frame from camera
        :param encode_list_known: known face encoding
        :param class_names: known face names
        :return:
        """
        # face recognition
        faces_cur_frame = face_recognition.face_locations(frame)
        encodes_cur_frame = face_recognition.face_encodings(frame, faces_cur_frame)
        # count = 0

        insert_val = self

        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            match = face_recognition.compare_faces(encode_list_known, encodeFace, tolerance=0.50)
            face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
            name = "unknown"
            best_match_index = np.argmin(face_dis)
            # print("s",best_match_index)

            if match[best_match_index]:

                name = class_names[best_match_index].upper()
                now = datetime.datetime.now()
                dtString = now.strftime('%H:%M:%S')

                if not self.run_once:
                    insert_val.insert_values(name, dtString)
                    self.run_once = True
                    # self.Result_Label.setText('<font color="green">Attendance Recorded !</font>')
                    self.Result_Label.setStyleSheet("background-color: green")
                
                
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 20), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                with open('Attandence.csv', 'r+') as f:
                    myDataList = f.readlines()
                    nameList = []
                    for line in myDataList:
                        entry = line.split(',')
                        nameList.append(entry[0])

                    if name not in nameList:
                        f.writelines(f'\n{name},{dtString}')
            else:
                    self.Result_Label.setStyleSheet("background-color: red")
        self.image = frame
        return frame
    
    def insert_values(self, name, dtString):

        try:
            sqliteConnection = sqlite3.connect('database.db')
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")

            cursor.execute("INSERT INTO Entries (user_name,date_time) VALUES(?, ?)", (name, dtString))

            sqliteConnection.commit()

            print("Record inserted successfully into table ", cursor.rowcount)

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")
    
    def displayImage(self, image, window=1):
        """
        :param image: frame from camera
        :param encode_list: known face encoding list
        :param class_names: known face names
        :param window: number of window
        :return:
        """
        image = cv2.resize(image, (640, 480))
        try:
            # image = self.face_rec_(image, encode_list, class_names)
            dummy  = 0
            
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)


        
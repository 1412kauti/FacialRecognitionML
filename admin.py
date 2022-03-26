from atexit import register
import sqlite3
import sys
import threading
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot,QThread,pyqtSignal,Qt
from PyQt5.QtWidgets import QApplication, QDialog,QFileDialog
from PyQt5.QtGui import QImage,QPixmap
import cv2
import resource
import time
import os
import configparser
import shutil


class Admin(QDialog):

    age = 0


    def __init__(self):
        super(Admin, self).__init__()
        loadUi("./admin.ui", self)
        self.load_users()
        self.load_entries()
        
        config = configparser.RawConfigParser()   
        config.read('camconfig.txt') 
        camcode = config.get('cam-config','camcode')
        

        self.Register_Button.clicked.connect(self.reg)

        self.Upload_Button.clicked.connect(self.open)


        self.Capture_Button.clicked.connect(self.save_image)


        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)

        self.Capture = cv2.VideoCapture(camcode)

        self.comboBox.activated[str].connect(self.comboBoxClicked)
        self.Thread_init3 = threading.Thread(target=self.load_qss)
        self.Thread_init3.start()

        self.show()
        
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
    
    def open(self):
        filePath = QFileDialog.getOpenFileName(self, 'OpenFile')
        pixmap = QPixmap(str(filePath[0]))
        pixmap = pixmap.scaled(270, 405, Qt.KeepAspectRatio)
        self.Camera_View.setPixmap(pixmap)
        image_root,imageName = os.path.split(str(filePath[0]))
        imagePath = 'ImagesAttendance/'
        shutil.copyfile(filePath[0],imagePath+imageName)
    
    def ImageUpdateSlot(self, Image):
        self.Camera_View.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.stop()
    
    def get_image(self):
        retval, im  = self.Capture.read()
        return im
    
    def save_image(self):
        camera_capture = self.get_image()
        file = str(self.Name_Line.text())+".png"
        path = os.path.abspath(os.getcwd())+"/ImagesAttendance/"
        cv2.imwrite(path+file,camera_capture)



    @pyqtSlot()
    def reg(self):
        connection = sqlite3.connect("database.db")  
        cursor = connection.cursor()
        query = "INSERT INTO users (name,adress,role) VALUES('{}','{}','{}')"
        cursor.execute(query.format(self.Name_Line.text(),self.Adress_Line.text(),self.Role_Line.text()))
        connection.commit()
        
        self.load_users()


    def load_users(self):

        connection = sqlite3.connect("database.db")
        query = "SELECT name,adress,role FROM users"
        result = connection.execute(query)

        self.Users_View.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.Users_View.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Users_View.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        connection.close()
       
    def load_entries(self):
        connection = sqlite3.connect("database.db")
        query = "SELECT user_name,date_time FROM entries"
        result = connection.execute(query)

        self.Entries_View.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.Entries_View.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Entries_View.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        connection.close()

class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    
    def run(self):
        config = configparser.RawConfigParser()   
        config.read('camconfig.txt') 
        camcode = config.get('cam-config','camcode')
        self.ThreadActive = True
        Capture = cv2.VideoCapture(camcode)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(293, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Admin()
    sys.exit(app.exec_())





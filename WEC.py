# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 14:15:21 2021

@author: antoine
"""

import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore
from riotwatcher import LolWatcher
import cv2
import Fonctions_Live as fcl
from main_window_ui import Ui_MainWindow

os.chdir(r"D:\Antoine\CNAM\3A\WEC")
lol_watcher = LolWatcher('RGAPI-1497b4c3-048f-4d37-b2f6-c397facefde7')     #refresh tous les jours
#pred = prediction(model, gameInfo)

class Window(QMainWindow, Ui_MainWindow):
    """Class de la fenetre principale"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        """Renvoie une connection au trigger"""
        self.actionpgmLauncher.triggered.connect(self.pgmLauncher)
        
    def about(self):
        """Renvoie un message'About'"""
        QMessageBox.about(
            self,
            "About Sample Editor",
            "<p>A sample text editor app built with:</p>"
            "<p>- PyQt</p>"
            "<p>- Qt Designer</p>"
            "<p>- Python</p>",)

    def pgmLauncher(self):
        """Execute le programme et affiche les infos"""
        gameData = fcl.requestLiveGameData("https://127.0.0.1:2999/liveclientdata/allgamedata")
        root = "D:/Antoine/CNAM/3A/WEC/"
        liveData, displayInfo = fcl.getGameInfo(gameData, lol_watcher, root)
        self.textBlueMain.setText("Blue Team WEC ?%")
        self.textRedMain.setText('Red Team WEC ?%')
        self.textBlueTop.setHtml(displayInfo[0][0]+" elo: "+str(displayInfo[2][0])+" wr: "+str(displayInfo[3][0])+"%"+" streak: "+str(displayInfo[4][0]))
        self.textBlueJgl.setHtml(displayInfo[0][1]+" elo: "+str(displayInfo[2][1])+" wr: "+str(displayInfo[3][1])+"%"+" streak: "+str(displayInfo[4][1]))
        self.textBlueMid.setHtml(displayInfo[0][2]+" elo: "+str(displayInfo[2][2])+" wr: "+str(displayInfo[3][2])+"%"+" streak: "+str(displayInfo[4][2]))
        self.textBlueBot.setHtml(displayInfo[0][3]+" elo: "+str(displayInfo[2][3])+" wr: "+str(displayInfo[3][3])+"%"+" streak: "+str(displayInfo[4][3]))
        self.textBlueSup.setHtml(displayInfo[0][4]+" elo: "+str(displayInfo[2][4])+" wr: "+str(displayInfo[3][4])+"%"+" streak: "+str(displayInfo[4][4]))
        self.textRedTop.setHtml(displayInfo[0][5]+" elo: "+str(displayInfo[2][5])+" wr: "+str(displayInfo[3][5])+"%"+" streak: "+str(displayInfo[4][5]))
        self.textRedJgl.setHtml(displayInfo[0][6]+" elo: "+str(displayInfo[2][6])+" wr: "+str(displayInfo[3][6])+"%"+" streak: "+str(displayInfo[4][6]))
        self.textRedMid.setHtml(displayInfo[0][7]+" elo: "+str(displayInfo[2][7])+" wr: "+str(displayInfo[3][7])+"%"+" streak: "+str(displayInfo[4][7]))
        self.textRedBot.setHtml(displayInfo[0][8]+" elo: "+str(displayInfo[2][8])+" wr: "+str(displayInfo[3][8])+"%"+" streak: "+str(displayInfo[4][8]))
        self.textRedSup.setHtml(displayInfo[0][9]+" elo: "+str(displayInfo[2][9])+" wr: "+str(displayInfo[3][9])+"%"+" streak: "+str(displayInfo[4][9]))
        self.displayImage(cv2.imread(displayInfo[1][0]), "self.imgBlueTop")
        self.displayImage(cv2.imread(displayInfo[1][1]), "self.imgBlueJgl")
        self.displayImage(cv2.imread(displayInfo[1][2]), "self.imgBlueMid")
        self.displayImage(cv2.imread(displayInfo[1][3]), "self.imgBlueBot")
        self.displayImage(cv2.imread(displayInfo[1][4]), "self.imgBlueSup")
        self.displayImage(cv2.imread(displayInfo[1][5]), "self.imgRedTop")
        self.displayImage(cv2.imread(displayInfo[1][6]), "self.imgRedJgl")
        self.displayImage(cv2.imread(displayInfo[1][7]), "self.imgRedMid")
        self.displayImage(cv2.imread(displayInfo[1][8]), "self.imgRedBot")
        self.displayImage(cv2.imread(displayInfo[1][9]), "self.imgRedSup")
        cv2.destroyAllWindows()

    def displayImage(self, img, obj):
        """Display l'image dans l'objet"""
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if(img.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        eval(obj).setPixmap(QPixmap.fromImage(img))
        eval(obj).setScaledContents(True)
        eval(obj).setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        #self.imgBlueBot.setStyleSheet("border: 1px solid blue;") Pour display une bordure

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

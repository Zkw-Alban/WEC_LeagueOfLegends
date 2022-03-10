# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 14:15:21 2021

@author: antoine
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore
from riotwatcher import LolWatcher
import cv2
import Fonctions_Live as fcl
from WECPrevLauncher import Ui_MainWindow

os.chdir(os.getcwd())
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
            "About Sample Editor",
            "<p>A sample text editor app built with:</p>"
            "<p>- PyQt</p>"
            "<p>- Qt Designer</p>"
            "<p>- Python</p>",)

    def pgmLauncher(self):
        """Execute le programme et affiche les infos"""
        playerList = []
        playerList.append(self.SNBlueTop.text())
        playerList.append(self.SNBlueJungle.text())
        playerList.append(self.SNBlueMid.text())
        playerList.append(self.SNBlueBot.text())
        playerList.append(self.SNBlueSup.text())
        playerList.append(self.SNRedTop.text())
        playerList.append(self.SNRedJungle.text())
        playerList.append(self.SNRedMid.text())
        playerList.append(self.SNRedBot.text())
        playerList.append(self.SNRedSup.text())
        print(playerList)
        championNameList = []
        championNameList.append(str(self.ChampBlueTop.currentText()))
        championNameList.append(str(self.ChampBlueJungle.currentText()))
        championNameList.append(str(self.ChampBlueMid.currentText()))
        championNameList.append(str(self.ChampBlueBot.currentText()))
        championNameList.append(str(self.ChampBlueSup.currentText()))
        championNameList.append(str(self.ChampRedTop.currentText()))
        championNameList.append(str(self.ChampRedJungle.currentText()))
        championNameList.append(str(self.ChampRedMid.currentText()))
        championNameList.append(str(self.ChampRedBot.currentText()))
        championNameList.append(str(self.ChampRedSup.currentText()))
        print(championNameList)
        liveData, displayInfo = fcl.getGameInfo(playerList, championNameList, lol_watcher)
        self.textBlueTop.setHtml("<div style='text-align:center;'>"+displayInfo[0][0]+" "+str(displayInfo[2][0])+"<br />"+str(displayInfo[3][0])+"% wr"+" streak: "+str(displayInfo[4][0])+"</div>")
        self.textBlueJgl.setHtml("<div style='text-align:center;'>"+displayInfo[0][1]+" "+str(displayInfo[2][1])+"<br />"+str(displayInfo[3][1])+"% wr"+" streak: "+str(displayInfo[4][1])+"</div>")
        self.textBlueMid.setHtml("<div style='text-align:center;'>"+displayInfo[0][2]+" "+str(displayInfo[2][2])+"<br />"+str(displayInfo[3][2])+"% wr"+" streak: "+str(displayInfo[4][2])+"</div>")
        self.textBlueBot.setHtml("<div style='text-align:center;'>"+displayInfo[0][3]+" "+str(displayInfo[2][3])+"<br />"+str(displayInfo[3][3])+"% wr"+" streak: "+str(displayInfo[4][3])+"</div>")
        self.textBlueSup.setHtml("<div style='text-align:center;'>"+displayInfo[0][4]+" "+str(displayInfo[2][4])+"<br />"+str(displayInfo[3][4])+"% wr"+" streak: "+str(displayInfo[4][4])+"</div>")
        self.textRedTop.setHtml("<div style='text-align:center;'>"+displayInfo[0][5]+" "+str(displayInfo[2][5])+"<br />"+str(displayInfo[3][5])+"% wr"+" streak: "+str(displayInfo[4][5])+"</div>")
        self.textRedJgl.setHtml("<div style='text-align:center;'>"+displayInfo[0][6]+" "+str(displayInfo[2][6])+"<br />"+str(displayInfo[3][6])+"% wr"+" streak: "+str(displayInfo[4][6])+"</div>")
        self.textRedMid.setHtml("<div style='text-align:center;'>"+displayInfo[0][7]+" "+str(displayInfo[2][7])+"<br />"+str(displayInfo[3][7])+"% wr"+" streak: "+str(displayInfo[4][7])+"</div>")
        self.textRedBot.setHtml("<div style='text-align:center;'>"+displayInfo[0][8]+" "+str(displayInfo[2][8])+"<br />"+str(displayInfo[3][8])+"% wr"+" streak: "+str(displayInfo[4][8])+"</div>")
        self.textRedSup.setHtml("<div style='text-align:center;'>"+displayInfo[0][9]+" "+str(displayInfo[2][9])+"<br />"+str(displayInfo[3][9])+"% wr"+" streak: "+str(displayInfo[4][9])+"</div>")
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
        df = pd.DataFrame(liveData, index=[0])
        loaded_clf = joblib.load("random_forest_1.joblib")
        pred = loaded_clf.predict_proba(df)
        pred1 = round(np.around(pred[0][0], 3).item() * 100, 1)
        pred2 = (100-pred1)
        self.textBlueMain.setHtml("<div style='text-align:center;'>"+"Blue Team WEC "+str(pred1)+"%"+"</div>")
        self.textRedMain.setHtml("<div style='text-align:center;'>"+"Red Team WEC "+str(pred2)+"%"+"</div>")

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

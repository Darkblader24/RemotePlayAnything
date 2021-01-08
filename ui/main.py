# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources\main.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(810, 600)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("#startGameButton {\n"
"    background-color:rgb(255, 35, 35);\n"
"    color:white;\n"
"    border-style:outset;\n"
"    border-width:2px;\n"
"    border-radius:20px;\n"
"    border-color:black;\n"
"    font:bold 22px;\n"
"}\n"
"\n"
"#startGameButton:hover {\n"
"    background-color:rgb(255, 75, 75);\n"
"}\n"
"\n"
"#startGameButton:pressed {\n"
"    background-color:rgb(201, 14, 14);\n"
"}\n"
"\n"
"#gamesList {\n"
"    font: 15px;\n"
"    background-color: rgba(255,255,255,150);\n"
"}\n"
"\n"
"#selectedGameLabel {\n"
"    font:bold 15px;\n"
"}\n"
"\n"
"#gamesList {\n"
"    font: 15px;\n"
"    background-color: rgba(255,255,255,150);\n"
"}\n"
"\n"
"[accessibleName=\"listEditButton\"] {\n"
"    font: 13px;\n"
"}\n"
"\n"
"#gameListTitleLabel {\n"
"    font: bold 14px;\n"
"}\n"
"\n"
"#backgroundImage {\n"
"    background: url(:/Icons/background.png)\n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        self.startGameButton = QtWidgets.QPushButton(self.centralwidget)
        self.startGameButton.setGeometry(QtCore.QRect(310, 490, 191, 61))
        self.startGameButton.setObjectName("startGameButton")
        self.selectedGameLabel = QtWidgets.QLabel(self.centralwidget)
        self.selectedGameLabel.setGeometry(QtCore.QRect(20, 420, 771, 61))
        self.selectedGameLabel.setScaledContents(False)
        self.selectedGameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.selectedGameLabel.setWordWrap(True)
        self.selectedGameLabel.setObjectName("selectedGameLabel")
        self.gamesList = QtWidgets.QListWidget(self.centralwidget)
        self.gamesList.setGeometry(QtCore.QRect(80, 50, 651, 331))
        self.gamesList.setObjectName("gamesList")
        item = QtWidgets.QListWidgetItem()
        self.gamesList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.gamesList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.gamesList.addItem(item)
        self.addGameButton = QtWidgets.QPushButton(self.centralwidget)
        self.addGameButton.setGeometry(QtCore.QRect(80, 390, 91, 31))
        self.addGameButton.setObjectName("addGameButton")
        self.removeGameButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeGameButton.setGeometry(QtCore.QRect(620, 390, 111, 31))
        self.removeGameButton.setObjectName("removeGameButton")
        self.editGameButton = QtWidgets.QPushButton(self.centralwidget)
        self.editGameButton.setGeometry(QtCore.QRect(180, 390, 91, 31))
        self.editGameButton.setObjectName("editGameButton")
        self.gameListTitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.gameListTitleLabel.setGeometry(QtCore.QRect(80, 20, 221, 21))
        self.gameListTitleLabel.setObjectName("gameListTitleLabel")
        self.backgroundImage = QtWidgets.QGraphicsView(self.centralwidget)
        self.backgroundImage.setGeometry(QtCore.QRect(0, 0, 810, 600))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.Dense1Pattern)
        self.backgroundImage.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.Dense5Pattern)
        self.backgroundImage.setForegroundBrush(brush)
        self.backgroundImage.setInteractive(False)
        self.backgroundImage.setObjectName("backgroundImage")
        self.versionLabel = QtWidgets.QLabel(self.centralwidget)
        self.versionLabel.setGeometry(QtCore.QRect(630, 560, 171, 31))
        self.versionLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.versionLabel.setObjectName("versionLabel")
        self.backgroundImage.raise_()
        self.startGameButton.raise_()
        self.selectedGameLabel.raise_()
        self.gamesList.raise_()
        self.addGameButton.raise_()
        self.removeGameButton.raise_()
        self.gameListTitleLabel.raise_()
        self.editGameButton.raise_()
        self.versionLabel.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Remote Play Anything"))
        self.startGameButton.setText(_translate("MainWindow", "Start Game"))
        self.selectedGameLabel.setText(_translate("MainWindow", "Please select a game.."))
        __sortingEnabled = self.gamesList.isSortingEnabled()
        self.gamesList.setSortingEnabled(False)
        item = self.gamesList.item(0)
        item.setText(_translate("MainWindow", "Heroes of Might and Magic 7"))
        item = self.gamesList.item(1)
        item.setText(_translate("MainWindow", "Battlefield 4"))
        item = self.gamesList.item(2)
        item.setText(_translate("MainWindow", "Magicka The Unknown Place of Farts"))
        self.gamesList.setSortingEnabled(__sortingEnabled)
        self.addGameButton.setAccessibleName(_translate("MainWindow", "listEditButton"))
        self.addGameButton.setText(_translate("MainWindow", "Add Game"))
        self.removeGameButton.setAccessibleName(_translate("MainWindow", "listEditButton"))
        self.removeGameButton.setText(_translate("MainWindow", "Remove Game"))
        self.editGameButton.setAccessibleName(_translate("MainWindow", "listEditButton"))
        self.editGameButton.setText(_translate("MainWindow", "Edit Game"))
        self.gameListTitleLabel.setText(_translate("MainWindow", "Your Games:"))
        self.versionLabel.setText(_translate("MainWindow", "Remote Play Anything v1.0"))
import resources_rc
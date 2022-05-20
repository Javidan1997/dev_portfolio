import sys
from pathlib import Path
from PyQt6.QtCore import QTimer
from PyQt6 import QtGui
from PyQt6.QtWidgets import (QApplication,
                             QDialog, QGridLayout, QGroupBox, QLabel, QLineEdit,
                             QProgressBar, QPushButton,
                             QVBoxLayout)


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        self.createTopGroupBox()
        self.createProgressBar()
        self.createBottomTabWidget()
        self.createBottomMiddleWidget()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.caption, 1, 0)
        mainLayout.addWidget(self.subcaption, 2, 0)
        mainLayout.addWidget(self.link, 3, 0)
        mainLayout.addWidget(self.copylink, 3, 1)
        mainLayout.addWidget(self.lbl, 4, 0)
        mainLayout.addWidget(self.path, 5, 0)
        mainLayout.addWidget(self.browse, 5, 1)
        mainLayout.addWidget(self.opera, 6, 0)
        mainLayout.addWidget(self.operaLink, 7, 0)
        mainLayout.addWidget(self.lbl2, 8, 0)
        mainLayout.addWidget(self.pbar, 9, 0)
        mainLayout.addWidget(self.bottomleftbar, 10, 0)
        mainLayout.addWidget(self.bottomcenterbar, 10, 1)

        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)
        self.setStyleSheet("background-color: #F0F0F0;")
        self.setWindowTitle("Title V2.1")
        self.operaLink.setOpenExternalLinks(True)
        self.link.setReadOnly(True)

        self.setWindowIcon(QtGui.QIcon('Title.png'))

    def createTopGroupBox(self):
        self.caption = QLabel(
            '*******************************.')
        self.subcaption = QLabel('*******************************.')
        self.link = QLineEdit('*******************************.')
        self.copylink = QPushButton('Copy link', clicked=self.copyToClipboard)
        self.lbl = QLabel()

        self.path = QLineEdit(
            "'*******************************.'")
        self.browse = QPushButton('Connect', clicked=self.timerstart2)
        self.opera = QLabel(
            'Dont have an Opera browser?')
        urlLink = "'*******************************.'
        self.operaLink = QLabel(urlLink)

    def createProgressBar(self):
        self.lbl2 = QLabel()
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.pbar.setValue(0)

    def timerstart(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.handleTimer)
        self.timer.start(1000)

    def timerstart2(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.connected)
        self.timer.start(1000)

    def handleTimer(self):
        value = self.pbar.value()
        if self.browse.text() != 'Connected':
            self.lbl2.setText('Error:'*******************************.'')
            self.lbl2.setStyleSheet('color: red; font-size: 14px')
        else:
            if value < 30:
                value = value + 5
                self.pbar.setValue(value)
            elif value == 30:
                self.lbl2.setText(
                    'Error: '*******************************.'')
                self.lbl2.setStyleSheet('color: red; font-size: 14px')

            else:
                self.timer.stop()

    def copyToClipboard(self):
        cb = QApplication.clipboard()
        cb.clear()
        cb.setText(self.link.text())
        self.lbl.setText('Content is copied')

    def connected(self):
        self.browse.setText('Connecting..')
        self.browse.setStyleSheet("background-color: #FFFF00")
        value = self.pbar.value()

        if value < 100:
            value = value + 10
            self.pbar.setValue(value)
        elif value == 100:
            self.browse.setText(
                'Connected')
            self.browse.setStyleSheet("background-color: #008000")
            value = 0
            self.pbar.setValue(value)
            self.timer.stop()

        else:
            self.timer.stop()

    def createBottomTabWidget(self):
        self.bottomleftbar = QGroupBox()
        leftbar = QLineEdit(''*******************************.')
        leftbar.setMaximumWidth(100)
        leftbar.setMaximumHeight(100)
        leftbar.setStyleSheet(
            'color:grey; font-size: 64px')
        leftbar.setReadOnly(True)
        text = "<img src='*******************************.' style=width:100px;height:100px;>"
        rightbar = QLabel(text)

        layout = QGridLayout()
        layout.addWidget(leftbar, 1, 0)
        layout.addWidget(rightbar, 2, 0)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        self.bottomleftbar.setLayout(layout)

    def createBottomMiddleWidget(self):
        self.bottomcenterbar = QGroupBox()
        radioButton1 = QLineEdit()
        radioButton1.setPlaceholderText(''*******************************.'')
        radioButton2 = QPushButton("RUN", clicked=self.timerstart)
        radioButton3 = QPushButton("History", clicked=self.history)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addStretch()
        self.bottomcenterbar.setLayout(layout)

    def history(self):
        self.lbl2.setText('History is empty!')
        self.lbl2.setStyleSheet('color: red; font-size: 14px')


if __name__ == '__main__':

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())

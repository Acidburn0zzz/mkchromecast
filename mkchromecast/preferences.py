#!/usr/bin/env python

# This file is part of mkchromecast.

import sys
from PyQt5.QtWidgets import (QWidget, QLabel,
    QComboBox, QApplication)

from PyQt5 import QtCore


class Example(QWidget):

    def __init__(self):
        try:
            super().__init__()
        except TypeError:
            super().__init__(self)

        self.initUI()


    def initUI(self):
        platform = 'Darwin'

        if platform == 'Darwin':
            self.lbl = QLabel("node", self)
        else:
            self.lbl = QLabel("ffmpeg", self)


        """
        Backend
        """
        self.backend = QLabel('Select Backend', self)
        self.backend.move(20, 54)
        self.qcbackend = QComboBox(self)
        self.qcbackend.move(180, 50)
        self.qcbackend.setMinimumContentsLength(7)
        self.qcbackend.addItem("node")
        self.qcbackend.addItem("ffmpeg")
        self.qcbackend.addItem("avconv")
        self.qcbackend.activated[str].connect(self.onActivated)

        """
        Bitrate
        """
        self.bitrate = QLabel('Select Bitrate (kbit/s)', self)
        #self.bitrate.setAlignment(QtCore.Qt.AlignLeft)
        self.bitrate.move(20, 86)
        self.qcbitrate = QComboBox(self)
        self.qcbitrate.move(180, 84)
        self.qcbitrate.setMinimumContentsLength(7)
        self.qcbitrate.addItem("128")
        self.qcbitrate.addItem("160")
        self.qcbitrate.addItem("192")
        self.qcbitrate.addItem("224")
        self.qcbitrate.addItem("256")
        self.qcbitrate.addItem("320")
        self.qcbitrate.addItem("500")
        self.qcbitrate.activated[str].connect(self.onActivated)

        """
        Notifications
        """
        self.notifications = QLabel('Notifications', self)
        self.notifications.move(20, 118)
        self.qcnotifications = QComboBox(self)
        self.qcnotifications.move(180, 118)
        self.qcnotifications.setMinimumContentsLength(7)
        self.qcnotifications.addItem("Enabled")
        self.qcnotifications.addItem("Disabled")

        self.lbl.move(50, 150)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Preferences')
        self.show()


    def onActivated(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

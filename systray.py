#!/usr/bin/env python

# This file is part of mkchromecast.

from mkchromecast.audiodevices import *
from mkchromecast.streaming import *
from mkchromecast.cast import *
from PyQt5 import QtCore, QtGui, QtWidgets
import signal
import os.path


cc = casting()
class menubar(object):
    def __init__(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self.app = QtWidgets.QApplication([])

        icon = QtGui.QIcon('images/google.ico')
        tray = QtWidgets.QSystemTrayIcon(icon)

        self.menu = QtWidgets.QMenu()
        self.search_menu()
        self.separator_menu()
        self.populating_menu()
        self.separator_menu()
        self.stop_menu()
        self.resetaudio_menu()
        self.about_menu()
        self.exit_menu()

        tray.setContextMenu(self.menu)
        tray.show()
        self.app.exec_()

    def search_menu(self):
        self.SearchAction = self.menu.addAction("Search for Google cast devices")
        self.SearchAction.triggered.connect(self.search_cast)

    def stop_menu(self):
        self.StopCastAction = self.menu.addAction("Stop casting")
        self.StopCastAction.triggered.connect(self.stop_cast)

    def separator_menu(self):
        self.menu.addSeparator()

    def populating_menu(self):
        if self.SearchAction.triggered.connect == True:
            self.cast_list()

    def resetaudio_menu(self):
        self.ResetAudioAction = self.menu.addAction("Reset audio")
        self.ResetAudioAction.triggered.connect(self.reset_audio)

    def about_menu(self):
        self.AboutAction = self.menu.addAction("About")

    def exit_menu(self):
        exitAction = self.menu.addAction("Exit")
        exitAction.triggered.connect(self.app.quit)

    """
    These are methods for interacting with the mkchromecast objects
    """

    def search_cast(self):
        args.select_cc = True
        cc.initialize_cast()
        self.cast_list()

    def cast_list(self):
        if len(cc.availablecc) == 0:
            print ('No devices found!')
        else:
            self.menu.clear()
            self.search_menu()
            self.separator_menu()
            for index,menuentry in enumerate(cc.availablecc):
                print ('Lo hizo!')
                print menuentry[0]
                self.index = index
                self.index = self.menu.addAction(str(menuentry[1]))
                self.index.triggered.connect(self.play_cast)
                if self.index.triggered.connect == True:
                    self.play_cast()
            self.separator_menu()
            self.stop_menu()
            self.resetaudio_menu()
            self.about_menu()
            self.exit_menu()

    def play_cast(self):
        cc.inp_cc()
        inputdev()
        outputdev()
        stream()
        cc.get_cc()
        cc.play_cast()

    def stop_cast(self):
        ncast = cc.cast
        cc.stop_cast()
        self.reset_audio()

    def reset_audio(self):
        inputint()
        outputint()

if __name__ == '__main__':
    if os.path.exists('/tmp/mkcrhomecast.tmp') == True:     #This is to verify that pickle tmp file exists
       os.remove('/tmp/mkcrhomecast.tmp')
    menubar()

#!/usr/bin/env python

# This file is part of mkchromecast.
# brew install pyqt5 --with-python --without-python3

import mkchromecast.__init__        # This is to verify against some needed variables
from mkchromecast.audiodevices import *
from mkchromecast.cast import *
from mkchromecast.node import *
import mkchromecast.tray_threading
import pychromecast
import signal
import os.path
from os import getpid
import psutil, pickle
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot


platform = mkchromecast.__init__.platform

global entries

class menubar(object):
    def __init__(self):
        self.cc = casting()
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.cast = None
        self.stopped = False

        """
        This is used when searching for cast devices
        """
        self.obj = mkchromecast.tray_threading.Worker()  # no parent!
        self.thread = QThread()  # no parent!

        self.obj.intReady.connect(self.onIntReady)
        self.obj.moveToThread(self.thread)
        self.obj.finished.connect(self.thread.quit)
        self.thread.started.connect(self.obj._search_cast_)

        """
        This is used when one click on cast device
        """
        self.objp = mkchromecast.tray_threading.Player()  # no parent!
        self.threadplay = QThread()  # no parent!

        self.objp.moveToThread(self.threadplay)
        self.objp.pcastready.connect(self.pcastready)
        self.objp.pcastfinished.connect(self.threadplay.quit)
        self.threadplay.started.connect(self.objp._play_cast_)

        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False) # This avoid the QMessageBox to close parent processes.
        self.w = QtWidgets.QWidget()

        if os.path.exists('images/google.icns') == True:
            self.icon = QtGui.QIcon()
            if platform == 'Darwin':
                self.icon.addFile('images/google.icns')#, QtCore.QSize(48,48))
            else:
                self.icon.addFile('images/google.png')
        else:
            self.icon = QtGui.QIcon()
            self.icon.addFile('google.icns')#, QtCore.QSize(48,48))

        self.tray = QtWidgets.QSystemTrayIcon(self.icon)

        self.menu = QtWidgets.QMenu()
        self.search_menu()
        self.separator_menu()
        self.populating_menu()
        self.separator_menu()
        self.stop_menu()
        self.resetaudio_menu()
        self.about_menu()
        self.exit_menu()

        self.tray.setContextMenu(self.menu)
        self.tray.show()
        self.app.exec_()

    def search_menu(self):
        self.SearchAction = self.menu.addAction("Search for Google Cast devices")
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
        self.AboutAction = self.menu.addAction("About mkchromecast")
        self.AboutAction.triggered.connect(self.about_show)

    def exit_menu(self):
        exitAction = self.menu.addAction("Quit")
        exitAction.triggered.connect(self.exit_all)

    """
    These are methods for interacting with the mkchromecast objects
    """

    def onIntReady(self, availablecc):
        print ('availablecc')
        self.availablecc = availablecc
        self.cast_list()

    def search_cast(self):
        if os.path.exists('images/google_working.icns') == True:
            if platform == 'Darwin':
                self.tray.setIcon(QtGui.QIcon('images/google_working.icns'))
            else:
                self.tray.setIcon(QtGui.QIcon('images/google_working.png'))
        else:
            self.tray.setIcon(QtGui.QIcon('google_working.icns'))

        args.select_cc = True
        if self.stopped == True and os.path.exists('/tmp/mkcrhomecast.tmp') == True:
            os.remove('/tmp/mkcrhomecast.tmp')

        self.thread.start()


    def cast_list(self):
        if os.path.exists('images/google.icns') == True:
            if platform == 'Darwin':
                self.tray.setIcon(QtGui.QIcon('images/google.icns'))
            else:
                self.tray.setIcon(QtGui.QIcon('images/google.png'))
        else:
            self.tray.setIcon(QtGui.QIcon('google.icns'))
        if len(self.availablecc) == 0:
            self.menu.clear()
            self.search_menu()
            self.separator_menu()
            self.NodevAction = self.menu.addAction("No Cast devices found.")
            if os.path.exists('images/google_nodev.icns') == True:
                if platform == 'Darwin':
                    self.tray.setIcon(QtGui.QIcon('images/google_nodev.icns'))
                else:
                    self.tray.setIcon(QtGui.QIcon('images/google_nodev.png'))
            else:
                self.tray.setIcon(QtGui.QIcon('google_nodev.icns'))
            self.separator_menu()
            self.stop_menu()
            self.resetaudio_menu()
            self.about_menu()
            self.exit_menu()
        else:
            self.menu.clear()
            self.search_menu()
            self.separator_menu()
            print ('Available Google Cast devices', self.availablecc)
            for index, menuentry in enumerate(self.availablecc):
                self.entries = menuentry
                self.menuentry = self.menu.addAction(str(menuentry[1]))
                self.menuentry.triggered.connect(self.play_cast)
                self.menuentry.setCheckable(True)
            self.separator_menu()
            self.stop_menu()
            self.resetaudio_menu()
            self.about_menu()
            self.exit_menu()

    def pcastready(self, done):
        print ('done', done)
        if os.path.exists('/tmp/mkcrhomecast.tmp') == True:
            self.cast = mkchromecast.tray_threading.cast
            self.ncast = self.cast
        if os.path.exists('images/google.icns') == True:
            if platform == 'Darwin':
                self.tray.setIcon(QtGui.QIcon('images/google.icns'))
            else:
                self.tray.setIcon(QtGui.QIcon('images/google.png'))
        else:
            self.tray.setIcon(QtGui.QIcon('google.icns'))

    def play_cast(self):
        self.menuentry.setChecked(True)
        if os.path.exists('images/google_working.icns') == True:
            if platform == 'Darwin':
                self.tray.setIcon(QtGui.QIcon('images/google_working.icns'))
            else:
                self.tray.setIcon(QtGui.QIcon('images/google_working.png'))
        else:
            self.tray.setIcon(QtGui.QIcon('google_working.icns'))

        #print ('yes')
        print (self.entries[0], self.entries[1])
        self.index = self.entries[0]
        self.castto = self.entries[1]
        if os.path.exists('/tmp/mkcrhomecast.tmp') == True:
            self.tf = open('/tmp/mkcrhomecast.tmp', 'wb')
        pickle.dump(self.index, self.tf)
        self.tf.close()
        self.threadplay.start()

    def stop_cast(self):
        if self.stopped == False:
            pass

        if self.cast != None or self.stopped == True:
            self.ncast.quit_app()
            self.menuentry.setChecked(False)
            self.reset_audio()
            self.parent_pid = getpid()
            self.parent = psutil.Process(self.parent_pid)
            for child in self.parent.children(recursive=True):  # or parent.children() for recursive=False
                child.kill()
            checkmktmp()
            self.search_cast()
            self.ncast.quit_app()
            self.stopped = True

    def reset_audio(self):
        inputint()
        outputint()

    def about_show(self):
        #self.threadabout.start()
        #QtWidgets.QMessageBox.about(self.w, "About", "An example messagebox @ pythonspot.com ")
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText("<a href='http://mkchromecast.com'>mkchromecast</a>: v"+mkchromecast.__init__.__version__)
        msgBox.setInformativeText("""Created by: Muammar El Khatib.
                \nUX design: Claudia Vargas.
                """)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    def exit_all(self):
        if self.cast == None and self.stopped == False:
            self.app.quit()
        elif self.stopped == True or self.cast != None:
            self.stop_cast()
            for child in self.parent.children(recursive=True):  # or parent.children() for recursive=False
                child.kill()
            self.stop_cast()
            self.app.quit()
        else:
            self.app.quit()

def main():
    menubar()

if __name__ == '__main__':
    checkmktmp()
    main()

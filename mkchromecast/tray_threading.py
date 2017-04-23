#!/usr/bin/env python

# This file is part of mkchromecast.

import mkchromecast.__init__
from mkchromecast.audio_devices import *
from mkchromecast.cast import *
from mkchromecast.config import *
import mkchromecast.audio
from mkchromecast.node import *
from mkchromecast.preferences import ConfigSectionMap
from mkchromecast.pulseaudio import create_sink, check_sink
from mkchromecast.systray import *
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import os.path
import pickle
import pychromecast
"""
Configparser is imported differently in Python3
"""
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser # This is for Python3

platform = mkchromecast.__init__.platform
debug = mkchromecast.__init__.debug
config = ConfigParser.RawConfigParser()
configurations = config_manager()    # Class from mkchromecast.config
configf = configurations.configf

class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(list)

    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot()
    def _search_cast_(self):
        try:                        # This should fix the error socket.gaierror making the system tray to be closed.
            self.cc = casting()
            self.cc.initialize_cast()
            self.cc.availablecc()
        except socket.gaierror:
            if debug == True:
                print(colors.warning(':::Threading::: Socket error, CC set to 0'))
            pass
        except TypeError:
            pass
        if len(self.cc.availablecc) == 0 and tray == True:
            availablecc = []
            self.intReady.emit(availablecc)
            self.finished.emit()
        else:
            availablecc = self.cc.availablecc
            self.intReady.emit(availablecc)
            self.finished.emit()

class Player(QObject):
    pcastfinished = pyqtSignal()
    pcastready = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot()
    def _play_cast_(self):
        if os.path.exists(configf):
            print(colors.warning(':::Threading::: Configuration file exists'))
            print(colors.warning(':::Threading::: Using defaults set there'))
            config.read(configf)
            backend = ConfigSectionMap('settings')['backend']
            print(':::Threading backend::: '+backend)
        else:
            backend = mkchromecast.__init__.backend
        global cast
        if backend == 'node':
            stream()
        else:
            try:
                reload(mkchromecast.audio)
            except NameError:
                from imp import reload
                reload(mkchromecast.audio)
            mkchromecast.audio.main()
        if platform == 'Linux':
            if check_sink() == False: # We create the sink only if it is not available
                create_sink()

        start = casting()
        start.initialize_cast()
        try:
            start.get_cc()
            start.play_cast()
            cast = start.cast
            if platform == 'Darwin': # Let's change inputs at the end to avoid muting sound too early.
                inputdev()           # For Linux it does not matter given that user has to select sink in pulse audio.
                outputdev()          # Therefore the sooner it is available, the better.
            self.pcastready.emit('_play_cast_ success')
        except AttributeError:
            self.pcastready.emit('_play_cast_ failed')
        self.pcastfinished.emit()

class Updater(QObject):
    """This class is employed to check for new mkchromecast versions"""
    upcastfinished = pyqtSignal()
    updateready = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot()
    def _updater_(self):
        chk = casting()
        if chk.ip == '127.0.0.1' or None:       # We verify the local IP.
            self.updateready.emit('None')
        else:
            try:
                from mkchromecast.version import __version__
                import requests
                url = 'https://api.github.com/repos/muammar/mkchromecast/releases/latest'
                response = requests.get(url).text.split(',')

                for e in response:
                    if 'tag_name' in e:
                        version = e.strip('"tag_name":')
                        break

                if version > __version__:
                    print ('Version ' + version + ' is available to download')
                    self.updateready.emit(version)
                else:
                    print ('You are up to date')
                    self.updateready.emit('False')
            except UnboundLocalError:
                self.updateready.emit('error1')
            except requests.exceptions.ConnectionError:
                self.updateready.emit('error1')

        self.upcastfinished.emit()

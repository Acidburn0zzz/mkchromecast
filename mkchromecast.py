#!/usr/bin/env python

# This file is part of mkchromecast.

import mkchromecast.__init__
from mkchromecast.version import __version__
from mkchromecast.audio_devices import *
from mkchromecast.cast import *
import mkchromecast.colors as colors
from mkchromecast.pulseaudio import create_sink, remove_sink
from mkchromecast.utils import terminate
import subprocess
import os.path
import time
import atexit
import signal


class mk(object):
    """Class to manage cast process"""
    def __init__(self):
        print(colors.bold('Mkchromecast ')+'v'+__version__)
        self.platform = mkchromecast.__init__.platform
        self.adevice = mkchromecast.__init__.adevice
        self.debug = mkchromecast.__init__.debug
        self.ccname = mkchromecast.__init__.ccname
        self.videoarg = mkchromecast.__init__.videoarg
        self.youtubeurl = mkchromecast.__init__.youtubeurl
        self.tray = mkchromecast.__init__.tray
        self.discover = mkchromecast.__init__.discover
        self.source_url = mkchromecast.__init__.sourceurl
        self.encoder_backend = mkchromecast.__init__.backend
        self.select_cc = mkchromecast.__init__.select_cc
        self.control = mkchromecast.__init__.control

        self.cc = casting()
        checkmktmp()
        writePidFile()

        """
        Initializing backend array
        """
        self.backends = [
          'ffmpeg',
          'avconv',
          'parec',
          'gstreamer'
          ]

        self.check_connection()
        if self.tray == False and self.videoarg == False:
            if self.platform == 'Linux':
                self.audio_linux()
            else:
                self.audio_macOS()
        elif self.tray == False and self.videoarg == True:
            self.cast_video()
        else:
            self.start_tray()

    def audio_linux(self):
        """This method manages all related to casting audio in Linux"""
        if self.youtubeurl == None and self.source_url == None:
            if adevice == None:
                print('Creating Pulseaudio Sink...')
                print(colors.warning('Open Pavucontrol and Select the Mkchromecast Sink.'))
                create_sink()
            print(colors.important('Starting Local Streaming Server'))
            print(colors.success('[Done]'))
            self.start_backend(self.encoder_backend)
            self.cc.initialize_cast()
            self.get_cc(self.select_cc)
            self.cc.play_cast()
            self.show_control(self.control)

        elif self.youtubeurl == None and self.source_url != None:
            self.start_backend(self.encoder_backend)
            self.cc.initialize_cast()
            self.get_cc(self.select_cc)
            self.cc.play_cast()
            self.show_control(self.control)

        elif youtubeurl != None and self.videoarg == False: # When casting youtube url, we do it through the audio module
            import mkchromecast.audio
            mkchromecast.audio.main()
            self.cc.initialize_cast()
            self.get_cc(self.select_cc)
            self.cc.play_cast()
            self.show_control(self.control)

    def audio_macOS(self):
        """This method manages all related to casting audio in macOS"""
        if self.youtubeurl == None and self.source_url == None:
            self.start_backend(self.encoder_backend)
            self.cc.initialize_cast()
            self.get_cc(self.select_cc)

            print('Switching to SoundFlower...')
            inputdev()
            outputdev()
            print(colors.success('[Done]'))
            self.cc.play_cast()
            self.show_control(self.control)

        elif self.youtubeurl == None and self.source_url != None:
            self.start_backend(self.encoder_backend)
            self.cc.initialize_cast()
            self.get_cc(self.select_cc)
            self.cc.play_cast()
            self.show_control(self.control)

            print('Switching to SoundFlower...')
            inputdev()
            outputdev()
            print(colors.success('[Done]'))
            self.cc.play_cast()
            self.show_control(self.control)

        elif self.youtubeurl != None and self.videoarg == False: # When casting youtube url, we do it through the audio module
            import mkchromecast.audio
            mkchromecast.audio.main()
            self.cc.initialize_cast()
            self.get_cc(self.select_cc)
            self.cc.play_cast()
            self.show_control(self.control)

    def cast_video(self):
        """This method launches video casting"""
        print(colors.important('Starting Video Cast Process...'))
        import mkchromecast.video
        mkchromecast.video.main()
        self.cc.initialize_cast()
        self.get_cc(self.select_cc)
        self.cc.play_cast()
        self.show_control(self.control)

    def get_cc(self, select_cc):
        """Get chromecast name, and let user select one from a list if
        select_cc flag is True.
        """
        if select_cc == True: # This is done for the case that -s is passed
            self.cc.sel_cc()
            self.cc.inp_cc()
            self.cc.get_cc()
        else:
            self.cc.get_cc()

    def start_backend(self, encoder_backend):
        """Starting backends"""
        if encoder_backend == 'node' and self.source_url == None:
            from mkchromecast.node import stream
            stream()
        elif encoder_backend in self.backends and self.source_url == None:
            import mkchromecast.audio
            mkchromecast.audio.main()

    def check_connection(self):
        """Check if the computer is connected to a network"""
        if self.cc.ip == '127.0.0.1':        # We verify the local IP.
            print(colors.error('Your Computer is not Connected to Any Network'))
            terminate()
        elif self.cc.ip != '127.0.0.1' and self.discover == True:
            self.cc.initialize_cast()
            terminate()

    def terminate_app(self):
        """Terminate the app (kill app)"""
        self.cc.stop_cast()
        if platform == 'Darwin':
            inputint()
            outputint()
        elif platform == 'Linux' and adevice == None:
            remove_sink()
        terminate()

    def controls_msg(self):
        """Messages shown when controls is True"""
        print('')
        print(colors.important('Controls:'))
        print(colors.important('========='))
        print('')
        print(colors.options(           'Volume Up:')+' u')
        print(colors.options(         'Volume Down:')+' d')
        if videoarg == True:
            print(colors.options(       'Pause Casting:')+' p')
            print(colors.options(      'Resume Casting:')+' r')
        print(colors.options('Quit the Application:')+' q or Ctrl-C')
        print('')

    def show_control(self, control):
        """Method to show controls"""
        if control == True:
            from mkchromecast.getch import getch, pause

            self.controls_msg()
            try:
                while(True):
                    key = getch()
                    if(key == 'u'):
                        self.cc.volume_up()
                        if self.encoder_backend == 'ffmpeg':
                            if self.debug == True:
                                self.controls_msg()
                    elif(key == 'd'):
                        self.cc.volume_down()
                        if self.encoder_backend == 'ffmpeg':
                            if self.debug == True:
                                self.controls_msg()
                    elif(key == 'p'):
                        if self.videoarg == True:
                            print('Pausing Casting Process...')
                            action = 'pause'
                            self.backend_handler(action, self.encoder_backend)
                            if self.encoder_backend == 'ffmpeg':
                                if self.debug == True:
                                    self.controls_msg()
                        else:
                            pass
                    elif(key == 'r'):
                        if self.videoarg == True:
                            print('Resuming Casting Process...')
                            action = 'resume'
                            self.backend_handler(action, self.encoder_backend)
                            if self.encoder_backend == 'ffmpeg':
                                if self.debug == True:
                                    self.controls_msg()
                        else:
                            pass
                    elif(key == 'q'):
                        print(colors.error('Quitting application...'))
                        self.terminate_app()
                    elif(key == '\x03'):
                        raise KeyboardInterrupt
                        atexit.register(self.terminate_app())
            except KeyboardInterrupt:
                self.terminate_app()

        else:
            if self.platform == 'Linux' and self.adevice == None:
                print(colors.warning('Remember to open pavucontrol and select the mkchromecast sink.'))
            print('')
            print(colors.error('Ctrl-C to kill the Application at any Time'))
            print('')
            signal.signal(signal.SIGINT,
                          lambda *_: atexit.register(self.terminate_app()))
            signal.signal(signal.SIGTERM,
                          lambda *_: atexit.register(self.terminate_app()))
            signal.pause()

    def backend_handler(self, action, backend):
        """Methods to handle pause and resume state of backends"""
        if action == 'pause' and backend == 'ffmpeg':
            subprocess.call(['pkill', '-STOP', '-f', 'ffmpeg'])
        elif action == 'resume' and backend == 'ffmpeg':
            subprocess.call(['pkill', '-CONT', '-f', 'ffmpeg'])
        elif action == 'pause' and backend == 'node' and self.platform == 'Linux':
            subprocess.call(['pkill', '-STOP', '-f', 'nodejs'])
        elif action == 'resume' and backend == 'node' and self.platform == 'Linux':
            subprocess.call(['pkill', '-CONT', '-f', 'nodejs'])
        elif action == 'pause' and backend == 'node' and self.platform == 'Darwin':
            subprocess.call(['pkill', '-STOP', '-f', 'node'])
        elif action == 'resume' and backend == 'node' and self.platform == 'Darwin':
            subprocess.call(['pkill', '-CONT', '-f', 'node'])

    def start_tray(self):
        """This method starts the system tray"""
        import mkchromecast.systray
        checkmktmp()
        writePidFile()
        mkchromecast.systray.main()

if __name__ == "__main__":
    mk()

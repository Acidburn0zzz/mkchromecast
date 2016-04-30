#!/usr/bin/env python

# This file is part of mkchromecast.

from __future__ import print_function
from .__init__ import *
import time
import pychromecast
import socket
from .terminate import *
from .audiodevices import *
import os.path
import pickle

class casting(object):
    def __init__(self): ## __init__ to call the self.ip
        self.ip = socket.gethostbyname(socket.gethostname())

    def initialize_cast(self):
        from pychromecast import socket_client
        self.cclist = list(pychromecast.get_chromecasts_as_dict().keys())

        import mkchromecast.__init__        # This is to verify against some needed variables
        self.platform = mkchromecast.__init__.platform
        try:
            self.youtubeurl = mkchromecast.__init__.youtubeurl
        except AttributeError:
            self.youtubeurl = None

        if len(self.cclist) != 0 and args.select_cc == False:
            print(' ')
            print('List of Google Cast devices available in your network:')
            print('------------------------------------------------------')
            print(' ')
            print('Index   Friendly name')
            print('=====   ============= ')
            for self.index,device in enumerate(self.cclist):
                print(str(self.index)+'      ', str(device))
            print(' ')
            print('We will cast to first device in the list above!')
            print(' ')
            self.castto = self.cclist[0]
            print(self.castto)
            print(' ')

        elif len(self.cclist) != 0 and args.select_cc == True:
            if os.path.exists('/tmp/mkcrhomecast.tmp') == False:
                self.tf = open('/tmp/mkcrhomecast.tmp', 'wb')
                print(' ')
                print('List of Google Cast devices available in your network:')
                print('------------------------------------------------------')
                print(' ')
                print('Index   Friendly name')
                print('=====   ============= ')
                self.availablecc=[]
                for self.index,device in enumerate(self.cclist):
                    print(str(self.index)+'      ',str(device))
                    toappend = [self.index,device]
                    self.availablecc.append(toappend)
                #print ('Array')
                #print (availablecc)

            else:
                self.tf = open('/tmp/mkcrhomecast.tmp', 'rb')
                self.index=pickle.load(self.tf)
                self.castto = self.cclist[int(self.index)]
                print(' ')
                print('Casting to: ', self.castto)
                print(' ')

        elif len(self.cclist) != 0 and args.select_cc == False and args.tray == True :
                self.tf = open('/tmp/mkcrhomecast.tmp', 'rb')
                self.index=pickle.load(self.tf)
                self.castto = self.cclist[int(self.index)]
                print(' ')
                print('Casting to: ', self.castto)

        elif len(self.cclist) == 0 and args.tray == False:
            print('No devices found!')
            if self.platform == 'Linux':
                import mkchromecast.pulseaudio
                mkchromecast.pulseaudio.remove_sink()
            else:
                inputint()
                outputint()
            terminate()
            exit()

        elif len(self.cclist) == 0 and args.tray == True:
            print('No devices found!')
            self.availablecc = []

    def sel_cc(self):
            print(' ')
            print('Please, select the index of the Google Cast device that you want to use:')
            self.index = input()

    def inp_cc(self):
            pickle.dump(self.index, self.tf)
            self.tf.close()
            self.castto = self.cclist[int(self.index)]
            print(' ')
            print('Casting to: ', self.castto)
            print(' ')

    def get_cc(self):
            self.cast = pychromecast.get_chromecast(self.castto)
            # Wait for cast device to be ready
            self.cast.wait()
            print(' ')
            print('Information about ', self.castto)
            print(' ')
            print(self.cast.device)
            print(' ')
            print('Status of device ', self.castto)
            print(' ')
            print(self.cast.status)
            print(' ')

    def play_cast(self):
        if self.platform == 'Linux':
            import commands
            localip = commands.getoutput("hostname -I").strip()
        else:
            start = casting()
            localip = start.ip

        print ('Your local IP is: ', localip)


        if self.youtubeurl != None:
            print ('The Youtube URL chosen: ', youtubeurl)
            import pychromecast.controllers.youtube as youtube
            yt = youtube.YouTubeController()
            self.cast.register_handler(yt)
            try:
                import urlparse
                url_data = urlparse.urlparse(youtubeurl)
                query = urlparse.parse_qs(url_data.query)
            except ImportError:
                import urllib.parse
                url_data = urllib.parse.urlparse(youtubeurl)
                query = urllib.parse.parse_qs(url_data.query)
            video = query["v"][0]
            print ('Playing video: ', video)
            yt.play_video(video)
        else:
            ncast = self.cast
            if args.encoder_backend == 'ffmpeg':
                import mkchromecast.ffmpeg
                mtype = mkchromecast.ffmpeg.mtype
                print(' ')
                print ('The media type string used is: ',mtype)
                ncast.play_media('http://'+localip+':5000/stream', mtype)
            else:
                print(' ')
                print ('The media type string used is: audio/mpeg')
                ncast.play_media('http://'+localip+':3000/stream.mp3', 'audio/mpeg')
            print(' ')
            print('Cast media cotroller status')
            print(' ')
            print(ncast.status)
            print(' ')

    def stop_cast(self):
        ncast = self.cast
        ncast.quit_app()

    def volume_up(self):
        """ Increment volume by 0.1 unless it is already maxed.
        Returns the new volume.
        """
        ncast = self.cast
        volume = round(ncast.status.volume_level, 1)
        return ncast.set_volume(volume + 0.1)

    def volume_down(self):
        """ Decrement the volume by 0.1 unless it is already 0.
        Returns the new volume.
        """
        ncast = self.cast
        volume = round(ncast.status.volume_level, 1)
        return ncast.set_volume(volume - 0.1)

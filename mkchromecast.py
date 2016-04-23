#!/usr/bin/env python

# This file is part of mkchromecast.

from mkchromecast.audiodevices import *
from mkchromecast.cast import *
from mkchromecast.terminate import *
import os.path, time

import atexit

if args.tray == False:

    cc = casting()
    checkmktmp()
    writePidFile()

    if cc.ip == '127.0.0.1' or None:        # We verify the local IP.
        print ('Your computer is not connected to any network')
        terminate()

    if args.youtube == None:
        print('Switching to soundflower...')
        outputdev()
        print('Done!')

        print('Starting local streaming server')
        if args.encoder_backend == 'node':
            from mkchromecast.node import *
            stream()

        if args.encoder_backend == 'ffmpeg':
            import mkchromecast.ffmpeg
            mkchromecast.ffmpeg.main()

    cc.initialize_cast()

    if args.select_cc == True: # This is done for the case that -s is passed
        cc.sel_cc()
        cc.inp_cc()
        cc.get_cc()
        cc.play_cast()
    else:
        cc.get_cc()
        cc.play_cast()


    def terminateapp():
        cc.stop_cast()
        inputint()
        outputint()
        terminate()
        return

    try:
        volumearg = mkchromecast.__init__.volumearg
    except AttributeError:
        volumearg = False

    if volumearg == True:
        from getch import getch, pause

        print('Controls:')
        print('========')
        print('')
        print('Volume up: u')
        print('Volume up: d')
        print('Quit the application: q')
        print('')
        try:
            while(True):
                key = getch()
                if(key == 'u'):
                    print('Increasing volume...')
                    cc.volume_up()
                elif(key == 'd'):
                    print('Decreasing volume...')
                    cc.volume_down()
                elif(key == 'q'):
                    print('Quitting application...')
                    terminateapp()
        except KeyboardInterrupt:
            terminateapp()

    else:
        print('Ctrl-C to kill the application at any time')
        print('')
        try:
            input()
        except KeyboardInterrupt:
            atexit.register(terminateapp)
else:
    import mkchromecast.systray
    checkmktmp()
    writePidFile()
    mkchromecast.systray.main()

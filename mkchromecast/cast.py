#!/usr/bin/env python

# This file is part of mkchromecast.

# mkchromecast is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# mkchromecast is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with mkchromecast.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
import time
import pychromecast
import socket
from .terminate import *
from .audiodevices import *

class casting(object):

    def __init__(self): ## __init__ to call the self.ip
        self.ip = socket.gethostbyname(socket.gethostname())

    def initialize_cast(self):
        from pychromecast import socket_client
        self.listofcc = pychromecast.get_chromecasts_as_dict().keys()

        if len(self.listofcc) != 0:
            print('List of CC in your network')
            print(self.listofcc)
        else:
            print('No devices found!')
            inputint()
            outputint()
            terminate()
            exit()

    def get_cc(self):
            # For the moments it casts to the first device in the list
            self.cast = pychromecast.get_chromecast(self.listofcc[0])
            # Wait for cast device to be ready
            self.cast.wait()
            print(self.cast.device)
            print(self.cast.status)

    def play_cast(self):
        start = casting()
        localip = start.ip
        print (localip)
        ncast = self.cast
        ncast.play_media('http://'+localip+':3000/stream.mp3', 'audio/mpeg')
        print(ncast.status)

    def stop_cast(self):
        ncast = self.cast
        ncast.quit_app()

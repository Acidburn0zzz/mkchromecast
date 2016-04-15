#!/usr/bin/env python

# This file is part of mkchromecast.

"""
Google cast device has to point out to http://ip:5000/stream
"""

import mkchromecast.__init__
import os
from functools import partial
from subprocess import Popen, PIPE
from flask import Flask, Response
import multiprocessing

mp3file = 'stream'

codec = mkchromecast.__init__.codec

if  codec == 'mp3':
    appendmtype = 'mpeg'
elif codec == 'aac':
    appendmtype = 'mp4' #This is the container used
else:
    appendmtype = codec

mtype = 'audio/'+appendmtype

"""
MP3 192k
"""
if  codec == 'mp3':
    command = ['ffmpeg', '-re', '-f', 'avfoundation', '-audio_device_index', '0', '-i', '', '-acodec', 'libmp3lame', '-f', 'mp3', '-b:a', '192k','pipe:1']

"""
OGG 192k
"""
if  codec == 'ogg':
    command = ['ffmpeg', '-re', '-f', 'avfoundation', '-audio_device_index', '0', '-i', '', '-acodec', 'libvorbis', '-f', 'ogg', '-b:a', '192k','pipe:1']

"""
AAC 128k for Stereo
"""
if  codec == 'aac':
    command = ['ffmpeg', '-re', '-f', 'avfoundation', '-audio_device_index', '0', '-i', '', '-acodec', 'libfdk_aac', '-f', 'adts', '-b:a', '128k','pipe:1']

"""
WAV 24-Bit
"""
if  codec == 'wav':
    command = ['ffmpeg', '-re', '-f', 'avfoundation', '-audio_device_index', '0', '-i', '', '-acodec', 'pcm_s24le', '-f', 'wav', '-ac', '2','pipe:1']

"""
FLAC 24-Bit
"""
if  codec == 'flac':
    command = ['ffmpeg', '-re', '-f', 'avfoundation', '-audio_device_index', '0', '-i', '', '-acodec', 'flac', '-f', 'flac', 'pipe:1']
app = Flask(__name__)

@app.route('/')
def index():
    return """<!doctype html>
<title>Play {mp3file}</title>
<audio controls autoplay >
    <source src="{mp3file}" type="audio/mp3" >
    Your browser does not support this audio format.
</audio>""".format(mp3file=mp3file)


@app.route('/' + mp3file)
def stream():
    process = Popen(command, stdout=PIPE, bufsize=-1)
    read_chunk = partial(os.read, process.stdout.fileno(), 1024)
    return Response(iter(read_chunk, b''), mimetype=mtype)

def start_app():
    app.run(host= '0.0.0.0')

class multi_proc(object):
    def __init__(self):
        self.proc = multiprocessing.Process(target=start_app)
        self.proc.daemon = True

    def start(self):
        self.proc.start()

def main():
    st = multi_proc()
    st.start()

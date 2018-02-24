#!/usr/bin/env python

# This file is part of mkchromecast.

import psutil
import pickle
from os import getpid
import os.path
import mkchromecast.colors as colors

try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse

"""
To call them:
    from mkchromecast.terminate import name
    name()
"""


def terminate():
    del_tmp()
    parent_pid = getpid()
    parent = psutil.Process(parent_pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()
    return


def del_tmp():
    """Delete files created in /tmp/"""
    delete_me = ['/tmp/mkchromecast.tmp', '/tmp/mkchromecast.pid']

    print(colors.important('Cleaning up /tmp/...'))

    for f in delete_me:
        if os.path.exists(f) is True:
            os.remove(f)

    print(colors.success('[Done]'))
    return


def is_installed(name, path, debug):
    PATH = path
    iterate = PATH.split(':')
    for item in iterate:
        verifyif = str(item + '/' + name)
        if os.path.exists(verifyif) is False:
            continue
        else:
            if debug is True:
                print('Program %s found in %s.' % (name, verifyif))
            return True
    return


def check_url(url):
    """Check if a URL is correct"""
    try:
        result = urlparse(url)
        return True if [result.scheme, result.netloc, result.path] else False
    except Exception as e:
        return False


def writePidFile():
    # This is to verify that pickle tmp file exists
    if os.path.exists('/tmp/mkchromecast.pid') is True:
        os.remove('/tmp/mkchromecast.pid')
    pid = str(os.getpid())
    f = open('/tmp/mkchromecast.pid', 'wb')
    pickle.dump(pid, f)
    f.close()
    return


def checkmktmp():
    # This is to verify that pickle tmp file exists
    if os.path.exists('/tmp/mkchromecast.tmp') is True:
        os.remove('/tmp/mkchromecast.tmp')
    return

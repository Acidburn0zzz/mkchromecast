# This file is part of mkchromecast.

import subprocess
import time

_sink_num = None


def create_sink():
    global _sink_num

    sink_name = "Mkchromecast"

    create_sink = ["pactl", "load-module", "module-null-sink", "sink_name=" + sink_name, "sink_properties=device.description=" + sink_name]

    cs = subprocess.Popen(create_sink, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    csoutput, cserror = cs.communicate()
    _sink_num = csoutput[:-1]

    return


def remove_sink():
    if _sink_num is None:
        return

    remove_sink = ["pactl", "unload-module", _sink_num]

    rms = subprocess.Popen(remove_sink, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    rmsoutput, rmserror = rms.communicate()
    return


def check_sink():
    try:
        check_sink = ["pacmd", "list-sinks"]
        chk = subprocess.Popen(
            check_sink, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        chkoutput, chkerror = chk.communicate()
    except FileNotFoundError:
        return None

    try:
        if "Mkchromecast" in chkoutput:
            return True
        else:
            return False
    except TypeError:
        if "Mkchromecast" in chkoutput.decode("utf-8"):
            return True
        else:
            return False

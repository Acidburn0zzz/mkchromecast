mkchromecast
============
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/muammar/mkchromecast/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/pyversions/pychromecast.svg?maxAge=2592000)](https://github.com/muammar/mkchromecast/)
[![node](https://img.shields.io/node/v/gh-badges.svg?maxAge=2592000)](https://github.com/muammar/mkchromecast/blob/master/nodejs/)
[![GitHub
release](https://img.shields.io/github/release/muammar/mkchromecast.svg)](https://github.com/muammar/mkchromecast/releases)

This is a program to cast your **Mac OS X** audio, or **Linux** audio to your
Google Cast devices.

It is written in Python, and it can stream via `node.js`, `parec` (Linux only),
`ffmpeg`, or `avconv`.  **mkchromecast** is capable of using lossy and lossless
audio formats provided that `ffmpeg` is installed. Additionally, a system tray
menu is also available.

By default, **mkchromecast** streams with `node.js` (or `parec` in **Linux**)
together with `mp3` audio coding format at a sample rate of `44100Hz` and
average bitrate of `192k`.  These defaults can be changed using the
`--sample-rate` and `-b` flags. It is useful to modify these parameters when
your wireless router is not very powerful like mine, or in the case you don't
want to degrade the sound quality. For more information visit the
[wiki](https://github.com/muammar/mkchromecast/wiki/), and the
[FAQ](https://github.com/muammar/mkchromecast/wiki/FAQ) for more information.

For **Linux**, you can optionally install `ffmpeg` (or `avconv`) together with
`pulseaudio` ([more information
here](https://github.com/muammar/mkchromecast/wiki/Linux)).  Note that sometimes the lag
between playing a song and hearing may be of 8 seconds.

Requirements:
------------

#### Mac OS X

In order to use **mkchromecast** you need the following software to stream with
`node.js`:

* Python2 (already shipped in OS X), or Python3.
* pychromecast.
* psutil.
* mutagen.
* [Soundflower](https://github.com/mattingalls/Soundflower/).
* py_getch (optional if you want to control the volume of the Google cast
  device).
* PyQt5 (optional if you want to use the system tray menu).

For more control, you need `ffmpeg` as backend.  In that case install
following:

* flask (optional).
* ffmpeg (optional).

#### Linux

* Pulseaudio.
* Python2, or Python3.
* pychromecast.
* psutil.
* mutagen.
* flask.
* vorbis-tools.
* sox.
* lame.
* flac.
* faac.
* ffmpeg (optional).
* avconv (optional).
* py_getch (optional if you want to control the volume of the Google cast
  device).
* PyQt5 (optional if you want to use the system tray menu).

Install
-------

There are two ways of installing this application:

1. Using the binaries.
2. From sources.

#### Binaries

##### Mac OS X

There is available a standalone application for Mac OS X users. You need to
drag it to your `/Applications/` folder. It works just with the `node` backend.

[Download the latest dmg
here](https://github.com/muammar/mkchromecast/releases/).
You need also to [install
Soundflower](https://github.com/muammar/mkchromecast#soundflower-mac-users-only).

###### Homebrew Cask

Now it is possible to install the binary as follows:

```
brew cask install mkchromecast
```

If you find any problem with the application, please [report it
here](https://github.com/muammar/mkchromecast/issues).

##### Linux

* Debian
* Ubuntu

Download the latest [deb package
here](https://github.com/muammar/mkchromecast/releases/), and install it as
follows:

```
sudo dpkg -i mkchromecast_$VERSION_all.deb
```

where `$VERSION = X.Y.Z-Rev`, _e.g._: `0.2.6-1`. Then, if the dependencies are
not available you have to do:

```
sudo apt-get -f install
```

This should work in Debian Unstable and Testing. I would appreciate Ubuntu
testers as well. If you find any problems, please [report it
here](https://github.com/muammar/mkchromecast/issues).

#### From sources

To install **mkchromecast**, clone this repository:

```
git clone https://github.com/muammar/mkchromecast.git
```

Or you may download one of the [stable releases
here](https://github.com/muammar/mkchromecast/releases), and unzip the file.

##### Python

To install the python requirements use the `requirements.txt` file shipped in
this repository:

```
pip install -r requirements.txt
```

**Note**: if this step fails, maybe you need to run the installation with
`sudo` as shown below. However, before installing using this method verify why
a regular user cannot install the requirements.

```
sudo pip install -r requirements.txt
```

**Linux** users can try to install these python requirements using the package
managers coming with their distributions.

Example for Debian based distros:

```
sudo apt-get install python2.7 python-pip python-pychromecast python-flask python-psutil python-setuptools python-mutagen python-gi vorbis-tools sox lame flac faac opus-tools
```

Additionally, using `pip` you need:

```
pip install py_getch
```

##### Soundflower (Mac users only)

For Soundflower you can check
[https://github.com/mattingalls/Soundflower/](https://github.com/mattingalls/Soundflower/)
or if you have [Homebrew](http://brew.sh/) you can use [brew
cask](https://caskroom.github.io/) as follows:

```
brew cask install soundflower
```

Or just download the [latest dmg
file](https://github.com/mattingalls/Soundflower/releases).

By default, the sample rate in Soundflower is set to `44100Hz`. If you desire
to stream at higher sample rates follow the [instructions in the wiki](https://github.com/muammar/mkchromecast/wiki/Soundflower).

**Note**: re-sampling to higher sample rates is not a good idea. It was indeed
an issue in the chromecast audio. See [this thread](https://goo.gl/yNVODZ).
Therefore, if you want to go beyond `44100Hz` you have to [capture the sound at
a higher sample rate](https://github.com/muammar/mkchromecast/wiki/Soundflower).

##### ffmpeg or avconv

The easiest way of installing `ffmpeg` is using a package manager, *e.g.*: brew,
macports or fink. Or in the case of Linux, *e.g.*: apt, yum, or pacman.

###### Mac OS X

I will briefly describe the case of Homebrew here. First, you will need
Homebrew:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Once Homebrew is ready, you can install `ffmpeg`.  As stated in the [ffmpeg
website](https://trac.ffmpeg.org/wiki/CompilationGuide/MacOSX), and for using
all audio coding formats in **mkchromecast**, it is better to install some
additional `ffmpeg`'s options:

```
brew install ffmpeg --with-fdk-aac --with-ffplay --with-freetype --with-libass --with-libquvi --with-libvorbis --with-libvpx --with-opus --with-x265
```

**mkchromecast** does not support `avconv` in Mac OS X.

###### Linux

As I use Debian, the way of installing `ffmpeg` is:

```
apt-get install ffmpeg
```
or

```
apt-get install libav-tools
```

**Audio coding formats available with `ffmpeg` and `avconv`**

**Audio coding format** | **Description**                   | **Notes**
------------------------| ----------------------------------|------------------
  `mp3`                 | MPEG Audio Layer III (default)    | Lossy compression format (default bitrate: 192k)
  `ogg`                 | Ogg Vorbis                        | Lossy compression format (default bitrate: 192k)
  `aac`                 | Advanced Audio Coding (AAC)       | Lossy compression format (default bitrate: 192k)
  `wav`                 | Waveform Audio File Format        | Lossless format (HQ sound)
  `flac`                | Free Lossless Audio Codec         | Lossless format (HQ sound)


##### PyQt5

These Python bindings are needed if you intend to use the system tray menu. As
of today April 28th, `pip` is able to install `PyQt5`. Therefore, you can do
a `pip install pyqt5`.

If this does not work for you, I suggest you to install it using a package
manager.

###### Mac OS X

Example with Homebrew:

```
brew install pyqt5 --with-python
```

###### Linux

* **Debian**

For Python2:

```
apt-get install python-pyqt5
```

For Python3:

```
apt-get install python3-pyqt5
```

or if you desire it you can do it yourself from the sources.

Updating
--------

To update **mkchromecast** sources, just get into the cloned directory and:

```
git pull
```

or if you prefer just pass the `--update` argument to `mkchromecast`:

```
python mkchromecast.py --update
```

If you are using the Mac OS X application, [download the latest dmg
here](https://github.com/muammar/mkchromecast/releases/), and replace the
`mkchromecast.app` in your `/Applications/` directory.

Usage
-----

Get into the cloned **mkchromecast** directory and execute:

```
python mkchromecast.py
```

This will launch **mkchromecast** using `node.js` (or `parec` for **Linux**
users), and will do the streaming part together with the `mp3` audio coding
format.  `node.js` works decently, **however** I would like to point out that
the node version of this implementation is ancient. Moreover, the `node.js`
server tends to _fail_. In such a case, **mkchromecast** is able to restart the
streaming/casting process automatically. So, some hiccups are expected.

**Note**: most of the steps described herein are the same for Mac and Linux
users. However, if you launch the command above in **Linux**, the process is
less automatized.  In **Linux**, you need to select with `pavucontrol` the sink
called `mkchromecast` to stream.  See the [wiki for more
information](https://github.com/muammar/mkchromecast/wiki/Linux). tl;dr?, just
check the gif below.

![Example of using mkchromecast](https://raw.githubusercontent.com/muammar/mkchromecast/master/images/mkchromecast_linux.gif)

##### Using the `ffmpeg` backend with **mkchromecast** installed from sources

Below an example using `mp3`:

```
python mkchromecast.py --encoder-backend ffmpeg
```

This is way more stable than the `node` implementation in Mac. With `ffmpeg`
you can modify the codec:

```
python mkchromecast.py --encoder-backend ffmpeg -c aac
```

change the bitrate and sample rate:

```
python mkchromecast.py --encoder-backend ffmpeg -c mp3 -b 128 --sample-rate 31000
```

check the section
[https://github.com/muammar/mkchromecast#soundflower-mac-users-only](https://github.com/muammar/mkchromecast#soundflower-mac-users-only)
for more about sample rates.

##### Other examples with **mkchromecast** installed using the debian package

```
mkchromecast --encoder-backend ffmpeg -c wav
```

There is also an option to change the `bitrate`:

```
mkchromecast --encoder-backend ffmpeg -c ogg -b 128
```

and another one to change the sampling rate:

```
mkchromecast --encoder-backend ffmpeg -c ogg -b 128 --sample-rate 48000
```

**Note**: to use `avconv` just replace from `ffmpeg` to `avconv` in the
commands above.

#### Playing Youtube URLs in Google Cast TV

You can play Youtube URLs headlessly from the command line:

```
python mkchromecast.py -y https://www.youtube.com/watch\?v\=NVvAJhZVBT
```

**Note**: you may need to enclose the URL between quotation marks. This does
not work in Google Cast audio.

#### Controlling the Google Cast volume

You can control the volume of your Google Cast device by launching
**mkchromecast** with the option `--volume`:

```
python mkchromecast.py --encoder-backend ffmpeg -c ogg -b 320 --volume
```

This will allow you to press <kbd>u</kbd> and <kbd>d</kbd> keys for `volume up`
and `volume down` respectively.

**Note**: you need the module `py-getch` for this option to work. You can
install it using the `requirements.txt` file shipped in the repository as
described above.

More help
---------

To get more help:

```
python mkchromecast.py -h
```

or when installing the debian package:

```
mkchromecast -h
```


Killing the application
-----------------------

To kill **mkchromecast** when you run it from console, there are two ways of
doing it: if you didn't use the `--volume` option, just press
<kbd>Ctrl-C</kbd>. Otherwise, you will need to press the
<kbd>q</kbd> key to quit.

Notes
-----

A **beta** system tray menu is now provided. It requires you to install
`PyQt5`. To launch it:

```
python mkchromecast.py -t
```

or


```
mkchromecast -t
```

Additionally, Mac OS X users can install the standalone app.

It looks like:

##### Mac OS X

[![Example](https://raw.githubusercontent.com/muammar/mkchromecast/master/images/screencast.png)](https://www.youtube.com/embed/d9Qn_LltOjU)

##### Linux

Check these images:

* [Gnome 1](https://raw.githubusercontent.com/muammar/mkchromecast/master/images/Gnome1.png)
* [Gnome 2](https://raw.githubusercontent.com/muammar/mkchromecast/master/images/Gnome2.png)
* [KDE5 1](https://raw.githubusercontent.com/muammar/mkchromecast/master/images/Kde5_1.png)
* [KDE5 2](https://raw.githubusercontent.com/muammar/mkchromecast/master/images/Kde5_2.png)

**Note**: you can set all options described above using the `preferences` in
the system tray.

Known issues
------------

##### Mac OS X

No new issues reported.

##### Linux

When using `parec` and `lame` encoder, the delay between audio played and
listened can be up to 8 seconds. I suggest you to use something different than
mp3.

You can also check the [FAQ](https://github.com/muammar/mkchromecast/wiki/FAQ)
for more information.

TODO
----

* Verify all exceptions when the system tray menu fails.
* Check that the index of the cast selected is correctly passed in the
system tray.
* Video?.

Contribute
----------

If you want to contribute, help me improving this application by [reporting
issues](https://github.com/muammar/mkchromecast/issues), [creating pull
requests](https://github.com/muammar/mkchromecast/pulls), or you may also buy
me some pizza :).

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JQGD4UXPBS96U)

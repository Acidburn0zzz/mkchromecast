mkchromecast
============

This is a tiny program to cast your **Mac OS X** audio to your google cast
devices. It is written in Python, and it streams using node.js, or ffmpeg.

For Linux you have a program called
[pulseaudio-dlna](https://github.com/masmu/pulseaudio-dlna) that does this
beautifully.

### Requirements:

In order to use **mkchromecast** you need the following software to stream with
node.js:

* Python2 (already shipped in OS X), or Python3.
* pychromecast.
* psutil.
* mutagen.
* [Soundflower](https://github.com/mattingalls/Soundflower/).
* PyQt5 for the system tray (optional if you want to use the system tray menu).

If you want more control, you may want to use ffmpeg as backend. In that case
you need the following:

* flask (optional).
* ffmpeg (optional).

### Installation and updating

To install **mkchromecast**, clone this repository:

```
git clone https://github.com/muammar/mkchromecast.git
```

Or you may download one of the [stable releases
here](https://github.com/muammar/mkchromecast/releases), and unzip the file.

#### Python

To install the python requirements use the `requirements.txt` file shipped in
this repository:

```
pip install -r requirements.txt
```

_Note_: if this step fails, maybe you will need to run the installation with
`sudo` as shown below. However, before installing using this method verify why
a regular user cannot install the requirements.

```
sudo pip install -r requirements.txt
```

#### Soundflower

For Soundflower you can check
[https://github.com/mattingalls/Soundflower/](https://github.com/mattingalls/Soundflower/)
or if you have [Homebrew](http://brew.sh/) you can use [brew
cask](https://caskroom.github.io/) to install it as follows:

```
brew cask install soundflower
```

Or just download the [latest dmg
file](https://github.com/mattingalls/Soundflower/releases).

#### ffmpeg

The easiest way of installing ffmpeg is using a package manager, *e.g.* brew,
macports or fink.

I will briefly describe the case of Homebrew here. First, you will need to
install Homebrew:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Once Homebrew is ready, you can install ffmpeg as follows:

```
brew install ffmpeg
```

As stated in the [ffmpeg
website](https://trac.ffmpeg.org/wiki/CompilationGuide/MacOSX), it is better to
install some additional ffmpeg's options:

```
brew install ffmpeg --with-fdk-aac --with-ffplay --with-freetype --with-libass --with-libquvi --with-libvorbis --with-libvpx --with-opus --with-x265
```

When using ffmpeg, the following codecs are available:

- mp3  [192k]           MPEG Audio Layer III (default)
- ogg  [192k]           Ogg Vorbis
- aac  [128k]           Advanced Audio Coding (AAC)
- wav  [24-Bit, HQ]     Waveform Audio File Format
- flac [24-Bit, HQ]     Free Lossless Audio Codec

Example using wav:

```
python mkchromecast.py --encoder-backend ffmpeg -c wav
```

#### PyQt5

These Python bindings are needed if you intend to use the system tray menu.  As
previously said, I also suggest you to install it using Homebrew:

```
brew install pyqt5 --with-python
```

or if you desire it you can do it yourself from the sources.

#### Updating

To update **mkchromecast**, just get into the cloned directory and:

```
git pull
```

### How to execute it

Get into the cloned **mkchromecast** directory and execute:

```
python mkchromecast.py
```

To get help:

```
python mkchromecast.py -h
```

### Killing the application

To kill **mkchromecast** when you run it from console, just press `Ctrl-c`.

### Notes

A **beta** system tray menu is now provided. It requires you to install
`PyQt5`. To launch it:

```
python mkchromecast.py -t
```

It looks like:

![Image of
working menu](https://raw.githubusercontent.com/muammar/mkchromecast/master/images/screenshot.png)

**Note**:You can pass the options when using ffmpeg as backend and adding `-t`
to launch the system tray. I am still working on improving all of this.

### TODO

* Check all codecs used with ffmpeg, quality, and stability.
* Verify all exceptions when the system tray menu fails.
* Check that the index of the cast selected is correctly passed in the
system tray.
* Generate a standalone Mac OS X application.
* Video?.

### Contribute

If you want to contribute, help me improving this application by [reporting
issues](https://github.com/muammar/mkchromecast/issues), [creating pull
requests](https://github.com/muammar/mkchromecast/pulls), or you may also buy
me some pizza :).

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JQGD4UXPBS96U)

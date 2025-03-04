
# How to use it

## Dependencies (linux)

`configure` for bad apple requires `ffmpeg`
everything else requires `python3-pillow python3-opencv python3-numpy` (note packages may be named `python-<package>` rather than `python3-<package>` on your distro)
If you are on windows, use pip to install the packages.

## Install

First, configure the library with `./configure`
run by using `python3 .` or `python3 <bad apple repo directory>`
`image-to-ascii` is designed to be used from the command line so creating a symbolic link to it from `/usr/bin` or `/usr/local/bin` should allow it to be called like a normal command. (i have it symlinked to `see` for convenience)

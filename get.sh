#!/bin/bash
#
# get components to build ffmpeg

#wget http://downloads.sourceforge.net/faac/faac-1.28.tar.bz2
wget http://netcologne.dl.sourceforge.net/project/faac/faac-src/faac-1.28/faac-1.28.tar.bz2
tar xfj faac-1.28.tar.bz2
cd faac-1.28
wget http://www.linuxfromscratch.org/patches/blfs/svn/faac-1.28-glibc_fixes-1.patch
patch -Np1 -i faac-1.28-glibc_fixes-1.patch
sed -i -e '/obj-type/d' -e '/Long Term/d' frontend/main.c
cd ..
#wget http://sourceforge.net/projects/lame/files/lame/3.99/lame-3.99.5.tar.gz
wget http://kent.dl.sourceforge.net/project/lame/lame/3.99/lame-3.99.5.tar.gz
tar xfz lame-3.99.5.tar.gz
git clone git://git.videolan.org/x264.git
cd x264 && git checkout stable && cd ..
wget https://www.libsdl.org/release/SDL-1.2.15.tar.gz
tar xfz SDL-1.2.15.tar.gz
wget http://ffmpeg.org/releases/ffmpeg-2.6.3.tar.bz2
tar xfj ffmpeg-2.6.3.tar.bz2

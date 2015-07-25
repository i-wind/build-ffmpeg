#!/bin/bash

. shell/utils.sh

# get faac-1.28
get_faac() {
  if [ ! -e "faac-1.28.tar.bz2" ]; then
    download http://downloads.sourceforge.net/faac/faac-1.28.tar.bz2
  else
    echo "faac-1.28.tar.bz2 already exists..."
  fi
  if [ ! -d "faac-1.28" ]; then
    extract faac-1.28.tar.bz2
    # apply patch for faac
    cp ../patches/faac-1.28-glibc_fixes-1.patch faac-1.28/
    cd faac-1.28
    patch -Np1 -i faac-1.28-glibc_fixes-1.patch
    sed -i -e '/obj-type/d' -e '/Long Term/d' frontend/main.c
    cd ..
  fi
}

# get lame-3.99.5
get_lame() {
  if [ ! -e "lame-3.99.5.tar.gz" ]; then
    download http://sourceforge.net/projects/lame/files/lame/3.99/lame-3.99.5.tar.gz
  else
    echo "lame-3.99.5.tar.gz already exists..."
  fi
  [ -d "lame-3.99.5" ] || extract lame-3.99.5.tar.gz
}

# clone x264
get_x264() {
  if [ ! -d "x264" ]; then
    git clone git://git.videolan.org/x264.git
    cd x264 && git checkout stable && cd ..
  fi
}

# get SDL-1.2.15
get_sdl() {
  if [ ! -e "SDL-1.2.15.tar.gz" ]; then
    download https://www.libsdl.org/release/SDL-1.2.15.tar.gz
  else
    echo "SDL-1.2.15.tar.gz already exists..."
  fi
  if [ ! -d "SDL-1.2.15" ]; then
    extract SDL-1.2.15.tar.gz
    # apply patch for sdl
    cp ../patches/libsdl-1.2.15-const-xdata32.patch SDL-1.2.15/
    cd SDL-1.2.15
    patch -Np1 -i libsdl-1.2.15-const-xdata32.patch
    ./autogen.sh
    cd ..
  fi
}

# get ffmpeg
get_ffmpeg() {
  local version="$1"
  if [ ! -e "ffmpeg-${version}.tar.bz2" ]; then
    download http://ffmpeg.org/releases/ffmpeg-${version}.tar.bz2
  else
    echo "ffmpeg-${version}.tar.bz2 already exists..."
  fi
  [ -d "ffmpeg-${version}" ] || extract ffmpeg-${version}.tar.bz2
}

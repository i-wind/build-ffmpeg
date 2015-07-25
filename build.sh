#!/bin/bash
#
# get components to build ffmpeg

. shell/downloads.sh

FFMPEG_VERSION="$1"
[ -z $FFMPEG_VERSION ] && FFMPEG_VERSION="2.6.3"

mkdir -p build && cd build

get_faac
get_lame
get_x264
get_sdl
get_ffmpeg $FFMPEG_VERSION

ln -s ../Makefile.static Makefile >/dev/null 2>&1

exit 0

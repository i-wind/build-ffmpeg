Build FFMPEG on Linux
=====================

Build statically ffmpeg 2.6.3 on Linux with faac 1.28, lame 3.99.5, last stable x264 and SDL-1.2.15 (for ffplay).

Download compnents to build directory and patch faac and sdl

    $ ./build.sh

Build ffmpeg 2.6.3

    $ cd build
    $ make &

View logs when building

    $ tail -f `ls *.log |tail -1`

Results will be in ./usr directory

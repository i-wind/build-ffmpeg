Build FFMPEG on Linux
=====================

Build statically ffmpeg 2.6.3 on Linux with faac 1.28, lame 3.99.5, last stable x264 and SDL-1.2.15 (for ffplay).

Build ffmpeg 2.6.3

    $ python build.py >build_ffmpeg.log 2>&1 &

View logs when building

    $ tail -f build_ffmpeg.log

Results will be in ./usr directory

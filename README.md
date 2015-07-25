Build FFMPEG on Linux
=====================

Build statically ffmpeg with defined version on Linux with faac 1.28, lame 3.99.5, last stable x264 and SDL-1.2.15 (for ffplay).

Build ffmpeg (now default version 2.6.3)

    $ python build.py >build_ffmpeg.log 2>&1 &

or

    $ python build.py 2.0.3 >build_ffmpeg.log 2>&1 &

View logs when building

    $ tail -f build_ffmpeg.log

Results will be in ./usr directory

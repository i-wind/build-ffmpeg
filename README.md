Build FFMPEG on Linux
=====================

Build statically ffmpeg with defined version on Linux with faac 1.28, lame 3.99.5, last stable x264 and SDL-1.2.15 (for ffplay).

Build ffmpeg
------------

For now default build version of ffmpeg is 2.6.4

    $ python builder.py >build_ffmpeg.log 2>&1 &

or

    $ python builder.py -f 2.0.3 >build_ffmpeg.log 2>&1 &
    $ python builder.py --ffmpeg 2.7.2 >build_ffmpeg.log 2>&1 &

Help
----

    $ python builder.py --help

Logging
-------

View logs when building

    $ tail -f build_ffmpeg.log

Results
-------

Results will be in ./usr directory

Build FFMPEG on Linux
=====================

Build statically ffmpeg with defined version on Linux with faac 1.28, lame 3.99.5, last stable x264 and SDL-1.2.15 (for ffplay).

Build ffmpeg
------------

For now default build version of ffmpeg is 2.6.4

    $ python builder.py &

or

    $ python builder.py -f 2.0.3 &
    $ python builder.py --ffmpeg 2.7.2 &

Help
----

    $ python builder.py --help

Logging
-------

View logs when building

    $ tail -f `ls *.log |tail -1`

Results
-------

Results will be in ./usr directory

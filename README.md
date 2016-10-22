Build FFmpeg on Linux
=====================

[FFmpeg library](http://ffmpeg.org/) - A complete, cross-platform solution to record, convert and stream audio and video.

Build statically ffmpeg with defined version on Linux with faac 1.28, lame 3.99.5, last stable x264 and SDL-1.2.15 (for ffplay).

Build ffmpeg
------------

For now default build version of ffmpeg is 2.6.4

    $ python builder.py &

or

    $ python builder.py -f 2.0.3 &
    $ python builder.py --ffmpeg 2.7.2 --prefix usr --log &
    $ python builder.py --ffmpeg 2.6.4 --enable openssl --prefix usr --log &

Help
----

    $ python builder.py --help

Logging
-------

View logs from file when building

    $ tail -f `ls *.log |tail -1`

Results
-------

Results will be in ./usr directory

Build FFmpeg with QSV support
=============================

Create /usr/lib64/pkgconfig/libmfx.pc

    cat > /usr/lib64/pkgconfig/libmfx.pc < EOF
    prefix=/opt/intel/mediasdk
    exec_prefix=${prefix}
    libdir=${exec_prefix}/lib/lin_x64
    includedir=${prefix}/include

    Name: libmfx
    Description: Intel Media SDK Dispatched static library
    Version: 1.17
    Requires:
    Requires.private:
    Conflicts:
    Libs: -L${libdir} -lmfx -ldispatch_shared -lva -lva-drm -lsupc++ -lstdc++ -ldl
    Libs.private:
    Cflags: -I${includedir} -I${includedir}/mfx
    EOF

Add to /etc/environment

    LD_LIBRARY_PATH="/usr/local/lib:/usr/lib64"
    LIBVA_DRIVER_NAME=iHD
    LIBVA_DRIVERS_PATH=/opt/intel/mediasdk/lib64

Copy the /opt/intel/mediasdk/include to include/mfx

    sudo mkdir -p /opt/intel/mediasdk/include/mfx
    sudo cp /opt/intel/mediasdk/include/*.h /opt/intel/mediasdk/include/mfx

Add --enable-libmfx parameter to ./configure

Links:

[Accessing Intel® Media Server Studio for Linux* codecs with FFmpeg](https://software.intel.com/en-us/articles/accessing-intel-media-server-studio-for-linux-codecs-with-ffmpeg)<br>
[Intel QuickSync Video and FFmpeg](http://www.intel.com/content/dam/www/public/us/en/documents/white-papers/quicksync-video-ffmpeg-install-valid.pdf)

To build

    $ python builder.py --ffmpeg 3.1.3 --enable libmfx --prefix usr --log &

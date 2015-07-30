## FFMPEG builder changelog

### 0.1.2 (2015-07-30)

Features:

 - add logging to file

Bugfixes:

 - fix buffered stdout of subprocess Popen

### 0.1.1 (2015-07-26)

Features:

 - display download progress in console
 - command line option to define ffmpeg version
 - split builder into modules
 - build components in separate directory

### 0.1.0 (2015-07-25)

Features:

 - download faac-1.28, lame-3.99.5, SDL-1.2.15, ffmpeg-2.6.3
 - clone x264 from videolan repository
 - apply patches for faac and sdl
 - build methods to all components

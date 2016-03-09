# Dockerfile for building ffmpeg
# $ docker build -t company/ffmpeg:12.04 .

FROM ubuntu:12.04

MAINTAINER Igor Vetrov <i.vetrov@inventos.ru>

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install apt-utils && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install \
        wget git bzip2 make autoconf autotools-dev libtool python-dev libzvbi-dev libass-dev && \
    mkdir /tmp/repo && cd /tmp/repo && \
    wget http://www.tortall.net/projects/yasm/releases/yasm-1.2.0.tar.gz && \
    tar xfz yasm-1.2.0.tar.gz && cd yasm-1.2.0 && \
    ./configure --prefix=/usr/local && make && make install && \
    cd .. && git clone https://github.com/i-wind/build-ffmpeg.git && \
    cd build-ffmpeg && python builder.py --ffmpeg 2.6.4 --prefix=/usr/local

CMD ["/bin/bash"]

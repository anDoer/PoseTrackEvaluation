FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN echo "hey"
RUN apt-get update
RUN apt-get install -y apt-file
RUN apt-get update
RUN apt-get install -y build-essential \
    checkinstall \
    cmake \
    pkg-config \
    yasm \
    git \
    gfortran \
    libjpeg8-dev libpng-dev \
    libtiff-dev \
    libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev \
    libxine2-dev libv4l-dev \
    liblmdb-dev libleveldb-dev libsnappy-dev \
    mesa-utils and libgl1-mesa-glx x11-apps eog \
    vim tmux curl

RUN apt-get install -y  python-minimal
RUN apt-get install -y  python-pip
RUN pip install numpy pandas scipy tqdm click shapely

WORKDIR /opt/
RUN git clone --recurse-submodules https://github.com/leonid-pishchulin/poseval.git
RUN chmod -R 777 poseval

WORKDIR /home/

RUN echo "DONE"



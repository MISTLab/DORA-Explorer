FROM ubuntu:18.04
LABEL Maintainer="Pierre-Yves Lajoie <lajoie.py@gmail.com>"
LABEL DBM-SMS.version="0.1"

# Install common dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    dpkg \ 
    git \
    pkg-config \
    python \
    python-dev \
    python-numpy \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Install ARGoS
RUN apt-get update && apt-get install -y \
    wget \
    freeglut3-dev \
    qt5-default \
    libxi-dev \
    libxmu-dev \
    libfreeimage-dev \
    libfreeimageplus-dev \
    liblua5.2-dev \
    lua5.2 \
    liblua5.3-dev \
    lua5.3 \
    libboost-filesystem-dev \
    cmake \
    && rm -rf /var/lib/apt/lists/*
    
RUN apt-get update && \
    apt-get -y install sudo
RUN adduser --disabled-password --gecos '' docker
RUN adduser docker sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER docker
RUN sudo chmod -R ugo+rw /home/docker
USER root

# Add dummy argument to force rebuild starting from that point
ARG CODE_UPDATE_ARGOS=unknown

# Install Argos
RUN cd /home/docker/ &&\
    git clone https://github.com/lajoiepy/argos3.git &&\
    cd argos3 &&\
    mkdir build_simulator &&\
    cd build_simulator &&\
    cmake ../src -DCMAKE_BUILD_TYPE=Debug \
     -DARGOS_BUILD_FOR=simulator \
     -DARGOS_THREADSAFE_LOG=ON \
     -DARGOS_DYNAMIC_LOADING=ON &&\
    make

RUN touch /home/docker/argos3/build_simulator/argos3.1.gz &&\
    touch /home/docker/argos3/build_simulator/README.html &&\
    cd /home/docker/argos3/build_simulator &&\
    make install

RUN chmod +x /home/docker/argos3/build_simulator/argos_post_install.sh &&\
    ./home/docker/argos3/build_simulator/argos_post_install.sh &&\
    echo "\nsource /home/docker/argos3/build_simulator/setup_env.sh\n" >> /.bashrc

# Install and setup some editing and debugging tools
RUN sudo apt-get install -y nano strace valgrind

# Add dummy argument to force rebuild starting from that point
ARG CODE_UPDATE_BUZZ=unknown

# Install Buzz
RUN git clone https://github.com/lajoiepy/Buzz.git /home/docker/buzz
RUN cd /home/docker/buzz &&\
    git pull &&\
    git checkout bandwidth-log &&\
    mkdir build &&\
    cd build &&\
    cmake -DCMAKE_BUILD_TYPE=Debug ../src &&\
    make &&\
    make install &&\
    ldconfig

# Simulation dependencies
RUN apt-get update && apt-get install -y python-pip
RUN pip install matplotlib && pip install scipy
RUN apt-get update && apt-get install -y libjsoncpp-dev &&\
    ln -s /usr/include/jsoncpp/json/ /usr/include/json

# Clone simulation
ADD https://api.github.com/repos/lajoiepy/DBM-SMS/git/refs/heads/master version.json
RUN cd /home/docker/ &&\
    git clone https://github.com/lajoiepy/DBM-SMS.git

# Compile C++ controller
RUN cd /home/docker/DBM-SMS/sim/controller &&\
   mkdir build &&\
   cd build/ &&\
   cmake ../src &&\
   make &&\
   make install

# Compile buzz script
RUN cd /home/docker/DBM-SMS/sim &&\
    bzzc dbm-random-walk.bzz &&\
    bzzc dbm-gradient.bzz

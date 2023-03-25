FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y \
        software-properties-common \
        sudo \
        make \
        git \
        less \
        wget \
        flex \
        bison \
        nano \
        vim \
        python3 \
        python3-pip \
        lsof \
        jupyter \
        curl \
        graphviz

# not needed since we do not compile from source
#clang \
#gcc \
#g++ \
#g++-multilib \
#gdb \
#clang-tidy \
#clang-format \
#gcovr \
#llvm \
#libgraphviz-dev \
#libboost-all-dev \

# This adds the 'default' user to sudoers with full privileges:
RUN HOME=/home/default && \
    mkdir -p ${HOME} && \
    GROUP_ID=1000 && \
    USER_ID=1000 && \
    groupadd -r default -f -g "$GROUP_ID" && \
    useradd -u "$USER_ID" -r -g default -d "$HOME" -s /sbin/nologin \
    -c "Default Application User" default && \
    chown -R "$USER_ID:$GROUP_ID" ${HOME} && \
    usermod -a -G sudo default && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

ENV CC=/usr/bin/gcc
ENV CXX=/usr/bin/g++
ENV CCACHE_DIR=/build/docker_ccache
ENV LD_LIBRARY_PATH=/usr/local/lib

ENV CUDD_VERSION="3.0.0"
ENV MONA_VERSION="1.4-19.dev0"
ENV SYFT_TAG="v0.1.1"

WORKDIR /build

ARG GIT_REF=main

# Clone and build Lydia
#RUN git clone --recursive https://github.com/whitemech/lydia.git /build/lydia
#RUN git checkout ${GIT_REF} &&\
#    rm -rf build &&\
#    mkdir build &&\
#    cd build &&\
#    cmake -DCMAKE_BUILD_TYPE=Release .. &&\
#    cmake --build . --target lydia-bin -j4 &&\
#    make install &&\
#    cd .. &&\
#    rm -rf /build/lydia

WORKDIR /home/default

USER default


# Install CUDD
RUN wget https://github.com/whitemech/cudd/releases/download/v${CUDD_VERSION}/cudd_${CUDD_VERSION}_linux-amd64.tar.gz &&\
    tar -xf cudd_${CUDD_VERSION}_linux-amd64.tar.gz &&\
    cd cudd_${CUDD_VERSION}_linux-amd64 &&\
    sudo cp -P lib/* /usr/local/lib/ &&\
    sudo cp -Pr include/* /usr/local/include/ &&\
    rm -rf cudd_${CUDD_VERSION}_linux-amd64*

# Install MONA
RUN wget https://github.com/whitemech/MONA/releases/download/v${MONA_VERSION}/mona_${MONA_VERSION}_linux-amd64.tar.gz &&\
    tar -xf mona_${MONA_VERSION}_linux-amd64.tar.gz &&\
    cd mona_${MONA_VERSION}_linux-amd64 &&\
    sudo cp -P lib/* /usr/local/lib/ &&\
    sudo cp -Pr include/* /usr/local/include &&\
    rm -rf mona_${MONA_VERSION}_linux-amd64*

# Build and install Syft
#RUN git clone https://github.com/whitemech/Syft.git &&\
#    cd Syft &&\
#    git checkout ${SYFT_TAG} &&\
#    mkdir build && cd build &&\
#    cmake -DCMAKE_BUILD_TYPE=Release .. &&\
#    make -j &&\
#    make install &&\
#    cd .. &&\
#    rm -rf Syft

# install Syft
RUN wget https://github.com/whitemech/Syft/releases/download/v0.1.0/syft-3.0.0_ubuntu-20.04.tar.gz && \
  tar -xf syft-3.0.0_ubuntu-20.04.tar.gz &&\
  cd syft-3.0.0_ubuntu-20.04 && \
  sudo cp -P lib/* /usr/local/lib/

# install Lydia
RUN wget https://github.com/whitemech/lydia/releases/download/v0.1.3/lydia &&\
  chmod u+x lydia &&\
  sudo cp lydia /usr/local/bin/lydia &&\
  sudo chown default:default /usr/local/bin/lydia




# RUN pip install --no-cache-dir -r /home/default/MDP-Planner-Chip-Production/requirements.txt
RUN cd MDP-Planner-Chip-Production && pip install -e .

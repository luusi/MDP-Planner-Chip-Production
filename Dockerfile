FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /home

RUN apt-get update &&\
    apt-get install -y \
        python3 \
        python3-pip \
        git \
        cmake \
        lsof \
        sudo \
        less \
        wget \
        jupyter \
        curl \
        graphviz \
        flex \
        bison && \
    apt-get clean &&\
    rm -rf /var/cache

RUN git clone https://github.com/luusi/MDP-Planner-Chip-Production.git
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


RUN docker pull whitemech/lydia:latest && \
    alias lydia="docker run -v$(pwd):/home/default -it whitemech/lydia lydia "

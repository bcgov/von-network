FROM ubuntu:16.04

ARG uid=1000
ARG indy_stream=master

ARG indy_plenum_ver=1.1.143
ARG indy_anoncreds_ver=1.0.32
ARG indy_node_ver=1.1.159
ARG python3_indy_crypto_ver=0.1.6
ARG indy_crypto_ver=0.1.6

ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
ENV SHELL="/bin/bash"

# Install environment
RUN apt-get update -y && apt-get install -y \
    git \
    wget \
    python3.5 \
    python3-pip \
    python-setuptools \
    python3-nacl \
    apt-transport-https \
    ca-certificates

RUN pip3 install -U \
    pip \
    setuptools

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 68DB5E88
RUN echo "deb https://repo.sovrin.org/deb xenial $indy_stream" >> /etc/apt/sources.list

RUN useradd -ms /bin/bash -u $uid indy

RUN apt-get update -y && apt-get install -y \
    indy-plenum=${indy_plenum_ver} \
    indy-anoncreds=${indy_anoncreds_ver} \
    indy-node=${indy_node_ver} \
    python3-indy-crypto=${python3_indy_crypto_ver} \
    libindy-crypto=${indy_crypto_ver} \
    vim


RUN apt-get install -y dnsutils

USER indy
WORKDIR /home/indy

ADD --chown=indy:indy . /home/indy
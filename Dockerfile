FROM von-image:py35-latest

ADD --chown=indy:indy indy_config.py /etc/indy/

USER root

RUN apt-get update -y && \
	apt-get install -y --no-install-recommends \
		build-essential && \
	pip --no-cache-dir install \
		sanic==0.7.0 \
		ujson==1.33 && \
	apt-get remove --purge -y \
		build-essential && \
	apt-get autoremove -y && \
	rm -rf /var/lib/apt/lists/*

ADD --chown=indy:indy . $HOME

RUN mkdir -p $HOME/ledger/sandbox/data && \
    mkdir -p $HOME/.indy-cli/networks && \
    mkdir -p $HOME/.indy_client/wallet && \
    chown -R indy:indy $HOME && \
    chmod -R ug+rw $HOME

USER indy

# used by validator-info
# RUN apt-get install -y --no-install-recommends iproute2 sovrin

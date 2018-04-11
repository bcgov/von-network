FROM von-indy:latest

USER root

ADD --chown=indy:indy indy_config.py /etc/indy/

RUN apt-get update -y && \
	apt-get install -y --no-install-recommends \
		build-essential \
		python3.5-dev && \
	pip --no-cache-dir install \
		sanic==0.7.0 \
		ujson==1.33 && \
	apt-get remove --purge -y \
		build-essential \
		python3.5-dev && \
	apt-get autoremove -y && \
	rm -rf /var/lib/apt/lists/*

ADD . $HOME

RUN mkdir -p $HOME/ledger/sandbox/data && \
	mkdir -p $HOME/.indy_client/wallet && \
	chown -R indy:indy $HOME && \
	chmod -R ug+rw $HOME

# used by validator-info
#RUN apt-get install -y --no-install-recommends iproute2 sovrin

USER indy

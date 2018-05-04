FROM andrewwhitehead/von-image:py35-indy1.3.1-dev-441-ew

ADD --chown=indy:indy indy_config.py /etc/indy/

ADD --chown=indy:indy . $HOME

USER root

RUN mkdir -p \
        $HOME/ledger/sandbox/data \
        $HOME/.indy-cli/networks \
        $HOME/.indy_client/wallet && \
    chown -R indy:indy $HOME && \
    chmod -R ug+rw $HOME

USER indy

# used by validator-info
# RUN apt-get install -y --no-install-recommends iproute2 sovrin

ENV RUST_LOG ${RUST_LOG:-warning}

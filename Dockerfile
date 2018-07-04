FROM bcgovimages/von-image:py35-1.0rc3

ADD --chown=indy:indy indy_config.py /etc/indy/

ADD --chown=indy:indy . $HOME

USER root

RUN mkdir -p \
    $HOME/ledger/sandbox/data \
    $HOME/.indy-cli/networks \
    $HOME/.indy_client/wallet && \
    chown -R indy:indy $HOME/ledger $HOME/.indy-cli $HOME/.indy_client && \
    chmod -R ug+rw $HOME/ledger $HOME/.indy-cli $HOME/.indy_client

USER indy

# used by validator-info
# RUN apt-get install -y --no-install-recommends iproute2 sovrin

ENV RUST_LOG ${RUST_LOG:-warning}

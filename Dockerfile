FROM bcgovimages/von-image:py35-1.6-8

USER indy

RUN pip install --no-cache-dir aiosqlite~=0.6.0 \
  "git+https://github.com/Supervisor/supervisor.git@0cc0a3989211996d502a0ac46c0ea320e1dec928"

ENV RUST_LOG ${RUST_LOG:-warning}

RUN mkdir -p \
        $HOME/ledger/sandbox/data \
        $HOME/log \
        $HOME/.indy-cli/networks \
        $HOME/.indy_client/wallet && \
    chmod -R ug+rw $HOME/log $HOME/ledger $HOME/.indy-cli $HOME/.indy_client

ADD --chown=indy:indy indy_config.py /etc/indy/

ADD --chown=indy:indy . $HOME

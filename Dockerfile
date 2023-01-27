FROM bcgovimages/von-image:node-1.12-6

ENV LOG_LEVEL ${LOG_LEVEL:-info}
ENV RUST_LOG ${RUST_LOG:-warning}

ADD config ./config
ADD server/requirements.txt server/

# Here we need to upgrade pip in order to intsall IndyVDR binary
# However, this causes issue with 'plenum' package (for example: https://github.com/bcgov/von-network/issues/238)
# So we need to downgrade to pip 9.0.3 after requirements install
RUN pip3 install -U pip && \
    pip install --no-cache-dir -r server/requirements.txt && \
    python -m pip install pip==9.0.3

ADD --chown=indy:indy indy_config.py /etc/indy/
ADD --chown=indy:indy . $HOME

RUN chmod +x scripts/init_genesis.sh

RUN mkdir -p \
    $HOME/cli-scripts \
    && chmod -R ug+rw $HOME/cli-scripts

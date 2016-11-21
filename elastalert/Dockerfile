FROM debian:jessie

RUN \
  apt-get update && \
  apt-get install -y curl \
                     gcc \
                     python \
                     python-dev

RUN curl -sSL https://bootstrap.pypa.io/get-pip.py | /usr/bin/python

RUN /usr/local/bin/pip install elastalert

CMD ["/usr/local/bin/elastalert", "--config", "/etc/elastalert/config.yaml", "--verbose"]

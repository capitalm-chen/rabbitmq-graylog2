FROM debian:jessie

RUN \
  apt-get update && \
  apt-get install -y curl \
                     gcc \
                     python \
                     python-dev

RUN curl -sSL https://bootstrap.pypa.io/get-pip.py | /usr/bin/python

RUN /usr/local/bin/pip install elastalert

ADD ./wait-for-it/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

ADD start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]

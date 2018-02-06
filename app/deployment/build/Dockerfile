FROM ubuntu:latest

RUN apt-get -qq update && apt-get install -y software-properties-common language-pack-en-base \
    && apt-get update \
    && add-apt-repository ppa:jonathonf/python-3.6 \
    && apt-get update \
    && apt-get install -y --allow-unauthenticated software-properties-common language-pack-en-base \
    python3.6 nano build-essential libssl-dev libffi-dev python-dev python3-dev python3.6-dev curl htop wget libmysqlclient-dev \
    supervisor net-tools socat nginx iputils-ping nginx-extras \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

run wget https://bootstrap.pypa.io/get-pip.py && python3.6 get-pip.py

run apt-get install -y libpcre3

run mkdir -p /var/log/uwsgi
run mkdir -p /var/evernode
run chown -R www-data:www-data /var/log/uwsgi

run pip3 install --upgrade pip
run pip3 install uwsgi

run mkdir /run/uwsgi && chown www-data:www-data /run/uwsgi

ADD nginx /etc/nginx

ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENTRYPOINT pip3 install var/evernode/evernode-0.2.7.tar.gz --upgrade && ./usr/bin/supervisord

FROM debian:latest
RUN apt-get update && apt-get install -y apt-transport-https software-properties-common
RUN echo 'APT::Default-Release "stable";' | tee -a /etc/apt/apt.conf.d/00local
RUN cat /etc/apt/apt.conf.d/00local
RUN apt-get update
RUN add-apt-repository \
    "deb [arch=amd64] http://ftp.de.debian.org/debian testing main" && \
    apt-get update && \
    apt-get -t testing install -y python3.6
RUN apt-get install -t testing -y --allow-unauthenticated \
    nano build-essential libssl-dev libffi-dev python-dev python3-dev python3.6-dev curl wget default-libmysqlclient-dev \
    supervisor net-tools socat nginx iputils-ping nginx-extras \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.6 get-pip.py

RUN mkdir -p /var/log/uwsgi
run mkdir -p /var/evernode
run mkdir -p /etc/nginx/ssls
RUN chown -R www-data:www-data /var/log/uwsgi

RUN pip3 install --upgrade pip
RUN pip3 install uwsgi

RUN mkdir /run/uwsgi && chown www-data:www-data /run/uwsgi


ADD nginx /etc/nginx

ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENTRYPOINT cd /var/evernode && pip3 install --upgrade "$(ls | tail -1)" && /bin/bash > /srv/logs/uwsgi.log && /usr/bin/supervisord
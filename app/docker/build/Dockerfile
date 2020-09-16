FROM debian:latest
RUN apt-get update
RUN apt-get update && apt-get install -y --allow-unauthenticated \
    curl wget apt-transport-https software-properties-common nano build-essential libssl-dev libffi-dev \
    supervisor python-dev python3-dev default-libmysqlclient-dev net-tools socat nginx iputils-ping nginx-extras \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN wget https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tar.xz && tar xvf Python-3.8.5.tar.xz && cd Python-3.8.5 \
    && ./configure --enable-optimizations --with-ensurepip=install && make -j8 && make altinstall
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.8 50
RUN pip3.8 install --upgrade pip
RUN pip3.8 install uwsgi
RUN mkdir -p /var/log/uwsgi
run mkdir -p /var/evernode
run mkdir -p /etc/nginx/ssls
RUN chown -R www-data:www-data /var/log/uwsgi
RUN mkdir /run/uwsgi && chown www-data:www-data /run/uwsgi
ADD nginx /etc/nginx
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ENTRYPOINT cd /var/evernode && pip3.8 install --upgrade "$(ls | tail -1)" && /bin/bash > /srv/logs/uwsgi.log && python2.7 /usr/bin/supervisord
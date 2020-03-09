FROM ubuntu:16.04
# Nginx + UWSGI Plugin
RUN apt-get update && \
    apt-get -y install \
    curl \
    python3.5-dev \
    python3-pip \
    gcc\
    nginx \
    supervisor \
    vim

WORKDIR /app
# install pip
RUN pip3 install --upgrade pip -i https://pypi.douban.com/simple
COPY requirements.txt /app
RUN pip3 install --no-cache-dir  -r requirements.txt -i https://pypi.douban.com/simple
COPY . /app
RUN sh runtest.sh
CMD /usr/local/bin/gunicorn -c gunicorn_config.py manage:app

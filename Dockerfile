FROM python:2.7

RUN apt-get update && apt-get install -y build-essential zsh git vim-nox tree \
  htop libjpeg-dev libfreetype6-dev graphviz gettext python-setuptools \
  python-pip python-dev default-jre

VOLUME /var/src

WORKDIR /var/src
ADD /src/requirements.txt /var/src
RUN pip install -r requirements.txt

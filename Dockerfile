FROM ubuntu:bionic

RUN apt-get update && apt-get install -y \ 
    build-essential \
    python3 \
    python \
    python-dev \
    libxml2-dev \
    libxslt-dev \
    libssl-dev \
    zlib1g-dev \
    libyaml-dev \
    libffi-dev \
    python-pip \
    python3-pip \
    wget

RUN apt-get update -qq && apt-get install -y \
  ghostscript \
  libgs-dev \
  imagemagick \
  bc

COPY policy.xml /etc/ImageMagick-6/policy.xml

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app




# add app
ADD . /usr/src/app


RUN wget "http://www.fmwconcepts.com/imagemagick/downloadcounter.php?scriptname=localthresh&dirname=localthresh" -O /usr/bin/localthresh
RUN chmod 777 /usr/bin/localthresh 

CMD python3 main.py
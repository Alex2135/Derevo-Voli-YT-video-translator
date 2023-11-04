FROM nvidia/cuda:11.1.1-base-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive 

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN apt install -y build-essential \
    zlib1g-dev libncurses5-dev libgdbm-dev \
    libnss3-dev libssl-dev libsqlite3-dev \
    libreadline-dev libffi-dev wget libbz2-dev 
RUN apt-get update
RUN apt-get install -y ffmpeg
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt install -y python3.10 python3-pip

RUN apt-get install -y libsndfile1-dev
RUN pip3 install -r requirements.txt


ENTRYPOINT [ "python3", "demo.py" ]
FROM ubuntu:16.04

# Moves files to docker build
COPY . /

# Gets Python
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update
RUN apt-get install python3.6

# Gets pip to install requirements
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py

# Install requirements
RUN pip3.6 -r requirements.txt

# //TODO: Run server
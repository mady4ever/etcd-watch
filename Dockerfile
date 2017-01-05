FROM python:2.7
MAINTAINER Mahendra Patel
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y python-pip 
RUN git clone https://github.com/mady4ever/etcd-watch.git
RUN cd etcd-watch/python-etcd/;python setup.py install
RUN cd etcd-watch/conman/;python setup.py install
RUN cd /etcd-watch/conman/tests;python dyn_conf_program.py / watch.log http 172.31.42.40 2379

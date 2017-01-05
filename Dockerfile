FROM python:2.7
MAINTAINER Mahendra Patel
RUN pip install git
RUN git clone https://github.com/mady4ever/etcd-watch.git
RUN python /etcd-watch/python-etcd/setup.py install
RUN python /etcd-watch/conman/setup.py install
RUN python /etcd-watch/conman/tests/dyn_conf_program.py / watch.log http 172.31.42.40 2379

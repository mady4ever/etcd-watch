FROM python:2.7
MAINTAINER Mahendra Patel
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y python-pip
RUN pip install influxdb 
RUN pip install etcd3
CMD echo "hi"
RUN git clone https://github.com/mady4ever/etcd-watch.git
RUN cd etcd-watch/python-etcd/;python setup.py install
RUN cd etcd-watch/conman/;python setup.py install
#RUN pip install influxdb
#RUN cd /etcd-watch/conman/tests;nohup python dyn_conf_program.py / watch.log http 35.166.173.147 2379 &
#CMD ["python","/etcd-watch/conman/tests/dyn_conf_program.py"," / watch.log http 35.166.173.147 2379 &"]

# etcd-watch
watch etcd using python with multi threading

#Build container
sudo docker build -t etcd-watch .

#Run container
sudo docker run -it  etcd-watch /bin/bash
#Run python deamon process
nohup python etcd-watch/conman/tests/dyn_conf_program.py / watch.log http ip_of_etcd 2379 &

#Change etcd contents
etcdctl set /mesage "a:1,b:2,c:3,d:4"

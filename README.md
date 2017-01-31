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

# Get images from docker hub directly
docker run -it . mahipatel/etcd-watcher

# etcd v3 supported
#nohup python etcd-watch/conman/tests/dyn_conf_program_v3.py prefix-of-key-to-watch log-file-name http etcd-ip etcd-port influxdb-ip influxdb-port &

# new changes with envinment variables
docker run -it  -e "EW_KEY_PREFIX_WATCH"="localhost" -e "EW_LOG_FILE"="watch.log" -e "EW_ETCD_PROTOCOL"="http" -e "EW_ETCD_IP"="localhost" -e "EW_ETCD_PORT"="2379" -e "EW_INFLUX_IP"="localhost" -e "EW_INFLUX_PORT"="8083" -e "EW_HOST_IP"="localhost" etcd-watch bash

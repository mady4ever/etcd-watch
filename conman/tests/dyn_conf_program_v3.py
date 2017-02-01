import etcd3,sys
import os
from influxdb import InfluxDBClient


etcd_ip = os.environ.get("EW_ETCD_IP") or "localhost"
etcd_port = os.environ.get("EW_ETCD_PORT") or 2379
etcd_key_prefix = os.environ.get("EW_KEY_PREFIX_WATCH") or "except"
etcd_log_file = os.environ.get("EW_LOG_FILE") or "watch.log"
influx_ip = os.environ.get("EW_INFLUX_IP") or "localhost"
influx_port = os.environ.get("EW_INFLUX_PORT") or 8086
host_ip = os.environ.get("EW_HOST_IP") or "localhost"

etcd = etcd3.client(etcd_ip, int(etcd_port))
# watch prefix
#watch_count = 0
#template/testing/game
#filename = open(etcd_log_file, 'a')
prev_key = None
prev_value = None
neglact_duplicate = False
events_iterator, cancel = etcd.watch_prefix(etcd_key_prefix)
for event in events_iterator:
    #print(type(event))
    value = None    
    #filename.write(str(event))
    if isinstance(event,etcd3.events.PutEvent):
       #print("put event key",event.key)
       #print("put event value=",event.value)
       value = event.value
       if neglact_duplicate == True:
          if prev_key != None or prev_value != None:      
             if event.key == prev_key or event.value == prev_value:
                  continue
       splitedMsg = event.key.split('/')
	   
       containerId = splitedMsg[2]
       etcdSplitedMsg = splitedMsg[3].split('_')

       appName = etcdSplitedMsg[0]
       command = etcdSplitedMsg[1]
       sourceIp = etcdSplitedMsg[2].split(':')[0]
       sourcePort = etcdSplitedMsg[2].split(':')[1]
       destIp = etcdSplitedMsg[3].split(':')[0]
       destPort = etcdSplitedMsg[3].split(':')[1]
       #host_ip = os.environ.get("EW_HOST_IP") or "localhost"
       client = InfluxDBClient(influx_ip,int(influx_port),'root','root','docker_metadata')
       data = [{
               "measurement":"faultData",
               "tags":{
                   "host":host_ip,
                   "region":"us-west-1",
                   "appName" : appName,
                   "containerId": containerId
                   },
               "fields":{
                   "key":event.key,
                   "value":event.value,
                   "appName" : appName,
                   "containerId": containerId,
                   "command": command,
                   "sourceIp": sourceIp,
                   "sourcePort": sourcePort,
                   "destIp": destIp,
                   "destPort": destPort
                   }
               }]
       print(data)
       client.write_points(data)
       prev_key = event.key
       prev_value = event.value
       open(etcd_log_file, 'a').write(str(event))
    #watch_count += 1
    #if watch_count > 10:
    #    cancel()

# recieve watch events via callback function

#def watch_callback(event):
#    print(event)

#watch_id = etcd.add_watch_callback("template/testing/game", watch_callback)
# cancel watch
#etcd.cancel_watch(watch_id)

import time

import sys

from conman.conman_etcd import ConManEtcd
from influxdb import InfluxDBClient

class Program(object):
    def __init__(self,
                 key,
                 filename,
                 protocol='http',
                 host='127.0.0.1',
                 port=4001,
                 username=None,
                 password=None):
        self.conman = ConManEtcd(protocol=protocol,
                                 host=host,
                                 port=int(port),
                                 username=username,
                                 password=password,
                                 on_change=self.on_configuration_change,
                                 watch_timeout=0)
        self.filename = filename
        open(self.filename, 'w+')
        self.key = key
        self.last_change = None
        self.run()
    def on_configuration_change(self, key, action, value):
        # Sometimes the same change is reported multiple times. Ignore repeats
        if self.last_change == (key, action, value):
            return

        self.last_change = (key, action, value)
        line = 'key: {}, action: {}, value: {}\n'.format(key,
                                                        action,
                                                        value)
        open(self.filename, 'a').write(line)
        if action == 'set':
           data = [{
               "measurement":"faultData",
               "tags":{
                   "host":"ip-35.166.173.147",
                   "region":"us-west-1"
                   },
               "fields":{
                   "faultInfo":value
                   }
               }]
           client = InfluxDBClient('35.166.173.147',8086,'root','root','dockerData')
           client.write_points(data)
        self.conman.refresh(self.key)

    def run(self):
        self.conman.refresh(self.key)
        self.conman.watch(self.key)
        time.sleep(1)
        #while True:
        #    if self.conman[self.key].get('stop') == '1':
        #        open(self.filename, 'a').write('Stopping...\n')
        #        self.conman.stop_watchers()
        #        return
        #    time.sleep(1)

if __name__ == '__main__':
    Program(*sys.argv[1:])

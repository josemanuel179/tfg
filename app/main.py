#!/usr/bin/python3

import time
import configparser
import ipaddress
import service

config = configparser.ConfigParser()

try:
    config.read('service.conf')
    network = config['DEFAULT']['network']
    time = config['DEFAULT']['time']

except:
    raise
    
ips = ipaddress.ip_network(network).hosts()
seconds = int(time) * 3600


while True:
    for ip in ips:
        print(ip)
        service.execute_analisys(str(ip), 'root', 'root')
    time.sleep(seconds)

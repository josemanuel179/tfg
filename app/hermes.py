#!/usr/bin/python3

import service
import time
import configparser
import ipaddress

# 
config = configparser.ConfigParser()

# 
try:
    #
    config.read('/etc/hermesd/service.conf')
    
    # 
    network = config['DEFAULT']['network']
    ips = [str(ip) for ip in ipaddress.IPv4Network(network)]
    
    # 
    hours = int(config['DEFAULT']['time'])

# 
except:
    pass


# 
while True:
    
    
    for ip in ips:
     
        service.execute_analisys(str(ip), 'root', 'root')
        print('fin')

    time.sleep(hours * 3600)
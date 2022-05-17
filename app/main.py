#!/usr/bin/python3

from ast import arguments
import time
import sys
import configparser
import ipaddress
import service

# 
config = configparser.ConfigParser()
print('algo')
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

print(str(sys.argv))
exit()

'''
# 
while True:
    
    # 
    for ip in ips:
    
        # 
        service.execute_analisys(str(ip), user, password)
    
    # 
    time.sleep(hours * 3600)
'''
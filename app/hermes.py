#!/usr/bin/python3

import service
import time
import configparser
import ipaddress

# Configuración parser fichero configuración
config = configparser.ConfigParser()

# Obtención información fichero configuración
try:

    # Lectura fichero configuración
    config.read('/etc/hermesd/service.conf')
    
    # Obtención y análisis datos red del fichero configuración
    network = config['DEFAULT']['network']
    ips = [str(ip) for ip in ipaddress.IPv4Network(network)]
    
    # Obtención y análisis datos tiempo del fichero configuración
    hours = int(config['DEFAULT']['time'])

# En caso contrario
except:
    pass

while True:
    
    # Bucle por todas las IPs
    for ip in ips:
     
        # Ejecución servicio
        service.execute_analisys(str(ip), 'root', 'root')

    # Estado inactivo hasta que el tiempo finalice
    time.sleep(hours * 3600)
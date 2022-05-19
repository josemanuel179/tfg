#!/usr/bin/python3

import sys
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

    # Obtención de las credenciales de autentificacion
    user = config['CREDENTIALS']['user']
    password = config['CREDENTIALS']['password']
    key = config['CREDENTIALS']['key']

# En caso contrario
except:
    print("Exception. No se ha podido leer el fichero de configuración")
    sys.stdout.flush()

while True:
    
    # Bucle por todas las IPs
    for ip in ips:
     
        # Ejecución servicio
        if key != 'null':
            service.execute_analisys(str(ip), user, password, key)
        else:
            service.execute_analisys(str(ip), user, password)

    # Estado inactivo hasta que el tiempo finalice
    time.sleep(hours * 3600)
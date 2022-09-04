#!/usr/bin/python3

import sys
import service
import time
import configparser
import os

# Método secundario para obtener el estado de una máquina
def get_status_machine(host):
    
    # Obtención del estado
    try:
        
        # Ejecución del comando PING
        response = os.system("ping -c 1 " + host)

        # Si el PING obtiene una respuesta positiva desde la máquina 
        if response == 0:
            return 'OK'
        
        # En caso contrario
        else:
            return 'NOK'

    # En caso contrario
    except:
        print("Exception. No se ha realizar ping sobre la maquina" + host)
        sys.stdout.flush()  

# Configuración parser fichero configuración
config = configparser.ConfigParser()

# Intaciación del DashBoard
# dashboard.create_dash()

# Obtención información fichero configuración
try:

    # Lectura fichero configuración
    config.read('/etc/hermesd/service.conf')
    
    # Obtención y análisis datos red del fichero configuración
    network = config['DEFAULT']['network']
    ips = service.get_ip_range(network)
    
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
        
        # Si se puede alcanzar la máquina  
        if get_status_machine(ip) == 'OK':

            # Ejecución servicio si hay KEY
            if key != 'null':
                service.execute_analisys(str(ip), user, password, key)

            # En caso contrario
            else:
                service.execute_analisys(str(ip), user, password)
        
        # En caso contario
        else:
            print("Exception. No se ha podido ejecutar el análisis sobre la máquina")
            sys.stdout.flush()

    # Estado inactivo hasta que el tiempo finalice
    time.sleep(hours * 3600)
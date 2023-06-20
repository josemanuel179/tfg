#!/usr/bin/python3

import sys
import time
import signal
import service
import configparser

# Método destinado para la gestion del comando 'systemctl stop'
def sigterm_handler(signum, frame):
    print('parando el servicio')
    sys.stdout.flush()
    service.copia_datos()
    sys.exit(0)

# -------------------------------------------------

# Método destinado para la gestion del comando 'systemctl restart'
def sigusr1_handler(signum, frame):
    print('reinciando servicio')
    sys.stdout.flush()
    service.copia_datos()
    main()

# -------------------------------------------------

# Método principal del servicio
def main():

    # Gestión del comando 'systemctl stop'
    signal.signal(signal.SIGTERM, sigterm_handler)
    
    # Gestión del comando 'systemctl restart'
    signal.signal(signal.SIGUSR1, sigusr1_handler)

    os_check, systemctl_check = service.get_machine_specs()

    if service.check_machine_specs(os_check, systemctl_check) == False:
        print("Exception. La máquina no cuenta con los requisitos para lanzar el servicio")
        sys.stdout.flush()
        sys.exit(0)

    # Configuración parser fichero configuración
    config = configparser.ConfigParser()

    # Obtención información fichero configuración
    try:

        # Lectura fichero configuración
        config.read('/etc/hermesd/service.conf')

    # En caso contrario
    except:
        print("Exception. No se ha podido leer el fichero de configuración")
        sys.stdout.flush()

    try:
        # Obtención IPs del fichero configuración
        network = config['DEFAULT']['network']

    # En caso contrario
    except:
        print("Exception. No se ha podido leer el fichero de configuración")
        sys.stdout.flush()
        sys.exit(0)
    
    # Análisis IPs
    ips = service.get_ip_range(network)

    # Obtención del tiempo entre ejecuciones
    try:
        # Obtención y análisis datos tiempo del fichero configuración
        hours = int(config['DEFAULT']['time'])
    
    # En caso de error, se usa el valor por defecto
    except:
        hours = 6

    # Obtención de las credenciales de autentificacion
    user = config['CREDENTIALS']['user']
    password = config['CREDENTIALS']['password']

    while True:
        
        # Bucle por todas las IPs
        for ip in ips:
            
            # Se ejecuta el análisis sobre cada máquina
                service.execute_analisys(str(ip), user, password)
            
        # Estado inactivo hasta que el tiempo finalice
        time.sleep(hours * 3600)

# -------------------------------------------------

if __name__ == "__main__":
    main()
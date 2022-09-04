#!/usr/bin/env python3

from operator import ne
import re
import paramiko
import sys
import ipaddress
import csv
import datetime

# Método secundario destinado a la obtención de las instrucciones necesarios para la operación del servicio dependiendo del S.O. de la máquina
def get_commands_distro(distro):
    # Si el S.O. de la maquina basadas en Fedora (Fedora, Red Hat, CentOS)
    if 'fedora' in distro:
        commands = ['fedora','yum list --installed', 'yum list updates', 'yum update --assumeyes ']
    
    # Si el S.O. de la maquina basadas en Debian (Debian, Ubuntu)
    elif 'debian' in distro:
        commands = ['debian', 'apt list --installed', 'apt list --upgradable', 'apt install -y ']
    
    # Si el S.O. de la maquina basadas en OpenSuse
    elif 'opensuse' in distro or 'suse' in distro:
        commands = ['opensuse', 'zypper list-updates', 'zypper list-updates', 'zypper up -y']
    
    return commands

# Método secundario destinado a la ejecución de instrucciones remotas a otras máquinas mediante SSH 
def execute_command(client, command):
    
    # Ejecución del comando y obtención del resultado
    stdin, stdout, stderr = client.exec_command(command)
    
    # Decodificación del resultado para poder ser almacenada en una variable
    output = stdout.read().decode()

    return output

# Método principal destinado a la obtención del S.O. de una máquina
def get_distro(client):
    # Ejecución del comando 'cat /etc/os-release' a través del método secundario 'execute_command()'
    result = execute_command(client, 'cat /etc/os-release')

    return result

# Método principal destinado a la obtención de los servicios instalados en la máquina analizada
def get_installed_services(client, commands):
    # Instanciación de la variable necesaria para la ejecución del método
    services = []
    
    # Ejecución del comando destintado a la obtención de los servicios, a través del método secundario 'execute_command()'
    # El comando usado para esta línea dependerá del S.O de la máquina analizada
    output = execute_command(client, commands[1])

    # Alteración y análsis de los datos obtenidos en la salida
    services_list = output.split('\n')
    services_list_clean = [" ".join(element.split()) for element in services_list]
    services_split = [element.split(' ') for element in services_list_clean][:-1]
    
    # Si el S.O. de la máquina es una variante de Fedora
    if commands[0] == 'fedora':
        
        # Almacenamiento de los datos
        for service in services_split[1:]:
            services.append([service[0], service[1]])
    
    # Si el S.O. de la máquina es una variante de Debian
    elif commands[0] == 'debian':
        
        # Almacenamiento de los datos
        for service in services_split[1:]:
            if '/' in service:
                services.append([service[0].split('/')[0], service[1]])
            else:
                services.append([service[0], service[1]])

    # Si el S.O. de la máquina es una variante de OpenSUSE
    elif commands[0] == 'opensuse':
        
        # Almacenamiento de los datos
        for service in services_split[5:]:
            services.append([service[4], service[6]])

    return services, len(services)
 

# Método secundario destinado al análisis del versiones de un servicio
def analize_services(actual, new):
    # Instanciación de la variable necesaria para la ejecución del método
    comparison = []

    # Si ambas entradas no estan vacías
    if actual != '' and new != '':
        
        try:
            # Obtención de las versiones a través de expresiones regulares
            install_version = re.findall('[\d{1,3}\.]*\d{1,3}-\d{1,3}', actual)[0].split('.')
            last_version = re.findall('[\d{1,3}\.]*\d{1,3}-\d{1,3}', new)[0].split('.')
            
            # Alteración de las versiones para su posterior análisis
            old = list(map(int, install_version[:-1] + install_version[-1].split('-')))
            new = list(map(int, last_version[:-1] + last_version[-1].split('-')))
            
            # Bucle por ambas lista con las versiones del servicio
            for i in range(0, len(old)):

                # Si la misma posición en las dos versiones es igual
                if old[i] == new[i]:
                    comparison.append('IGUAL')

                # Si la posición en la versión previa es inferior a la nueva
                elif old[i] > new[i]:
                    comparison.append('MENOR')
                
                # Si la posición en la versión nueva es inferior a la previa
                elif old[i] < new[i]:
                    comparison.append('MAYOR')

            # Si todas las posiciones de la lista equivalen a 'IGUAL'
            if comparison[0] == 'IGUAL' and len(set(comparison)) == 1:
                result = 'OK'

            # En caso de que la primera posición equivalga a 'IGUAL'
            elif comparison[0] == 'IGUAL':

                # Si 'MAYOR' se encuentra dentro de la lista
                if 'MAYOR' in comparison[1:]:
                    result = 'UPDATE'

                # En caso contrario
                else:
                    result = 'OK'

            # En caso contrario
            else:
                result = 'OK'

        except:
            result = 'OK'

    # En caso contrario
    else:
        result = 'OK'

    return result

# Método principal destinado a la obtención de las últimas versiones de los servicios instalados
def get_last_versions(client, commands, installed_services):
    # Instanciación de las variables necesarias para la ejecución del método
    services = []
    services_names = []
    result = []
    
    # Ejecución del comando destintado a la obtención de las versiones de los servicios, a través del método secundario 'execute_command()'
    # El comando usado para esta línea dependerá del S.O de la máquina analizada
    output = execute_command(client, commands[2])
    
    # Alteración y análsis de los datos obtenidos en la salida
    services_list = output.split('\n')
    services_list_clean = [" ".join(element.split()) for element in services_list]
    services_split = [element.split(' ') for element in services_list_clean][:-1]

    # Si el S.O. de la máquina es una variante de Fedora
    if commands[0] == 'fedora':
        
        # Comprobación lista no vacia
        if len(services_split) > 3:
            
            # Bucle por los datos obtenidos
            for service in services_split[2:]:

                # Almacenamiento de los datos en dos listas
                services.append([service[0], service[1]])
                services_names.append(service[0])

        # En caso contario
        else:
            services = []
            services_names = []
    
    # Si el S.O. de la máquina es una variante de Debian
    elif commands[0] == 'debian':

        # Comprobación lista no vacia
        if len(services_split) > 2:

            # Bucle por los datos obtenidos
            for service in services_split[1:]:
                
                # Si hay un '/' dentro de los datos analizados
                if '/' in service:
                    
                    # Almacenamiento de los datos en dos listas 
                    services.append([service[0].split('/')[0], service[1]])
                    services_names.append(service[0].split('/')[0])
                
                # En caso contrario
                else:

                    # Almacenamiento de los datos en dos listas 
                    services.append([service[0], service[1]])
                    services_names.append(service[0])
        
        # En caso contario
        else:
            services = []
            services_names = []
    
    # Si el S.O. de la máquina es una variante de OpenSUSE
    elif commands[0] == 'opensuse':
        
         # Comprobación lista no vacia
        if len(services_split) > 6:
        
            # Bucle por los datos obtenidos
            for service in services_split[5:]:
                
                # Almacenamiento de los datos en dos listas 
                services.append([service[4], service[8]])
                services_names.append(service[4])
        
        # En caso contario
        else:
            services = []
            services_names = []

    # Almacenamiento de los resultados  
    for element in installed_services:
        
        # Si el nobre del servicio se encuentra en la lista 'service_names'
        if element[0] in services_names:

            # Determinar la posición del elemento en la lista
            pos = services_names.index(element[0])
            status = analize_services(element[1], services[pos][1])

            # Ejecutar el analisis sobre las versiones 
            if status == 'UPDATE':
                result.append(element[0].split('.')[0])
        else:
            pass

    return result, len(services_names), len(result)

# Método principal destinado a la actualización de servicios con versiones nuevas
def update_services(client, commands, updates):   
    
    # Si la lista de 'updates' no esta vacía
    if updates:

        # Ejecutamos la actualización de todos los servicios
        command = commands[3] + " ".join(updates)
        execute_command(client, command)

    return None

#  Método principal destinado a la obtención de las IPs de las máquinas a analizar
def get_ip_range(network):
    
    # En el caso de que sea un rango
    if '-' in network:
        result = []

        # División del rango de una lista
        ip_range = network.split('-')
        ip_range2 = [element.strip() for element in ip_range]

        # Almacenamiento del rango en una lista
        for i in range(int(ip_range2[0][-1]),int(ip_range2[1][-1])+1):
            result.append(ip_range2[0][:-1]+ str(i))
    
    # En el caso de que sea una red
    elif '/' in network:
        
        # Recolección de todas las IPs dentro de la red
        ips = list(ipaddress.ip_network(network).hosts())
        result = [str(element) for element in ips]
    
    # En el caso de que sean varias IPs
    elif ',' in network:

        # División del rango de una lista
        ip_range = network.split(',')
        result = [element.strip() for element in ip_range]
    
    # En el caso de que solo sea una IP
    else:
        result = [network]

    return result

# Método principal destinado a la ejecución de los método previos de forma conjunta
def execute_analisys(ip, user, password, key='null'):
    # Instanciación del cliente SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Establecimiento conexión a la máquina a analizar 
    try:

        # Si existe una llave en el fichero de configuración
        if key != 'null':

            # Conexión SSH a la máquina a analizar
            client.connect(hostname=ip, username=user, password=password, key_filename=key)
       
        # En caso contrario       
        else:

            # Conexión SSH a la máquina a analizar
            client.connect(hostname=ip, username=user, password=password)
    
    # En el caso de que la conexión falle, se continua con la ejecución del servicio
    except:
        print("Excpetion. No se ha podido establecer una conexión con la máquina " + str(ip))
        sys.stdout.flush()
    
    # Ejecución de los métodos isntanciados previamente
    try:
        distro = get_distro(client)
        commands = get_commands_distro(distro)
        print(commands)
        sys.stdout.flush()
        actual_services, actual_services_len = get_installed_services(client, commands)
        print(actual_services)
        sys.stdout.flush()
        last_versions, last_versions_len , update_versions_len = get_last_versions(client, commands, actual_services)
        print(last_versions)
        update_services(client, commands, last_versions)
        sys.stdout.flush()

    # En el caso de que la ejecucuión de algun método falle, se continua con la ejecución del servicio
    except:
        print("Exception. No se ha podidio ejecutar el análisis en la máquina " + str(ip))
        sys.stdout.flush()


    # Almacenamiento datos estadísticos
    try:
        # Obtención de la fecha y hora
        date = datetime.datetime.now()

        # Almacenamiento de los datos en un fichero csv
        with open('/hermesd/hermes.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([date.strftime("%Y-%m-%d %H:%M:%S"), commands[0].capitalize(), actual_services_len, update_versions_len, actual_services_len-last_versions_len, last_versions_len])

    # En caso contrario
    except:
        print("Exception. No se ha almacenar los datos en el fichero hermes.csv")
        sys.stdout.flush()

    # Cierre de conexión
    client.close()
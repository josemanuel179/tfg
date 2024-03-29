#!/usr/bin/env python3

import re
import os
import sys
import csv
import shutil
import socket
import platform
import paramiko
import datetime
import ipaddress
import subprocess

## MÉTODOS SECUNDARIOS ##

# Método secundario destinado a la ejecución de instrucciones remotas a otras máquinas mediante SSH 
def execute_command(client, command):
    
    # Ejecución del comando y obtención del resultado
    stdin, stdout, stderr = client.exec_command(command)
    
    # Configuración para que ejecute el función 'exec_command' hasta que termine
    while not stdout.channel.recv_ready():
        pass 

    # Decodificación del resultado para poder ser almacenada en una variable
    output = stdout.read().decode()

    return output

##### ------------------------------------ ######

## MÉTODOS PRINCIPALES ##

# Método destinado a obtener el S.O. de la máquina analizadora y el comando systemctl
def get_machine_specs():
    
    # Se obtiene el S.O. de la máquina
    os_check = platform.system()

    # Se comprueba si la herramienta systemclt se encuentra en la máquina 
    systemctl_check = os.system('command -v systemctl >/dev/null 2>&1')

    return os_check, systemctl_check

# -------------------------------------------------

# Método destinado a obtener que la máquina analizadora cuenta con un S.O. UNIX y con el comando systemctl
def check_machine_specs(os_check, systemctl_check):

    # En el caso de que sea una máquina UNIX y cuente con systemctl
    if os_check in ['Linux', 'Darwin'] and systemctl_check == 0:
        return True
    
    # En caso contrario
    else:
        return False

# -------------------------------------------------

#  Método destinado a la obtención de las IPs de las máquinas a analizar
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
        clean_network = network.replace(" ", "")
        ips = list(ipaddress.ip_network(clean_network).hosts())
        result = [str(element) for element in ips]
    
    # En el caso de que sean varias IPs
    elif ',' in network:

        # División del rango de una lista
        ip_range = network.split(',')
        result = [element.strip() for element in ip_range]
    
    # En el caso de que solo sea una IP
    else:
        result = [network]

    ip_exp = r'^(\d{1,3}\.){3}\d{1,3}$'

    # Se comprueba que todas las IPs tengan formato correcto
    for element in result:
        if not re.match(ip_exp, element):
            result.remove(element)

    # En el caso de que haya un error
    if len(result) == 1 and result[0] == '':
        result = []
    
    return result

# -------------------------------------------------

# Método a la comprobación, mediante paquetes ICMP, la conexión ente máquinas
def get_ping(client_ip):
    
    # Comando ping
    ping_command = ['ping', '-c', '1', client_ip]
    
    # Ejecución del comando ping y obtención del código de retorno
    response = subprocess.run(ping_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Si se alcanza la máquina   
    if response.returncode == 0:
        return True
    
    # En caso contrario
    else:
        return False

# -------------------------------------------------

# Método para comprobar si los puertos requeridos se encuentran abiertos
def check_port_connections(client_ip, port = 22):
    
    # Instanciación de un socket con el que abrir una conexión con el puerto 22 - SSH
    sockect_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conexión con el host y puerto especificados
        sockect_connection.connect((client_ip, port))

        # En el caso de que se genere una conexión 
        return True

    # En caso de que la máquina destino rechaze la conexión
    except:
        return False
    
    # En cualquier casuística que se de, se cierra el puerto
    finally:
        sockect_connection.close()

# -------------------------------------------------

# Método destinado a la obtención del S.O. de una máquina
def get_distro(client):
    
    # Ejecución del comando 'cat /etc/os-release' a través del método secundario 'execute_command()'
    result = execute_command(client, 'cat /etc/os-release')

    return result

# -------------------------------------------------

# Método destinado a la comprobación del S.O. de una máquina
def check_distro(distro):
    
    # Listado de sistemas operativos
    applied_distros = ['fedora', 'debian', 'opensuse','suse']
    
    # Se comprueba que la distribución sea derivada de Debian, Fedora o Suse
    return any(element.lower() in distro for element in applied_distros)

# -------------------------------------------------

# Método destinado a la obtención de las instrucciones necesarios para la operación del servicio dependiendo del S.O. de la máquina
def get_commands_distro(distro):
    
    # Listado con los comandos necesarios
    commands = []
    
    # Si el S.O. de la maquina basadas en Fedora (Fedora, Red Hat, CentOS)
    if 'fedora' in distro:
        commands = ['fedora','yum list installed', 'yum list updates', 'yum update --assumeyes ']
    
    # Si el S.O. de la maquina basadas en Debian (Debian, Ubuntu)
    elif 'debian' in distro:
        commands = ['debian', 'apt list --installed', 'apt list --upgradeable', 'apt install -y ']
    
    # Si el S.O. de la maquina basadas en Suse
    elif 'opensuse' in distro or 'suse' in distro:
        commands = ['suse', 'zypper pa --installed-only', 'zypper list-updates', 'zypper up -y ']
    
    else:
        commands = None
        
    return commands

# -------------------------------------------------

# Método destinado a la obtención de los servicios instalados en la máquina analizada
def get_installed_services(client, commands):
    # Instanciación de la variable necesaria para la ejecución del método
    services = []
    
    # Ejecución del comando destintado a la obtención de los servicios, a través del método secundario 'execute_command()'
    # El comando usado para esta línea dependerá del S.O de la máquina analizada
    output = execute_command(client, commands[1])

    # Alteración y análsis de los datos obtenidos en la salida si es fedora o debian
    if commands[0] in ['fedora', 'debian']:
        services_list = output.split('\n')
        services_list_clean = [" ".join(element.split()) for element in services_list]
        services_split = [element.split(' ') for element in services_list_clean][:-1]
    
    # En el caso de que sea suse
    else:
        services_list = output.split('\n')
        services_split = [element.split('|') for element in services_list]

    # Si el S.O. de la máquina es una variante de Fedora
    if commands[0] == 'fedora':
        
        # Almacenamiento de los datos
        for service in services_split[1:]:
            if '.' in service[0]:
                services.append([service[0].rsplit('.', 1)[0], service[1]])
            else:
                services.append([service[0], service[1]])
    
    # Si el S.O. de la máquina es una variante de Debian
    elif commands[0] == 'debian':
        
        # Almacenamiento de los datos
        for service in services_split[1:]:
            if '/' in service[0]:
                services.append([service[0].split('/')[0], service[1]])
            else:
                services.append([service[0], service[1]])

    # Si el S.O. de la máquina es una variante de Suse
    elif commands[0] == 'suse':
        
        # Almacenamiento de los datos
        for service in services_split[4:-1]:
            if service[0].strip() in ['i','i+']:
                services.append([service[2].strip(), service[3].strip()])

    return services, len(services)
 
# -------------------------------------------------

# Método destinado al análisis del versiones de un servicio
def analize_services(actual, new):
    # Instanciación de la variable necesaria para la ejecución del método
    comparison = []

    try:

        # Si ambas entradas no estan vacías
        if actual != '' and new != '':
            
            # Obtención de las versiones a través de expresiones regulares
            install_version = re.search(r"\d+(\.\d+){1,2}(-\d+)?", actual).group()
            last_version = re.search(r"\d+(\.\d+){1,2}(-\d+)?", new).group()
                
            # Alteración de las versiones para su posterior análisis
            old = [int(element) for item in install_version.split('.') for element in item.split('-')]
            new = [int(element) for item in last_version.split('.') for element in item.split('-')]
                
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

        # En caso contrario
        else:
          result = 'OK'  

    # En caso contrario
    except:
        result = 'OK'

    return result

# -------------------------------------------------

# Método principal destinado a la obtención de las últimas versiones de los servicios instalados
def get_last_versions(client, commands, installed_services):
    # Instanciación de las variables necesarias para la ejecución del método
    services = []
    services_names = []
    result = []
    
    # Ejecución del comando destintado a la obtención de las versiones de los servicios, a través del método secundario 'execute_command()'
    # El comando usado para esta línea dependerá del S.O de la máquina analizada
    output = execute_command(client, commands[2])
    
    # Alteración y análsis de los datos obtenidos en la salida si es fedora o debian
    if commands[0] in ['fedora', 'debian']:
        services_list = output.split('\n')
        services_list_clean = [" ".join(element.split()) for element in services_list]
        services_split = [element.split(' ') for element in services_list_clean][:-1]
    
    # En el caso de que sea suse
    else:
        services_list = output.split('\n')
        services_split = [element.split('|') for element in services_list]

    # Si el S.O. de la máquina es una variante de Fedora
    if commands[0] == 'fedora':
        
        # Comprobación lista no vacia
        if len(services_split) > 3:
            
            # Bucle por los datos obtenidos
            for service in services_split[2:]:
                
                # Si hay un '.' dentro de los datos analizados
                if '.' in service[0]:
                    
                    # Almacenamiento de los datos en dos listas 
                    services.append([service[0].rsplit('.', 1)[0], service[1]])
                    services_names.append(service[0].split('.')[0])
                
                # En caso contrario
                else:

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
                if '/' in service[0]:
                    
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
    
    # Si el S.O. de la máquina es una variante de Suse
    elif commands[0] == 'suse':
        
         # Comprobación lista no vacia
        if len(services_split) > 5:
        
            # Bucle por los datos obtenidos
            for service in services_split[4:-1]:
                
                # Almacenamiento de los datos en dos listas 
                services.append([service[2].strip(), service[4].strip()])
                services_names.append(service[2].strip())
        
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

# -------------------------------------------------

# Método principal destinado a la actualización de servicios con versiones nuevas
def update_services(client, commands, updates):   
    
    # Si la lista de 'updates' no esta vacía
    if updates:

        # Ejecutamos la actualización de todos los servicios
        command = commands[3] + " ".join(updates)
        _ = execute_command(client, command)

    return None

# -------------------------------------------------

# Método principal destinado a la copia de los datos tras la suspensión del servicio y borrado del fichero 'hermes.csv'
def copia_datos():
    
    # Se obtiene la fecha y se copian los datos
    try:
        actual_time = datetime.datetime.now()
        shutil.copy('/hermesd/hermes.csv', '/hermesd/' + actual_time.strftime("%Y%m%d") + '_hermes.csv')

    # En caso de error
    except:
        print("Exception. No se han podido copiar los datos")
        sys.stdout.flush()

    # Se abre el documento 'hermes.csv' y se crea un nuevo fichero temporal
    with open('/hermesd/hermes.csv', 'r') as input, open('/hermesd/hermes_tmp.csv', 'w', newline='') as output:
        
        # Se intancia tanto el modulo lector como escritor
        csv_reader = csv.reader(input)
        csv_writer = csv.writer(output)

        # Se lee la primera fila del fichero y se copia en el temporal
        firt_line = next(csv_reader)
        csv_writer.writerow(firt_line)

    # Se copian los datos del fichero temporal a 'hermes.csv'  
    try:

        # Se renombra el archivo temporal para reemplazar el archivo original
        shutil.move('/hermesd/hermes_tmp.csv', '/hermesd/hermes.csv')
    
    # En caso contrario
    except:
        print("Exception. No se han podido copiar los datos")
        sys.stdout.flush()

# -------------------------------------------------

# Método principal destinado a la ejecución de los método previos de forma conjunta
def execute_analisys(ip, user, password, key='null'):
    
    # Comprobación de que la máquina este levantada
    try:

        # Se ejecuta un ping sobre la máquina a analizar
        ping = get_ping(ip)

        # Si se obtiene respuesta
        if ping == True:
            pass

        # En caso contrario
        else:
            print("Excpetion. La máquina " + str(ip) + " no se encuentra levantada")
            sys.stdout.flush()
            return  

    # En caso contrario
    except:
        print("Excpetion. No se ha podido llegar a la máquina " + str(ip))
        sys.stdout.flush()
        return
    
    # Comprobación de que la máquina tenga el puerto 22 activo
    try:
        
        # Se prueba la conxexión por el puerto TCP 22
        port_connection = check_port_connections(ip)

        # Si se obtiene respuesta
        if port_connection == True:
            pass

        # En caso contrario
        else:
            print("Excpetion. No es posible acceder a la máquina " + str(ip) + " por el puerto TCP 22")
            sys.stdout.flush()
            return

    # En caso contrario
    except:
        print("Excpetion. No es posible acceder a la máquina " + str(ip) + " por el puerto TCP 22")
        sys.stdout.flush()
        return
    
    # Instanciación del cliente SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Establecimiento conexión a la máquina a analizar 
    try:
        # Conexión SSH a la máquina a analizar
        client.connect(hostname=ip, username=user, password=password)
    
    # En el caso de que la conexión falle, se continua con la ejecución del servicio
    except:
        print("Excpetion. No se ha podido establecer una conexión con la máquina " + str(ip))
        sys.stdout.flush()
        return
    
    # Ejecución de los métodos isntanciados previamente
    try:
        
        # Obtención de la distribución
        distro = get_distro(client)

        # Obtención de los comandos
        commands = get_commands_distro(distro)

        # Obtención de los servicios intalados y su cantidad
        actual_services, actual_services_len = get_installed_services(client, commands)
        print(actual_services)
        sys.stdout.flush()

        # Obtención de los servicios a actualizar, la cantidad de servicios disponibles a acutilzar y la cantidad de servicios actualizados
        last_versions, last_versions_len , update_versions_len = get_last_versions(client, commands, actual_services)
        print(last_versions)
        sys.stdout.flush()
        update_services(client, commands, last_versions)
        
    # En el caso de que la ejecucuión de algun método falle, se continua con la ejecución del servicio
    except:
        print("Exception. No se ha podidio ejecutar el análisis en la máquina " + str(ip))
        sys.stdout.flush()
        return
    
    # Ejecución de reinicio de los servicios de la máquina
    try:
        # Actualización de systemctl
        _, _, _ = client.exec_command('systemctl daemon-reload')

        # Actualización de los servicios
        command = "sudo systemctl list-unit-files --type=service --no-pager --no-legend | awk '!/poweroff.target|reboot.target|halt.target|hermesd(-dashboard)?\.service/{print $1}' | xargs -I{} sudo systemctl try-restart {}"
        if len(last_versions) != 0:
            _, _, _ = client.exec_command(command)
        print("Servicios de la máquina " + str(ip) + " han sido reiniciados")
        sys.stdout.flush()
    
    except:
        print("Exception. No se ha podidio reiniciar los servicios en la máquina " + str(ip))
        sys.stdout.flush()

    # Almacenamiento datos estadísticos
    try:
        # Obtención de la fecha y hora
        date = datetime.datetime.now()

        # Almacenamiento de los datos en un fichero csv
        with open(r'/hermesd/hermes.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            fields = [date.strftime("%Y-%m-%d %H:%M:%S"), commands[0].capitalize(), actual_services_len, update_versions_len, actual_services_len-last_versions_len+update_versions_len, last_versions_len-update_versions_len]
            writer.writerow(fields)
            print("Métricas de la máquina " + str(ip) + " han sido almacenadas")
            sys.stdout.flush()

    # En caso contrario
    except:
        print("Exception. No se ha almacenar los datos en el fichero hermes.csv")
        sys.stdout.flush()
        return

    # Cierre de conexión
    client.close()
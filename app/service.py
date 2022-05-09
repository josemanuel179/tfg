#!/usr/bin/env python3

import re
import paramiko

# Método secundario destinado a la obtención de las instrucciones necesarios para la operación del servicio dependiendo del S.O. de la máquina
def get_commands_distro(distro):
    # Si el S.O. de la maquina es CentOS
    if distro == 'centos':
        commands = []
    
    # Si el S.O. de la maquina es Ubuntu
    if distro == 'centos':
        commands = []
    
    # Si el S.O. de la maquina es OpenSuse
    if distro == 'centos':
        commands = []
    
    # Si el S.O. de la maquina es Fedora
    if distro == 'centos':
        commands = []
    
    # Si el S.O. de la maquina es Arch
    if distro == 'centos':
        commands = []
    
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
    output = execute_command(client, 'cat /etc/os-release')
    
    # Alteración de la salida para su posterior análisis
    os_info = output.split('\n')
    
    # Mediante una expresión regular, obtenemos de la salida el S.O. de la máquina
    result = re.findall(r'\b[a-z\s\d]+\b', os_info[2])[0]
    return result

# Método principal destinado a la obtención de los servicios instalados en la máquina analizada
def get_installed_services(client, distro):
    # Instanciación de la variable necesaria para la ejecución del método
    services = []
    
    # Ejecución del comando destintado a la obtención de los servicios, a través del método secundario 'execute_command()'
    # El comando usado para esta línea dependerá del S.O de la máquina analizada
    output = execute_command(client, 'yum list --installed')

    # Alteración y análsis de los datos obtenidos en la salida
    services_list = output.split('\n')
    services_list_clean = [" ".join(element.split()) for element in services_list]
    services_split = [element.split(' ') for element in services_list_clean][:-1]
    
    # Almacenamiento de los datos analizados en la variable instanciada previamente
    for service in services_split:
        services.append([service[0], service[1]])

    return service

# Método secundario destinado al análisis del versiones de un servicio
def analize_services(actual, new):
    # Instanciación de la variable necesaria para la ejecución del método
    comparison = []

    # Si ambas entradas no estan vacías
    if actual != '' and new != '':
        
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

    # En caso contrario
    else:
        result = 'OK'

    return result

# Método principal destinado a la obtención de las últimas versiones de los servicios instalados
def get_last_versions(client, distro, installed_services):
    # Instanciación de las variables necesarias para la ejecución del método
    services = []
    services_names = []
    result = []
    
    # Ejecución del comando destintado a la obtención de las versiones de los servicios, a través del método secundario 'execute_command()'
    # El comando usado para esta línea dependerá del S.O de la máquina analizada
    output = execute_command(client, 'yum list updates')
    
    # Alteración y análsis de los datos obtenidos en la salida
    services_list = output.split('\n')
    services_list_clean = [" ".join(element.split()) for element in services_list]
    services_split = [element.split(' ') for element in services_list_clean][:-1]
     
    # Almacenamiento de los datos analizados para su posterior analisis
    for service in services_split:
        services.append([service[0], service[1]])
        services_names.append(service[0])

    # Almacenamiento de los resultados  
    for element in installed_services:
        
        # Si el nobre del servicio se encuentra en la lista 'service_names'
        if element[0] in services_names:

            # Determinar la posición del elemento en la lista
            pos = services_names.index(element[0])

            # Ejecutar el analisis sobre las versiones 
            result.append([element[0], element[1], services[pos][0], 
                analize_services(element[1], services[pos][1])])
        else:
            pass

    return result

# Método principal destinado a la actualización de servicios con versiones nuevas
def update_services(client, distro, updates):   
    # Bucle por todos los servicios a actualizar
    for element in updates:

        # Generación del comando destinado a actualizar cada servicio  
        # El comando usado para esta línea dependerá del S.O de la máquina analizada
        command = '' + element
        
        # Ejecución del comando destintado a la obtención de los servicios, a través del método secundario 'execute_command()'
        execute_command(client, command)

    return None

# Método principla destinado a la ejecución de los método previos de forma conjunta
def execute_analisys(ip, user, password):
    # Instanciación del cliente SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Establecimiento conexión a la máquina a analizar 
    try:
        client.connect(hostname=ip, username=user, password=password)
    
    # En el caso de que la conexión falle, se continua con la ejecución del servicio
    except:
        pass
    
    # Ejecución de los métodos isntanciados previamente
    try:
        distro = get_distro(client)
        actual_services = get_installed_services(client, distro)
        last_versions = get_last_versions(client, distro, actual_services)        
        update_services(client, distro, last_versions)
    
    # En el caso de que la ejecucuión de algun método falle, se continua con la ejecución del servicio
    except:
        pass

    # Cierre de conexión
    client.close()
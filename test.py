#!/usr/bin/env python3

import paramiko

services_names = []
services_desired_versions = []

def execute_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    return output

def get_last_versions(client):
    services = []
    
    output = execute_command(client, 'yum list updates')
    
    services_list = output.split('\n')
    services_list_clean = [" ".join(element.split()) for element in services_list]
    services_split = [element.split(' ') for element in services_list_clean][:-1]
     
    for service in services_split:
        services.append([service[0], service[1]])
    
    return services

def test(ip, user, password):
    result = []

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname=ip, username=user, password=password)
    except:
        pass
    
    try:
        services = get_last_versions(client)
        for service in services:
            if service[0] in services_names:
                pos = services_names.index(service[0])
                if service[1] == services_names[pos]:
                    pass
                    # ok
                else:
                    pass
                    # nok
            else:
                pass
    except:
        pass

    client.close()
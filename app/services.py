#!/usr/bin/env python
import os
import nmap3
nmap = nmap3.Nmap()

ip = "127.0.0.1"

package_manager = {
    "REHL": ,
    "Unbuntu": ,
    "Debian": ,
    "Arch": ,
    "Open Suse": ,
    "Suse": ,
    "Oracle": ,
    "Fedora": ,
}

def get_services():
    result = list()
    services = nmap.nmap_version_detection(ip)[ip]["ports"]

    for service in services:
        result.append({
            "servicio": service["service"]["name"],
            "producto": service["service"]["product"],
            "version": service["service"]["version"]
        })
    
    return result

def get_os():
    os_data = os.popen('cat /etc/os-release').read().strip()
    clean_os_data = os_data.split("\n")

    for element in clean_os_data:
        i = element.index("=")
        keys.append(element[0:i])
        values.append(element[i+2:-1])

    os = dict(zip(keys, values))

    return {
        "os": {
            "name": os["ID"]
            "version": int(os["VERSION"])
            "like": os["ID_LIKE"]
        }
    }

def get_package_manager(os, os_like):
    result = str()

    if os in package_manager.keys():
        result = package_manager[os]
    elif os_like in package_manager.keys():
        result = package_manager[os]
    
    return result


def get_data():
    os = get_os()
    package_manager = get_package_manager()
    services = get_services()
    result = {**os, **package_manager, **services}
    return result


def update_data()
    pass

print(get_data)
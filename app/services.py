#!/usr/bin/env python
import nmap3
nmap = nmap3.Nmap()

def get_services():
    result = list()

    services = nmap.nmap_version_detection("127.0.0.1")
    print(services)
    for service in services:
        print(service)
        result.append({
            "servicio": service["service"]["name"],
            "producto": service["service"]["product"],
            "version": service["service"]["version"]
        })
    
    return result

def main():
    result = get_services()
    print(result)


if __name__ == '__main__':
    main()
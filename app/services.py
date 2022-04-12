#!/usr/bin/env python
import os
import nmap3
import json

nmap = nmap3.Nmap()
ip = "127.0.0.1"

def get_services():
    data = dict()
    services = nmap.nmap_version_detection(ip)[ip]["ports"]

    for service in services:
        data.append({
            "servicio": service["service"]["name"],
            "producto": service["service"]["product"],
            "version": service["service"]["version"]
        })

    result = {"servicios" : data}
    
    with open("servicesData.json", "w") as jsonFile:
        json.dump(result, jsonFile)

def update_services():
    with open("servicesData.json", "r") as jsonFile:
        data = json.load(jsonFile)

    update = dict()
    services = nmap.nmap_version_detection(ip)[ip]["ports"]

    for service in services:
        update.append({
            "servicio": service["service"]["name"],
            "producto": service["service"]["product"],
            "version": service["service"]["version"]
        })

    data["services"] = update

    with open("servicesData.json", "w") as jsonFile:
        json.dump(data, jsonFile)
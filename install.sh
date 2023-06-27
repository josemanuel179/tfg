#!/bin/bash

path=$(dirname "$(readlink -f "$0")")

echo '########## INSTALADOR SERVICIO HERMESD ##########'

echo 'Descargando paquetes necesarios...'

pip3 install --upgrade pip
pip3 install paramiko==3.2.0
pip3 install dash==2.10.2
pip3 install dash_bootstrap_components==1.4.1
pip3 install dash_core_components==2.0.0
pip3 install dash_html_components==2.0.0 
pip3 install plotly==5.15.0
pip3 install pandas==2.0.2 

systemctl start sshd

echo 'Generando directorios requeridos...'

mkdir -p /etc/hermesd/
mkdir -p /hermesd/

echo 'Copian los fichero en los correspondientes directorios...'

cp "$path/app/hermesd.service" /etc/systemd/system/.
cp "$path/app/hermesd-dashboard.service" /etc/systemd/system/.
cp "$path/app/service.conf" /etc/hermesd/.
cp "$path/app/hermes.py" /hermesd/.
cp "$path/app/service.py" /hermesd/.
cp "$path/app/dashboard.py" /hermesd/.

rm /hermesd/hermes.csv > /dev/null 2>&1
cp "$path/app/hermes.csv" /hermesd/.

chmod 600 /etc/hermesd/service.conf
chmod 400 /hermesd/hermes.csv
chmod 777 /etc/systemd/system/hermesd.service
chmod 777 /etc/systemd/system/hermesd-dashboard.service

chmod 100 /hermesd/hermes.py
chmod 100 /hermesd/service.py
chmod 100 /hermesd/dashboard.py

echo 'Reiniciando systemd...'
systemctl daemon-reload

echo '########## FIN ##########'
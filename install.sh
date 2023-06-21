#!/bin/bash

echo '########## INSTALADOR SERVICIO HERMESD ##########'

echo 'Descargando paquetes necesarios...'

pip3 install --upgrade pip > /dev/null 2>&1
pip3 install paramiko==3.2.0 --ignore-installed > /dev/null 2>&1
pip3 install dash==2.10.2 --ignore-installed > /dev/null 2>&1
pip3 install dash_bootstrap_components==1.4.1 --ignore-installed > /dev/null 2>&1
pip3 install dash_core_components==2.0.0 --ignore-installed > /dev/null 2>&1
pip3 install dash_html_components==2.0.0 --ignore-installed > /dev/null 2>&1
pip3 install plotly==5.15.0 --ignore-installed > /dev/null 2>&1
pip3 install pandas==2.0.2 --ignore-installed > /dev/null 2>&1

systemctl start sshd

echo 'Generando directorios requeridos...'

mkdir -p /etc/hermesd/
mkdir -p /hermesd/

echo 'Copian los fichero en los correspondientes directorios...'

cp app/hermesd.service /etc/systemd/system/.
cp app/service.conf /etc/hermesd/.
cp app/hermes.py /hermesd/.
cp app/service.py /hermesd/.
cp app/dashboard.py /hermesd/.
cp app/start.sh /hermesd/.

rm /hermesd/hermes.csv > /dev/null 2>&1
cp app/hermes.csv /hermesd/.

chmod 600 /etc/hermesd/service.conf
chmod 400 /hermesd/hermes.csv
chmod 777 /lib/systemd/system/hermesd.service

chmod 700 /hermesd/hermes.py
chmod 700 /hermesd/service.py
chmod 700 /hermesd/dashboard.py
chmod 700 /hermesd/start.sh

echo 'Reiniciando systemd...'
systemctl daemon-reload

echo '########## FIN ##########'
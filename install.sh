#!/bin/bash

echo '########## INSTALADOR SERVICIO HERMESD ##########'

echo 'Descargando paquetes necesarios...'

pip3 install --upgrade pip > /dev/null 2>&1
pip3 install setuptools_rust > /dev/null 2>&1
pip3 install paramiko > /dev/null 2>&1
pip3 install dash > /dev/null 2>&1
pip install pandas > /dev/null 2>&1

systemctl start sshd

echo 'Generando directorios requeridos...'

mkdir -p /etc/hermesd/
mkdir -p /hermesd/

echo 'Copian los fichero en los correspondientes directorios...'

cp app/hermesd.service /lib/systemd/system/.
cp app/service.conf /etc/hermesd/.
cp app/hermes.py /hermesd/.
cp app/service.py /hermesd/.
cp app/dashboard.py /hermesd/.
cp app/start.sh /hermesd/.

rm /hermesd/hermes.csv > /dev/null 2>&1
cp app/hermes.csv /hermesd/.

chmod 600 /etc/hermesd/service.conf
chmod +x /hermesd/start.sh

echo 'Reiniciando systemd...'
systemctl daemon-reload

echo '########## FIN ##########'
#!/bin/bash

echo '########## INSTALADOR SERVICIO HERMESD ##########'

echo 'Descargando paquetes necesarios...'

pip3 install --upgrade pip
pip3 install setuptools_rust
pip3 install paramiko
pip3 install dash
pip install pandas

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

chmod 600 app/service.conf

echo 'Reiniciando systemd...'
systemctl daemon-reload

echo '########## FIN ##########'


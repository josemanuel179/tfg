#!/bin/bash

echo '########## INSTALADOR SERVICIO HERMESD ##########'

echo 'Descargando paquetes necesarios...'

apt install -y python3-paramiko > /dev/null 2>&1
yum install -y python3-paramiko > /dev/null 2>&1
zypper install -y python3-paramiko > /dev/null 2>&1

apt install -y openssh /dev/null 2>&1
yum install -y openssh /dev/null 2>&1
zypper install -y openssh /dev/null 2>&1

/dev/null 2>&1systemctl sshd

echo 'Generando directorios requeridos...'

mkdir -p /etc/hermesd/
mkdir -p /hermesd/

echo 'Copian los fichero en los correspondientes directorios...'

cp app/hermesd.service /lib/systemd/system/.
cp app/service.conf /etc/hermesd/.
cp app/hermes.py /hermesd/.
cp app/service.py /hermesd/.
cp app/test-service.py /hermesd/.
cp app/Makefile /hermesd/.

rm /hermesd/hermes.csv > /dev/null 2>&1
cp app/hermes.csv /hermesd/.

echo 'Reiniciando systemd...'
systemctl daemon-reloaid

echo '########## FIN ##########'
fi

#!/bin/bash

echo '########## DESINSTALADOR SERVICIO HERMESD ##########'

echo 'Parando servicios...'

systemctl stop hermesd
systemctl stop hermesd-dashboard

echo 'Eliminando ficheros...'

rm -rf /etc/hermesd/
rm -rf /hermesd/
rm /etc/systemd/system/hermesd.service
rm /etc/systemd/system/hermesd-dashboard.service

echo 'Reiniciando servicios...'

systemctl daemon-reload

echo '########## FIN ##########'


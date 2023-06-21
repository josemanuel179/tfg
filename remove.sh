#!/bin/bash

echo '########## DESINSTALADOR SERVICIO HERMESD ##########'

echo 'Parando servicios...'

systemctl stop hermesd

echo 'Eliminando ficheros...'

rm -rf /etc/hermesd/
rm -rf /hermesd/
rm /etc/systemd/system/hermesd.service

echo 'Reiniciando servicios...'

systemctl daemon-reload

echo '########## FIN ##########'


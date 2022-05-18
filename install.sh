#!/bin/bash

echo '########## INSTALADOR SERVICIO HERMESD ##########'

apt install -y python3-paramiko
yum install -y python3-paramiko
zypper install -y python3-paramiko

mkdir -p /etc/hermesd/
mkdir -p /hermesd/

cp app/hermesd.service /lib/systemd/system/.
cp app/service.conf /etc/hermesd/.
cp app/service.py /hermesd/.
cp app/hermes.py /hermesd/.

systemctl daemon-reload
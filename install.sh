#!/bin/bash

echo '########## INSTALADOR SERVICIO HERMESD ##########'

pip install --upgrade pip
pip3 install -r app/requirements.txt

mkdir -p /etc/hermesd/
mkdir -p /hermesd/

cp app/hermesd.service /lib/systemd/system/.
cp app/service.conf /etc/hermesd/.
cp app/service.py /hermesd/.
cp app/main.py /hermesd/.

systemctl daemon-reload
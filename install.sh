#!/bin/bash

echo '########## INSTALADOR SERVICIO HERMESD ##########'

echo 'Instalación de los módulos necesarios'
echo -ne '>>>                       [20%]\r'
pip install --upgrade pip
pip3 install -r app/requirements.txt
sleep 2

echo 'Creación de los directorios necesarios'
echo -ne '>>>>>>>                   [40%]\r'
mkdir -p /etc/hermesd/
mkdir -p /hermesd/
sleep 2

echo 'Ejecución test unitarios servicio'
echo -ne '>>>>>>>>>>>>>>            [60%]\r'
python3 -m unittest -v app/test-service.py
sleep 2

echo 'Copia de los fichero necesarios a los directorios'
echo -ne '>>>>>>>>>>>>>>>>>>>>>>>   [80%]\r'
cp app/hermesd.service /lib/systemd/system.
cp app/service.conf /etc/hermesd/.
cp app/service.py /hermesd/.
cp app/main.py /hermesd/.
sleep 2

echo 'Reinicio systemctl'
echo -ne '>>>>>>>>>>>>>>>>>>>>>>>>>>[100%]\r'
systemctl daemon-reload
echo -ne '\n'
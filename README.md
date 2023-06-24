# Trabajo Fin de Grado - Servicio Linux - Hermes

## Introducción
Servicio diseñado para identificar, analizar y actualizar, de forma automática, todos los servicios instalados en una máquina Linux a través de SSH. Las máquinas deben estar basadas en las distribuciones Debian, Fedora y OpenSUSE.

1. **Autor**: José Manuel Martínez Sánchez
2. **Lenguaje de programación**: Python 3.8
3. **Herramientas de desarrollo**: VS Code, VIM, VirtualBox, GNU Make 3.81

# Módulos necesarios
Para ejecutar el servicio se requiere de los módulos
```
paramiko==2.10.4
dash==2.10.2
dash_bootstrap_components==1.4.1
dash_core_components==2.0.0
dash_html_components==2.0.0
plotly==5.15.0
pandas==2.0.2
```

## Instalación
El proceso de instalación del servicio es muy sencillo, solo se debe **ejecutar el fichero install.sh** desde una terminal de la siguiente forma

```
sh ./install.sh
```

Una vez se haya ejecutado el fichero, se puede **comprobar** que el servicio ha sido **instalado correctamente** mediante la instrucción
```
systemctl status hermesd
```
El resultado de esta ejecución dese de ser

![intalled service](https://github.com/josemanuel179/tfg/blob/main/doc/capturas/intalled.png)

## Configuración del servicio
Antes de poder ejecutar el, se deberá configurar el fichero **/etc/hermesd/service.conf**. En este encontraremos los siguientes campos

<dl>
  <dt>network</dt>
  <dd>Dirección o direcciones IP de las máquinas a analizar. Este campo permite introducir: </dd>
  <dd>IP únicas - 192.168.56.1<br />Varias IPs - 192.168.56.1, 192.168.56.2, 192.168.56.3<br />Rangos de IPs - 192.168.56.110-192.168.56.114<br />Redes completas -192.168.56.0/24</dd>

  <dt>time</dt>
  <dd>Tiempo de espera entre cada análisis, en horas.</dd>

  <dt>user</dt>
  <dd>Nombre del usuario de acceso las maquinas analizadas.</dd>

  <dt>password</dt>
  <dd>Contraseña para el usuario.</dd>
</dl>


## Ejecución del servicio
Para ejecutar el servicio únicamente debe **ejecutar la instrucción**. 
```
systemctl start hermesd
```
En el caso de que se quiera ejecutar el servicio siempre en el momento de inicio de la máquina, se deberá usar la siguiente instrucción
```
systemctl enable hermesd
```

Una vez ejecutada la instrucción, puede **comprobar** que el servicio se ha **levantado correctamente** mediante el comando previamente usado
```
systemctl status hermesd
```
El resultado de esta ejecución dese ser

![start service](https://github.com/josemanuel179/tfg/blob/main/doc/capturas/start.png)

## Ejecución de los test unitarios
Para ejecutar los test unitarios, primero se deberán configurar las credenciales de acceso **en los ficheros incluidos en el directorio app/test/**. Estas credencias deben de contar con privilegios de superusuario en la máquina en donde se desean ejecutar. 

Una vez configurdo, desde el directorio **app**, se podrán ejecutar los test mediante la instrucción
```
make test
```

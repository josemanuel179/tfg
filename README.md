# Trabajo Fin de Grado - Servicio Linux - Hermes

## Introducción
Servicio diseñado para indentificar, analizar y actulizar, de forma automática, todos los servicios instalados en una máquina Linux a través de SSH. Las máquinas deben estar basadas en las distribuciones Debian, Fedora y OpenSUSE.

1. **Autor**: José Manuel Martínez Sánchez
2. **Lenguaje de programación**: Python 3.8
3. **Herramientas de desarrollo**: VS Code, VIM, VirtualBox, GNU Make 3.81

# Modulos necesarios
Para ejecutar el servicio se requiere del módulo
```
paramiko==2.10.4
```

## Instalación
El proceso de instalación del servicio es muy sencillo, solo se debe **ejecutar el fichero install.sh** desde una terminal de la siguiente forma

```
./install.sh
```

Una vez se haya ejecutado el fichero, se puede **comprobar** que el servicio ha sido **instalado correctamente** mediante la instrucción
```
systemctl status hermesd
```
El resultado de esta ejecución dese de ser

![intalled service](https://github.com/josemanuel179/tfg/blob/main/documentacion/capturas/intalled.png)

## Configuración del servicio
Antes de poder ejecutar el, se debera configurar el fichero **/etc/hermesd/service.conf**. En este encontraremos los siguiente campos

<dl>
  <dt>network</dt>
  <dd>Dirección o direcciones IP de las máquinas a analizar. Este campo permite introducir: </dd>
  <dd>IP únicas - 192.168.56.1<br />Varias IPs - 192.168.56.1, 192.168.56.2, 192.168.56.3<br />Rangos de IPs - 192.168.56.110-192.168.56.114<br />Redes completas -192.168.56.0/24</dd>

  <dt>time</dt>
  <dd>Tiempo de espera entre cada análisis, en horas.</dd>

  <dt>user</dt>
  <dd>Nombre de usuario de acceso las maquinas analiazadas.</dd>

  <dt>password</dt>
  <dd>Contrasña para el usuario.</dd>

  <dt>key</dt>
  <dd>LLave privada, en caso de que la conexión SSH a la máquina lo requiera.</dd>
</dl>


## Ejeccución del servicio
Para ejecutar el servicio unicmanete debe **ejecutar la instrucción**. 
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

![start service](https://github.com/josemanuel179/tfg/blob/main/documentacion/capturas/start.png)

## Ejeccución de los test unitarios
Para ejecutar los test unitarios en una terminal, desde el directorio **app**, ejecutar la intrucción
```
make test
```
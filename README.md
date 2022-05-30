# Trabajo Fin de Grado - Servicio Linux - Hermes

## Introducción
Servicio diseñado para indentificar, analizar y actulizar, de forma automática, todos los servicios instalados en una máquina Linux a través de SSH. Las máquinas deben estar basadas en las distribuciones Debian, Fedora y OpenSUSE.

1. **Autor**: José Manuel Martínez Sánchez
2. **Lenguaje de programación**: Python 3.8
3. **Herramientas de desarrollo**: VS Code, VIM, VirtualBox, Terminal

## Instalación
El proceso de instalación del servicio es muy sencillo, solo se debe ejecutar el fichero **install.sh** desde una terminal de la siguiente forma

```
./install.sh
```

Una vez se haya ejecutado el fichero, se puede **comprobar** que el servicio ha sido instalado correctamente mediante la instrucción
```
systemctl status hermesd
```
El resultado de este ejecución dese ser
![intalled service](https://github.com/josemanuel1792/tfg/tree/main/documentacion/capturas/installed.png)


## Configuración del servicio
Antes de poder ejecutar el, se debera configurar el fichero **/etc/hermesd/service.conf**. En este encontraremos los siguiente campos

<dl>
  <dt>network</dt>
  <dd>Dirección o direcciones IP de las máquinas a analizar. Este campo permite introducir: </dd>
  <dd>IP únicas (192.168.56.1)</dd>
  <dd>Rangos de IPs (192.168.56.110-192.168.56.114)</dd>
  <dd>Redes completas (192.168.56.0/24)</dd>

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
Para ejecutar el servicio unicmanete debe ejecutar la instrucción. 
```
systemctl start hermesd
```
En el caso de que se quiera ejecutar el servicio en el momento de inicio de la máquina, se deberá usar la siguiente instrucción
```
systemctl enable hermesd
```

Una vez ejecutada la instrucción, puede comprobar que el servicio se ha levantado correctamente mediante el comando previamente usado
```
systemctl status hermesd
```
El resultado de este ejecución dese ser
![start service](https://github.com/josemanuel1792/tfg/tree/main/documentacion/capturas/start.png)

## Ejeccución de los test unitarios

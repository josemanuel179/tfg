# Trabajo Fin de Grado - Servicio Linux - Hermes

## Introducción
Servicio diseñado para indentificar, analizar y actulizar, de forma automática, todos los servicios instalados en una máquina Linux. Las máquinas deben estar basadas en las distribuciones Debian, Fedora y OpenSUSE.

**Autor**: José Manuel Martínez Sánchez
**Lenguaje de programación**: Python 3.8
**Herramientas de desarrollo**: VS Code, VIM, VirtualBox, Terminal

## Instalación
El proceso de instalación del servicio es muy sencillo, solo se debe ejecutar el fichero **install.sh** desde una terminal de la siguiente forma

```
./install.sh
```

Una vez se haya ejecutado el fichero, se puede comprobar que el servicio se ha instalado correctamente mediante la instrucción
```
systemctl status hermesd
```
El resultado de este ejecución dese ser
# Meter foto


## Configuración del servicio
Antes de poder ejecutar el, se debera configurar el fichero **/etc/hermesd/service.conf**. En este encontraremos los siguiente campos
1. **network**
    Dirección o direcciones IP de las máquinas a analizar. Este campo permite introducir IP únicas (192.168.56.1), rangos de IPs (192.168.56.110-192.168.56.114) o redes completas (192.168.56.0/24)
2. **time**
    Tiempo de espera entre cada análisis, en horas
3. ***user**
    Nombre de usuario de las maquinas analiazadas
4. **password**
    Contrasña para el usuario
5. **key**
    LLave 


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


## Ejeccución de los test unitarios

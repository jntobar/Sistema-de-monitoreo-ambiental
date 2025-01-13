# Sistema de Monitoreo de Condiciones Ambientales

## Descripción
Este proyecto integrador de Ingeniería en Telemática tiene como objetivo el desarrollo de un sistema de monitoreo de condiciones ambientales para espacios públicos. El sistema permitirá recopilar y analizar datos sobre la calidad del aire, temperatura, humedad y otros factores ambientales, contribuyendo a la mejora del entorno urbano.

## Diagrama Esquemático
A continuación, se muestra el diagrama esquemático del sistema:

![Esquemático del Sistema](https://github.com/jntobar/Sistema-de-monitoreo-ambiental/blob/main/Circuit%20Schematic/Esquematico.png?raw=true)


## Tecnologías Utilizadas
- **InfluxDB**: Base de datos de series temporales para almacenar los datos de sensores.
- **Grafana**: Herramienta de visualización de datos para mostrar en tiempo real los parámetros monitoreados.
  
## Instalación
Sigue estos pasos para instalar y configurar el sistema en tu entorno local:

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/jntobar/Sistema-de-monitoreo-ambiental.git
   cd Sistema-de-monitoreo-ambiental

2. **Compilar codigo en esp32**:
   En la carpeta Hardware code se encuentra el codigo final para la esp32, este codigo se lo debe ejecutar utilizando algun IDE de microcontroladores o placas
3. **Compilar codigo en raspberry pi**:
   para correr este codigo dirijase a la carpeta sofware code y ejecute el script con sudo python datos.py y pongalo como servicio para que al iniciar el sistema se ejecute directamente.

from influxdb_client import InfluxDBClient, Point, WritePrecision
import serial
import time
import threading

# Configuración de InfluxDB
url = "http://localhost:8086"  # URL de InfluxDB (ajusta según la configuración de tu servidor)
token = "E5tNZbL2HPUSfR-eXV_AS0UK1fxDoKivEw6-B2vZuIyOWAgTu75mii47COrRX8mlrnUYtQalhx3KHejHJMqANQ=="  # Token de autenticación de InfluxDB
org = "Totem"      # Organización en InfluxDB
bucket = "Totem_Sensores"         # Bucket para almacenar los datos

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Configura los puertos seriales
ESP32_PORT = '/dev/ttyUSB0'  # Puerto de la ESP32
SENSOR_PORT = '/dev/ttyUSB1'  # Puerto del sensor AM1008W
BAUD_RATE = 9600

# Comando a enviar al sensor
cubic = bytearray([0x11, 0x02, 0x01, 0x01, 0xEB])

# Variable compartida para almacenar los datos
data = {"esp32": None, "sensor": None}

# Función para escribir datos en InfluxDB
def write_to_influxdb(measurement,data):
    point = Point(measurement).tag("device", measurement)
    for key, value in data.items():
        point = point.field(key, value)
    write_api.write(bucket=bucket, org=org, record=point)
    
# Función para leer datos de la ESP32
def read_esp32():
    try:
        esp32_ser = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Espera a que el puerto serial este listo

        while True:
            if esp32_ser.in_waiting > 0:
                line = esp32_ser.readline().decode('utf-8').rstrip()  # Lee la linea y decodifica
                data["esp32"] = line  # Actualiza los datos de la ESP32
                write_to_influxdb(data["esp32"])
                print_combined_data()  # Imprime los datos combinados
    except serial.SerialException as e:
        print(f"Error al abrir el puerto ESP32: {e}")

# Función para leer datos del sensor AM1008W
def read_sensor():
    try:
        sensor_ser = serial.Serial(SENSOR_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Espera para establecer la conexión

        while True:
            sensor_ser.write(cubic)  # Envía el comando al sensor
            time.sleep(0.25)  # Espera para permitir que el sensor responda
            if sensor_ser.in_waiting >= 25:  # Verifica si hay datos disponibles
                response = sensor_ser.read(25)  # Lee 25 bytes
                co2 = (response[3] * 256.0) + response[4]
                voc = (response[5] * 256.0) + response[6]
                rh = ((response[7] * 256.0) + response[8]) / 10
                temp = ((response[9] * 256.0 + response[10] - 500) / 10)
                grimn = (response[13] * 256.0) + response[14]
                tsi = (response[15] * 256.0) + response[16]

                # Actualiza los datos del sensor
                data["sensor"] = f"CO2: {co2} ppm - VOC: {voc} - RH: {rh}% - Temp: {temp}°C - GRIMM PM 2.5: {grimn} µg/m³ - TSI PM 2.5: {tsi} µg/m³"
                write_to_influxdb(data["sensor"])
                print_combined_data()  # Imprime los datos combinados
            else:
                print("No hay respuesta del sensor.")
    except serial.SerialException as e:
        print(f"Error al abrir el puerto del sensor: {e}")

# Función para imprimir los datos combinados
def print_combined_data():
    if data["esp32"] and data["sensor"]:
        print(f"{data['esp32']} - {data['sensor']}")

# Crea y ejecuta los hilos para leer ambos dispositivos
try:
    esp32_thread = threading.Thread(target=read_esp32)
    sensor_thread = threading.Thread(target=read_sensor)

    esp32_thread.start()
    sensor_thread.start()

    esp32_thread.join()
    sensor_thread.join()

except KeyboardInterrupt:
    print("Interrumpido por el usuario.")
finally:
    # No es necesario cerrar los puertos aquí, ya que los hilos se ejecutan indefinidamente
    pass

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import serial
import time
import threading

# Configura los puertos seriales
ESP32_PORT = '/dev/ttyS0'  # Puerto de la ESP32
SENSOR_PORT = '/dev/ttyUSB0'  # Puerto del sensor AM1008W
BAUD_RATE = 9600

# Configuración de InfluxDB
url = "https://us-east-1-1.aws.cloud2.influxdata.com/"
token = "Cbu8yUvzzcR04cnpqJTfTwDrCJsXVrA0Xw4dF5Lr9FQwSAnr2b16UTi75LtlWZuJlt67QjK5q9IFc0V3MOI3MA=="
org = "Totem"
bucket = "Totem_1"

# Inicializar cliente de InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Comando a enviar al sensor
cubic = bytearray([0x11, 0x02, 0x01, 0x01, 0xEB])

# Variable compartida para almacenar los datos
data = {"esp32": None, "sensor": None}

# Función para enviar datos a InfluxDB
def send_to_influxdb(data):
    point = (
        Point("SensorData")
        .field("MQ135_sensor_AO_value", float(data["esp32"].split("-")[0].split(":")[1].strip()))
        .field("Percentage", float(data["esp32"].split("-")[1].split(":")[1].strip().replace('%', '')))
        .field("Rain_Analog_Value", float(data["esp32"].split("-")[2].split(":")[1].strip()))
        .field("Rain_Digital_Value", float(data["esp32"].split("-")[3].split(":")[1].strip()))
        .field("Temperature", float(data["esp32"].split("-")[4].split(":")[1].strip().split(" ")[0]))
        .field("Humidity", float(data["esp32"].split("-")[5].split(":")[1].strip().split(" ")[0]))
        .field("Pressure", float(data["esp32"].split("-")[6].split(":")[1].strip().split(" ")[0]))
        .field("Approx_Altitude", float(data["esp32"].split("-")[7].split(":")[1].strip().split(" ")[0]))
        .field("Valor_crudo_ruido", float(data["esp32"].split("-")[8].split(":")[1].strip()))
        .field("Noise_Level", float(data["esp32"].split("-")[9].split(":")[1].strip().split(" ")[0]))
        .field("CO2", float(data["sensor"].split("-")[0].split(":")[1].strip().replace('ppm', '').strip()))
        .field("VOC", float(data["sensor"].split("-")[1].split(":")[1].strip()))
        .field("RH", float(data["sensor"].split("-")[2].split(":")[1].strip().split("%")[0]))
        .field("Temp", float(data["sensor"].split("-")[3].split(":")[1].strip().split("°")[0]))
        .field("GRIMM_PM_2_5", float(data["sensor"].split("-")[4].split(":")[1].strip().split(" ")[0]))
        .field("TSI_PM_2_5", float(data["sensor"].split("-")[5].split(":")[1].strip().split(" ")[0]))
    )
    write_api.write(bucket=bucket, org=org, record=point)
    print("Datos enviados a InfluxDB.")

# Función para leer datos de la ESP32
def read_esp32():
    try:
        esp32_ser = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)

        while True:
            if esp32_ser.in_waiting > 0:
                line = esp32_ser.readline().decode('utf-8').rstrip()
                data["esp32"] = line
                print_combined_data()
    except serial.SerialException as e:
        print(f"Error al abrir el puerto ESP32: {e}")

# Función para leer datos del sensor AM1008W
def read_sensor():
    try:
        sensor_ser = serial.Serial(SENSOR_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)

        while True:
            sensor_ser.write(cubic)
            time.sleep(0.25)
            if sensor_ser.in_waiting >= 25:
                response = sensor_ser.read(25)
                co2 = (response[3] * 256.0) + response[4]
                voc = (response[5] * 256.0) + response[6]
                rh = ((response[7] * 256.0) + response[8]) / 10
                temp = ((response[9] * 256.0 + response[10] - 500) / 10)
                grimn = (response[13] * 256.0) + response[14]
                tsi = (response[15] * 256.0) + response[16]
                data["sensor"] = f"CO2: {co2} ppm - VOC: {voc} - RH: {rh}% - Temp: {temp}°C - GRIMM PM 2.5: {grimn} µg/m³ - TSI PM 2.5: {tsi} µg/m³"
                print_combined_data()
            else:
                print("No hay respuesta del sensor.")
    except serial.SerialException as e:
        print(f"Error al abrir el puerto del sensor: {e}")

# Función para imprimir los datos combinados
def print_combined_data():
    if data["esp32"] and data["sensor"]:
        print(f"{data['esp32']} - {data['sensor']}")
        send_to_influxdb(data)

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

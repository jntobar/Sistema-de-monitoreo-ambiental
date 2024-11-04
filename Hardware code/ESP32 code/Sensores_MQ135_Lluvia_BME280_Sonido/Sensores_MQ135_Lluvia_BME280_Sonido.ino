#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define AO_PIN 36         // Pin GPIO36 del ESP32 para el sensor MQ135
#define RAIN_ANALOG 39    // Pin GPIO39 para la lectura analógica del sensor de lluvia
#define RAIN_DIGITAL 34   // Pin GPIO34 para la lectura digital del sensor de lluvia
#define NOISE_SENSOR_PIN 14  // Pin GPIO34 para el sensor de ruido
#define SEALEVELPRESSURE_HPA (1013.25) // Presión a nivel del mar en hPa

// Inicializa el sensor BME280
Adafruit_BME280 bme;

const int minValue = 1000;  // Valor mínimo de lectura (0%)
const int maxValue = 2000; // Valor máximo de lectura (100%)

const int noiseMinValue = 0;    // Valor mínimo del sensor
const int noiseMaxValue = 1023;  // Valor máximo del sensor
const float noiseMinDB = 30.0;   // Nivel mínimo en dB
const float noiseMaxDB = 120.0;  // Nivel máximo en dB


void setup() {
  Serial.begin(9600);
  pinMode(RAIN_DIGITAL, INPUT);  // Configura el pin digital del sensor de lluvia
  analogSetAttenuation(ADC_11db); // Configura la atenuación del ADC

  // Inicia el sensor BME280
  /*if (!bme.begin(0x76)) { // Dirección I2C del BME280
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1) delay(10);
  }*/
  
  bool status = bme.begin(); 
  if (!status) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }

  Serial.println("Warming up the MQ135 sensor");
  delay(30000);  // Espera 30 segundos para calentar el sensor
}

void loop() {
  // Lectura del sensor MQ135
  int gasValue = analogRead(AO_PIN);
  float percentage = map(gasValue, minValue, maxValue, 0, 100);
  percentage = constrain(percentage, 0, 100);  // Limitar entre 0 y 100

  // Lectura del sensor de lluvia
  int rainAnalogVal = analogRead(RAIN_ANALOG); // Lee el valor analógico
  int rainDigitalVal = digitalRead(RAIN_DIGITAL); // Lee el valor digital

  // Lecturas del sensor BME280
  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();
  float pressure = bme.readPressure() / 100.0F; // Convertir a hPa
  float altitude = bme.readAltitude(SEALEVELPRESSURE_HPA); // Altitud en metros

  // Lectura del sensor de ruido
  int noiseValue = analogRead(NOISE_SENSOR_PIN);
  // Convertir el valor analógico a dB
  float noiseDB = map(noiseValue, noiseMinValue, noiseMaxValue, noiseMinDB, noiseMaxDB);


  // Mostrar resultados en una sola línea
  String dataString = "MQ135 sensor AO value: " + String(gasValue) + 
                      " - Percentage: " + String(percentage) + "%" +
                      " - Rain Analog Value: " + String(rainAnalogVal) + 
                      " - Rain Digital Value: " + String(rainDigitalVal) +
                      " - Temperature: " + String(temperature) + " °C" + 
                      " - Humidity: " + String(humidity) + " %" + 
                      " - Pressure: " + String(pressure) + " hPa" + 
                      " - Approx. Altitude: " + String(altitude) + " m" +
                      " - Valor crudo del ruido: " + String(noiseValue) + 
                      " - Noise Level: " + String(noiseDB) + " dB";

  Serial.println(dataString);

  
  delay(1000);  // Espera 1 segundo antes de la siguiente lectura
}
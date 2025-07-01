import network
import time
from machine import Pin
import dht
import ujson
import urequests
import random

SSID = 'Wokwi-GUEST'
PASSWORD = ''

SERVER_URL = "http://<NGROK_URL>/procesar_datos"

sensor_pins = [15, 4, 5, 18, 19]
led_pins = [13, 12, 14, 27, 26]
ubicaciones = [
  (-7.317960, -79.537392),
  (-7.310000, -79.537392),
  (-7.317960, -79.527392),
  (-7.320000, -79.545000),
  (-7.312000, -79.540000),
]

sensores = [dht.DHT22(Pin(p)) for p in sensor_pins]
leds = [Pin(p, Pin.OUT) for p in led_pins]

print("Conectando a WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(SSID, PASSWORD)
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" ¡Conectado!")

UMBRAL_HUMEDAD = 30

while True:
  for i in range(5):
    try:
      sensores[i].measure()
      temp = round(random.uniform(22.0 + i, 30.0 + i), 1)
      hum = round(random.uniform(15.0 + i, 55.0 - i), 1)
      soil = round(random.uniform(15.0 + i, 55.0 - i), 1)
      alerta = 1 if hum < UMBRAL_HUMEDAD else 0
      leds[i].value(alerta)

      payload = {
        "sensor_id": f"sensor_{i+1}",
        "temperature": temp,
        "humidity": hum,
        "soil_moisture": soil,
        "alerta_humedad": alerta,
        "lat": ubicaciones[i][0],
        "lng": ubicaciones[i][1]
      }

      headers = {
        "Content-Type": "application/json"
      }

      print(f"[{payload['sensor_id']}] Enviando datos:", payload)
      response = urequests.post(SERVER_URL, headers=headers, data=ujson.dumps(payload))
      print(f"[{payload['sensor_id']}] Respuesta:", response.status_code)
      response.close()

    except Exception as e:
      print(f"Error en sensor {i+1}:", e)

    time.sleep(1)  # pequeña pausa entre sensores

  print("Esperando 10 segundos para siguiente ciclo...\n")
  time.sleep(10)

import time
import random
import json
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
TOPIC = "sensor/pressure"

client = mqtt.Client()
client.connect(BROKER, 1883)

print("Sensore simulato avviato")

while True:
    value = round(random.uniform(1020, 1050), 2)

    payload = {
        "sensor": "pressure",
        "value": value,
        "unit": "hPa"
    }

    client.publish(TOPIC, json.dumps(payload))
    print("Pubblicato:", payload)

    time.sleep(1)

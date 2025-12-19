import time
import random
import json
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
TOPIC = "sensor/temperature"

client = mqtt.Client()
client.connect(BROKER, 1883)

print("Sensore simulato avviato")

while True:
    value = round(random.uniform(18, 30), 2)

    payload = {
        "sensor": "temperature",
        "value": value,
        "unit": "C"
    }

    client.publish(TOPIC, json.dumps(payload))
    print("Pubblicato:", payload)

    time.sleep(1)

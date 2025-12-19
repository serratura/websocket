import time
import random
import json
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
TOPIC = "sensor/humidity"

client = mqtt.Client()
client.connect(BROKER, 1883)

print("Sensore simulato avviato")

while True:
    value = round(random.uniform(40, 60), 2)

    payload = {
        "sensor": "humidity",
        "value": value,
        "unit": "%"
    }

    client.publish(TOPIC, json.dumps(payload))
    print("Pubblicato:", payload)

    time.sleep(1)

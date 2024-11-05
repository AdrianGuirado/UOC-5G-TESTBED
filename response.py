import paho.mqtt.client as mqtt
import time

from functions.parameters import *

output_file = "mqtt_messages.txt"

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Message received on topic {msg.topic}: {message}")

    with open(output_file, "a") as file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] Topic: {msg.topic}, Message: {message}\n")

def configure_mqtt():
    global mqtt_client

    mqtt_client = mqtt.Client()
    mqtt_client.on_message = on_message
    mqtt_client.connect(server_ip)
    mqtt_client.subscribe(response_topic)

    mqtt_client.loop_start()

try:
    configure_mqtt()
    while True:
        pass 
except KeyboardInterrupt:
    print("Disconnecting...")
finally:
    mqtt_client.loop_stop()
    mqtt_client.disconnect()

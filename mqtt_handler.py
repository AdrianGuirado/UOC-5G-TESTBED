# mqtt_handler.py

import paho.mqtt.client as mqtt
from task_manager import process_tasks
from functions.parameters import *

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Message received on topic {msg.topic}: {message}")
    process_tasks(message)

def configure_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(server_ip, 1883)
    client.subscribe(commands_topic)
    client.loop_forever()

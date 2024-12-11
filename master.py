import paho.mqtt.client as mqtt
from functions.parameters import *
import time
import os

file_path_commands = "commands.txt"

client = mqtt.Client()
client.connect(server_ip)

with open(file_path_commands, "r") as file:
    for line in file:
        command = line.strip()
        if command:
            time.sleep(0.1)
            client.publish(commands_topic, command)
            print(f"Message transmitted: {command}")

client.disconnect()

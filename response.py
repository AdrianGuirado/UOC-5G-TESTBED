import paho.mqtt.client as mqtt
from functions.parameters import *
from datetime import datetime

messages_by_header = {}

def on_message(client, userdata, message):
    message_content = message.payload.decode()
    print(f"Message received: {message_content}")

    if "_" in message_content:
        header, content = message_content.split("_", 1)
    else:
        header, content = message_content.split(" ", 1)
        
    if header not in messages_by_header:
        messages_by_header[header] = []
    messages_by_header[header].append(content)
    
    if message_content.startswith("STOP_"):
        stop_header = message_content.split("_", 1)[1].strip()
        
        if stop_header in messages_by_header:
            filename = f"{stop_header}.txt"
            
            with open(filename, "w") as file:
                for msg in messages_by_header[stop_header]:
                    file.write(f"{msg}\n")
            print(f"Saved all messages for {stop_header} to {filename}")
            
            del messages_by_header[stop_header]

client = mqtt.Client()
client.on_message = on_message
client.connect(server_ip, 1883)
client.subscribe(response_topic)
client.loop_forever()
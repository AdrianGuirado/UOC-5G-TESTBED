import paho.mqtt.client as mqtt
from functions.parameters import *
from datetime import datetime

current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"messages_received_{current_time}.txt"

all_messages = []

def on_message(client, userdata, message):
    message = message.payload.decode()
    print(f"Message received: {message}")
    
    all_messages.append(message)
    
    if message.startswith("SAVE_FILE "):
        filename = message.split(" ", 1)[1].strip()
        
        with open(filename, "w") as file:
            for msg in all_messages:
                file.write(f"{msg}\n")
            print(f"Saved all messages to {filename}")
    
    with open(output_file, "a") as file:
        file.write(f"{message}\n")

client = mqtt.Client()
client.on_message = on_message
client.connect(server_ip, 1883)
client.subscribe(response_topic)
client.loop_forever()

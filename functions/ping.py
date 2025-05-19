# ping.py

import threading
import subprocess
import time
import paho.mqtt.client as mqtt
from functions.parameters import *

ping_process = None

def run_ping(arguments):

    global ping_process
    command = ["ping"]
    arguments = arguments.split(" ")
    for arg in arguments:
        command.append(str(arg)) 
    print(command)   
    ping_process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

def read_ping_output(header):
    
    client = mqtt.Client()
    client.connect(server_ip, 1883)
    client.subscribe(response_topic)
    time.sleep(0.1) 
    with open(f"{header}.txt", "w") as file:
        try:
            while ping_process and ping_process.poll() is None:
                line = ping_process.stdout.readline()
                if line:
                    file.write(line)
                    print(f"Estoy guardando esto {line}")
                    client.publish(response_topic, f"{header} {line.strip()}")
                else:
                    break
        finally:
            client.disconnect()

def ping_function(arguments):

    header, arguments = arguments.split(" ")

    thread_ping = threading.Thread(target=run_ping, args=(arguments,))
    thread_ping.start()

    time.sleep(0.1)

    thread_read = threading.Thread(target=read_ping_output, args=(header,))
    thread_read.start()

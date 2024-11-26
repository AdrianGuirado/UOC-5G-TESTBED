import threading
import subprocess
import time
import paho.mqtt.client as mqtt
from functions.parameters import *


connect_progress = None

def run_connect(arguments):

    global connect_progress
    command = [""]
    arguments = arguments.split(" ")
    for arg in arguments:
        command.append(str(arg)) 
    connect_progress = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

def read_connect_output(header):

    client = mqtt.Client()
    client.connect(server_ip, 1883)
    client.subscribe(response_topic)
    time.sleep(0.1)

    try:
        with open(f"{header}.txt", "w") as file:
            while connect_progress and connect_progress.poll() is None:
                line = connect_progress.stdout.readline()
                if line:
                    client.publish(response_topic, f"CONNECT SLICE {line.strip()}")
                    file.write(line)
                else:
                    break
            file.write("\n--- CONNECTSLICE COMPLETED ---\n")
            client.publish(response_topic, f"CONNECTSLICE FINISH")
        
    finally:
        client.disconnect()

def connect_function(arguments):

    header, arguments = arguments.split(" ")

    thread_ping = threading.Thread(target=run_connect, args=(arguments,))
    thread_ping.start()

    time.sleep(0.1)

    thread_read = threading.Thread(target=read_connect_output, args=(header,))
    thread_read.start()

# ping.py

import threading
import subprocess
import time
import paho.mqtt.client as mqtt
from functions.parameters import *

ping_process = None

def run_hping(arguments):

    global ping_process
    command = ["hping"]
    arguments = arguments.split(" ")
    for arg in arguments:
        command.append(str(arg)) 
    print(command)   
    ping_process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

def read_hping_output():
    client = mqtt.Client()
    client.connect(server_ip, 1883)
    client.subscribe(response_topic)
    time.sleep(0.1) 

    try:
        while ping_process and ping_process.poll() is None:
            line = ping_process.stdout.readline()
            if line:
                client.publish(response_topic, f"HPING {line.strip()}")
            else:
                break
    finally:
        client.disconnect()

def hping_function(arguments):
    thread_ping = threading.Thread(target=run_hping, args=(arguments,))
    thread_ping.start()

    time.sleep(0.1)

    thread_read = threading.Thread(target=read_hping_output)
    thread_read.start()

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
    ping_process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

def read_hping_output(header):
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
                    client.publish(response_topic, f"{header} {line.strip()}")
                else:
                    break
        finally:
            client.disconnect()

def hping_function(arguments):

    header, arguments = arguments.split(" ")

    thread_ping = threading.Thread(target=run_hping, args=(arguments,))
    thread_ping.start()

    time.sleep(0.1)

    thread_read = threading.Thread(target=read_hping_output, args=(header,))
    thread_read.start()

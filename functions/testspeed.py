# speedtest.py

import threading
import subprocess
import time
import paho.mqtt.client as mqtt
from functions.parameters import *

def speedtest_run(arguments):

    global speedtest_progres
    command = ["speedtest-cli"]
    arguments = arguments.split(" ")
    for arg in arguments:
        command.append(str(arg)) 
    print(command)   
    speedtest_progres = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

def speedtest_output(header):
    
    client = mqtt.Client()
    client.connect(server_ip, 1883)
    client.subscribe(response_topic)
    time.sleep(0.1) 
    with open(f"{header}.txt", "w") as file:
        try:
            while speedtest_progres and speedtest_progres.poll() is None:
                line = speedtest_progres.stdout.readline()
                if line:
                    file.write(line)
                    client.publish(response_topic, f"{header} {line.strip()}")
                else:
                    break
        finally:
            client.disconnect()

def speedtest_function(arguments):

    header, arguments = arguments.split(" ")

    thread_ping = threading.Thread(target=speedtest_run, args=(arguments,))
    thread_ping.start()

    time.sleep(0.1)

    thread_read = threading.Thread(target=speedtest_output, args=(header,))
    thread_read.start()
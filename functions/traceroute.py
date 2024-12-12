# traceroute.py

import threading
import subprocess
import time
import paho.mqtt.client as mqtt
from functions.parameters import *

traceroute_process = None


def run_traceRoute(arguments):
    global traceroute_process

    command = ["traceroute"]
    command.append(arguments)

    traceroute_process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

def read_traceRoute_output(header):

    client = mqtt.Client()
    client.connect(server_ip, 1883)
    client.subscribe(response_topic)

    try:
        with open(f"{header}.txt", "w") as file:
            while traceroute_process and traceroute_process.poll() is None:
                line = traceroute_process.stdout.readline()
                if line:
                    client.publish(response_topic, f"TRACEROUTE {line.strip()}")
                    file.write(line)
                else:
                    break
            file.write("\n--- TRACEROUTE COMPLETED ---\n")
            client.publish(response_topic, f"TRACEROUTE FINISH")
        
    finally:
        client.disconnect()

def traceRoute_function(arguments):

    header, arguments = arguments.split(" ")

    thread_traceRoute = threading.Thread(target=run_traceRoute, args=(arguments,))
    thread_traceRoute.start()

    time.sleep(0.1)

    thread_read = threading.Thread(target=read_traceRoute_output, args=(header,))
    thread_read.start()

    



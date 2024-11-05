# traceroute.py

import time
import paho.mqtt.client as mqtt
import threading
from functions.parameters import *
ping_process = None


def run_traceRoute(ip, max_hops, timeout):
    global ping_process

    command = ["traceroute"]

    if max_hops is not None:
        command.extend(["-m", str(max_hops)])
    if timeout is not None:
        command.extend(["-w", str(timeout)])
    command.append(ip)

def read_traceRoute_output():

    client = mqtt.Client()
    client.connect(server_ip, 1883)
    client.subscribe(response_topic)

    while ping_process and ping_process.stdout:
        line = ping_process.stdout.readline()
        if line:
            client.publish(response_topic, f"{line.strip()}")
        else:
            break

    client.disconnect()

def traceRoute_function(ip, max_hops, timeout):
    
    thread_traceRoute = threading.Thread(target=run_traceRoute, args=(ip, max_hops, timeout))
    thread_traceRoute.start()

    time.sleep(0.1)

    thread_read = threading.Thread(target=read_traceRoute_output)
    thread_read.start()

    client = mqtt.Client()
    client.connect(server_ip, 1883)
    client.subscribe(response_topic)

    command = ["traceroute"]

    if max_hops is not None:
        command.extend(["-m", str(max_hops)])
    if timeout is not None:
        command.extend(["-w", str(timeout)])
    command.append(ip)
    



# ping.py

import threading
import subprocess
import time
import paho.mqtt.client as mqtt
from functions.parameters import *



ping_process = None

def run_ping(ip, count=None, interval=None, timeout=None, size=None, ttl=None):

    global ping_process
    command = ["ping"]
    
    if count is not None:
        command.extend(["-c", str(count)])
    if interval is not None:
        command.extend(["-i", str(interval)])
    if timeout is not None:
        command.extend(["-W", str(timeout)])
    if size is not None:
        command.extend(["-s", str(size)])
    if ttl is not None:
        command.extend(["-t", str(ttl)])

    command.append(ip)

    print(command)

    ping_process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

def read_ping_output():
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

#def ping_function(ip, count, interval, timeout, size, ttl):
def ping_function(ip):
    thread_ping = threading.Thread(target=run_ping, args=(ip,))
    thread_ping.start()

    time.sleep(0.1)

    thread_read = threading.Thread(target=read_ping_output)
    thread_read.start()

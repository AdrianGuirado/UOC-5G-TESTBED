# speedtest.py

import time
import paho.mqtt.client as mqtt
from functions.parameters import *


def speedTest_function():
    while True:
        print(f"Executing speedTest_function, result: {3 * 3}")
        time.sleep(1)

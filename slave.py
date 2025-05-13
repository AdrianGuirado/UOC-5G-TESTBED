# slave.py

import multiprocessing
from mqtt_handler import configure_mqtt
from functions.parameters import *

if __name__ == '__main__':
    mqtt_listener_process = multiprocessing.Process(target=configure_mqtt)
    mqtt_listener_process.start()

    while True:
        pass

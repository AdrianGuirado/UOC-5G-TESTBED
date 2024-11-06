# task_manager.py

import multiprocessing

from functions.traceroute import traceRoute_function
from functions.ping import ping_function
from functions.custom import custom_function
from functions.hping import hping_function
from functions.testspeed import speedTest_function
from functions.parameters import *
 
import time

import paho.mqtt.client as mqtt

task_processes = {}
user = "USER1"

def start_process(function_key, target_function, *args):
        process = multiprocessing.Process(target=target_function, args=args)
        process.start()
        task_processes[function_key] = process

def stop_process(function_key):
        if function_key in task_processes:
            task_processes[function_key].terminate()
            task_processes[function_key].join()
            del task_processes[function_key]
        
def process_tasks(task):
    global task_processes

    if user not in task and "ALL" not in task:
        return
    
    function_type = task.split(":")

    print(function_type[1])

    if len(function_type) <= 1:
        print("Error in the command")
        return
    
    if "TRACEROUTE_STOP" in function_type[1]:
        stop_process("traceroute_function")

    elif "TRACEROUTE" in function_type[1]:
        command_parts = function_type[1].split()
        
        if command_parts[0].upper() == 'TRACEROUTE':
            command_parts = command_parts[1:]
        else:
            raise Exception("Error in the format using TRACEROUTE")
        
        arguments = ' '.join(command_parts)
        start_process("traceroute_function", traceRoute_function, arguments)

    
    elif "SPEEDTEST_STOP" in function_type[1] :
        stop_process("speedtest_function")

    elif "SPEEDTEST" in function_type[1]:
        start_process("speedtest_function", speedTest_function)

    elif "PING_STOP" in function_type[1]:
        stop_process("ping_function")

    elif "PING" in function_type[1]:
        command_parts = function_type[1].split()
        if command_parts[0].upper() == 'PING':
            command_parts = command_parts[1:]
        else:
            raise Exception("Error in the format using PING")
        
        arguments = ' '.join(command_parts)
        start_process("ping_function", ping_function, arguments)

    
    elif "HPING_STOP" in function_type[1]:
        stop_process("hping_function")
    
    elif "HPING" in function_type[1]:
        command_parts = function_type[1].split()
        if command_parts[0].upper() == 'HPING':
            command_parts = command_parts[1:]
        else:
            raise Exception("Error in the format using HPING")
        
        arguments = ' '.join(command_parts)
        start_process("ping_function", hping_function, arguments)

    elif "SAVE_FILE" in function_type[1]:
        command_parts = function_type[1].split()

        if command_parts[0].upper() == 'SAVE_FILE':
            command_parts = command_parts[1:]
        else:
            raise Exception("Error in the format using SAVE_FILE")

        rest_of_command = ' '.join(command_parts)

        client = mqtt.Client()
        client.connect(server_ip, 1883)
        client.subscribe(response_topic)

        client.publish(response_topic, f"SAVE_FILE {rest_of_command}")

    elif "DELAY" in function_type[1]:
        command_parts = function_type[1].split(" ")
        delay = int(command_parts[1])

        time.sleep(delay)
    elif "CUSTOM" in function_type[1]:
        command_parts = function_type[1].split()
        
        if command_parts[0].upper() == 'TRACEROUTE':
            command_parts = command_parts[1:]
        else:
            raise Exception("Error in the format using TRACEROUTE")
        
        arguments = ' '.join(command_parts)
        start_process("traceroute_function", custom_function, arguments)
    elif "CUSTOM_STOP" in function_type[1]:
        stop_process("ping_function")
    

    else:
        print("This command does not exist")

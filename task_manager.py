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

    if len(function_type) <= 1:
        print("Error in the command")
        return
    
    if "STOP_TRACEROUTE" in function_type[1]:
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

    elif "STOP_PING" in function_type[1]:
        print(function_type)
        print(f"esto es function type {function_type}")
        header = function_type[1].split(" ")[1]

        client_stop = mqtt.Client()
        client_stop.connect(server_ip, 1883)
        client_stop.subscribe(response_topic)

        client_stop.publish(response_topic, "STOP_" + str(header))

        client_stop.disconnect()

        header = function_type[1].split(" ")[1]

        stop_process("ping_function" + str(header))

    elif "PING" in function_type[1]:
        command_parts = function_type[1].split()
        
        if command_parts[1].upper() == 'PING':
            header = function_type[1].split(" ")[0]
            additional_arguments = command_parts[2:]
            all_arguments = [header] + additional_arguments
            arguments_str = ' '.join(all_arguments)
            start_process("ping_function" + str(header), ping_function, arguments_str)
        else:
            raise Exception("Error in the format using PING")

    
    elif "STOP_HPING" in function_type[1]:
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

    elif "STOP_CUSTOM" in function_type[1]:
        stop_process("ping_function") 
   
    elif "CUSTOM" in function_type[1]:
        command_parts = function_type[1].split()
        
        if command_parts[0].upper() == 'CUSTOM':
            command_parts = command_parts[1:]
        else:
            raise Exception("Error in the format using CUSTOM")
        
        arguments = ' '.join(command_parts)
        start_process("custom_function", custom_function, arguments)

    else:
        print("This command does not exist")

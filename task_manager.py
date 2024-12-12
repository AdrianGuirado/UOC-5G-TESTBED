# task_manager.py

import multiprocessing

from functions.traceroute import traceRoute_function
from functions.ping import ping_function
from functions.custom import custom_function
from functions.hping import hping_function
from functions.testspeed import speedtest_function
from functions.connect_slice import connectSlice_function
from functions.parameters import *
from functions.authenticate import authenticate_function
 
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

def process_comand(function, command):
    command = command.split(" ")
    
    if str(command[1].upper()) == function:
        header = command[0]
        command_parts = command[2:]
    else:
        raise Exception(f"Error in the format using {function}")
    
    return header, command_parts

def build_arguments(function, expected_function_type):

    header, command_parts = process_comand(function, expected_function_type)

    all_arguments = [header] + command_parts
    return ' '.join(all_arguments)

def process_tasks(task):
    global task_processes

    if user not in task and "ALL" not in task:
        return
                             
    function_type = task.split(":")

    if len(function_type) <= 1:
        print("Error in the command")
        return
    
    if "STOP_CONNECT_SLICE" in function_type[1]:
        stop_process("connectslice_function")

    elif "CONNECT_SLICE" in function_type[1]:
        arguments = build_arguments('CONNECT_SLICE', function_type[1])
        header = arguments.split(" ")[0]
        start_process("connectslice_function"+ str(header), connectSlice_function, arguments)

    elif "STOP_AUTHENTICATE" in function_type[1]:
        stop_process("authenticate_function")    

    elif "AUTHENTICATE" in function_type[1]:
        arguments = build_arguments('AUTHENTICATE', function_type[1])
        header = arguments.split(" ")[0]
        start_process("authenticate_function"+ str(header), authenticate_function, arguments)
        
    elif "STOP_TRACEROUTE" in function_type[1]:
        stop_process("traceroute_function")

    elif "TRACEROUTE" in function_type[1]:
        arguments = build_arguments('TRACEROUTE', function_type[1])
        header = arguments.split(" ")[0]
        start_process("traceroute_function"+ str(header), traceRoute_function, arguments)
    
    elif "STOP_SPEEDTEST" in function_type[1] :
        stop_process("speedtest_function")

    elif "SPEEDTEST" in function_type[1]:
        arguments = build_arguments('SPEEDTEST', function_type[1])
        header = arguments.split(" ")[0]
        start_process("speedtest_function"+ str(header), speedtest_function, arguments)

    elif "STOP_PING" in function_type[1]:
        header = function_type[1].split(" ")[1]
        stop_process("ping_function" + str(header))

    elif "PING" in function_type[1]:
        arguments = build_arguments('PING', function_type[1])
        header = arguments.split(" ")[0]
        start_process("ping_function"+ str(header), ping_function, arguments)
        
    elif "STOP_HPING" in function_type[1]:
        header = function_type[1].split(" ")[1]
        stop_process("hping_function" + str(header))
    
    elif "HPING" in function_type[1]:
        arguments = build_arguments('HPING', function_type[1])
        header = arguments.split(" ")[0]
        start_process("hping_function"+ str(header), hping_function, arguments)

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
        arguments = build_arguments('CUSTOM', function_type[1])
        header = arguments.split(" ")[0]
        start_process("custom_function"+ str(header), custom_function, arguments)

    else:
        print("This command does not exist")

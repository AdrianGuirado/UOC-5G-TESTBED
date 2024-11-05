# task_manager.py

import multiprocessing

from functions.traceroute import traceRoute_function
from functions.ping import ping_function
from functions.testspeed import speedTest_function

task_processes = {}
user = "USER1"

def start_process(function_key, target_function, *args):
    if function_key not in task_processes:
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

    print("Este es el mensaje")

    if user not in task and "ALL" not in task:
        return
    
    function_type = task.split(":")

    print(function_type[1])

    if len(function_type) <= 1:
        print("Error in the command")
        return

    if function_type[1] == "TRACEROUTE":
        start_process("traceroute_function", traceRoute_function)

    elif function_type[1] == "TRACEROUTE_STOP":
        stop_process("traceroute_function")

    elif function_type[1] == "SPEEDTEST":
        start_process("speedtest_function", speedTest_function)

    elif function_type[1] == "SPEEDTEST_STOP":
        stop_process("speedtest_function")

    elif function_type[1] == "PING":
        ip = function_type[2]
        #count = function_type[3]
        #interval = function_type[4]
        #timeout = function_type[5]
        #size = function_type[6]
        #ttl = function_type[7]

        #start_process("ping_function", ping_function, ip, count, interval, timeout, size, ttl)

        start_process("ping_function", ping_function, ip)
    elif function_type[1] == "PING_STOP":
        stop_process("ping_function")

    else:
        print("This command does not exist")

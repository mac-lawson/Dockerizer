import docker
import psutil
import os
import time

client = docker.from_env()

# function to get container status
def get_container_status(container):
    status = container.status
    if status == "running":
        return "\033[92mRunning\033[0m"
    elif status == "exited":
        return "\033[91mExited\033[0m"
    else:
        return status

# function to get container metrics
def get_container_metrics(container):
    stats = container.stats(stream=False)
    cpu_percent = stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage'] * 100
    mem_percent = stats['memory_stats']['usage'] / stats['memory_stats']['limit'] * 100
    net_io_counters = psutil.net_io_counters(pernic=True)
    net_io = net_io_counters[container.name]
    net_in = net_io.bytes_recv
    net_out = net_io.bytes_sent
    return (cpu_percent, mem_percent, net_in, net_out)

# function to print container info
def print_container_info(container):
    name = container.name
    image = container.image.tags[0]
    status = get_container_status(container)
    cpu_percent, mem_percent, net_in, net_out = get_container_metrics(container)
    print(f"{name:30} {image:30} {status:10} {cpu_percent:8.2f}% {mem_percent:8.2f}% {net_in:12} {net_out:12}")

# function to print header
def print_header():
    os.system('clear')
    print(f"{'Name':30} {'Image':30} {'Status':10} {'CPU %':8} {'Mem %':8} {'Net In':12} {'Net Out':12}")
    print("-" * 100)

# main loop
while True:
    containers = client.containers.list(all=True)
    print_header()
    for container in containers:
        print_container_info(container)
    time.sleep(5)

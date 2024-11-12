import psutil
import socket

def get_LocalIP():
    # Get all network interfaces and their IP addresses
    interfaces = psutil.net_if_addrs()
    Local_IP = ''
    # Specify the name of the interface you want to check (e.g., 'Local Area Connection* 4')
    interface_name = "Local Area Connection* 4"  # Use the exact name of the interface

    # Check if the interface exists and retrieve the IP address
    if interface_name in interfaces:
        for addr in interfaces[interface_name]:
            if addr.family == socket.AF_INET:  # Use socket.AF_INET for IPv4
                #print(f"{interface_name} IP Address: {addr.address}") #Local Area Connection 4
                Local_IP = addr.address
                print(Local_IP)
                return Local_IP
    else:
        print(f"Interface '{interface_name}' not found.")

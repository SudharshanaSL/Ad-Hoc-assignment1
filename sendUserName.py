import socket
import subprocess
import time


print("\nPreparing endpoint...")
print("Finding username...")
machine_username = subprocess.check_output(['who']).decode().split()[0]
print("Your username is...",machine_username)
print("Finding your IP...")
machine_ip,machine_interface = subprocess.check_output(['./print_ip_interface.sh']).decode("utf-8").strip().split()
print("Your IP is...",machine_ip)
print("\nAll done! Now waiting for username requests...\n")

def sendUserName():#on receiver
    send_hostname_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    send_hostname_socket.bind((machine_ip,23000))
    while True:
        data,sender_address = send_hostname_socket.recvfrom(512)
        data = data.decode()
        if data == "send":
            print("Received username request from ",sender_address[0])
            send_hostname_socket.sendto(machine_username.encode(),sender_address)

sendUserName()
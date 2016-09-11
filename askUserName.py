import socket
import subprocess

def getUserNameNode(node_ip):#on sender
    get_hostname_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    get_hostname_socket.sendto("send".encode(),(node_ip,23000))
    node_hostname = get_hostname_socket.recvfrom(512)[0].decode()
    return node_hostname

print(getUserNameNode("10.65.242.99"))
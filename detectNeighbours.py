import subprocess
import socket
import time

ip_hostnames = dict()




def getHostNameNode(node_ip):#on sender
    get_hostname_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print("Asking for username of ",node_ip," ......")
    get_hostname_socket.sendto("send".encode(),(node_ip,23000))
    node_hostname = get_hostname_socket.recvfrom(512)[0].decode()
    return node_hostname



def detectNeighbors():
    while True:
        tcpdump_output = subprocess.Popen("sudo tcpdump -c 30 \"broadcast\" | grep -P -o '([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*? >'",stdout=subprocess.PIPE,shell=True)
        output_ips = tcpdump_output.stdout.read().decode("utf-8").splitlines()
        output_ips = list(set(output_ips))
        output_ips = [ i.split()[0] for i in output_ips ]
        ip_file = open("ip_hostnames.txt","w")
        for each_ip in output_ips:
            if each_ip not in ip_hostnames.keys():
                print("Getting user name at ",each_ip)
                ip_hostnames[each_ip] = getHostNameNode(each_ip)
        copy_ip_hostnames = dict(ip_hostnames)
        for each_ip in copy_ip_hostnames:
            node_status = subprocess.call("ping "+each_ip,stdout=subprocess.DEVNULL,shell=True)
            if node_status == 1:
                ip_file.write(ip_hostnames[each_ip]+"|"+each_ip+"\n")
            else:
                ip_hostnames.pop(each_ip)
        ip_file.close()

detectNeighbors()



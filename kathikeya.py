import subprocess
import socket
import time
import threading
import getpass
import pprint

ip_hostnames = dict()
ip_pkey_received = list()


def joinNetwork():
    #scan
    subprocess.call("./scan.sh "+machine_interface+" "+network_ssid,shell=True)
    #join or create, both need same code
    subprocess.call("./create.sh "+network_ssid+" "+network_password,shell=True)
    machine_ip = subprocess.check_output("./print_ip_interface.sh",shell=True).decode().split()[0]
    



def getHostNameNode(node_ip):#on sender
    get_hostname_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    get_hostname_socket.sendto("send".encode(),(node_ip,23000))
    node_hostname = get_hostname_socket.recvfrom(512)[0].decode()
    return node_hostname



def detectNeighbors():
    while True:
        choice = int(input("Enter 0 for data transfer, 1 to exit, anything else to continue:"))
        if choice == 1:
            break
        elif choice == 0:
            print("Detected IPs and users are shown below, choose whom to send.")
            pprint(ip_hostnames,width=1)
            #user chooses receivers #append it to receiver list
            receiver_ips = []
            print("Choose files/folder to select:")
            #user will have selected directory or the files to be selected
            files_to_be_sent = []
            for each_ip in receiver_ips:
                node_status = subprocess.call("ping "+each_ip,stdout=subprocess.DEVNULL,shell=True)
                if node_status == 1:
                    #scp
                    print("SCP stats are displayed for each transfer")
                    for each_file in files_to_be_sent:
                        if each_ip not in ip_pkey_received:
                            ip_pkey_received.append(each_ip)
                            subprocess.call("./sender.sh "+each_ip+" "+ip_hostnames[each_ip]+" "+each_file+" 0",shell=True)
                        else:
                            subprocess.call("./sender.sh "+each_ip+" "+ip_hostnames[each_ip]+" "+each_file+" 1",shell=True)
                print("------\n"*4)




print("Finding username....")
machine_username = subprocess.check_output('who',shell=True).decode().split()[0]
print("Your username is...",machine_username)

network_ssid = input("Enter the ssid of the ad-hoc network:")
network_password = getpass.getpass(prompt="Enter the password for the network:")

machine_interface = subprocess.check_output(['./print_ip_interface.sh']).decode("utf-8").strip().split()[1]

joinNetwork()
# now username listener endpoint and broadcast process will be running in background
detectNeighbors()



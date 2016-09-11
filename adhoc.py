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
    subprocess.call("./scan.sh "+network_ssid,shell=True)
    #join or create, both need same code
    subprocess.call("./create.sh "+network_ssid+" "+network_password+" "+machine_username,shell=True)
    



def getHostNameNode(node_ip):#on sender
    get_hostname_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    get_hostname_socket.sendto("send".encode(),(node_ip,23000))
    node_hostname = get_hostname_socket.recvfrom(512)[0].decode().strip()
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
                print("Sending username request to ",each_ip)
                ip_hostnames[each_ip] = getHostNameNode(each_ip)
        print("Got usernames of newly detected IPs")
        active_ips = []
        for each_ip in ip_hostnames:
            print("Pinging ",each_ip)
            node_status = subprocess.call("ping -c 5 "+each_ip,stdout=subprocess.DEVNULL,shell=True)
            if node_status == 0:
                print(each_ip," is active")
                ip_file.write(ip_hostnames[each_ip]+"|"+each_ip+"\n")
                print("Wrote to file")
                active_ips.append(each_ip)
        ip_file.close()
        print("Active IPs were...")
        pprint.pprint(active_ips)
        choice = int(input("Enter 0 for data transfer, 1 to exit:"))
        if choice == 1:
            subprocess.call("./refresh.sh ",shell=True)
            break
        elif choice == 0:
            print("Detected IPs and users were shown above, choose whom to send.")
            #user chooses receivers #append it to receiver list
            receiver_ips = []
            while True:
                choice = input("Enter detected IPs of your choice (1 to stop):\t")
                if(choice == "1"):
                    break
                receiver_ips.append(choice)
            print("Choose files/folder to select:")
            contents = subprocess.check_output("ls adhocDir",shell=True).decode().split()
            pprint.pprint(contents)
            #user will have selected directory or the files to be selected
            files_to_be_sent = []
            while True:
                choice = input("Enter files of your choice (1 to stop):\t")
                if(choice == "1"):
                    break
                files_to_be_sent.append(choice)
            for each_ip in receiver_ips:
                node_status = subprocess.call("ping -c 5 "+each_ip,stdout=subprocess.DEVNULL,shell=True)
                if node_status == 0:
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

#scan and join
joinNetwork()
#get ip and interface
machine_ip,machine_interface = subprocess.check_output("./print_ip_interface.sh",shell=True).decode().split()
# now username listener endpoint and broadcast process will be running in background,
# next step is detect neighbours and ask for data transfer
detectNeighbors()



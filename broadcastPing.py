import subprocess
import os,time

null_fd = open(os.devnull,"w")

def startBroadcast():
    while True:
        subprocess.call("sudo ping -q -b -c 10 10.255.255.255",shell=True,stdout=null_fd,stderr=null_fd)

print("\nPing broadcast started`\n")
startBroadcast()
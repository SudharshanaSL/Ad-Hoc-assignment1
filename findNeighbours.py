import subprocess,pprint

ip_hostnames = dict()


def tcpdumpScan():
    #tcpdump_output = subprocess.check_output(['tcpdump','-G','10','-W','1','-e','-i','wlan0'])
    #tcpdump_output = subprocess.call("sudo tcpdump -c 15 \"broadcast\" | grep -P -o '([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*? > ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)'",shell=True)
    tcpdump_output = subprocess.Popen("sudo tcpdump -c 15 \"broadcast\" | grep -P -o '([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*? >'",stdout=subprocess.PIPE,shell=True)
    output_ips = tcpdump_output.stdout.read().decode("utf-8").splitlines()
    output_ips = list(set(output_ips))
    output_ips = [ i.split()[0] for i in output_ips ]
    ip_hostnames.extend(output_ips)
    pprint.pprint(output_ips)


tcpdumpScan()

#!/bin/bash

# 1st param
network_interface=$1
# 2nd param
network_ssid=$2
# 3rd param
network_password=$3

sudo service network-manager stop
sudo ip link set 

sudo iwconfig $network_interface essid $network_ssid key s:$network_password mode Ad-Hoc
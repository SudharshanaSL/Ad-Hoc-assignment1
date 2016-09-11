#!/bin/bash

SECONDS=0

iface=`ifconfig -a | awk '/^w.[a-z]/{print $1}'`
mac=`ifconfig -a | awk '/^w.[a-z]/{print $NF}'`

ssid=$1
password=$2
username=$3


sudo service network-manager stop
sudo ip link set "$iface" down


sudo iwconfig "$iface" mode ad-hoc
sudo iwconfig "$iface" channel auto
sudo iwconfig "$iface" essid "$ssid"
sudo iwconfig "$iface" key "$password"
sudo ip link set "$iface" up


str1=`echo $mac |cut -d':' -f4` 
str2=`echo $mac |cut -d':' -f5`
str3=`echo $mac |cut -d':' -f6`

o2=`echo $((0x$str1))`
o3=`echo $((0x$str2))`
o4=`echo $((0x$str3))`

ip=10.$o2.$o3.$o4/8
sudo ip addr add "$ip" dev "$iface"


echo "$ip is the IP"
echo "$iface is the interface"
echo "It took $SECONDS seconds to join"
echo
sudo python3 sendUserName.py &
echo
sudo python3 broadcastPing.py &
echo
sudo ./receiver.sh "$username" &
echo

sudo mkdir /home/$username/adhocreceiver
sudo chmod 777 /home/$username/adhocreceiver
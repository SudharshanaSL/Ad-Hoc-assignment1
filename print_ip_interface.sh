#!/bin/bash

iface=`ifconfig -a | awk '/^w.[a-z]/{print $1}'`
mac=`ifconfig -a | awk '/^w.[a-z]/{print $NF}'`

str1=`echo $mac |cut -d':' -f4` 
str2=`echo $mac |cut -d':' -f5`
str3=`echo $mac |cut -d':' -f6`

o2=`echo $((0x$str1))`
o3=`echo $((0x$str2))`
o4=`echo $((0x$str3))`

ip=10.$o2.$o3.$o4
echo $ip
echo $iface
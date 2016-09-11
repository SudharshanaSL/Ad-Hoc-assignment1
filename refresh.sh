#!/bin/bash

echo "Before:"
ps aux | grep -P "sudo|10000"
echo "------------"

pid=`ps aux | grep -P "sudo ./receiver.sh" | awk '{print $2}' | head -n 1`
pid1=`ps aux | grep -P "nc -l 10000" | awk '{print $2}' | head -n 1`
echo "Killing keypair listener processes - $pid and $pid1..."
kill "$pid" "$pid1"
echo "...done!"
echo "------------"

pid=`ps aux | grep -P "sudo python3 broadcastPing.py" | awk '{print $2}' | head -n 1`
echo "Killing ping broadcaster process - $pid..."
kill "$pid"
echo "...done!"
echo "------------"

pid=`ps aux | grep -P "sudo python3 sendUserName.py" | awk '{print $2}' | head -n 1`
echo "Killing username listener process - $pid..."
kill "$pid"
echo "...done!"
echo "------------"

echo "After:"
sudo service network-manager start
ps aux | grep -P "sudo|10000"
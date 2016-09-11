#!/bin/bash

# first param is ssid

echo "Scanning for ad-hoc $1..."
SECONDS=0
searchResult=`nmcli dev wifi | grep -P -o "'$1'.*?Ad-Hoc"`
echo "Took $SECONDS seconds to scan for network"
echo $searchResult
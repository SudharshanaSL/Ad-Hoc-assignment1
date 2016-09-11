#!/bin/bash

recipientIP=$1
hostName=$2
file=$3
val=$4 #indicates whether to send public key or not

sender_name=`who`
port=10000
echo $recipientIP
z=0
if [ "$val" -eq  "$z" ]; then
	# need to send public key
	nc "$recipientIP" "$port" < /home/$sender_name/.ssh/id_rsa.pub #use tcp
fi

SECONDS=0
scp -r adhocDir/$3 "$hostName"@"$recipientIP":/home/$hostName/adhocreceiver/
echo "It took $SECONDS seconds for transfer of $3 to $hostName@$recipientIP"

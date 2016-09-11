#!/bin/bash

echo "/home/$1/.ssh/authorized_keys will be the folder i will be placing keys in"

while :
do
    echo "Listening for keypairs...";
    nc -l 10000 >> /home/$1/.ssh/authorized_keys
done

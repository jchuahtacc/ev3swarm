#!/bin/sh
set -e
echo "Launching ev3host setup"

apt-get update
apt-get install python python-dev ev3ev
easy_install pika
easy_install rpyc_classic
chmod +x ev3host
chmod +x ev3host.py
cp ev3host /etc/init.d/
cp ev3host.py /usr/local/bin
update-rc.d /etc/init.d/ev3host defaults
/etc/init.d/ev3host start

echo "ev3host should be up and running now!"

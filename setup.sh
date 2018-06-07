#!/bin/bash

# Install the wifi setup library

# Install the forked-daapd service
wget -q -O - http://www.gyfgafguf.dk/raspbian/forked-daapd.gpg | sudo apt-key add -
sudo echo "deb http://www.gyfgafguf.dk/raspbian/forked-daapd/ stretch contrib" >> /etc/apt/sources.list
sudo apt update
sudo apt install forked-daapd

# Install the ada-play service
sudo pip install python-daemon
sudo cp system/ada-play.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/ada-play.service

# Start the daemons
sudo systemctl daemon-reload
sudo systemctl enable ada-play
sudo systemctl start ada-play
sudo systemctl enable forked-daapd
sudo systemctl start forked-daapd

# Make the daemons start on boot
sudo head -n -1 /etc/rc.local > /etc/rc.local
sudo echo "systemctl start forked-daapd" >> /etc/rc.local
sudo echo "systemctl start ada-play" >> /etc/rc.local

# Install mpc (sends commands to forked-daapd to start songs)
sudo apt install mpc

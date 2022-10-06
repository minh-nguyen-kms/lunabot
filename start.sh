#!/usr/bin/bash

#Service file at /lib/systemd/system/lunabot.service 
cd /home/pi/ntm/lunabot
# python --version
python ./server/main.py & npm start --prefix ./client/web-controller/
#node --version
#node /home/pi/ntm/lunabot/server/start.js
#!/usr/bin/bash

#Service file at /lib/systemd/system/lunabot.service 
cd /home/pi/ntm/lunabot
# python --version
python /home/pi/ntm/lunabot/server/main.py & npm start --prefix /home/pi/ntm/lunabot/client/web-controller/
# python /home/pi/ntm/lunabot/server/main.py &
#npm start --prefix /home/pi/ntm/lunabot/client/web-controller &
#node --version
#node /home/pi/ntm/lunabot/server/start.js
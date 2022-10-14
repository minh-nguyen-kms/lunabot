# lunabot

## Hardwares
### Logitech C270 USB Camera
- Plug and play
### Waveshare Motor Driver Hat
- Please refer the setting here https://www.waveshare.com/wiki/Motor_Driver_HAT
### Speech to Text
- `sudo apt-get install libasound2-dev`
- https://www.geeksforgeeks.org/python-convert-speech-to-text-and-text-to-speech/

### nodejs
- sudo apt-get install nodejs
- sudo apt-get install npm

## Start up services
- /etc/systemd/system/lunabot.service
```
[Unit]
[Unit]
Description=LunaBot
After=systemd-networkd-wait-online.service
Requires=systemd-networkd-wait-online.service

[Service]
Type=idle
ExecStart=python /home/pi/ntm/lunabot/server/main.py

[Install]
WantedBy=systemd-networkd-wait-online.service
```

- /etc/systemd/system/lunabotclient.service
```
[Unit]
Description=LunaBotClient
After=network-online.target

[Service]
Type=idle
ExecStart=http-server /home/pi/ntm/lunabot/client/web-controller/out -p 9001

[Install]
WantedBy=network-online.target
```
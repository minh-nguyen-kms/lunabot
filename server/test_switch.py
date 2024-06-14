import ipaddress
import sys
import os

from modules.switch.light_switch_controller import LightSwitchController

sys.path.insert(0, '/home/pi/ntm/lunabot/server')

import logging
import asyncio
import time

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def main():
    light_switch = LightSwitchController()
    light_switch.on()
    # wait for 5 seconds
    time.sleep(5)


if __name__=='__main__':
   main()
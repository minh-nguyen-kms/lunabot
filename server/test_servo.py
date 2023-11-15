import ipaddress
import sys
import os

sys.path.insert(0, '/home/pi/ntm/lunabot/server')

import logging
import asyncio
import time
from modules.mortor.servo_driver import ServoDriver

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def main():
    print("this is a servo driver test code")
    # servo = ServoDriver(7, max_pulse=2600, min_pulse=500)
    servo = ServoDriver(6, max_pulse=2600, min_pulse=500)
    
    print("turn 50%")
    servo.turn(50)
    time.sleep(3)
    
    # print("turn 0%")
    # servo.turn(0)
    # time.sleep(3)
    
    # print("turn 50%")
    # servo.turn(50)
    # time.sleep(3)
    
    # print("turn 100%")
    # servo.turn(100)
    # time.sleep(3)
    
    # print("turn 50")
    # servo.turn(50)
    # time.sleep(3)

    print("stop")
    servo.stop()


if __name__=='__main__':
   main()
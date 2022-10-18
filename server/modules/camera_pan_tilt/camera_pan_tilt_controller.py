
#!/usr/bin/python
from datetime import datetime
import json
import logging
from threading import Thread
import RPi.GPIO as GPIO
import pigpio
import time
import os

from libs.event_bus.event_bus import EventBus
from libs.event_bus.event_names import EventNames

class CameraPanTiltController():
    def __init__(self, event_bus: EventBus):
        self.log = logging.getLogger(self.__class__.__name__)
        self.event_bus = event_bus
        
        self.servo1_pin = 23
        self.servo2_pin = 24
        
        event_bus.on(EventNames.CAMERA_PANTILT, self.on_pantilt_move)

    def on_pantilt_move(self, data):
        x = data.get('x')
        y = data.get('y')

        self.log.debug(f'x_speed: {x} - y_speed: {y}')

        self.turn_servo(self.servo1_pin, -x)
        self.turn_servo(self.servo2_pin, -y)


    def stop_litening(self):
        self.is_life_cycle_runing = False
        self.log.info('Stop Camera Pan Tilt controller')

    def runLifeCycle(self):
        return
        
    def config_servo_pwm(self, servo_pin):
        self.pwm.set_mode(servo_pin, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency( servo_pin, 50 )
        
    def turn_servo(self, servo, vector):
        pulse = 1500 + vector * 1000
        self.pwm.set_servo_pulsewidth(servo, pulse)


    def start_listening(self):
        self.log.info('Start Camera Pan Tilt controller')
        self.is_life_cycle_runing = True

        # Start pigpiod service
        os.system('sudo pigpiod')
        time.sleep(1)
        self.pwm = pigpio.pi()

        return
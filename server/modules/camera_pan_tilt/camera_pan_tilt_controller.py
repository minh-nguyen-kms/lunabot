
#!/usr/bin/python
from datetime import datetime
import json
import logging
from threading import Thread
import pigpio
import time

from libs.event_bus.event_bus import EventBus
from libs.event_bus.event_names import EventNames

class CameraPanTiltController():
    def __init__(self, event_bus: EventBus):
        self.log = logging.getLogger(self.__class__.__name__)
        self.event_bus = event_bus
        
        self.servo1_pin = 23
        self.servo2_pin = 24

        # Auto stop all motor after 1000ms in case lost signal from socket
        self.auto_stop_time_duration = 1000

        # Controlling variables
        self.is_life_cycle_runing = False
        # self.auto_stop_time = 0
        # self.is_stoped = True
        
        # Event handlers
        event_bus.on(EventNames.CAMERA_PANTILT_MOVE, self.on_pantilt_move)
        event_bus.on(EventNames.CAMERA_PANTILT_STOP, self.on_pantilt_stop)
        event_bus.on(EventNames.CAMERA_PANTILT_CENTER_VIEW, self.on_pantilt_center_view)

    def on_pantilt_move(self, data):
        x = data.get('x')
        y = data.get('y')

        self.log.debug(f'x_speed: {x} - y_speed: {y}')

        self.turn_servo(self.servo1_pin, -x)
        self.turn_servo(self.servo2_pin, -y)

        # # set auto stop time to next period
        # current_time = datetime.now().timestamp() * 1000
        # self.auto_stop_time = current_time + self.auto_stop_time_duration

    def on_pantilt_center_view(self, data):
        self.turn_servo(self.servo1_pin, 0)
        self.turn_servo(self.servo2_pin, 0)
        time.sleep(0.5)
        self.stop_servo(self.servo1_pin)
        self.stop_servo(self.servo2_pin)

    def on_pantilt_stop(self, data):
        self.stop_servo(self.servo1_pin)
        self.stop_servo(self.servo2_pin)

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

    def stop_servo(self, servo):
        self.pwm.set_servo_pulsewidth(servo, 0)

    def start_listening(self):
        self.log.info('Start Camera Pan Tilt controller')
        self.is_life_cycle_runing = True

        self.pwm = pigpio.pi()

        self.turn_servo(self.servo1_pin, 0)
        self.turn_servo(self.servo2_pin, 0)
        time.sleep(1)
        self.stop_servo(self.servo1_pin)
        self.stop_servo(self.servo2_pin)

        return
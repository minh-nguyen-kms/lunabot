
#!/usr/bin/python
from datetime import datetime
import json
import logging
from threading import Thread
import pigpio
import time

from libs.event_bus.event_bus import EventBus
from libs.event_bus.event_names import EventNames
from modules.mortor.servo_driver import ServoDriver

class CameraPanTiltController():
    def __init__(self, event_bus: EventBus):
        self.log = logging.getLogger(self.__class__.__name__)
        self.event_bus = event_bus
        
        self.servo1 = ServoDriver(6, max_pulse=2530, min_pulse=570)
        self.servo1_min_angle = 0
        self.servo1_max_angle = 1
        self.servo1_center_angle = 0
        self.servo2 = ServoDriver(7, max_pulse=2600, min_pulse=500)
        self.servo2_min_angle = 0
        self.servo2_max_angle = 0.75
        self.servo2_center_angle = 0.2

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

        self.turn_servo1(-x)
        self.turn_servo2(-y)

        # # set auto stop time to next period
        # current_time = datetime.now().timestamp() * 1000
        # self.auto_stop_time = current_time + self.auto_stop_time_duration

    def on_pantilt_center_view(self, data):
        self.center_servos()

    def on_pantilt_stop(self, data):
        self.stop_servos()

    def stop_litening(self):
        self.is_life_cycle_runing = False
        self.log.info('Stop Camera Pan Tilt controller')

    def runLifeCycle(self):
        return
        
        
    def turn_servo(self, servo, vector, min_angle=0, max_angle=1):
        turn_angle = 0.5 + vector * 0.5
        if (turn_angle < min_angle):
            turn_angle = min_angle
        if (turn_angle > max_angle):
            turn_angle = max_angle
        servo.turn(turn_angle * 100)
    
    def turn_servo1(self, vector):
        self.turn_servo(self.servo1, vector, min_angle=self.servo1_min_angle, max_angle=self.servo1_max_angle)
    
    def turn_servo2(self, vector):
        self.turn_servo(self.servo2, vector, min_angle=self.servo2_min_angle, max_angle=self.servo2_max_angle)

    def stop_servo(self, servo):
        servo.stop()
        
    def stop_servos(self):
        self.stop_servo(self.servo1)
        self.stop_servo(self.servo2)
        
    def center_servos(self):
        self.turn_servo1(self.servo1_center_angle)
        self.turn_servo2(self.servo2_center_angle)
        time.sleep(1)
        self.stop_servos()
        

    def start_listening(self):
        self.log.info('Start Camera Pan Tilt controller v2')
        self.is_life_cycle_runing = True

        self.center_servos()

        return
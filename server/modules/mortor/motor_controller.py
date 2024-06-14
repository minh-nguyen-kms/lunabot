
#!/usr/bin/python
import asyncio
from datetime import datetime
import json
import logging
from threading import Thread
import time

from libs.event_bus.event_bus import EventBus
from libs.event_bus.event_names import EventNames
from .motor_driver import MotorDriver

class MotorController():
    def __init__(self, event_bus: EventBus):
        self.log = logging.getLogger(self.__class__.__name__)
        self.event_bus = event_bus
        self.motor = MotorDriver()
        
        # Left motor is 0 and Right is 1
        self.l_motor = 0
        self.r_motor = 1

        # Righ motor is faster than the left
        # => slow down it a litle
        self.l_motor_speed_adjustment = 100 # 100 is the maximum
        self.r_motor_speed_adjustment = 98 # 100 is the maximum

        # Auto stop all motor after 1000ms in case lost signal from socket
        self.auto_stop_time_duration = 1000

        # Controlling variables
        self.is_life_cycle_runing = False
        self.auto_stop_time = 0
        self.is_stoped = True

        # Distance variables
        self.last_l_speed = 0
        self.last_r_speed = 0
        self.min_distance = 15 # cm
        self.distance = -1

        # Register event
        event_bus.on(EventNames.MOVING, self.on_moving)
        event_bus.on(EventNames.ULTRASONIC_ON_MEAUSRE, self.on_ultrasonic_on_measure)

    def __del__(self):
        self.stop_motor()
        self.log.info(f'Cleanup')

    def get_direction(self, l_speed, r_speed):
        if (l_speed == 0 and r_speed == 0):
            return 'STOP'
        if (l_speed > 0 and r_speed > 0):
            return 'FORWARD'
        if (l_speed < 0 and r_speed < 0):
            return 'BACKWARD'
        if (l_speed > 0 and r_speed < 0):
            return 'RIGHT'
        if (l_speed < 0 and r_speed > 0):
            return 'LEFT'
        return 'UNKNOWN'

    def check_and_stop_mortor_on_short_distance(self):
        direction = self.get_direction(self.last_l_speed, self.last_r_speed)
        isShortDistance = self.distance > 0 and self.distance <= self.min_distance 

        # Check distance if too close to the wall
        if(isShortDistance and direction == 'FORWARD'):
            self.log.debug(f'Too close to the wall')
            self.stop_motor()
            return True
        return False

    def on_ultrasonic_on_measure(self, data):
        self.distance = data.get('distance')

        # Check distance if too close to the wall
        self.check_and_stop_mortor_on_short_distance();

    def run_motor(self, x_speed, y_speed):
        # Calculate speed for each motor
        l_speed = y_speed + x_speed
        r_speed = y_speed - x_speed

        self.last_l_speed = l_speed
        self.last_r_speed = r_speed

        # Check distance if too close to the wall
        if self.check_and_stop_mortor_on_short_distance():
            return

        # self.log.debug(f'{l_speed} - {r_speed}')
        self.motor.run(self.l_motor, l_speed * self.l_motor_speed_adjustment)
        self.motor.run(self.r_motor, r_speed * self.r_motor_speed_adjustment)

    def stop_motor(self):
        self.motor.stop(self.l_motor)
        self.motor.stop(self.r_motor)
        self.is_stoped = True

        # ask ultrasonic to stop measure and clear last distance
        self.event_bus.emit(EventNames.ULTRASONIC_STOP_MEAUSRE, {})

        self.log.debug('All Motors stoped')

    def on_moving(self, data):
        x_speed = data.get('xSpeed')
        y_speed = data.get('ySpeed')
        # self.log.debug(f'x_speed: {x_speed} - y_speed: {y_speed}')

        # # Ask ultrasonic to start measure
        self.event_bus.emit(EventNames.ULTRASONIC_START_MEAUSRE, {})

        # Run motor
        self.run_motor(x_speed, y_speed)
        self.is_stoped = False

        # set auto stop time to next period
        current_time = datetime.now().timestamp() * 1000
        self.auto_stop_time = current_time + self.auto_stop_time_duration
        # self.log.debug(f'auto_stop_time = {self.auto_stop_time}')

    def check_for_auto_stop(self):
        if (self.is_stoped):
            return
        current_time = datetime.now().timestamp() * 1000
        # self.log.debug(f'current_time = {current_time} - ${self.auto_stop_time}')
        if (current_time > self.auto_stop_time):
            self.stop_motor()

    def stop_litening(self):
        self.is_life_cycle_runing = False
        self.log.info('Stop Motor controller')

    def runLifeCycle(self):
        while self.is_life_cycle_runing:
            self.check_for_auto_stop()
            time.sleep(0.5)
        

    def start_listening(self):
        self.log.info('Start Motor controller')
        
        self.stop_motor()

        # # Ask ultrasonic to start measure
        # self.event_bus.emit(EventNames.ULTRASONIC_START_MEAUSRE, {})

        self.is_life_cycle_runing = True
        self.thread = Thread(target=self.runLifeCycle,args=())
        self.thread.daemon = True
        self.thread.start()

        return self.thread
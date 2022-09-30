
#!/usr/bin/python
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

        # Auto stop all motor after 1000ms in case lost signal from socket
        self.auto_stop_time_duration = 1000

        # Controlling variables
        self.is_life_cycle_runing = False
        self.auto_stop_time = 0
        self.is_stoped = True

        event_bus.on(EventNames.MOVING, self.on_moving)

    def __del__(self):
        self.stop_motor()
        self.log.info(f'Cleanup')

    def run_motor(self, x_speed, y_speed):
        l_speed = y_speed + x_speed
        r_speed = y_speed - x_speed

        # self.log.debug(f'{l_speed} - {r_speed}')
        self.motor.run(self.l_motor, l_speed * 100)
        self.motor.run(self.r_motor, r_speed * 100)

    def stop_motor(self):
        self.motor.stop(self.l_motor)
        self.motor.stop(self.r_motor)
        self.is_stoped = True
        self.log.debug('All Motors stoped')

    def on_moving(self, data):
        x_speed = data.get('xSpeed')
        y_speed = data.get('ySpeed')
        # self.log.debug(f'x_speed: {x_speed} - y_speed: {y_speed}')
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
        self.is_life_cycle_runing = True
        self.thread = Thread(target=self.runLifeCycle,args=())
        self.thread.daemon = True
        self.thread.start()

        return self.thread

#!/usr/bin/python
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
        self.l_motor = 0
        self.r_motor = 1

        self.is_listening = False

        event_bus.on(EventNames.MOVING, self.on_moving)

    def run_motor(self, x_speed, y_speed):
        l_speed = y_speed + x_speed
        r_speed = y_speed - x_speed

        self.log.debug(f'{l_speed} - {r_speed}')

        self.motor.run(self.l_motor, l_speed * 100)
        self.motor.run(self.r_motor, r_speed * 100)

    def on_moving(self, data):
        x_speed = data.get('xSpeed')
        y_speed = data.get('ySpeed')
        self.run_motor(x_speed, y_speed)

    def stop_litening(self):
        self.is_listening = False
        self.log.info('Stop Motor controller')

    def litening(self):
        while self.is_listening:
            pass

    def start_listening(self):
        self.log.info('Start Motor controller')
        self.thread = Thread(target=self.litening,args=())
        self.thread.start()

        return self.thread
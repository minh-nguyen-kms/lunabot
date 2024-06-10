
#!/usr/bin/python
from datetime import datetime
import json
import logging
from threading import Thread
import time
import pigpio
import asyncio

from libs.event_bus.event_bus import EventBus
from libs.event_bus.event_names import EventNames
from libs.async_helpers.periodic import Periodic

class UltraSonicController():
    def __init__(self, event_bus: EventBus):
        self.log = logging.getLogger(self.__class__.__name__)
        self.event_bus = event_bus
        self.is_start_measure = False

        event_bus.on(EventNames.ULTRASONIC_START_MEAUSRE, self.on_start_measure)
        event_bus.on(EventNames.ULTRASONIC_STOP_MEAUSRE, self.on_stop_measure)
        
        self.pi = pigpio.pi()

        # Define GPIO pins to use on Pi (BMC numbering)
        self.pin_trigger = 27
        self.pin_echo = 17

        self.start = None
        self.prev = 0
        self.max_dif = 80
        self.distance = None
        self.verbose = True
        self.interval = 1

        # Speed of sound in cm/ms at temperature (changed from cm/s)
        self.temperature = 28
        self.sound_speed = 33.1 + (0.0006*self.temperature)

        #  Set pin modes and output level
        self.pi.set_mode(self.pin_trigger, pigpio.OUTPUT)
        self.pi.write(self.pin_trigger, 0)
        self.pi.set_mode(self.pin_echo, pigpio.INPUT)

    def __del__(self):
        self.stop_litening()
        self.stop_measure()

    def on_start_measure(self, data):
        self.log.debug('Start measure')
        self.start_measure()
        

    def on_stop_measure(self, data):
        self.log.debug('Stop measure')
        self.stop_measure()

    def calc(self, gpio, level, tick):
        """
        Callback function to handle distance calculation.
        """
        if level == 1: #  Start of echo pulse
            self.start = tick
        if self.start and level == 0: #  If start has a value and echo pulse ended        
            echo = pigpio.tickDiff(self.start, tick) # Length of echo pulse in microseconds
            dist = round(((echo / 1000) * self.sound_speed)/2, 1)
            if self.verbose:
                print("echo: ", echo, "dist: ", dist)
            if not abs(self.prev - dist) > self.max_dif: #### May want to make this user setable
                self.distance = dist
            else:
                self.distance = -1
            self.prev = dist
            self.start = None
        return

    def measure(self):
            """
            Send a pulse and time the echo.
            """
            print("is_start_measure: ", self.is_start_measure)
            if not self.is_start_measure:
                return

            self.pi.gpio_trigger(self.pin_trigger, 10, 1) #  Send a 10 microsecond pulse on the trigger pin
            cb = self.pi.callback(self.pin_echo, pigpio.EITHER_EDGE, self.calc) #  Catch the echo pulse and pass timing to calc callback function
            time.sleep(self.interval)
            cb.cancel()
            if self.verbose and self.distance:
                print("distance: ", self.distance)

            self.event_bus.emit(EventNames.ULTRASONIC_ON_MEAUSRE, {
                'distance': self.distance
            })
            
            return self.distance

    def start_measure(self):
        self.is_start_measure = True
    
    def stop_measure(self):
        self.is_start_measure = False

    def stop_litening(self):
        self.is_life_cycle_runing = False
        self.log.info('Stop UtraSonic controller')

    def runLifeCycle(self):
        # Don't need to support life cycle in this version

        # while self.is_life_cycle_runing:
        #     pass
        return
        

    async def start_listening(self):
        self.log.info('Start UtraSonic controller')
        self.is_life_cycle_runing = True

        p = Periodic(lambda: self.measure(), 0.1)
        await p.start()

        return
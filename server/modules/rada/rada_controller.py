
#!/usr/bin/python
from datetime import datetime
import json
import logging
from threading import Thread
import pigpio
import time
import numpy as np

from libs.async_helpers.timeout import timeout
from libs.event_bus.event_bus import EventBus
from libs.event_bus.event_names import EventNames
from modules.mortor.servo_driver import ServoDriver

class RadaController():
    def __init__(self, event_bus: EventBus):
        self.log = logging.getLogger(self.__class__.__name__)
        self.event_bus = event_bus
        
        self.UNLIMITED_DISTANCE = 1000000
        
        self.init_servos()
        self.init_ultra_sonic()
        
        
        # Auto stop all motor after 1000ms in case lost signal from socket
        self.auto_stop_time_duration = 1000

        # Controlling variables
        self.is_life_cycle_runing = False
        self.is_scanning = False
        self.status = 'STOP'
        
        # Event handlers
        event_bus.on(EventNames.RADA_START_SCAN_FORWARD_CENTER, self.on_start_scan_forward_center)
        event_bus.on(EventNames.RADA_START_SCAN_ALL, self.on_start_scan_all)
        event_bus.on(EventNames.RADA_STOP_SCAN, self.on_stop_scan)
        
    def init_servos(self):
        self.current_vector = 0
        self.last_scan_result = {}
        
        # X axis
        self.servo1 = ServoDriver(8, max_pulse=2300, min_pulse=700)
        self.servo1_min_angle = 0.05
        self.servo1_max_angle = 1
        self.servo1_center_angle = 0.05

    def init_ultra_sonic(self):
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

    def on_pantilt_move(self, data):
        x = data.get('x')
        self.turn_servo1(-x)

        # # set auto stop time to next period
        # current_time = datetime.now().timestamp() * 1000
        # self.auto_stop_time = current_time + self.auto_stop_time_duration

    def on_pantilt_center_view(self, data):
        self.center_servos()

    def on_pantilt_stop(self, data):
        self.stop_servos()

    def stop_litening(self):
        self.is_life_cycle_runing = False
        self.log.info('Stop Rada controller')

    def runLifeCycle(self):
        return
        
    def calculate_turn_angle(self, vector, min_angle=0, max_angle=1):
        turn_angle = 0.5 + vector * 0.5
        if (turn_angle < min_angle):
            turn_angle = min_angle
        if (turn_angle > max_angle):
            turn_angle = max_angle
        return turn_angle
        
    def turn_servo(self, servo, vector, min_angle=0, max_angle=1):
        turn_angle = self.calculate_turn_angle(vector, min_angle=min_angle, max_angle=max_angle)
        servo.turn(turn_angle * 100)
    
    def turn_servo1(self, vector):
        self.turn_servo(self.servo1, vector, min_angle=self.servo1_min_angle, max_angle=self.servo1_max_angle)
    
    def stop_servo(self, servo):
        servo.stop()
        
    def stop_servos(self):
        self.stop_servo(self.servo1)
        
    def center_servos(self):
        self.turn_servo1(self.servo1_center_angle)
        self.current_vector = self.servo1_center_angle
        time.sleep(1)
        self.stop_servos()
        
    
    def calc_distance(self, gpio, level, tick):
        """
        Callback function to handle distance calculation.
        """
        if level == 1: #  Start of echo pulse
            self.start = tick
        if self.start and level == 0: #  If start has a value and echo pulse ended        
            echo = pigpio.tickDiff(self.start, tick) # Length of echo pulse in microseconds
            dist = round(((echo / 1000) * self.sound_speed)/2, 1)
            # if self.verbose:
            #     print("echo: ", echo, "dist: ", dist)
            if not abs(self.prev - dist) > self.max_dif: #### May want to make this user setable
                self.distance = dist
            else:
                self.distance = self.UNLIMITED_DISTANCE
            self.prev = dist
            self.start = None
        return

    def measure_distance(self, wait_time=0.2):
            """
            Send a pulse and time the echo.
            """
            # print("is_start_measure: ", self.is_start_measure)
            # if not self.is_start_measure:
            #     return

            pulseLen = 10
            self.pi.gpio_trigger(self.pin_trigger, pulseLen, 1)
            cb = self.pi.callback(self.pin_echo, pigpio.EITHER_EDGE, self.calc_distance) #  Catch the echo pulse and pass timing to calc callback function
            time.sleep(wait_time)
            cb.cancel()
            # if self.verbose and self.distance:
            #     print("distance: ", self.distance)

            # self.event_bus.emit(EventNames.ULTRASONIC_ON_MEAUSRE, {
            #     'distance': self.distance
            # })
            
            return self.distance
        
    def calculate_min_distance_from_last_result(self, from_vector=-1, to_vector=1, step=0.1):
        vector_range = self._get_range_vector(from_vector=from_vector, to_vector=to_vector, step=step)
        # Get distances within the specified range
        distances_within_range = [self.last_scan_result.get(round(value, 3), float('inf')) for value in vector_range]
        # Calculate the minimum distance
        min_distance = np.min(distances_within_range)

        return min_distance
        
        
    def detect_impact(self, step=0.1):
        min_distance_left = self.calculate_min_distance_from_last_result(from_vector=0.4, to_vector=1, step=step)
        min_distance_right = self.calculate_min_distance_from_last_result(from_vector=-1, to_vector=-0.4, step=step)
        min_distance_forward = self.calculate_min_distance_from_last_result(from_vector=-0.4, to_vector=0.4, step=step)
        
        impact = {
            'left': min_distance_left,
            'right': min_distance_right,
            'forward': min_distance_forward,
        }
        
        self.event_bus.emit(EventNames.RADA_ON_IMPACT, {
            'impact': impact,
            'status': self.status,
        })
        return impact
        
    
    def _get_range_vector(self, from_vector=-1, to_vector=1, step=0.1):
        range_vector = [from_vector]
        if from_vector < to_vector:
            range_vector = np.arange(from_vector, to_vector + step, step)
        return range_vector
    
    def check_if_can_continue_scan(self, count=1, loop_count=1):
        if (not self.is_scanning):
            return False
        if (loop_count < 0):
            return True
        return count < loop_count
    
    def scan(self, from_vector=-1, to_vector=1, step=0.1, interval=0.1, loop_count=1):
        self.log.info('Start scanning')
        self.is_scanning = True

        self.last_scan_result = {}
        range_vector = self._get_range_vector(from_vector=from_vector, to_vector=to_vector, step=step)
        
        count = 0
        can_continue = self.check_if_can_continue_scan(count, loop_count)
        while can_continue:
            for vector in range_vector:
                self.turn_servo1(vector)
                self.current_vector = vector
                time.sleep(interval)
                distance = self.measure_distance(interval)
                self.last_scan_result[round(vector, 3)] = distance
            
            # invert direction
            count += 1 if loop_count > 0 else 0
            range_vector = range_vector[::-1]
            
            can_continue = self.check_if_can_continue_scan(count, loop_count)
            # Detect impact if it isn't the last loop
            if (can_continue):
                self.detect_impact(step=step)
        
        self.center_servos()
        
        self.log.info('Stop scanning %s - %d - %d', self.is_scanning, count, loop_count, )
        # detect impact for last result
        if (self.is_scanning):
            self.detect_impact(step=step)
        self.is_scanning = False
        self.status = 'STOP'
        
    def scan_forward(self, step=0.1, interval=0.1, loop_count=1):
        self.scan(from_vector=-0.4, to_vector=0.4, step=step, interval=interval, loop_count=loop_count)
    
    def scan_right(self, step=0.1, interval=0.1, loop_count=1):
        self.scan(from_vector=-1, to_vector=-0.4, step=step, interval=interval, loop_count=loop_count)
        
    def scan_left(self, step=0.1, interval=0.1, loop_count=1):
        self.scan(from_vector=0.4, to_vector=1, step=step, interval=interval, loop_count=loop_count)
        

    def do_start_scan_forward_center(self):
        self.scan(from_vector=0, to_vector=0, step=0.1, interval=0.1, loop_count=-1)
        
    def do_start_scan_all(self):
        self.scan(from_vector=-1, to_vector=1, step=0.1, loop_count=1)
        
    async def timeout_handler(self, async_func, timeout_seconds = 1):
        try:
            # Wait for the async function with a timeout
            await asyncio.wait_for(async_func(), timeout=timeout_seconds)
            print("Operation finished within the timeout.")
        except asyncio.TimeoutError:
            print("Timeout! Operation took too long.")
            
    async def init_scan_forward_center(self):
        self.log.info('Init SCAN_FORWARD_CENTER')
        self.status = 'SCAN_FORWARD_CENTER'
        self.do_start_scan_forward_center()
        
    async def init_scan_all(self):
        self.log.info('Init SCAN_ALL')
        self.status = 'SCAN_ALL'
        self.do_start_scan_all()
        
        
    def on_start_scan_forward_center(self):
        self.log.info('on_start_scan_forward_center')
        if (self.is_scanning and self.status == 'SCAN_FORWARD_CENTER'):
            self.log.info('Already scanning')
            return
        elif (self.is_scanning):
            self.log.info('Force Stop scanning')
            self.is_scanning = False
        
        timeout(self.init_scan_forward_center, 1)

        
    def on_start_scan_all(self):
        self.log.info('on_start_scan_all')
        if (self.is_scanning and self.status == 'SCAN_ALL'):
            self.log.info('Already scanning')
            return
        elif (self.is_scanning):
            self.log.info('Force Stop scanning')
            self.is_scanning = False
        
        timeout(self.init_scan_all, 1)
        
    def on_stop_scan(self):
        self.log.info('on_stop_scan')
        self.status = 'STOP'
        self.is_scanning = False

    def start_listening(self):
        self.log.info('Start Rada controller')
        self.is_life_cycle_runing = True

        self.center_servos()
        return
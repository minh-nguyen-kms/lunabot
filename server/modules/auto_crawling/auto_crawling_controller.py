
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

class AutoCrawlingController():
    def __init__(self, event_bus: EventBus):
        self.log = logging.getLogger(self.__class__.__name__)
        self.event_bus = event_bus
        
        self.speed = 0.9
        self.min_distance = 40
        self.moving_status = 'STOP'
        

        # Controlling variables
        self.is_life_cycle_runing = False
        # self.auto_stop_time = 0
        # self.is_stoped = True
        
        # Event handlers
        event_bus.on(EventNames.RADA_ON_IMPACT, self.on_rada_impact)
        
    def stop(self):
        self.log.info('Stop')
        self.event_bus.emit(EventNames.MOVING, {'xSpeed': 0, 'ySpeed': 0})
        self.moving_status = 'STOP'
        return
    
    def forward(self):
        self.log.info('Forward')
        self.event_bus.emit(EventNames.MOVING, {'xSpeed': 0, 'ySpeed': self.speed})
        self.moving_status = 'FORWARD'
        return
    
    def backward(self):
        self.log.info('Backward')
        self.event_bus.emit(EventNames.MOVING, {'xSpeed': 0, 'ySpeed': -self.speed})
        self.moving_status = 'BACKWARD'
        return
    
    def turnLeft(self):
        self.log.info('Turn Left')
        self.event_bus.emit(EventNames.MOVING, {'xSpeed': -self.speed, 'ySpeed': 0})
        self.moving_status = 'LEFT'
        time.sleep(0.3)
        self.stop()
        
        return
    
    def turnRight(self):
        self.log.info('Turn Right')
        self.event_bus.emit(EventNames.MOVING, {'xSpeed': self.speed, 'ySpeed': 0})
        self.moving_status = 'RIGHT'
        time.sleep(0.3)
        self.stop()
        return
    
    def determineNextAction(self, impact_data):
        rada_data = impact_data.get('impact')
        rada_status = rada_data.get('status')
        
        self.log.info('Rada status: %s', rada_status)
        
        rada_forward = rada_data.get('forward')
        rada_left = rada_data.get('left')
        rada_right = rada_data.get('right')
        
        next_action = self.moving_status
        if(next_action == 'FORWARD' and rada_forward <= self.min_distance):
            next_action = 'STOPANDSCAN'
        elif(next_action == 'STOPANDSCAN'):
            if ((rada_forward > rada_left \
                and rada_forward > rada_right) \
                or rada_forward > 100 \
                ):
                next_action = 'FORWARD'
            elif(rada_left > rada_right):
                next_action = 'LEFT'
            else:
                next_action = 'RIGHT'
        else:
            next_action = 'FORWARD'
                
        return next_action
          
    
    async def request_rada_scan_all(self):
        self.event_bus.emit(EventNames.RADA_START_SCAN_ALL)
        return
    
    def action(self, next_action):
        # self.log.info('Emit action: %s', next_action)
        self.moving_status = next_action
        if(next_action == 'FORWARD'):
            self.event_bus.emit(EventNames.RADA_START_SCAN_FORWARD_CENTER)
            self.forward()
        elif(next_action == 'LEFT'):
            self.turnLeft()
            next_action = 'STOPANDSCAN'
            self.log.info('Emit action: %s', next_action)
            self.event_bus.emit(EventNames.RADA_STOP_SCAN)
            timeout(self.request_rada_scan_all, 1)
        elif(next_action == 'RIGHT'):
            self.turnRight()
            next_action = 'STOPANDSCAN'
            self.log.info('Emit action: %s', next_action)
            self.event_bus.emit(EventNames.RADA_STOP_SCAN)
            timeout(self.request_rada_scan_all, 1)
        elif(next_action == 'BACKWARD'):
            self.backward()
        elif(next_action == 'STOP'):
            self.stop()
        elif(next_action == 'STOPANDSCAN'):
            self.stop()
            self.event_bus.emit(EventNames.RADA_START_SCAN_ALL)
            
        self.moving_status = next_action
            
        return
                
        
        
    def on_rada_impact(self, data):
        self.log.info('Rada impact: %s', data)
        next_action = self.determineNextAction(data)
        self.log.info('Next action: %s', next_action)
        self.action(next_action)
        
    
    def start_crawling(self):
        self.moving_status = 'FORWARD'
        # self.event_bus.emit(EventNames.RADA_START_SCAN_ALL)
        
        self.event_bus.emit(EventNames.RADA_START_SCAN_FORWARD_CENTER)
        # time.sleep(3)
        # self.event_bus.emit(EventNames.RADA_STOP_SCAN)
        

        return

    def start_listening(self):
        self.log.info('Start Auto Crawling controller')
        self.is_life_cycle_runing = True

        self.start_crawling()

        return
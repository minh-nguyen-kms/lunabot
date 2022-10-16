
#!/usr/bin/python
from datetime import datetime
import json
import logging
from threading import Thread
import time
import os

from libs.event_bus.event_bus import EventBus
from libs.event_bus.event_names import EventNames

class SystemController():
    def __init__(self, event_bus: EventBus):
        self.log = logging.getLogger(self.__class__.__name__)
        self.event_bus = event_bus
        
        event_bus.on(EventNames.SYSTEM_RESTART, self.on_restart)

    def on_restart(self, data):
        os.system('sudo reboot')

    def stop_litening(self):
        self.is_life_cycle_runing = False
        self.log.info('Stop System controller')

    def runLifeCycle(self):
        while self.is_life_cycle_runing:
            pass
        

    def start_listening(self):
        self.log.info('Start System controller')
        self.is_life_cycle_runing = True
        self.thread = Thread(target=self.runLifeCycle,args=())
        self.thread.daemon = True
        self.thread.start()

        return self.thread
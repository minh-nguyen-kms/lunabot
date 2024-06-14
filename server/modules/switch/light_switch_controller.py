import logging
from .mosfet_driver import MosfetDriver

from libs.event_bus.event_bus import EventBus
from libs.event_bus.event_names import EventNames
from libs.async_helpers.periodic import Periodic

class LightSwitchController:
    def __init__(self, event_bus: EventBus):
        self.pin = 17
        self.driver = MosfetDriver(self.pin)
        
        self.log = logging.getLogger(self.__class__.__name__)
        self.event_bus = event_bus
        
        
        event_bus.on(EventNames.SWITCH_LIGHT_ON, self.on_light_on)
        event_bus.on(EventNames.SWITCH_LIGHT_OFF, self.on_light_off)
        
        self.is_life_cycle_runing = False
        self.log.info(f'Light switch controller is ready, pinout: {self.pin}')
        
    def on(self):
        self.driver.on()
        self.log.info('Light is on')
        
    def off(self):
        self.driver.off()
        self.log.info('Light is off')
        
    def on_light_on(self, data):
        self.log.info('Event: Light on')
        self.on()
        
    def on_light_off(self, data):
        self.log.info('Event: Light off')
        self.off()
        
    def stop_litening(self):
        self.is_life_cycle_runing = False
        self.log.info('Stop UtraSonic controller')

    def runLifeCycle(self):
        return

    async def start_listening(self):
        self.log.info('Start Light switch controller')
        self.is_life_cycle_runing = True

        p = Periodic(lambda: self.measure(), 0.1)
        await p.start()

        return
        
    def __del__(self):
        self.off()
        self.log.info(f'Ligh switch controller is cleaned up, pinout: {self.pin}')

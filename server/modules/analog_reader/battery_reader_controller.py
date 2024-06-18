import logging
from libs.event_bus.event_bus import EventBus
from libs.event_bus.event_names import EventNames
from .battery_reader import BatteryReader


class BatteryReaderController:
    def __init__(self, event_bus: EventBus):
        self.log = logging.getLogger(self.__class__.__name__)
        self.event_bus = event_bus
        self.reader = BatteryReader()
        
        self.event_bus.on(EventNames.BATTERY_INFO_REQUEST, self.on_battery_percentage_request)

    def on_battery_percentage_request(self, data):
        self.log.debug('Battery percentage request')
        (percentage, voltage) = self.reader.read_percentage()
        self.log.debug(f'Battery percentage: {percentage} - Voltage: {voltage}')
        self.event_bus.emit(EventNames.SOCKET_BROAD_CAST, {
                "event": EventNames.BATTERY_INFO,
                "data": {
                    "percentage": percentage,
                    "voltage": voltage
                }
            })
        
    def start_listening(self):
        self.log.info('Start Battery Reader controller')
        return
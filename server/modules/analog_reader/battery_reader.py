from .ads1115_driver import ADS1115Driver
import time


class BatteryReader:
    def __init__(self):
        self.reader = ADS1115Driver()
        self.channel = 0
        
        self.min_voltage = 9.2
        self.max_voltage = 12.0

    def read_voltage(self):
        return self.reader.read_voltage(self.channel)
    
    def read_percentage(self):
        voltage = self.read_voltage()
        voltage = min(voltage, self.max_voltage)
        percentage = (voltage - self.min_voltage) / (self.max_voltage - self.min_voltage) * 100
        
        return (percentage, voltage)
    
    
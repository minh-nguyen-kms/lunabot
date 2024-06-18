import logging
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

r1 = 30000.0
r2 = 7500.0

class ADS1115Driver:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        
        # Initialize the I2C interface
        self.i2c = busio.I2C(board.SCL, board.SDA)

        # Create an ADS1115 object
        self.ads = ADS.ADS1115(self.i2c)

        # Define the analog input channels
        self.channels= {
            0: AnalogIn(self.ads, ADS.P0),
            1: AnalogIn(self.ads, ADS.P1),
            2: AnalogIn(self.ads, ADS.P2),
            3: AnalogIn(self.ads, ADS.P3)
        }
        
    def read_voltage(self, channel):
        reader = self.channels.get(channel)
        self.log.debug(f'Channel {channel} voltage: {reader.voltage}')
        return reader.voltage * ((r1 + r2) / r2)
        
    def read_value(self, channel):
        return self.channels.get(channel).value
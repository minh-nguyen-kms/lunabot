import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create an ADS1115 object
ads = ADS.ADS1115(i2c)

# Define the analog input channels
channel0 = AnalogIn(ads, ADS.P0)
channel1 = AnalogIn(ads, ADS.P1)
channel2 = AnalogIn(ads, ADS.P2)
channel3 = AnalogIn(ads, ADS.P3)

r1 = 30000.0
r2 = 7500.0
ref_voltage = 12.0

# Loop to read the analog inputs continuously
while True:
    # print("Analog Value 0: ", channel0.value, "Voltage 0: ", channel0.voltage)
    
    # the channel0 connected to the voltage sensor that use to measure the voltage of the 12v battery
    # convert input value vrom channel0 to voltage
#     // Determine voltage at ADC input
#   adc_voltage  = (adc_value * ref_voltage) / 1024.0;
  
#   // Calculate voltage at divider input
#   in_voltage = adc_voltage*(R1+R2)/R2;
    vout = channel0.value * ref_voltage / 1024.0
    vin = vout / (r2 / (r1 + r2))
    # current = vin / (r1 + r2)
    # power = vin * current
    print("Analog Value 0: ", vin, "Voltage 0: ", channel0.voltage * ((r1 + r2) / r2))
    
    
    
    # print("Analog Value 1: ", channel1.value, "Voltage 1: ", channel1.voltage)
    # print("Analog Value 2: ", channel2.value, "Voltage 2: ", channel2.voltage)
    # print("Analog Value 3: ", channel3.value, "Voltage 3: ", channel3.voltage)
    
    # Delay for 1 second
    time.sleep(1)
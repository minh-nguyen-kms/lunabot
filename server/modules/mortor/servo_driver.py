
#!/usr/bin/python

from .PCA9685 import PCA9685
import time

class ServoDriver():
    def __init__(self, channel, min_pulse=500, max_pulse=2500):
        self.pwm = PCA9685(0x40, debug=False)
        self.pwm.setPWMFreq(50)
        self.channel = channel
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse

    def turn(self, rate):
        pulse = self._calculate_pulse(rate)
        self.pwm.setServoPulse(self.channel, pulse) 

    def stop(self):
        self.pwm.setDutycycle(self.channel, 0)
        
        
    def _calculate_pulse(self, rate):
        pulse_range = self.max_pulse - self.min_pulse
        return int(self.min_pulse + (rate * pulse_range / 100))
    
    

# if __name__=='__main__':
#     print("this is a servo driver test code")
#     servo = ServoDriver(6)
#     print("turn 90")
#     servo.turn(90)
#     time.sleep(1)
#     print("turn 0")
#     servo.turn(0)
#     time.sleep(1)
#     print("turn 90")
#     servo.turn(90)
#     time.sleep(1)
#     print("turn 180")
#     servo.turn(180)
#     time.sleep(1)
#     print("turn 90")
#     servo.turn(90)

#     print("stop")
#     servo.stop()
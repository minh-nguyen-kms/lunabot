
#!/usr/bin/python

from .PCA9685 import PCA9685
import time

pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)

class MotorDriver():
    def __init__(self):
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4

    def run(self, motor, speed):
        speed_abs = abs(speed)
        if speed_abs > 100:
            speed_abs = 100
        
        if(motor == 0):
            pwm.setDutycycle(self.PWMA, speed_abs)
            if(speed > 0):
                pwm.setLevel(self.AIN1, 0)
                pwm.setLevel(self.AIN2, 1)
            else:
                pwm.setLevel(self.AIN1, 1)
                pwm.setLevel(self.AIN2, 0)
        else:
            pwm.setDutycycle(self.PWMB, speed_abs)
            if(speed > 0):
                pwm.setLevel(self.BIN1, 0)
                pwm.setLevel(self.BIN2, 1)
            else:
                pwm.setLevel(self.BIN1, 1)
                pwm.setLevel(self.BIN2, 0)

    def stop(self, motor):
        if (motor == 0):
            pwm.setDutycycle(self.PWMA, 0)
        else:
            pwm.setDutycycle(self.PWMB, 0)

# print("this is a motor driver test code")
# Motor = MotorDriver()

# print("forward 2 s")
# Motor.MotorRun(0, 'forward', 50)
# Motor.MotorRun(1, 'forward', 50)
# time.sleep(20)

# print("backward 2 s")
# Motor.MotorRun(0, 'backward', 50)
# Motor.MotorRun(1, 'backward', 50)
# time.sleep(20)

# print("stop")
# Motor.MotorStop(0)
# Motor.MotorStop(1)
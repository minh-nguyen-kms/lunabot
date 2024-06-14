import pigpio

class MosfetDriver:
    def __init__(self, pin):
        self.pi = pigpio.pi()
        self.pin = pin
        self.pi.set_mode(self.pin, pigpio.OUTPUT)
        self.pi.write(self.pin, 0)

    def on(self):
        self.pi.write(self.pin, 1)

    def off(self):
        self.pi.write(self.pin, 0)

    def __del__(self):
        self.off()
        self.pi.set_mode(self.pin, pigpio.INPUT)
        self.pi.stop()
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

led_red = 12
led_green = 23
led_blue = 24

GPIO.setup(led_red, GPIO.OUT)
GPIO.setup(led_green, GPIO.OUT)
GPIO.setup(led_blue, GPIO.OUT)


class ServerControl:
    def __init__(self) -> None:
        pass

    def ServerOnline(self):
        self.ResetLed()
        GPIO.output(led_green, True)

    def ServerOffline(self):
        self.ResetLed()
        GPIO.output(led_red, True)

    def ServerPending(self):
        self.ResetLed()
        GPIO.output(led_blue, True)

    def ResetLed(self):
        # Turn all on 
        # Delay 2 sec
        # Turn all off
        pass
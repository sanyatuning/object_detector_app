import RPi.GPIO as GPIO


class Infrared(object):
    def __init__(self, dl=16, dr=19):
        self.dl = dl
        self.dr = dr

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(dr, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(dl, GPIO.IN, GPIO.PUD_UP)

    def getLeft(self):
        return GPIO.input(self.dl)

    def getRight(self):
        return GPIO.input(self.dr)

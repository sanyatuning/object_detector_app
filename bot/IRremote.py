import RPi.GPIO as GPIO
import time


class IRremote(object):
    def __init__(self, ir = 17):
        self.ir = ir
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(ir, GPIO.IN)

    def getkey(self):
        if GPIO.input(self.ir) == 0:
            count = 0
            while GPIO.input(self.ir) == 0 and count < 200:  # 9ms
                count += 1
                time.sleep(0.00006)
            if (count < 10):
                return
            count = 0
            while GPIO.input(self.ir) == 1 and count < 80:  # 4.5ms
                count += 1
                time.sleep(0.00006)

            idx = 0
            cnt = 0
            data = [0, 0, 0, 0]
            for i in range(0, 32):
                count = 0
                while GPIO.input(self.ir) == 0 and count < 15:  # 0.56ms
                    count += 1
                    time.sleep(0.00006)

                count = 0
                while GPIO.input(self.ir) == 1 and count < 40:  # 0: 0.56mx
                    count += 1  # 1: 1.69ms
                    time.sleep(0.00006)

                if count > 7:
                    data[idx] |= 1 << cnt
                if cnt == 7:
                    cnt = 0
                    idx += 1
                else:
                    cnt += 1
            if data[0] + data[1] == 0xFF and data[2] + data[3] == 0xFF:  # check
                return data[2]
            else:
                print("repeat")
                return "repeat"



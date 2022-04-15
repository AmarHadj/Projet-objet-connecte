import RPi.GPIO as GPIO
import time

#Classe qui s'occupe de la distance
class UltrasonicRanging(object):

    #Initialisation
    def __init__(self):
        self.trigPin = 16
        self.echoPin = 18
        self.MAX_DISTANCE = 220          # define the maximum measuring distance, unit: cm
        self.timeOut = self.MAX_DISTANCE*60   # calculate timeout according to the maximum measuring distance
        self.distance =0

        GPIO.setmode(GPIO.BOARD)      # use PHYSICAL GPIO Numbering
        GPIO.setup(self.trigPin, GPIO.OUT)   # set trigPin to OUTPUT mode
        GPIO.setup(self.echoPin, GPIO.IN)    # set echoPin to INPUT mode

    # Envoit une pulsion
    def pulseIn(self,pin,level):
        t0 = time.time()
        while(GPIO.input(pin) != level):
            if((time.time() - t0) > self.timeOut*0.000001):
                return 0;
        t0 = time.time()
        while(GPIO.input(pin) == level):
            if((time.time() - t0) > self.timeOut*0.000001):
                return 0;
        pulseTime = (time.time() - t0)*1000000
        return pulseTime

    # Détermine la distance par rapport au temos de retour de la pulsion
    def read_distance(self):
        GPIO.setup(18, GPIO.IN) 
        GPIO.output(self.trigPin,GPIO.HIGH)
        time.sleep(0.0001)
        GPIO.output(self.trigPin,GPIO.LOW)
        pingTime = self.pulseIn(self.echoPin,GPIO.HIGH)
        self.distance = pingTime * 340.0 / 2.0 / 10000.0


import RPi.GPIO as GPIO
import time

# Classe qui s'occupe de tourner le moteur et de le set
class SteppingMotor(object):

    #Intitialiser
    def __init__(self):
        self.motorPins = (12, 16, 18, 22)    # define pins connected to four phase ABCD of stepper motor
        self.CCWStep = (0x01,0x02,0x04,0x08) # define power supply order for rotating anticlockwise
        self.CWStep = (0x08,0x04,0x02,0x01)  # define power supply order for rotating clockwise
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
        for pin in self.motorPins:
            GPIO.setup(pin,GPIO.OUT)

    # Moteur bouge selon direction
    def move(self,direction,ms):
        GPIO.setup(18,GPIO.OUT)
        for j in range(0,4,1):
            for i in range(0,4,1):
                if (direction == 1):
                    GPIO.output(self.motorPins[i],((self.CCWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
                else :
                    GPIO.output(self.motorPins[i],((self.CWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
            if(ms<3):
                ms = 3
            time.sleep(ms*0.001)

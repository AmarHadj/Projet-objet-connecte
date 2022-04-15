import RPi.GPIO as GPIO
import time
import math
from ADCDevice import *

# Classe qui s'occupe de la température
class Thermometer(object):
    #Initialisation
    def __init__(self):
        self.adc = ADCDevice() # Define an ADCDevice class object
        self.tempC = 0
    
        if(self.adc.detectI2C(0x4b)): # Detect the ads7830
            self.adc = ADS7830()
        else:
            print("No correct I2C address found, \n"
            "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
            "Program Exit. \n");
            exit(-1)

    #Lire le voltage suivi d'un calcul pour déterminer la température en Celcius
    def read_temp(self):
        value = self.adc.analogRead(0)        # read ADC value A0 pin
        voltage = value / 255.0 * 3.3        # calculate voltage
        if (voltage !=3.3):
            Rt = 10 * voltage / (3.3 - voltage)    # calculate resistance value of thermistor
            tempK = 1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0) # calculate temperature (Kelvin)
            self.tempC = tempK -273.15        # calculate temperature (Celsius)
            time.sleep(0.01)
        
    # Détruire à ctl-c
    def destroy(self):
        self.adc.close()
        GPIO.cleanup()


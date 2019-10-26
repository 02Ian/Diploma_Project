import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN) #LED
GPIO.setup(24, GPIO.IN) #PIR

try:
    time.sleep(2) #to stable the sensor
    
while True:
#when motion detected turn on LED
    if(GPIO.input(PIR_input)):
        GPIO.output(26, GPIO.HIGH)
    else:
        GPIO.output(26, GPIO.LOW)

except:
    GPIO.cleanup(
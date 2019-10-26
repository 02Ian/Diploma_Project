import RPi.GPIO as GPIO
import time

channel = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

def fan_on(pin):
	GPIO.output(pin, GPIO.HIGH)
	
def fan_off(pin):
	GPIO.cleanup()
	
if __name__ == '__main__':
	try:
		fan_on(channel)
		time.sleep(10)
		fan_off(channel)
		time.sleep(10)
		GPIO.cleanup()
	except KeyboardInterrupt:
		GPIO.cleanup()
		pass

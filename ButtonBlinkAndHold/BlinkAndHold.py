"""
  This is a simple example that toggles an LED on a button press, but also will exit the
  program when the same button is held for 3 or more seconds. It uses an interrupt event
  to toggle the LED on and off while the main program watches for how long the button is pressed.
"""
import RPi.GPIO as GPIO
import time

LED_PIN = 17
BUTTON_PIN = 18

led_on = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def toggle_led(pin):
	led_on = not led_on
	GPIO.output(LED_PIN, led_on)

# we're going to use an interrupt event to toggle the LED on and off so the "main" program can 
# calculate the hold time and determine if we should exit the program or not. The "bouncetime"
# parameter is in ms
GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=toggle_led, bouncetime=200)
	
try:
	while True:
		if not GPIO.input(BUTTON_PIN):	#since we set BUTTON_PIN to use pull-up resistor, input() returns False on button press
			pressed_time = time.time()
			while not GPIO.input(BUTTON_PIN): 
				time.sleep(0.1)
			hold_time = time.time() - pressed_time
			if hold_time >= 3:	#if user held the button longer than 3 seconds
				break			#break the while True loop
			
	
except KeyboardInterrupt:
	GPIO.cleanup()			# clean up GPIO on CTRL+C exit

GPIO.cleanup()				# clean up GPIO on normal exit
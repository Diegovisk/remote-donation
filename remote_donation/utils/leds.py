import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


YELLOW_LED = 11
GREEN_LED = 13
BLUE_LED = 15
RED_LED = 29

GPIO.setup(YELLOW_LED, GPIO.OUT)

def yellow_led_on():
    GPIO.output(YELLOW_LED, 1)

def yellow_led_off():
    GPIO.output(YELLOW_LED, 0)

GPIO.setup(GREEN_LED, GPIO.OUT)

def green_led_on():
    GPIO.output(GREEN_LED, 1)

def green_led_off():
    GPIO.output(GREEN_LED, 0)

GPIO.setup(BLUE_LED, GPIO.OUT)

def blue_led_on():
    GPIO.output(BLUE_LED, 1)

def blue_led_off():
    GPIO.output(BLUE_LED, 0)

GPIO.setup(RED_LED, GPIO.OUT)

def red_led_on():
    GPIO.output(RED_LED, 1)

def red_led_off():
    GPIO.output(RED_LED, 0)
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
RELAY_PIN = 22
GPIO.setup(RELAY_PIN, GPIO.OUT)

def open_lock():
    GPIO.output(RELAY_PIN, 1)

def close_lock():
    GPIO.output(RELAY_PIN, 0)
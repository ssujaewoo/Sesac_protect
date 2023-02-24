import RPi.GPIO as GPIO
import time

def green_on(green_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(green_pin, GPIO.OUT)
    GPIO.output(green_pin, True)

def green_off(green_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(green_pin, GPIO.OUT)
    GPIO.output(green_pin, False)
    GPIO.cleanup(green_pin)
    
def yellow_on(yellow_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(yellow_pin, GPIO.OUT)
    GPIO.output(yellow_pin, True)

def yellow_off(yellow_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(yellow_pin, GPIO.OUT)

    GPIO.output(yellow_pin, False)
    GPIO.cleanup(yellow_pin)
    
def fan_on(fan_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(fan_pin, GPIO.OUT)
    
    GPIO.output(fan_pin, False)

def fan_off(fan_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(fan_pin, GPIO.OUT)
    
    GPIO.output(fan_pin, True)
    GPIO.cleanup(fan_pin)

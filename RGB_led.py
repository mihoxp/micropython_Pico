from machine import Pin
from utime import sleep_ms

red = Pin(16, Pin.OUT)
yellow = Pin(17, Pin.OUT)
green = Pin(25, Pin.OUT)

while(True):
    red.on()
    sleep_ms(1000)
    red.off()
    yellow.on()
    sleep_ms(1000)
    yellow.off()
    green.on()
    sleep_ms(1000)
    green.off()

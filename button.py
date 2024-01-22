from machine import Pin

led = Pin(16, Pin.OUT)
btn = Pin(27, Pin.IN, Pin.PULL_UP)
while(True):
    if(btn.value() == False):
        led.off()
    else:
        led.on()

from machine import I2C, Pin

i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000)
devices = i2c.scan()
print("I2C devices found:", devices)

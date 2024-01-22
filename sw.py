from machine import Pin
import time

# 配置 GPIO 引脚
button_pin = Pin(27, Pin.IN, Pin.PULL_UP)

# 读取按钮状态
while True:
    button_state = button_pin.value()
    print("Button State:", button_state)
    time.sleep(1)

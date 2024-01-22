from machine import Pin
import time
# 配置 GPIO 引脚
led_pin = Pin(25, Pin.OUT)

# 控制 LED 状态
while True:
    led_pin.value(not led_pin.value())  # 切换 LED 状态
    time.sleep(1)  # 等待 1 秒

import pcf8563
from machine import Pin, I2C
import utime

# 配置 I2C
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000)  # 根據實際連接調整引腳和頻率

# PCF8563 地址
pcf8563_addr = 0x51

# 創建 PCF8563 對象
rtc = pcf8563.PCF8563(i2c, pcf8563_addr)

try:
    while True:
        # 讀取 RTC 時間
        rtc_time = rtc.datetime()
        print("RTC Time:", rtc_time)
        
        # 暫停一秒
        utime.sleep(1)

except KeyboardInterrupt:
    pass


from machine import Pin, ADC, I2C
import time
#import utime
import struct
from sh1106 import SH1106_I2C
import usocket
#import ntptime
#import network
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral

# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()
# Create an instance of the BLESimplePeripheral class with the BLE object
sp = BLESimplePeripheral(ble)

# Set the debounce time to 0. Used for switch debouncing
debounce_time=0

# 定義 MPU-6050 地址
MPU6050_ADDR = 0x68

# 初始化 I2C
i2c = I2C(0, scl=Pin(13), sda=Pin(12), freq=400000)

# 初始化 OLED
oled_width = 128
oled_height = 64
#oled = SH1106_I2C(oled_width, oled_height, i2c)
oled = SH1106_I2C(oled_width, oled_height, i2c,rotate=180)

# 設置 MPU-6050
i2c.writeto_mem(MPU6050_ADDR, 0x6B, b'\x00')  # 喚醒 MPU-6050
# 設定 OLED 上下翻轉
#oled.flip(True)
# 定義馬達控制引腳
motor_pin = Pin(10, Pin.OUT)
# 定義搖桿的 GPIO 引腳
adc_x = ADC(Pin(27))  # 26是Pico上的一個可用的ADC引腳
adc_y = ADC(Pin(26))  # 27是Pico上的另一個可用的ADC引腳
button_pin = Pin(5, Pin.IN, Pin.PULL_UP)  # 使用內部上拉電阻
button_E = Pin(9, Pin.IN, Pin.PULL_UP)  # 使用內部上拉電阻
button_F = Pin(7, Pin.IN, Pin.PULL_UP)  # 使用內部上拉電阻
button_C = Pin(17, Pin.IN, Pin.PULL_UP)  # 使用內部上拉電阻
button_D = Pin(8, Pin.IN, Pin.PULL_UP)  # 使用內部上拉電阻
button_A = Pin(4, Pin.IN, Pin.PULL_UP)  # 使用內部上拉電阻
button_B = Pin(14, Pin.IN, Pin.PULL_UP)  # 使用內部上拉電阻

# 初始化 Wi-Fi
#wifi_ssid = "MihoXP"
#wifi_password = "88888888"
#wifi = network.WLAN(network.STA_IF)
#wifi.active(True)
#wifi.connect(wifi_ssid, wifi_password)

#def get_network_time():
#    NTP_SERVER = "pool.ntp.org"
#    try:
        # 連接 NTP 服務器，獲取時間
#        ntptime.host = NTP_SERVER
#        ntptime.settime()
#        return time.localtime()
#    except Exception as e:
#        print(f"Error getting time: {e}")
#        return None

try:
    while True:
        # Check if the pin value is 0 and if debounce time has elapsed (more than 300 milliseconds)
        if ((button_pin.value() is 0) and (time.ticks_ms()-debounce_time) > 300):
        # Check if the BLE connection is established
            if sp.is_connected():
            # Create a message string
                msg="pushbutton pressed\n"
            # Send the message via BLE
                sp.send(msg)
        # Update the debounce time    
            debounce_time=time.ticks_ms()
        #current_time = get_network_time()
        #if current_time:
            #time_str = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
          #  time_str = "{:02}:{:02}:{:02}".format(
    #current_time[0], current_time[1], current_time[2],
   # current_time[3], current_time[4], current_time[5]
#)
        # 讀取 MPU-6050 數據
        data = i2c.readfrom_mem(MPU6050_ADDR, 0x3B, 14)
        
        # 解析數據
        ax, ay, az, temp, gx, gy, gz = struct.unpack('>hhhhhhh', data)
        # 讀取搖桿和按鈕輸入
        x_value = adc_x.read_u16()
        y_value = adc_y.read_u16()
        button_value = button_pin.value()
        button_A_value = button_A.value()
        button_B_value = button_B.value()
        button_C_value = button_C.value()
        button_D_value = button_D.value()
        button_E_value = button_E.value()
        button_F_value = button_F.value()
        
        # 將ADC值轉換為範圍在0到1之間的浮點數
        x_normalized = x_value / 65535.0
        y_normalized = y_value / 65535.0

        # 打印輸入
        #print(f"Button: {button_value}, Button: {button_A_value}, Button: {button_B_value}, Button: {button_C_value}, Button: {button_D_value}, Button: {button_E_value}, Button: {button_F_value}")
        #print(f"X ADC Value: {x_value}, Normalized: {x_normalized}")
        #print(f"Y ADC Value: {y_value}, Normalized: {y_normalized}")
        #print(f"Accelerometer: ({ax}, {ay}, {az})")
        #print(f"Gyroscope: ({gx}, {gy}, {gz})")
        #print(f"Temperature: {temp / 340.0 + 36.53} °C")
        
        # 在 OLED 上顯示數據
        #for i in range(1, 51): # count 1 to 50
        oled.fill(0)
        oled.hline(0, 0, 127, 1)
        oled.hline(0, 63, 127, 1)
        oled.vline(0, 0, 64, 1)
        oled.vline(127, 0, 64, 1)
        oled.text(f"A:{ax},{ay},{az}", 3, 3, 1 )
        oled.text(f"G:{gx},{gy},{gz}", 3, 13, 1)
        #oled.text(f"G:{gx:.1f},{gy:.1f},{gz:.1f}", 0, 16)  # 使用 .2f 顯示兩位小數點
        oled.text("Temp:{:.1f}C".format(temp / 340.0 + 36.53), 3, 23, 1)
        #oled.text(f"Time:{time_str}", 3, 33, 1)
        oled.text(f"{button_value},{button_A_value},{button_B_value},{button_C_value},{button_D_value},{button_E_value},{button_F_value}", 3, 33, 1)
        oled.text(f"X:{x_value},Y:{y_value}", 3, 43, 1)
        oled.show()
            #utime.sleep(0.1) #wait 1/10th of a second
        
        # 檢測震動馬達觸發條件（這裡的條件僅作示例）
        if az > 20000:
            # 啟動震動馬達
            motor_pin.on()
            time.sleep(0.5)  # 震動持續時間，根據需要調整
            motor_pin.off()

        # 等待一段時間，可以根據需要調整
        time.sleep(0.1)

except KeyboardInterrupt:
    pass


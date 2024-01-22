from machine import Pin, UART, I2C
from time import sleep_ms
from ssd1306 import SSD1306_I2C
# using default address 0x3C
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=200000)#Grove - OLED Display 0.96" (SSD1315)
oled = SSD1306_I2C(128, 64, i2c)

oled.rotate(False)
oled.fill(0)  # Clear the screen
#oled.text("Hello, Seeder!", 10, 15)
oled.text("/////", 30, 40)
oled.text("(`3`)y", 30, 55)
oled.show()  # Show the text

class RYLR896:
    def __init__(self, port_num, tx_pin='', rx_pin=''):
        if tx_pin=='' and rx_pin=='':
            self._uart = UART(port_num)
        else:
            self._uart = UART(port_num, tx=tx_pin, rx=rx_pin)
                
    def cmd(self, lora_cmd):
        self._uart.write('{}\r\n'.format(lora_cmd))
        while(self._uart.any()==0):
            pass
        reply = self._uart.readline()
        print(reply.decode().strip('\r\n'))
    
    def test(self):
        self._uart.write('AT\r\n')
        while(self._uart.any()==0):
            pass
        reply = self._uart.readline()
        print(reply.decode().strip('\r\n'))

    def set_addr(self, addr):
        self._uart.write('AT+ADDRESS={}\r\n'.format(addr))
        while(self._uart.any()==0):
            pass
        reply = self._uart.readline()
        print(reply.decode().strip('\r\n'))
        print('Address set to:{}\r\n'.format(addr))


    def send_msg(self, addr, msg):
        self._uart.write('AT+SEND={},{},{}\r\n'.format(addr,len(msg),msg))
        while(self._uart.any()==0):
            pass
        reply = self._uart.readline()
        print(reply.decode().strip('\r\n'))
        
    def read_msg(self):
        if self._uart.any()==0:
            print('Nothing to show.')
            oled.fill(0)
            oled.text("Nothing to show.", 10, 15)
            oled.show()
        else:
            msg = ''
            while(self._uart.any()):
                msg = msg + self._uart.read(self._uart.any()).decode()
            print(msg.strip('\r\n'))
            oled.fill(0)
            oled.text(str(msg), 10, 15)
            oled.show()
    # 等待模块响应
    
lora = RYLR896(0) # Sets the UART port to be use
sleep_ms(100)
lora.set_addr(1)  # Sets the LoRa address






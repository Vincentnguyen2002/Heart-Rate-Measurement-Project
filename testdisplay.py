from machine import Pin,UART,I2C,Timer,ADC
from ssd1306 import SSD1306_I2C
from fifo import Fifo
from piotimer import Piotimer 
import time
import utime
from Algorithm import Heartrate
import micropython
micropython.alloc_emergency_exception_buf(200)
i2c = I2C(1, scl = Pin(15) , sda = Pin(14) , freq = 400000)
oled = SSD1306_I2C(128,64,i2c)

oled.fill_rect(0,20,128,10,1)
oled.text("measuring...",20,20,0)
oled.show()
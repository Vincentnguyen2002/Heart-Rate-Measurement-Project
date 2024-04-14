import time
from machine import Pin , UART , I2C , Timer , ADC
from ssd1306 import SSD1306_I2C

i2c = I2C(1 , scl = Pin(15) , sda = Pin(14) , freq = 400000)

oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width , oled_height , i2c)

height = 0
scroll_num = -8

while True:
    user = input("what do you want to eat ? :")
    if height >= 64:
        height = 56
        oled.scroll(0,scroll_num)
        oled.fill_rect(0,56,128,8,0)
    oled.text(user ,0,height,1)
    height += 8
    oled.show()

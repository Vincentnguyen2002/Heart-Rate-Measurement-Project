import time
from machine import Pin , UART , I2C , Timer , ADC
from ssd1306 import SSD1306_I2C

button_left = Pin(9, Pin.IN , Pin.PULL_UP)
button_right = Pin(7, Pin.IN , Pin.PULL_UP)

i2c = I2C(1 , scl = Pin(15) , sda = Pin(14) , freq = 400000)

oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width , oled_height , i2c)

character_width = 8
icon = "Si"
len_character = len(icon)

oled.fill(1)
oled.text(icon , 50 , 55 ,0)
oled.show()

count = 50

while True:
    while button_left() == 0:
        oled.fill(1)
        oled.text(icon,count ,55 , 0)
        count -= 1
        oled.show()
        if count <= 0:
            count = 0
            break
    while button_right() == 0:
        oled.fill(1)
        oled.text(icon , count , 55 , 0)
        count += 1
        oled.show()
        if count >= oled_width - len_character * character_width:
            count = oled_width - len_character * character_width
            break
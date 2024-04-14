import time
from machine import UART , Pin , I2C , Timer , ADC
from ssd1306 import SSD1306_I2C

#set up two button down and top and delete
button_top = Pin(7, Pin.IN , Pin.PULL_UP)
button_delete = Pin(8, Pin.IN , Pin.PULL_UP)
button_bot = Pin(9, Pin.IN , Pin.PULL_UP)

#set up i2c , oled
i2c = I2C(1 , scl = Pin(15) , sda = Pin(14) , freq = 400000 )
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width , oled_height , i2c)

def main_function(x_value , y_value , colour):
    while True:
        if button_top() == 0:
            oled.pixel(x_value,y_value,colour)
            oled.show()
            y_value -= 1
            x_value += 1
            if y_value == 0:
                y_value = 1 
        elif button_delete() == 0:
            oled.fill(0)
            x_value = 0
            y_value = 30
            oled.pixel(x_value , y_value , 1)
            oled.show()
            x_value += 1
            if x_value >= 128:
                x_value = 0            
        elif button_bot() == 0:
            oled.pixel(x_value , y_value , colour)
            oled.show()
            y_value += 1
            x_value +=1
            if y_value == 64:
                y_value = 63
        else:
            oled.pixel(x_value,y_value,colour)
            oled.show()
            x_value += 1
            if x_value >= 128:
                x_value = 0

x_value = 0
y_value = 30
colour = 1

main_function(x_value , y_value , colour)
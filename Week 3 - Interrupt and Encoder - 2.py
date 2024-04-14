from machine import Pin , UART , I2C , Timer , ADC
from ssd1306 import SSD1306_I2C
from led import Led
from fifo import Fifo
import time
import micropython
micropython.alloc_emergency_exception_buf(200)


class Showing:
    def __init__(self):
        
        self.i2c = I2C(1, scl = Pin(15) , sda = Pin(14) , freq = 400000)
        self.oled = SSD1306_I2C(128 , 64 , self.i2c)
        self.height_value = 5
        
class Scroll_Click:
 
    def __init__(self, rot_a , rot_b , showing , width , height):
        
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.button = Pin(12, Pin.PULL_UP , Pin.IN)
        self.show_text = showing
        
        self.i2c = I2C(1, scl = Pin(15) , sda = Pin(14) , freq = 400000)
        self.oled = SSD1306_I2C(128 , 64 , self.i2c)
        self.oled_width = width
        self.oled_height = height
        
        self.fifo = Fifo(30, typecode = 'i')
        self.second_fifo = Fifo(30,typecode = 'i')
        
        self.pre_time = 0
        self.current_time = 0
        
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        self.button.irq(handler = self.second_handler , trigger = Pin.IRQ_RISING , hard = True)

        
  
        self.led1_off = "LED1_OFF"
        self.led2_off = "LED2_OFF"
        self.led3_off = "LED3_OFF"
        
        self.led1_on = "LED1_ON"
        self.led2_on = "LED2_ON"
        self.led3_on = "LED3_ON"
        
  
        self.square_left ="["
        self.square_right = "]"
        
        self.oled.fill(0)
        self.oled.text(self.square_left , 20 , self.show_text.height_value , 1)
        self.oled.text(self.led1_off , 30 , 5 , 1)
        self.oled.text(self.led2_off , 30 , 20 , 1)
        self.oled.text(self.led3_off, 30 , 35 , 1)
        self.oled.text(self.square_right , 95 , self.show_text.height_value , 1)
        self.oled.show()
        
    def handler(self,pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)
            
    def second_handler(self,pin):
        self.current_time = time.ticks_ms()
        if self.current_time-self.pre_time > 300:
            self.second_fifo.put(1)
            self.pre_time = self.current_time
            
    def scrolling(self):
        while True:
            if self.fifo.has_data():
                saved_value = self.fifo.get()
                if saved_value == 1:
                    self.show_text.height_value += 15
                    if self.show_text.height_value >= 35:
                        self.show_text.height_value = 35                
                    self.oled.fill(0)
                    self.oled.text(self.square_left , 20 , self.show_text.height_value , 1)
                    self.oled.text(self.led1_off , 30 , 5 , 1)
                    self.oled.text(self.led2_off , 30 , 20 , 1)
                    self.oled.text(self.led3_off, 30 , 35 , 1)
                    self.oled.text(self.square_right , 95 , self.show_text.height_value , 1)
                    self.oled.show()
                    
                else:
                    self.show_text.height_value -= 15
                    
                    if self.show_text.height_value <= 5:
                        self.show_text.height_value = 5
                    self.oled.fill(0)
                    self.oled.text(self.square_left , 20 , self.show_text.height_value , 1)
                    self.oled.text(self.led1_off , 30 , 5 , 1)
                    self.oled.text(self.led2_off , 30 , 20 , 1)
                    self.oled.text(self.led3_off, 30 , 35 , 1)
                    self.oled.text(self.square_right , 95 , self.show_text.height_value , 1)
                    self.oled.show()
    
        
            
    
program = Showing()

main1 = Scroll_Click(10,11,program,128,64)
main1.scrolling()
main1.press()
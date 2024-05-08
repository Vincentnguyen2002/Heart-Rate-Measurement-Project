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


def welcome_text():
    oled.fill(1)
    i = 0
    horizontal1 = 0
    horizontal2 = 0
    for i in range(6):
        oled.pixel(4+horizontal1, 3, 0)
        oled.pixel(8+horizontal1, 3, 0)
        oled.pixel(4+horizontal1, 54, 0)
        oled.pixel(8+horizontal1, 54, 0)
    
        oled.line(3+horizontal1, 4, 5+horizontal1, 4, 0)
        oled.line(3+horizontal1, 55, 5+horizontal1, 55, 0)

        oled.line(7+horizontal1, 4, 9+horizontal1, 4, 0)
        oled.line(7+horizontal1, 55, 9+horizontal1, 55, 0)

        oled.line(2+horizontal1, 5, 10+horizontal1, 5, 0)
        oled.line(2+horizontal1, 56, 10+horizontal1, 56, 0)

        oled.line(3+horizontal1, 6, 9+horizontal1, 6, 0)
        oled.line(3+horizontal1, 57, 9+horizontal1, 57, 0)

        oled.line(4+horizontal1, 7, 8+horizontal1, 7, 0)
        oled.line(4+horizontal1, 58, 8+horizontal1, 58, 0)

        oled.line(5+horizontal1, 8, 7+horizontal1, 8, 0)
        oled.line(5+horizontal1, 59, 7+horizontal1, 59, 0)

        oled.pixel(6+horizontal1, 9, 0)
        oled.pixel(6+horizontal1, 60, 0)
        
        horizontal1 += 23
    
    for i in range(2):
        oled.pixel(4+horizontal2, 19, 0)
        oled.pixel(8+horizontal2, 19, 0)
        oled.pixel(4+horizontal2, 37, 0)
        oled.pixel(8+horizontal2, 37, 0)
    
        oled.line(3+horizontal2, 20, 5+horizontal2, 20, 0)
        oled.line(3+horizontal2, 38, 5+horizontal2, 38, 0)

        oled.line(7+horizontal2, 20, 9+horizontal2, 20, 0)
        oled.line(7+horizontal2, 38, 9+horizontal2, 38, 0)

        oled.line(2+horizontal2, 21, 10+horizontal2, 21, 0)
        oled.line(2+horizontal2, 39, 10+horizontal2, 39, 0)

        oled.line(3+horizontal2, 22, 9+horizontal2, 22, 0)
        oled.line(3+horizontal2, 40, 9+horizontal2, 40, 0)

        oled.line(4+horizontal2, 23, 8+horizontal2, 23, 0)
        oled.line(4+horizontal2, 41, 8+horizontal2, 41, 0)

        oled.line(5+horizontal2, 24, 7+horizontal2, 24, 0)
        oled.line(5+horizontal2, 42, 7+horizontal2, 42, 0)

        oled.pixel(6+horizontal2, 25, 0)
        oled.pixel(6+horizontal2, 43, 0)
        
        horizontal2 += 115
    oled.text("Welcome to", 26, 17, 0)
    oled.text("Group 9's", 29, 27, 0)
    oled.text("project!", 33, 37, 0)
    oled.show()
    utime.sleep_ms(2000)
welcome_text()
# Rotary Encoder

class Encoder:
    def __init__(self, rot_a, rot_b, rot_p,oled):
        self.a = Pin(rot_a, mode=Pin.IN, pull=Pin.PULL_UP)
        self.b = Pin(rot_b, mode=Pin.IN, pull=Pin.PULL_UP)
        self.button = Pin(rot_p, mode=Pin.IN, pull=Pin.PULL_UP)
        self.oled  = oled
         
        self.rolling_fifo = Fifo(10, typecode='i')
        self.press_fifo = Fifo(10, typecode= 'i')
         
        self.rolling  = True
        self.pressing = True
         
        self.back = 0
        self.last_time = 0
        self.option = 0
        self.flag_data = False
        self.val = 0
        self.val_2 = 0
        self.display_value = 0
        self.press_count = 0
        
        self.debounce = 0
        self.flag_back = True
#         self.start_display()
#         self.oled.fill(0)
#         self.oled.text("start measurement", 0, 8, 1)
#         self.oled.text("by press button" , 0 , 16 ,1)
#         self.oled.show()
#         self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)
        self.button.irq(handler=self.p_handler, trigger=Pin.IRQ_RISING, hard=True)
#     def handler(self, pin):
#         if self.rolling == True:
#             if self.b():
#                 self.rolling_fifo.put(-1)
#             else:
#                 self.rolling_fifo.put(1)
    
    def start_display(self):
        if self.display_value == 0:
            self.oled.fill(0)
            self.oled.text("start measurement", 0, 8, 1)
            self.oled.text("by press button" , 0 , 16 ,1)
            self.oled.show()
    def p_handler(self, pin):
        new_time = utime.ticks_ms()
        if self.pressing == True:
            if new_time - self.last_time > 100:
                self.press_fifo.put(1)  
                self.last_time = new_time
        
    def scrolling(self):
        while self.rolling_fifo.has_data():
            rolling_value = self.rolling_fifo.get()
            self.option += rolling_value
    def display_measuring(self):
        self.oled.fill(0)
        self.oled.fill_rect(0,20,128,10,0)
        self.oled.text("measuring...",20,20,1)
        self.oled.show()
        
    def press_button(self,hr):
        self.start_display()
        while self.press_fifo.has_data():
            press_value = self.press_fifo.get()
            self.press_count += press_value
            self.display_value ^= press_value
            measure = hr
            self.rolling = False
            self.pressing = False
            if self.option == 0 and self.display_value == 1:
                self.oled.fill(0)
                self.oled.fill_rect(0,20,128,10,0)
                self.oled.text("measuring...",20,20,1)
                self.oled.show()
                self.val ^= 1
                measure.control_measure ^= 1
                while self.val == 1:
                    measure.finding_threshold_margin()
                    measure.checking_hr()
                    measure.change_press_value()
code = Encoder(10,11,12,oled)
project = Heartrate(26,500,code)
tmr = Piotimer(mode = Piotimer.PERIODIC, freq = 250, callback = project.handler)

def main():
     while True:
         code.press_button(project)

main()

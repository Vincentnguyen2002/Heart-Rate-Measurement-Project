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

    
# OLED
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_height = 64
oled_width = 128
oled = SSD1306_I2C(oled_width, oled_height, i2c)

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
        self.rolling_fifo = Fifo(10, typecode='i')
        self.press_fifo = Fifo(10, typecode= 'i')
        
        self.rolling  = True
        self.pressing = True
        
        self.last_time = 0
        self.option = 0

        self.val = 0
        self.val_2 = 0
        self.count = 0
        self.in_menu = False
        self.update = True
        self.start = True
        self.press = False
        self.oled = oled
        
        self.oled.fill(0)
#         self.oled.text("->", 5,0,1)
#         self.oled.text("MEASURE HR", 25, 0, 1)
#         self.oled.text("HR ANALYSIS", 25, 8, 1)
#         self.oled.show()
        
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)
        self.button.irq(handler=self.p_handler, trigger=Pin.IRQ_RISING, hard=True)
    def handler(self, pin):
        if self.rolling == True or self.update == False and self.val != 1:
            if self.b():
                self.rolling_fifo.put(-1)
            else:
                self.rolling_fifo.put(1)
            
    def p_handler(self, pin):
        new_time = utime.ticks_ms()
        if self.pressing == True :
            if new_time - self.last_time > 100:
                self.press_fifo.put(1)  
                self.last_time = new_time
    def init_menu(self):
        if self.update == True and self.start == True:
            self.oled.fill(0)
            self.oled.text("->", 5,0,1)
            self.oled.text("MEASURE HR", 25, 0, 1)
            self.oled.text("HR ANALYSIS", 25, 8, 1)
            self.oled.show()
            self.update = False
            self.start = False            
    def scrolling(self):
        if self.update == False:
            while self.rolling_fifo.has_data():
                rolling_value = self.rolling_fifo.get()
                self.option += rolling_value
                if self.option >= 1:
                    self.option = 1
                if self.option <= 0:
                    self.option = 0
                self.update = True
    
    def show_option(self):
        if self.update == True:    
            self.oled.fill_rect(0,0,25,17,0)
            self.oled.text("->", 5,self.option*8,1)
            self.oled.show()
            self.update = False
    def is_press(self,press_value):
        if press_value == 1:
            self.press = True
            return True
        else:
            return False
    def press_to_dohr(self):
        if self.update == False:
        
            while True:
                measure.finding_threshold_margin()
                measure.checking_hr()
            self.press = False
            self.update = False
            
    def show_to_hr(self):
        if self.update == True:
            self.oled.fill(0)
            self.oled.text("Measure HR", 25, 0, 1)
            self.oled.show()
            self.update = False
    def press_button(self,hr):
        if self.update == False:
            while self.press_fifo.has_data():
                press_value = self.press_fifo.get()
                measure = hr
                self.rolling = False
                self.pressing = False
                self.update = True
                if self.is_press(press_value):
                    if self.option == 0:
                        self.val ^= 1
                        if self.val == 1:
                            self.press_to_dohr()
                            self.show_to_hr()
                        
                    if self.option == 1:
                        self.val_2 ^= 1
                        self.count += 1
                        self.oled.fill(0)
                        self.oled.text("Start", 0, 0, 1)
                        self.oled.text("measurement", 0, 8, 1)
                        self.oled.text("by placing your", 0 ,16, 1)
                        self.oled.text("finger on the", 0, 24, 1)
                        self.oled.text("sensor and press", 0, 32, 1)
                        self.oled.text("the button to", 0, 40, 1)
                        self.oled.text("start", 0, 48, 1)
                        self.rolling = False
                        self.pressing = True
                        self.oled.show()
                        self.press =  False
                        if self.val_2 == 0:
                            self.oled.fill(0)
                            self.oled.text("Collecting data", 0, 0, 1)
                            self.oled.show()
                            self.rolling = False
                            self.pressing = True
                            print(self.count)
                            self.press = False
                        
                    if self.count == 2:
                        self.oled.fill(0)
                        self.rolling = True
                        self.pressing  = True
                        self.oled.text("->", 5,0,1)
                        self.oled.text("MEASURE HR", 25, 0, 1)
                        self.oled.text("HR ANALYSIS", 25, 8, 1)
                        self.oled.show()
                        self.count = 0
                        self.press = False


code = Encoder(10,11,12,oled)
project = Heartrate(26,500,code)
tmr = Piotimer(mode = Piotimer.PERIODIC, freq = 250, callback = project.handler)

def main():
     while True:
        code.init_menu()
        code.scrolling()
        code.show_option()
        code.press_button(project)

main()

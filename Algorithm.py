from machine import Pin,UART,I2C,Timer,ADC
from ssd1306 import SSD1306_I2C
from fifo import Fifo
from piotimer import Piotimer 
import time
import utime
# from Algorithm import Heartrate
import micropython
micropython.alloc_emergency_exception_buf(200)
i2c = I2C(1, scl = Pin(15) , sda = Pin(14) , freq = 400000)
oled = SSD1306_I2C(128,64,i2c)
class Heartrate:
    def __init__(self,adc_pin_nr , samples_value,encoder):
        self.i2c = I2C(1, scl = Pin(15) , sda = Pin(14) , freq = 400000)
        self.oled = SSD1306_I2C(128,64,self.i2c)
        self.adc = ADC(adc_pin_nr)
        self.samples = Fifo(samples_value)
        self.encoder = encoder
        self.count = 0
        self.min_value = 0
        self.max_value = 0
        
        self.times = 0
        self.samples_count = 0
        self.value = 0
        
        self.min_hr = 30
        self.max_hr = 240
        
        self.threshold = 0
        self.th_count = 0
        self.margin = 0
        
        self.ppi = 0
        self.heart_rate = 0
        
        self.flag_count = False
        self.flag_threshold = False
        self.flag_margin = False
        self.control_measure = 0

    def handler(self,tid):
#         if self.encoder.button.value() == 1:
        if self.control_measure == 0:
            self.samples.put(self.adc.read_u16())
    
    def finding_threshold_margin (self):
        while self.samples.has_data():
            self.value = self.samples.get()
            min_value = min(self.samples.data)
            max_value = max(self.samples.data)
            self.threshold = (max_value - min_value)*0.86 + min_value
            self.margin =(max_value - min_value)*0.15 + min_value
            
    def checking_hr(self):
        if self.value > self.threshold:
            self.count += 1
            self.flag_count = True
            self.flag_threshold = True                
        if self.value < self.margin and self.flag_threshold == True:
            self.count += 1
            self.flag_count = True
            self.flag_margin = True
            self.flag_threshold = False
        if self.value >= self.threshold and self.flag_margin == True:
            self.ppi = self.count * 4
            self.heart_rate = 60000/self.ppi
            if 50 <= self.heart_rate <= 150:
#                 print(round(self.heart_rate))
                result = str(round(self.heart_rate))
                self.oled.fill(0)
                self.oled.text(result,40,30,1)
                self.oled.text("BPM",70,30,1)
                self.oled.text("Press to stop",10,50,1)
                self.oled.show()
            self.count = 0
            self.flag_count = False
            self.flag_margin = False
            self.flag_threshold = False
            
    def change_press_value(self):
        if self.encoder.button.value() == 0:
            while not self.encoder.button.value():
                pass
            time.sleep(0.01)
            self.control_measure ^= 1
            if self.control_measure == 0:
                self.encoder.display_measuring()
                if self.control_measure == 1:
                    self.encoder.start_display()
                

# project = Heartrate(26,500,oled)
# while True:
#     project.finding_threshold_margin()
#     project.checking_hr()

from machine import Pin,UART,I2C,Timer,ADC
from ssd1306 import SSD1306_I2C
from fifo import Fifo
from piotimer import Piotimer 
import time
import utime
from Algorithm import Heartrate
import micropython
micropython.alloc_emergency_exception_buf(200)
    
# OLED
# i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
# oled_height = 64
# oled_width = 128
# oled = SSD1306_I2C(oled_width, oled_height, i2c)

# def welcome_text():
#     oled.fill(1)
#     i = 0
#     horizontal1 = 0
#     horizontal2 = 0
#     for i in range(6):
#         oled.pixel(4+horizontal1, 3, 0)
#         oled.pixel(8+horizontal1, 3, 0)
#         oled.pixel(4+horizontal1, 54, 0)
#         oled.pixel(8+horizontal1, 54, 0)
    
#         oled.line(3+horizontal1, 4, 5+horizontal1, 4, 0)
#         oled.line(3+horizontal1, 55, 5+horizontal1, 55, 0)

#         oled.line(7+horizontal1, 4, 9+horizontal1, 4, 0)
#         oled.line(7+horizontal1, 55, 9+horizontal1, 55, 0)

#         oled.line(2+horizontal1, 5, 10+horizontal1, 5, 0)
#         oled.line(2+horizontal1, 56, 10+horizontal1, 56, 0)

#         oled.line(3+horizontal1, 6, 9+horizontal1, 6, 0)
#         oled.line(3+horizontal1, 57, 9+horizontal1, 57, 0)

#         oled.line(4+horizontal1, 7, 8+horizontal1, 7, 0)
#         oled.line(4+horizontal1, 58, 8+horizontal1, 58, 0)

#         oled.line(5+horizontal1, 8, 7+horizontal1, 8, 0)
#         oled.line(5+horizontal1, 59, 7+horizontal1, 59, 0)

#         oled.pixel(6+horizontal1, 9, 0)
#         oled.pixel(6+horizontal1, 60, 0)
        
#         horizontal1 += 23
    
#     for i in range(2):
#         oled.pixel(4+horizontal2, 19, 0)
#         oled.pixel(8+horizontal2, 19, 0)
#         oled.pixel(4+horizontal2, 37, 0)
#         oled.pixel(8+horizontal2, 37, 0)
    
#         oled.line(3+horizontal2, 20, 5+horizontal2, 20, 0)
#         oled.line(3+horizontal2, 38, 5+horizontal2, 38, 0)

#         oled.line(7+horizontal2, 20, 9+horizontal2, 20, 0)
#         oled.line(7+horizontal2, 38, 9+horizontal2, 38, 0)

#         oled.line(2+horizontal2, 21, 10+horizontal2, 21, 0)
#         oled.line(2+horizontal2, 39, 10+horizontal2, 39, 0)

#         oled.line(3+horizontal2, 22, 9+horizontal2, 22, 0)
#         oled.line(3+horizontal2, 40, 9+horizontal2, 40, 0)

#         oled.line(4+horizontal2, 23, 8+horizontal2, 23, 0)
#         oled.line(4+horizontal2, 41, 8+horizontal2, 41, 0)

#         oled.line(5+horizontal2, 24, 7+horizontal2, 24, 0)
#         oled.line(5+horizontal2, 42, 7+horizontal2, 42, 0)

#         oled.pixel(6+horizontal2, 25, 0)
#         oled.pixel(6+horizontal2, 43, 0)
        
#         horizontal2 += 115

#     oled.text("Welcome to", 26, 17, 0)
#     oled.text("Group 9's", 29, 27, 0)
#     oled.text("project!", 33, 37, 0)
#     oled.show()
#     utime.sleep_ms(2000)
# welcome_text()
# Rotary Encoder

class Encoder:
    def __init__(self, rot_a, rot_b, rot_p):
        self.a = Pin(rot_a, mode=Pin.IN, pull=Pin.PULL_UP)
        self.b = Pin(rot_b, mode=Pin.IN, pull=Pin.PULL_UP)
        self.p = Pin(rot_p, mode=Pin.IN, pull=Pin.PULL_UP)
        self.rolling_fifo_1 = Fifo(10, typecode='i')
        self.press_fifo_1 = Fifo(10, typecode= 'i')
        self.rolling_fifo_2 = Fifo(10,typecode = 'i')
        self.press_fifo_2 = Fifo(10,typecode = 'i')
#         i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
#         oled = SSD1306_I2C(128, 64, i2c)
        self.current_selector = None
        self.current_program = None
        
        self.last_time = 0
        self.option = 0
        self.comback = 0
        self.val1 = 0
        self.val2 = 0
        self.in_menu = False
#         oled.fill(0)
#         oled.text("->", 5,0,1)
#         oled.text("MEASURE HR", 25, 0, 1)
#         oled.text("HR ANALYSIS", 25, 8, 1)
#         oled.show()
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)
        self.p.irq(handler=self.p_handler, trigger=Pin.IRQ_RISING, hard=True)
    
    def updating_program(self,program):
        self.current_program =  program
        self.current_selector = program.selector
    
    def press_fifo_number(self):
        name = self.current_program.name
        if name == 1:
            return self.press_fifo_1
        elif name == 2:
            return self.press_fifo_2
    
    def turn_fifo_number(self):
        name = self.current_program.name
        if name == 1:
            return self.rolling_fifo_1
        elif name == 2:
            return self.rolling_fifo_2
    def p_handler(self,pin):
        if self.current_program != None:
            press_fifo = self.press_fifo_number()
            new_time = utime.ticks_ms()
            if new_time - self.last_time > 300:
                press_fifo.put(1)
                self.last_time = new_time
    
    def handler(self,pin):
        if self.current_selector != None:
            turn_fifo = self.turn_fifo_number()
            if self.b():
                turn_fifo.put(-1)
            else:
                turn_fifo.put(1)
    
class Display_Menu_Select:
    def __init__(self,amount):
        self.amount = amount

class Menu_Display:
    def __init__(self,i2c,scl_pin,sda_pin,frequency,width,height):
        self.i2c = I2C(i2c,scl = scl_pin, sda = sda_pin, freq = frequency)
        self.oled = SSD1306_I2C(width,height,self.i2c)
    
    def show_menu(self):
        self.oled.fill(0)
        self.oled.text("->", 5,0,1)
        self.oled.text("MEASURE HR", 25, 0, 1)
        self.oled.text("HR ANALYSIS", 25, 8, 1)
        self.oled.show()

class Menu:
    def __init__(self,name,encoder,oled, selector = None):
        self.name = name
        self.oled = oled
        self.encoder = encoder
        self.flag_current = True
        self.selector = selector
        self.press =  False
    
    def work(self):
        return self.flag_current
    
    def on(self):
        self.press = False
        self.flag_current = True
        self.encoder.updating_program(self)
        self.oled.show()
        self.handler()
        self.p_handler()
    
    def handle_press(self):
        press_fifo_1 = self.encoder.press_fifo_1
        while press_fifo_1.has_data():
            value = press_fifo_1.get()
            if value == 1:
                self.press = True
    
    def handle_rolling(self):
        rolling_fifo_1 = self.encoder.rolling_fifo_1
        while rolling_fifo_1.has_data():
            value = rolling_fifo_1.get()
            self.selector.amount += value
            if self.selector.amount >= 1:
                self.selector.amount = 1
            if self.selector.amount <= 0:
                self.selector.amount = 0
            self.oled.fill_rect(0,0,25,17,0)
            self.oled.text("->", 5,self.selector.amount*8,1)
        self.oled.show()
    
    def off(self):
        self.flag_current = False
        
        self.encoder.flag_current = False

class Inner_Menu_Select:
    def __init__(self,amount):
        self.amount = amount

class Menu_Inner:
    def __init__(self,width,height):
        self.i2c = I2C(1,scl = Pin(15), sda = Pin(14), freq = 40000)
        self.oled = SSD1306_I2C(width,height,self.i2c)
    
    def show(self):
        self.oled.fill(0)
        self.oled.text("Option 11",0,0)
        self.oled.show()

class Inner:
    def __init__(self,name,encoder,oled,selector = None):
        self.name = name
        self.encoder = encoder
        self.oled = oled
        self.flag_current = False
        self.press = False
        self.selector = selector
    def work(self):
        return self.flag_current
    
    def on(self):
        self.press = False
        self.flag_current = True
        self.encoder.flag_current = True
        self.encoder.updating_program(self)
        self.oled.show()
        
        self.handler()
        self.p_handler()
        
    def handle_press(self):
        press_fifo_2 = self.encoder.press_fifo_2
        while press_fifo_2.has_data():
            value = press_fifo_2.get()
            if value == 1:
                    self.press = True
    
    def handle_rolling(self):
        rolling_fifo_2 = self.encoder.rolling_fifo_2
        while rolling_fifo_2.has_data():
            value = rolling_fifo_2.get()
            self.selector.amount += value
            #de trong 
            #print(f'program :{self.name} selector :{self.selector.size}')
    
    def off(self):
        self.flag_current = False
        self.encoder.flag_current = False

class Main:
    def __init__(self,delay,menu,inner_menu):
        self.delay = delay
        self.menu = menu
        self.inner_menu = inner_menu
        self.state = self.state_menu
    
    def execute(self):
        self.state()
    
    def state_menu(self):
        self.inner_menu.off()
        self.menu.on()
        time.sleep(self.delay)
        
        if self.menu.press:
            print("to state inner")
            self.state = self.state_inner
        else:
            self.state = self.state_menu
    
    def state_inner(self):
        self.menu.off()
        self.inner_menu.on()
        time.sleep(self.delay)
        if self.inner_menu.press:
            print("to state menu")
            self.state = self.state_menu
        else:
            self.state = self.state_inner

hz = 20
waiting = round(1/hz , 2)

encoder = Encoder(10,11,12)
menu_selector = Display_Menu_Select(0)
display_menu = Menu_Display(1,Pin(15),Pin(14),40000,128,64)
menu = Menu(1,encoder,display_menu,menu_selector)


inner_menu_selector = Inner_Menu_Select(0)
inner_menu_display = Menu_Inner(128,64)
inner = Inner(2,encoder,inner_menu_display,inner_menu_selector)

main = Main(waiting,menu,inner)

while True:
    main.execute()            
        
        
        
    
    
    
    


# project = Heartrate(26,500)
# code = Encoder(10,11,12)
# tmr = Piotimer(mode = Piotimer.PERIODIC, freq = 250, callback = project.handler)

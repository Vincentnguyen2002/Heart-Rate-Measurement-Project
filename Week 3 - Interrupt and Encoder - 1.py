from machine import Pin
from led import Led
from fifo import Fifo
import time
from led import Led
import micropython
micropython.alloc_emergency_exception_buf(200)


class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        self.val = 0
    def handler(self,pin):
        if self.val == 1: # den tat
            if self.b():
                self.fifo.put(-10)
            else:
                self.fifo.put(10)
        



class Program:
    def __init__(self,encoder,button, led):
        self.encoder = encoder
        self.button = button
        self.led = led
        self.val = 0
        self.bright = 0
        
    def on_light(self):
        if self.button.value() == 0:
            while not self.button.value():
                pass
            time.sleep(0.1)
            print("pressed")
            self.val ^= 1
            self.encoder.val = self.val
            self.led.value(self.val)
        if self.val == 1:
            while self.encoder.fifo.has_data():
                saved = self.encoder.fifo.get()
                self.bright += saved
                self.led.brightness(self.bright)
            
        
button = Pin(12, pull = Pin.PULL_UP , mode = Pin.IN)
led = Led(22)
encoder = Encoder(10,11)
program = Program(encoder, button, led)

while True:
    program.on_light()
          
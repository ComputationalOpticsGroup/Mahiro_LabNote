# -*- coding: utf-8 -*-
"""
Created on Wed Aug  6 19:40:28 2025

@author: _s2520278
"""

import time
import sys
import board
import neopixel
import math

class LedPackage:
    
    # ---------------------------------
    # Class 2: LedSegment
    # ---------------------------------
    class LedSegment:
        def __init__(self, index, total_leds): # Constructor for LedSegment
            self.index = index
            self.color = (0, 0, 0)
            self.is_on = False
            self.on_time = 0.0
            self.fade_time = 0.0
            self.angle = (360 / total_leds) * index
        
        def set_color(self, R, G, B):　# Single LED status control (1)　
            self.color = (R, G, B)
        
        def turn_on(self):　# Single LED status control (2)
            self.is_on = True
        
        def turn_off(self): # Single LED status control (3)
            self.is_on = False
            
        def set_exposure_time(self, on_time):　# Exposure time control
            self.on_time = on_time
            
        def set_fade_time(self, fade_time):　# Fade time control
            self.fade_time = fade_time
    
    # ---------------------------------
    # Class1: LedPackage
    # ---------------------------------
    def __init__(self, led_pin, led_count=24):　# Constructor for LedPackage
        self.led_count = led_count
        self.led_pin = led_pin
        self.pixels = neopixel.NeoPixel(self.led_pin, self.led_count, auto_write=False)
        self.segments = [self.LedSegment(i, self.led_count) for i in range(self.led_count)]
        self.current_sequence = list(range(self.led_count))
        self.hold_state = False

    def set_sequence(self, sequence): # illumination sequence control (1)
        self.current_sequence = sequence

    def run_sequence(self, color, loops=1, delay=0.1):　# illumination sequence control (2)
        for _ in range(loops):
            for i in self.current_sequence:
                if self.hold_state:
                    time.sleep(1)
                    continue
                
                # Turns off all LEDs and turns on the current one.
                self.pixels.fill((0, 0, 0))
                self.pixels[i] = color
                self.segments[i].set_color(color[0], color[1], color[2])
                self.segments[i].turn_on()
                self.show()
                time.sleep(delay)
                
    def get_led_at_angle(self, degree):　# LED position control (1)
        closest_index = -1
        min_diff = 361
        for i in range(self.led_count):
            diff = abs(self.segments[i].angle - degree)
            if diff < min_diff:
                min_diff = diff
                closest_index = i
        return closest_index

    def illuminate_at_angle(self, degree, color):　# LED position control (2)
        index = self.get_led_at_angle(degree)
        if index != -1:
            self.pixels[index] = color
            self.segments[index].set_color(color[0], color[1], color[2])
            self.segments[index].turn_on()
            self.show()

    def reset(self):　# Resets all LEDs
        self.pixels.fill((0, 0, 0))
        for segment in self.segments:
            segment.turn_off()
            segment.set_color(0, 0, 0)
        self.show()
        
    def hold(self, state=True):　# Holds all LEDs
        self.hold_state = state

    def set_color_ratio(self, color_map): # Color ratio control
        # Here, implement rogic to set LED color based on the rate
        # e.g., color_map = {'red': 0.5, 'blue': 0.5}
        pass

    def show(self): # Sends signals to the Raspberry Pi
        self.pixels.show()

if __name__ == "__main__":
    try:
        # Create instance of LedPackage
        package = LedPackage(led_pin=board.D18)
        
        print("Start LED sequence.")
        #　--------------------------------
        # Something to illuminate LED
        # -----------------------------------
        package.reset()
        print("Completed.")
        
    except KeyboardInterrupt:
        print("\nCanceled program.")
    finally:
        if 'package' in locals():
            package.reset()
        sys.exit()
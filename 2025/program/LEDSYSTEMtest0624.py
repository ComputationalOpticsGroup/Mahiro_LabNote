# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 15:56:59 2025

@author: _s2520278
"""

import time
import board
import neopixel
import cv2
import numpy as np

# --- LED設定 ---
NUM_LEDS = 24
PIXEL_PIN = board.D18
BRIGHTNESS = 0.2  # 明るさ (0〜1)
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    PIXEL_PIN, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False, pixel_order=ORDER
)

# --- カメラ設定 ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("OpenCV camera access failed")

def capture_and_save(idx):
    ret, frame = cap.read()
    if not ret:
        print(f"Warning: capture failed for LED {idx}")
    else:
        cv2.imwrite(f"led_{idx+1:02d}.png", frame)

try:
    for i in range(NUM_LEDS):
        pixels.fill((0,0,0))
        pixels[i] = (255,255,255)  # 白で点灯
        pixels.show()
        time.sleep(0.05)  # 安定待ち

        # 露光時間待機
        time.sleep(0.5)

        capture_and_save(i)

        pixels[i] = (0,0,0)
        pixels.show()

    print("All done: images led_01.png ～ led_24.png")
finally:
    cap.release()
    pixels.fill((0,0,0))
    pixels.show()
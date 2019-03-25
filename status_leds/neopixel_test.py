#!/usr/bin/env python3
import board
import neopixel
from led_lights import LedLights

if __name__ == '__main__':
    pixels = neopixel.NeoPixel(board.D18, 12)
    LedLights.set_status_1_and_remaining(pixels)

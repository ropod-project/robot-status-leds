#!/usr/bin/env python3
import test
import board
import neopixel

if __name__ == '__main__':
    pixels = neopixel.NeoPixel(board.D18, 12)
    pixels.fill((255, 255, 255))
    time.sleep(3)
    pixels.fill((0, 0, 0))

import time
import math
from led_circle import LedCircle

class LedLights(object):

    """A class providing static methods to control a led_circle's led lights"""

    @staticmethod
    def show_percentage(lights, percentage):
        """show percentage on led lights

        :lights: list of tuples (each tuple is (r,g,b))
        :percentage: float between 0.0 and 100.0
        :returns: None

        """
        N = len(lights)
        single_led_percentage = 100.0/N
        on_led = percentage/single_led_percentage
        full_led = int(math.floor(on_led))
        dim_led = on_led - full_led
        for i in range(full_led):
            lights[i] = (255, 255, 255)
        lights[full_led] = tuple([int(255*dim_led)]*3)
        for i in range(full_led+1, N):
            lights[i] = (0, 0, 0)

    @staticmethod
    def circle_test(lights, color=(255,0,0)):
        """test the led lights by making a circle

        :lights: list of tuples (each tuple is (r,g,b))
        :color: tuple (r,g,b)
        :returns: None

        """
        N = len(lights)
        for i in range(N):
            lights[i] = (0, 0, 0)
        for i in range(N):
            lights[i] = color
            time.sleep(0.5)

    @staticmethod
    def set_status_1_and_remaining(lights, color1=(255, 0, 0), color2=(255, 255, 255)):
        """ Set color1 to led1 and color2 to remaining leds

        :lights: list of tuples (each tuple is (r,g,b))
        :color1: tuple (r,g,b)
        :color2: tuple (r,g,b)
        :returns: None

        """
        N = len(lights)
        lights[0] = color1
        for i in range(1, N) :
            lights[i] = color2

if __name__ == "__main__":
    led_circle = LedCircle()
    led_circle.start()
    # LedLights.show_percentage(led_circle.led_colors, 55.0)
    # LedLights.circle_test(led_circle.led_colors, (0, 255, 0))
    LedLights.set_status_1_and_remaining(led_circle.led_colors, color1=(0, 255, 0))
    time.sleep(1)
    led_circle.stop()

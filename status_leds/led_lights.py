import time
import math

class LedLights(object):

    """A class providing static methods to control a led_circle's led lights"""

    @staticmethod
    def show_percentage(lights, percentage=77.0):
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
    def circle_test2(lights, colors=[(255,0,0), (0, 255, 0), (0, 0, 255)]):
        """test the led lights by making a circle

        :lights: list of tuples (each tuple is (r,g,b))
        :color: list of tuple (r,g,b)
        :returns: None

        """
        black = (0, 0, 0)
        N = len(lights)
        for i in range(N):
            lights[i] = black
        for color in colors:
            for i in range(N):
                lights[i] = color
                time.sleep(0.05)
            for i in range(N):
                lights[i] = black
                time.sleep(0.05)

    @staticmethod
    def circle_test3(lights, colors=[(255,0,0), (0, 255, 0), (0, 0, 255)]):
        """test the led lights by making a circle

        :lights: list of tuples (each tuple is (r,g,b))
        :color: list of tuple (r,g,b)
        :returns: None

        """
        black = (0, 0, 0)
        N = len(lights)
        for i in range(N):
            lights[i] = black
        for color in colors:
            for i in range(N):
                lights[i] = color
                time.sleep(0.1)

    @staticmethod
    def circle_test4(lights, colors=[(255,0,0), (0, 255, 0), (0, 0, 255)]):
        """test the led lights by making a circle

        :lights: list of tuples (each tuple is (r,g,b))
        :color: list of tuple (r,g,b)
        :returns: None

        """
        black = (0, 0, 0)
        led_colors = []
        N = len(lights)
        if N % len(colors) != 0 :
            for i in range(int(N/len(colors))):
                led_colors.extend(colors)
            for i in range(N % len(colors)):
                led_colors.append(black)
        else :
            for i in range(int(N/len(colors)) - 1):
                led_colors.extend(colors)
            for i in range(len(colors)):
                led_colors.append(black)

        for i in range(N):
            for j in range(N):
                lights[j] = led_colors[j]
            led_colors.insert(0, led_colors.pop(-1))
            time.sleep(0.3)

    @staticmethod
    def set_status(lights, color1=(255, 0, 0), color2=(0, 255, 0), color3=(255, 255, 255)):
        """ Set color1 to led1 and color2 to remaining leds

        :lights: list of tuples (each tuple is (r,g,b))
        :color1: tuple (r,g,b)
        :color2: tuple (r,g,b)
        :returns: None

        """
        N = len(lights)
        second_led = int(N/2)
        lights[0] = color1
        lights[second_led] = color2
        for i in range(1, second_led) :
            lights[i] = color3
        for i in range(second_led+1, N) :
            lights[i] = color3

    @staticmethod
    def set_status_half_and_half(lights, color1=(255, 0, 0), color2=(255, 255, 255)):
        """ Set color1 to led1 and color2 to remaining leds

        :lights: list of tuples (each tuple is (r,g,b))
        :color1: tuple (r,g,b)
        :color2: tuple (r,g,b)
        :returns: None

        """
        N = len(lights)
        for i in range(int(N/2)) :
            lights[i] = color1
        for i in range(int(N/2), N) :
            lights[i] = color2

    @staticmethod
    def set_color(lights, color1=(255, 0, 0)):
        """ Set color1 to all the leds

        :lights: list of tuples (each tuple is (r,g,b))
        :color1: tuple (r,g,b)
        :returns: None

        """
        N = len(lights)
        for i in range(N) :
            lights[i] = color1

if __name__ == "__main__":
    from status_leds.gui_led_circle import LedCircle
    led_circle = LedCircle()
    led_circle.start()
    # LedLights.show_percentage(led_circle.led_colors, 55.0)
    # time.sleep(1)
    # LedLights.circle_test(led_circle.led_colors)
    # LedLights.circle_test2(led_circle.led_colors)
    # LedLights.circle_test3(led_circle.led_colors)
    # LedLights.circle_test4(led_circle.led_colors)
    # LedLights.circle_test4(led_circle.led_colors, colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 255, 255)])
    # LedLights.set_status(led_circle.led_colors)
    # time.sleep(1)
    # LedLights.set_status_half_and_half(led_circle.led_colors)
    # time.sleep(1)
    LedLights.set_color(led_circle.led_colors, color1=(0, 255, 0))
    time.sleep(1)
    led_circle.stop()

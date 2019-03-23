#! /usr/bin/env python

import time
import argparse

from led_pyre_communicator import LedPyreCommunicator
from led_lights import LedLights


class LedColorController(object):

    """Gets status of the robot from different components and decides the color
    of the leds accordingly"""

    _colors = {
        "ROBOT_PERFORMING_TASK":(0, 255, 0),
        "ROBOT_NOT_PERFORMING_TASK":(0, 255, 255),
        "BRINGUP_NOT_RUNNING":(255, 255, 255),
        "COMPONENTS_WORKING":(0, 255, 0),
        "COMPONENTS_NOT_WORKING":(255, 0, 0),
        "BLACK":(0, 0, 0)
    }
    def __init__(self):
        self._led_pyre_comm = LedPyreCommunicator(robot_id)
        self.color1 = self._colors['BLACK']
        self.color2 = self._colors['BLACK']
        self._blink_light_on = False

    def stop(self):
        """Cleanup function for pyre nodes
        :returns: TODO

        """
        self._led_pyre_comm.shutdown()

    def update_colors(self):
        """Update colors after getting updated status from different components.
        :returns: None

        """
        if self._led_pyre_comm.bringup_running:
            self.color1 = self._colors['ROBOT_NOT_PERFORMING_TASK'] # need a component for real value
            self.color2 = self._colors['COMPONENTS_WORKING'] if \
                    self._led_pyre_comm.everything_working else \
                    self._colors['COMPONENTS_NOT_WORKING']
        else:
            self._blink_light_on = not self._blink_light_on
            self.color1 = self._colors['ROBOT_NOT_PERFORMING_TASK']
            self.color2 = self._colors["BRINGUP_NOT_RUNNING"] if \
                    self._blink_light_on else self._colors['BLACK']


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Control LED lights for a ropod")
    parser.add_argument('-rid', '--robot_id', help='ID of robot on which the leds are attached', 
            default='ropod_001')
    parser.add_argument('-s', '--simulation', action='store_true', 
            help='Use tkinter gui window to see led lights instead of using actual hardware.')
    args = parser.parse_args()
    robot_id = args.robot_id
    simulation = args.simulation

    if simulation:
        from led_circle import LedCircle
        led_circle = LedCircle()
        led_circle.start()
        lights = led_circle.led_colors
    else:
        import board
        import neopixel
        lights = neopixel.NeoPixel(board.D18, 12)

    led_color_controller = LedColorController()
    LedLights.circle_test3(lights)
    try:
        while True:
            led_color_controller.update_colors()
            LedLights.set_status(lights, color1=led_color_controller.color1, color2=led_color_controller.color2)
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Interrupted execution. Exiting.")

    led_color_controller.stop()

    if simulation:
        led_circle.stop()
    else:
        pass # clean up of led lights library (if any)

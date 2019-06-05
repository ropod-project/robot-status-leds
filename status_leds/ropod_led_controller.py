#! /usr/bin/env python

import time
import argparse
import os.path
import yaml

from led_pyre_communicator import LedPyreCommunicator
from led_lights import LedLights


class LedColorController(object):

    """Gets status of the robot from different components and decides the color
    of the leds accordingly"""

    def __init__(self, config_file, use_brightness=True, robot_id='ropod_001', black_box_id='black_box_001'):
        self._led_pyre_comm = LedPyreCommunicator(robot_id=robot_id, black_box_id=black_box_id)
        self.variables = []
        self.color1 = (0, 0, 0)
        self.color2 = (0, 0, 0)
        self.color3 = (0, 0, 0)
        self._colors = None
        self._blink_light_on = False

        try:
            print(config_file)
            with open(config_file, 'r') as f:
                config_data = yaml.load(f)
            brightness = config_data.get('brightness', 20)
            self._colors = config_data.get('colors', None)
            if use_brightness:
                for i in self._colors:
                    for j in range(3):
                        if self._colors[i][j] == 255:
                            self._colors[i][j] = brightness
        except Exception as e:
            print("Encountered following error while reading config file\n", str(e))

    def stop(self):
        """Cleanup function for pyre nodes
        :returns: TODO

        """
        self._led_pyre_comm.shutdown()

    def update_colors(self):
        """Update colors after getting updated status from different components.
        :returns: None

        """
        if self._colors is None :
            return
        self.color1 = self._colors['ROBOT_PERFORMING_TASK'] if \
                self._led_pyre_comm.data['robot_performing_task'] else \
                self._colors['ROBOT_NOT_PERFORMING_TASK']

        if self._led_pyre_comm.is_health_status_stale():
            self.color3 = self._colors['BLACK']
        elif self._led_pyre_comm.data['e_stop_pressed']:
            self._blink_light_on = not self._blink_light_on
            self.color3 = self._colors["E_STOP_PRESSED"] if \
                    self._blink_light_on else self._colors['BLACK']
        else:
            if self._led_pyre_comm.data['bringup_running']:
                self.color3 = self._colors['COMPONENTS_WORKING'] if \
                        self._led_pyre_comm.data['everything_working'] else \
                        self._colors['COMPONENTS_NOT_WORKING']
            else:
                self._blink_light_on = not self._blink_light_on
                self.color3 = self._colors["BRINGUP_NOT_RUNNING"] if \
                        self._blink_light_on else self._colors['BLACK']

        bat_perc =  self._led_pyre_comm.data['battery_percentage']
        if bat_perc is None:
            self.color2 = self._colors['BLACK']
        elif bat_perc < 20 :
            self.color2 = self._colors['LOW_BATTERY']
        elif bat_perc < 50:
            self.color2 = self._colors['MEDIUM_BATTERY']
        else:
            self.color2 = self._colors['HIGH_BATTERY']

        self._led_pyre_comm.send_fms_query()
        self._led_pyre_comm.send_query(self.variables)


if __name__ == "__main__":
    code_dir = os.path.abspath(os.path.dirname(__file__))
    main_dir = os.path.dirname(code_dir)
    default_config_file = os.path.join(main_dir, 'config/config.yaml')

    parser = argparse.ArgumentParser(description="Control LED lights for a ropod")
    parser.add_argument('-rid', '--robot_id', help='ID of robot on which the leds are attached', 
            default='001')
    parser.add_argument('-s', '--simulation', action='store_true', 
            help='Use tkinter gui window to see led lights instead of using actual hardware.')
    parser.add_argument('-c', '--config_file', default=default_config_file, 
            help='Config file path')
    args = parser.parse_args()
    robot_id = 'robot_' + args.robot_id
    black_box_id = 'black_box_' + args.robot_id
    simulation = args.simulation
    config_file = args.config_file

    if simulation:
        from status_leds.gui_led_circle import LedCircle
        led_circle = LedCircle()
        led_circle.start()
        lights = led_circle.led_colors
    else:
        import board
        import neopixel
        lights = neopixel.NeoPixel(board.D18, 12)

    led_color_controller = LedColorController(
        config_file, 
        use_brightness=not simulation, 
        robot_id=robot_id, 
        black_box_id=black_box_id)
    LedLights.circle_test3(lights)
    try:
        while True:
            led_color_controller.update_colors()
            LedLights.set_status(
                    lights, 
                    color1=led_color_controller.color1, 
                    color2=led_color_controller.color2,
                    color3=led_color_controller.color3)
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Interrupted execution. Exiting.")

    led_color_controller.stop()

    if simulation:
        led_circle.stop()
    else:
        LedLights.set_color(lights, color1=(0, 0, 0))

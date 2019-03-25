import sys
import math
import threading
import time
# detect version of python and import tkinter accordingly
if sys.version_info[0] == 2 :
    from Tkinter import * # for python2
elif sys.version_info[0] == 3 :
    from tkinter import * # for python3 (sudo apt install python3-tk)

class LedCircle(object):

    """Create a gui window with tkinter. There will be a circle with N leds
    on the circle. Each led can be color coded.

    To start the GUI window, call start() method and to close the gui window
    call the stop() method.

    To change colors or led, access and change led_colors variable
    
    :key word arguments:
    :win_size: int (size of GUI window in pixels. length=width)
    :num_of_leds: int (number of leds on the circle)
    :led_radius: int (radius of each led in gui window in pixels)
    """

    def __init__(self, **kwargs):
        self.win_size = kwargs.get('win_size', 400)
        self.N = kwargs.get('num_of_leds', 12)
        self.led_size = kwargs.get('led_radius', 20)
        self.running = False
        self.led_colors = [(255, 0, 0)] * self.N
        self._tkinter_thread = threading.Thread(target=self.__run)

    def start(self):
        """ Start the execution of the tkinter gui window on a seperate thread

        :returns: None

        """
        self._tkinter_thread.start()

    def stop(self):
        """ Stop the execution of the tkinter gui window

        :returns: None

        """
        self.running = False
        self._tkinter_thread.join()

    def __run(self):
        """Main loop for the GUI. The window is updated until self.running is 
        set to False.
        :return: None

        """
        self.__setup()
        self.running = True
        while self.running:
            if len(self.led_colors) != self.N :
                self.led_colors = [(0, 0, 0)] * self.N
            for i in range(self.N):
                self._canvas.itemconfig(self._leds[i], fill=self.__rgb_to_hex(self.led_colors[i]))
            self._root.update()
            time.sleep(0.1)

    def __on_quit(self):
        self.running = False
        print("Stopped gui window")

    def __setup(self):
        """Create window and all widgets at its location.
        :returns: None

        """
        self._root = Tk()
        self._root.title('LED')
        self._root.protocol("WM_DELETE_WINDOW", self.__on_quit)
        self._root.geometry(str(self.win_size)+'x'+str(self.win_size))
        self._root.resizable(False, False)
        self._canvas = Canvas(self._root, width = self.win_size, height = self.win_size)
        self._canvas.pack()
        self._canvas.config(bg="black")

        main_circle = self._canvas.create_oval(self.win_size/8, self.win_size/8, 
                (self.win_size*7)/8, (self.win_size*7)/8, outline='white')
        self._leds = []
        radius = ((self.win_size*7)/8 - self.win_size/8)/2
        for i in range(self.N):
            y = -radius * math.cos(i * ((math.pi) * 2) / self.N)
            x = radius * math.sin(i * ((math.pi) * 2) / self.N)
            x += self.win_size/2
            y += self.win_size/2
            self._leds.append(self._canvas.create_oval(x-self.led_size, y-self.led_size, 
                x+self.led_size, y+self.led_size, outline='white', fill="red"))

    def __rgb_to_hex(self, rgb):
        if not isinstance(rgb, list) and not isinstance(rgb, tuple):
            return '#000000'
        if len(rgb) != 3 :
            return '#000000'
        rgb_list = [ min(max(i, 0), 255) if isinstance(i, int) else 0 for i in rgb ]
        return '#%02x%02x%02x' % tuple(rgb_list)

                
if __name__ == "__main__":
    led_circle = LedCircle()
    led_circle.start()
    for i in range(12):
        led_circle.led_colors[i] = (255, 255, 255)
        time.sleep(0.5)
    led_circle.stop()

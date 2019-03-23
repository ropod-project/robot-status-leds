# LED circle

Python code to control and simulate the leds in a circle electronics.

## Execution

### GUI window 
Execute with the following command to view led circle in a gui window
```
python led_lights.py
```

or 
```
python3 led_lights.py
```

**Note**: By default python3 does not come with tkinter (like python2). To
install tkinter library execute following command.
```
sudo apt install python3-tk
```

### ROPOD status controller
Execute following command to start the ropod status controller
```
python3 ropod_led_controller.py [-rid ROBOT_ID] [-s]
```
**Note**: By default, robot_id is 'ropod_001'. `-s` flag can be set to use
tkinter gui instead of actual led lights. See `python3 ropod_led_controller.py
--help` for more info.

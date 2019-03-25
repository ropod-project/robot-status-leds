#! /bin/sh

# export neccessary environment variables
export BLINKA_FORCEBOARD=RASPBERRY_PI_B_PLUS
export BLINKA_FORCECHIP=BCM2XXX

# run the actual code
python3 ropod_led_controller.py

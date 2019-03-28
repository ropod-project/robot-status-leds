#! /bin/sh

# export neccessary environment variables
export BLINKA_FORCEBOARD=RASPBERRY_PI_B_PLUS
export BLINKA_FORCECHIP=BCM2XXX

if [ "$1" = "test" ]; then
	# run test program
	python3 neopixel_test.py
else
	# run the actual code
	python3 ropod_led_controller.py
fi

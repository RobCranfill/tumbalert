
# tumbalert v1a

import time
import board
import digitalio

import adafruit_vcnl4010
from adafruit_bme280 import basic as adafruit_bme280
import neopixel


# some globals. so shoot me.

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

button = digitalio.DigitalInOut(board.BUTTON)
button.switch_to_input(pull=digitalio.Pull.UP)

DEBUG = False


import supervisor
supervisor.runtime.autoreload = False
print("f{supervisor.runtime.autoreload=}") if DEBUG else None

def led_status(color):
    pixel.fill(color)


i2c = board.I2C()   # uses board.SCL and board.SDA
temp_sensor = None
try:
    temp_sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c)
except:
    print("\n **** No temp sensor? OK\n")

light_sensor = adafruit_vcnl4010.VCNL4010(i2c)


# lux value threshold
LUX_THRESH = 200

# rotation threshold
# if we don't see a state change in this many seconds, it's an error.
ROTATION_THRESH = 4

SLEEP_TIME = 0.0 # needed??

ALARM_AGAIN_TIME = 2


last_reading_high = False
n_warnings = 0
last_state_change_time = time.monotonic() # ??

# when still in error state
in_error = False
alarm_time = 0


while True:

    if not button.value: # 'not' is pressed. why?
        print("Button!")
        # in_error = False # not sufficient


    # if temp_sensor is not None:
    #     print("   Temperature: %0.1f C" % temp_sensor.temperature)

    # check button push for reset???


    lux = light_sensor.ambient_lux
    # print(f"({lux=})") if DEBUG else None

    check_time = time.monotonic()
    check_delta = check_time - last_state_change_time
    print(f"{last_reading_high=}, {check_delta=}") if DEBUG else None

    if check_delta > ROTATION_THRESH:

        if in_error:
            if time.monotonic() > alarm_time + ALARM_AGAIN_TIME:
                print(f"  ALARM STILL ON! {reading_high=}")
                alarm_time = time.monotonic()
                led_status((255,255,0))

                n_warnings = n_warnings + 1
                if n_warnings % 5 == 0:
                    print("SEND MESSAGE AGAIN")

        else:
            print(f"ALARM: ROTATION_THRESH ({ROTATION_THRESH} seconds) EXCEEDED! {reading_high=}")
            in_error = True
            alarm_time = time.monotonic()
            led_status((255,0,0))

    reading_high = (lux > LUX_THRESH)
    if reading_high == last_reading_high:
        pass

    else: # state change
        print("state change; resetting timer") if DEBUG else None
        last_state_change_time = check_time
        last_reading_high = reading_high
        if in_error:
            print("  (Alarm cleared)")
        in_error = False
        
        led_status((0,0,255)) if reading_high else led_status((0,255,0))


    # led_status((128,128,128)) if not in_error else None
    time.sleep(SLEEP_TIME)
    # led_status((0,0,0)) if not in_error else None

# blue = sensor high, green = sensor low
# red = initial alarm, yellow = alarm still on


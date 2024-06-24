
# tumbalert v1a

import time
import board
import adafruit_vcnl4010
from adafruit_bme280 import basic as adafruit_bme280


import supervisor
supervisor.runtime.autoreload = False
print("f{supervisor.runtime.autoreload=}")


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


last_reading_high = False
n = 0
last_state_change_time = time.monotonic() # ??


while True:

    # if temp_sensor is not None:
    #     print("   Temperature: %0.1f C" % temp_sensor.temperature)

    # check button push for reset???


    lux = light_sensor.ambient_lux
    # print(f"({lux=})")

    check_time = time.monotonic()
    check_delta = check_time - last_state_change_time
    print(f"{last_reading_high=}, {check_delta=}")

    if check_delta > ROTATION_THRESH:

        # how to avoid this happening 'too often'?
        print(f"ROTATION_THRESH EXCEEDED!")


    reading_high = (lux > LUX_THRESH)
    if reading_high == last_reading_high:
        pass
    else:
        print("state change; resetting timer")
        last_state_change_time = check_time
        last_reading_high = reading_high


    time.sleep(SLEEP_TIME)


# tumbalert
Device to watch a rock tumbler, and alert when it stops rotating.

# Hardware
* Adafruit QT2040 Trinkey
   - Replace with something with WiFi?
* Adafruit VCNL4020 proximity / light sensor
  - overkill; replace with something smaller & cheaper
* Adafruit 5mW laser diode

# Software
* CircuitPython (latest, CircuitPython 9.0.5 currently)
* Adafruit libraries:
    * adafruit_vcnl4010 (v 0.11.10 used)
    * adafruit_bme28 (v 2.6.24 used)

# To Do
* Alerts
  * Local sound via speaker? piezo?
  * Online
    * Adafruit IO?
    * Something else??
* Use extra button on Trinkey
  - for reset? alarm silence?
* Use NeoPixel for status output
  - flash codes?
* Calculate - and use how? - RPM
* Temperature sensor



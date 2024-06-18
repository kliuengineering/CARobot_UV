from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
import time
from time import sleep


# Tests the I2C connection @ pin 17 and 16
def TestI2C():
    i2c = I2C(0, scl=Pin(17), sda=Pin(16))
    while True:
        devices = i2c.scan()
        if devices:
            for device in devices:
                print("I2C device found at address:", hex(device))
        else:
            print("No I2C devices found")
        time.sleep(2)


# The following section of code tests the SSD1306 display
def TestSSD1306():
    # Initialize I2C interface
    i2c = I2C(0, scl=Pin(17), sda=Pin(16))

    # Create SSD1306 OLED display instance
    oled = SSD1306_I2C(128, 64, i2c)

    # Clear the display
    oled.fill(0)

    # Display some text
    oled.text("Hello, World!", 0, 0)
    oled.text("Canada Robotix", 0, 10)
    oled.text("SSD1306 OLED", 0, 20)

    # Update the display to show the text
    oled.show()

    # Loop to keep the script running
    while True:
        sleep(1)


# Uncomment the following line to test the I2C connection
# TestI2C()

# Uncomment the following line to test the SSD1306 display
TestSSD1306()


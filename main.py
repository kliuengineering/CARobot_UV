from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from time import sleep


# The following section of codes test the SSD1306 display
# Can comment it out inside the main() section
def TestSSD1306():

    # Initialize I2C interface
    i2c = I2C(0, scl=Pin(17), sda=Pin(16))

    # Create SSD1306 OLED display instance
    oled = SSD1306_I2C(128, 64, i2c)

    # Clear the display
    oled.fill(0)

    # Display some text
    oled.text("Hello, World!", 0, 0)
    oled.text("MicroPython", 0, 10)
    oled.text("SSD1306 OLED", 0, 20)

    # Update the display to show the text
    oled.show()

    # Loop to keep the script running
    while True:
        sleep(1)


# main() 
if __name__ == "__main__":
    TestSSD1306()
from machine import I2C, Pin, ADC
from ssd1306 import SSD1306_I2C
import time
from time import sleep


# Initialize I2C for the OLED display
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SSD1306_I2C(128, 64, i2c)

# Initialize ADC for ML8511
adc = ADC(Pin(28))

# Enable the ML8511 sensor
enable = Pin(15, Pin.OUT)
enable.value(1)  # Set the EN pin to high to enable the sensor


# Function to convert voltage to UV index
def voltage_to_uv_index(voltage):
    # UV index calculation based on ML8511 sensor characteristics
    # These values are from the ML8511 datasheet
    if voltage < 0.99:
        return 0.0
    elif voltage > 2.8:
        return 15.0
    else:
        uv_index = (voltage - 0.99) * (15.0 / (2.8 - 0.99))
        return uv_index


# Function to read UV intensity from ML8511
def read_uv_index():
    raw_value = adc.read_u16()
    voltage = raw_value * (3.3 / 65535)  # Convert raw ADC value to voltage
    uv_index = voltage_to_uv_index(voltage)
    return uv_index


# Function to display UV index on OLED
def display_uv_index(uv_index):
    oled.fill(0)
    oled.text("UV Index:", 0, 0)
    oled.text("{:.2f}".format(uv_index), 0, 10)
    oled.show()


# Main routine to read UV index and update OLED
while True:
    uv_index = read_uv_index()
    display_uv_index(uv_index)
    sleep(1)


'''
################################ HARDWARE TESTING CODES ################################



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
    oled.text("Test Script...", 0, 0)
    oled.text("Canada Robotix", 0, 10)
    oled.text("SSD1306", 0, 20)

    # Update the display to show the text
    oled.show()

    # Loop to keep the script running
    while True:
        sleep(1)


# Uncomment the following line to test the I2C connection
# TestI2C()

# Uncomment the following line to test the SSD1306 display
# TestSSD1306()

################################ HARDWARE TESTING CODES ################################
'''


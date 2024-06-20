from machine import I2C, Pin, ADC
from ssd1306 import SSD1306_I2C
from time import sleep

# Initialize I2C for the OLED display
i2c = I2C(0, scl=Pin(9), sda=Pin(8))
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
    if voltage < 1.00:
        return 0.0
    elif voltage > 2.20:
        return 11.0  # Capping the UV index at 11 for this example
    else:
        uv_index = (voltage - 1.00) * (11.0 / (2.20 - 1.00))
        return uv_index


# Function to read UV intensity from ML8511
def read_uv_index():
    raw_value = adc.read_u16()  # Read raw 16-bit ADC value (0 to 65535)
    raw_value_12bit = raw_value >> 4  # Scale down to 12-bit value (0 to 4095)
    voltage = raw_value_12bit * (3.3 / 4095)  # Convert raw 12-bit ADC value to voltage (0V to 3.3V)
    uv_index = voltage_to_uv_index(voltage)  # Convert voltage to UV index
    return uv_index


# Function to scale up the readings due to insufficient current when using a coin-cell battery
def scale_uv_index(uv_index):
    if uv_index > 1.2 and uv_index <= 2.0:
        uv_index *= 1.3
    elif uv_index > 2.0 and uv_index <= 5.0:
        uv_index *= 1.5
    elif uv_index > 5.0 and uv_index <= 7.0:
        uv_index *= 1.2
    elif uv_index > 7.0 and uv_index <= 10.0:
        uv_index *= 1.1

    return uv_index


def print_level(uv_index, x_pos, y_pos):
    if uv_index <= 3.0:
        oled.text("(LOW)", x_pos, y_pos)
    elif uv_index > 3.0 and uv_index <= 5.0:
        oled.text("(MODERATE)", x_pos, y_pos)
    elif uv_index > 5.0 and uv_index <= 8.0:
        oled.text("(HIGH)", x_pos, y_pos)
    elif uv_index > 8.0:
        oled.text("(EXTREME)", x_pos, y_pos)
        

# Function to display UV index on OLED
def display_uv_index(uv_index):
    oled.fill(0)
    oled.text("Canada Robotix", 0, 0)
    oled.text("UV-B Index:", 0, 20)
    oled.text("{:.2f}".format(uv_index), 0, 30)
    print_level(uv_index, 40, 30)

    # Draw horizontal bar graph
    oled.text("Bar Graph:", 0, 50)
    bar_length = int((uv_index / 11.0) * 128)  # Scale UV index to 0-128 for bar length
    for i in range(bar_length):
        oled.pixel(i, 63, 1)  # Draw the bar starting at y=60

    oled.show()


# Main loop to continuously read UV index and update OLED
while True:
    uv_index = read_uv_index()
    uv_index = scale_uv_index(uv_index) # you can comment this line out if using a phone to power the Pico
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


from machine import Pin, UART
from time import sleep
import json

from max6675 import MAX6675

# ----- Pin setup -----

# Relays
relay_1_pin = 2
relay_2_pin = 3
relay_3_pin = 6
relay_4_pin = 7
relay_5_pin = 10
relay_6_pin = 11
relay_7_pin = 27
relay_8_pin = 26

# Thermocouple
thermo_clk_pin = 14
thermo_cs_pin = 15
thermo_so_pin = 16

# Bluetooth
scl_pin = Pin(1, Pin.OUT)
sda_pin = Pin(2, Pin.IN)

# LED
green_pin = 18
red_pin = 19
blue_pin = 20

# ----- Pin mode -----

# Relays
relay_1 = Pin(relay_1_pin, Pin.OUT)
relay_2 = Pin(relay_2_pin, Pin.OUT)
relay_3 = Pin(relay_3_pin, Pin.OUT)
relay_4 = Pin(relay_4_pin, Pin.OUT)
relay_5 = Pin(relay_5_pin, Pin.OUT)
relay_6 = Pin(relay_6_pin, Pin.OUT)
relay_7 = Pin(relay_7_pin, Pin.OUT)
relay_8 = Pin(relay_8_pin, Pin.OUT)

# Thermocouple
thermo_sck = Pin(thermo_clk_pin, Pin.OUT)
thermo_cs = Pin(thermo_cs_pin, Pin.OUT)
thermo_so = Pin(thermo_so_pin, Pin.IN)

# LED
green = Pin(green_pin, Pin.OUT)
red = Pin(red_pin, Pin.OUT)
blue = Pin(blue_pin, Pin.OUT)

# ----- Setup modules -----

# Thermocouple
thermocouple = MAX6675(thermo_sck, thermo_cs , thermo_so)

# Bluetooth
uart = UART(0, 9600)

# ----- Functions -----

def blink(pin):
    pin.value(1)
    sleep(0.5)
    pin.value(0)
    
relays = [relay_1, relay_2, relay_3, relay_4, relay_5, relay_6, relay_7, relay_8]

for relay in relays:
    relay.value(1)

while True:
    # temp = thermocouple.read()

    if uart.any():
        blink(green)
        
        data_string = uart.read()
        data_string_utf8 = data_string.decode('utf-8')

        print(data_string_utf8)
        
        try:
            data = json.loads(data_string_utf8)
            
            blink(blue)

            time1 = data.get("1", 0)
            time2 = data.get("2", 0)
            time3 = data.get("3", 0)
            time4 = data.get("4", 0)
            time5 = data.get("5", 0)

            print(time1, time2, time3, time4, time5)
               
            print("Step 1")      

            relay_1.value(0) # 1 -> On
            relay_5.value(0) # 5 -> On
            relay_6.value(0) # 6 -> On
            
            sleep(time1)
            
            print("Step 2")

            relay_2.value(0) # 2 -> On
            relay_1.value(1) # 1 -> Off

            sleep(time2)
            
            print("Step 3")

            relay_3.value(0) # 3 -> On
            relay_2.value(1) # 2 -> Off

            sleep(time3)
            
            print("Step 4")

            relay_4.value(0) # 4 -> On
            relay_3.value(1) # 3 -> Off
            relay_5.value(1) # 5 -> Off

            sleep(time4)
            
            print("Step 5")

            relay_4.value(1) # 4 -> Off
            relay_6.value(1) # 6 -> Off

            sleep(time5)
        except Exception as e:
            blink(red)

            print("Error:", e)
from machine import Pin, PWM
from time import sleep

# Define pins for each LED
RED_PIN = 2
GREEN_PIN = 3
BLUE_PIN = 4

# Initialize PWM for each LED
red_pwm = PWM(Pin(RED_PIN))
green_pwm = PWM(Pin(GREEN_PIN))
blue_pwm = PWM(Pin(BLUE_PIN))

# Set PWM frequency
pwm_freq = 1000
red_pwm.freq(pwm_freq)
green_pwm.freq(pwm_freq)
blue_pwm.freq(pwm_freq)

# Define a function to smoothly change brightness
def fade_led(pwm, duty_cycle):
    pwm.duty_u16(duty_cycle)
    sleep(0.01)  # Adjust sleep time for desired speed

# Define a function to transition between colors
def transition_color(color_from, color_to, duration):
    steps = 100
    for i in range(steps + 1):
        r = color_from[0] + (color_to[0] - color_from[0]) * i / steps
        g = color_from[1] + (color_to[1] - color_from[1]) * i / steps
        b = color_from[2] + (color_to[2] - color_from[2]) * i / steps
        red_pwm.duty_u16(int(r * 65535))
        green_pwm.duty_u16(int(g * 65535))
        blue_pwm.duty_u16(int(b * 65535))
        sleep(duration / steps)

# Main loop for fancy lighting effect
while True:
    # Transition between different colors
    transition_color((1, 0, 0), (0, 1, 0), 1)  # Red to Green
    transition_color((0, 1, 0), (0, 0, 1), 1)  # Green to Blue
    transition_color((0, 0, 1), (1, 0, 0), 1)  # Blue to Red
    
    # Blinking effect
    for _ in range(3):
        red_pwm.duty_u16(0)
        green_pwm.duty_u16(0)
        blue_pwm.duty_u16(0)
        sleep(0.5)
        red_pwm.duty_u16(65535)
        green_pwm.duty_u16(65535)
        blue_pwm.duty_u16(65535)
        sleep(0.5)
    
    # Color wipe effect
    colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    for color in colors:
        for i in range(100):
            red_pwm.duty_u16(int(color[0] * 65535 * i / 100))
            green_pwm.duty_u16(int(color[1] * 65535 * i / 100))
            blue_pwm.duty_u16(int(color[2] * 65535 * i / 100))
            sleep(0.01)
        sleep(0.5)




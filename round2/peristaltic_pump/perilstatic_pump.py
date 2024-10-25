from machine import Pin, PWM
from time import sleep

# Define the frequency for PWM
frequency = 1000

# Initialize pins for motor control
pin1 = Pin(3, Pin.OUT)
pin2 = Pin(1, Pin.OUT)
enable = PWM(Pin(2), frequency)

# Set min and max duty cycle values
min_duty = 15000
max_duty = 65535

# Function to set the duty cycle based on speed
def duty_cycle(speed):
    if speed <= 0 or speed > 100:
        return 0
    else:
        return int(min_duty + (max_duty - min_duty) * (speed / 100))

# Function to move the motor forward
def forward(speed):
    enable.duty_u16(duty_cycle(speed))
    pin1.value(1)
    pin2.value(0)

# Function to move the motor backward
def backwards(speed):
    enable.duty_u16(duty_cycle(speed))
    pin1.value(0)
    pin2.value(1)

# Function to stop the motor
def stop():
    enable.duty_u16(0)
    pin1.value(0)
    pin2.value(0)

# Main code to run the motor
try:
    print('Forward with speed: 10%')
    forward(10)
    sleep(5)
    
    print('Forward with speed: 40%')
    forward(40)
    sleep(5)
    
    stop()

except KeyboardInterrupt:
    print('Keyboard Interrupt')
    stop()

from machine import Pin, PWM
import time

#Pins 15 & 16

pwm = PWM(Pin(15, mode=Pin.OUT))

pwm.freq(50)

def close_tube():
    #center position
    pwm.duty_u16(3100)
    #pwm.duty_u16(3276)

def open_tube():
    #90 degree angle
    pwm.duty_u16(6553)


open_tube()

time.sleep(5)

close_tube()

# Testing servo motors at different PWM signals and positions
'''while True:
    #time.sleep_ms(900)

    #center position
    #pwm.duty_u16(3276)
    #time.sleep_ms(900)

    #45 degree angle
    pwm.duty_u16(4916)
    time.sleep_ms(5000)

    #90 degree angle
    pwm.duty_u16(6553)
    time.sleep_ms(5000)

    #back to center position
    pwm.duty_u16(3276)
    time.sleep_ms(5000)

    #almost 180 degree turn
    pwm.duty_u16(9835)
    time.sleep_ms(900)

    #45 degree turn in reverse
    #doesn't work properly tho
    pwm.duty_u16(1836)
    time.sleep_ms(900)'''
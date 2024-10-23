from machine import Pin, PWM
import time

pwm = PWM(Pin(15, mode=Pin.OUT))

pwm.freq(50)

while True:
    time.sleep_ms(900)

    #center position
    pwm.duty_u16(3276)
    time.sleep_ms(900)

    #45 degree angle
    pwm.duty_u16(4916)
    time.sleep_ms(900)

    #90 degree angle
    pwm.duty_u16(6553)
    time.sleep_ms(900)

    #back to center position
    pwm.duty_u16(3276)
    time.sleep_ms(900)

    #almost 180 degree turn
    pwm.duty_u16(9835)
    time.sleep_ms(900)

    #45 degree turn in reverse
    #doesn't work properly tho
    pwm.duty_u16(1836)
    time.sleep_ms(900)
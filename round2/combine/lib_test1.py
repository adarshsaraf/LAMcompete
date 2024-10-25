import machine
from machine import enable_irq, disable_irq, idle, PWM, I2C, Pin
import time

# SETUP ALL PINS
# -----------------------------------------------------------------
# for load cell:
clock = Pin(18, Pin.OUT)
data = Pin(19, Pin.IN)

# for pinch valves
pwmRED = PWM(Pin(15, mode=Pin.OUT))
pwmBLUE = PWM(Pin(16, mode=Pin.OUT))

# for stepper motor - linear actuator
IN1 = machine.Pin(28, machine.Pin.OUT)
IN2 = machine.Pin(27, machine.Pin.OUT)
IN3 = machine.Pin(26, machine.Pin.OUT)
IN4 = machine.Pin(22, machine.Pin.OUT)

# for OLED screen
i2c = I2C(0, scl=Pin(5), sda=Pin(4))  # I2C Default frequency of 400,000 Hz

# for peristaltic pump

# Define the frequency for PWM
frequency = 1000

pin1 = Pin(3, Pin.OUT)
pin2 = Pin(1, Pin.OUT)
enable = PWM(Pin(2), frequency)

# -----------------------------------------------------------------
#                      CODE FOR LOAD CELL
# -----------------------------------------------------------------

# HX711 configuration parameters
GAIN = 1  # Gain set to 128
OFFSET = 0
SCALE = 1  # This will be set after calibration

time_constant = 0.25
filtered_value = 0

def set_gain(gain):
    global GAIN
    if gain == 128:
        GAIN = 1
    elif gain == 64:
        GAIN = 3
    elif gain == 32:
        GAIN = 2
    read()  # Perform a read to set gain and stabilize the sensor

def conversion_done_cb(data):
    global conversion_done
    conversion_done = True
    data.irq(handler=None)

def read():
    global conversion_done
    conversion_done = False
    data.irq(trigger=Pin.IRQ_FALLING, handler=conversion_done_cb)
    
    # Wait for the sensor to be ready
    for _ in range(500):
        if conversion_done:
            break
        time.sleep_ms(1)
    else:
        data.irq(handler=None)
        raise OSError("Sensor does not respond")
    
    # Shift in data and gain/channel info
    result = 0
    for j in range(24 + GAIN):
        state = disable_irq()
        clock.value(True)
        clock.value(False)
        enable_irq(state)
        result = (result << 1) | data()
    
    # Shift back extra bits
    result >>= GAIN
    
    # Check for negative value
    if result > 0x7fffff:
        result -= 0x1000000
    
    return result

def read_average(times=3):
    total = 0
    for i in range(times):
        total += read()
    return total / times

def read_lowpass():
    global filtered_value
    filtered_value += time_constant * (read() - filtered_value)
    return filtered_value

def get_value():
    return read_lowpass() - OFFSET

def get_units():
    return get_value() / SCALE

def tare(times=15):
    global OFFSET
    OFFSET = read_average(times)

def set_scale(scale):
    global SCALE
    SCALE = scale

def set_offset(offset):
    global OFFSET
    OFFSET = offset

def set_time_constant(tc=None):
    global time_constant
    if tc is None:
        return time_constant
    elif 0 < tc < 1.0:
        time_constant = tc

def power_down():
    clock.value(False)
    clock.value(True)

def power_up():
    clock.value(False)


# -----------------------------------------------------------------
#                 CODE FOR THE PINCH-VALVE SERVOS
# -----------------------------------------------------------------

pwmRED.freq(50)
pwmBLUE.freq(50)

def close_tube(pwm):
    #center position
    pwm.duty_u16(3276)

def open_tube(pwm):
    #90 degree angle
    pwm.duty_u16(6553)

# -----------------------------------------------------------------
#                 CODE FOR STEPPER FOR MOVING SPOUT
# -----------------------------------------------------------------
# We have used 28BYJ-48 stepper motor

# Since we are only using full rotation, only full step sequence is written
full_step_sequence = [
    [1, 1, 0, 0],  # Step 1
    [0, 1, 1, 0],  # Step 2
    [0, 0, 1, 1],  # Step 3
    [1, 0, 0, 1],  # Step 4
]

# Number of steps for full (360 degrees) rotation
steps_per_revolution = 2048

# Function to set the step on the stepper motor
def set_step(p1, p2, p3, p4):
    IN1.value(p1)
    IN2.value(p2)
    IN3.value(p3)
    IN4.value(p4)

# Rotate stepper motor forward
def rotate_stepper_360(revolutions, delay_ms = 5):
    for step in range(revolutions * steps_per_revolution):
        # Calculate which step in the sequence to send
        current_step = step % len(full_step_sequence)
        
        # Apply the current step to the motor
        set_step(*full_step_sequence[current_step])
        
        # Delay between steps
        time.sleep_ms(delay_ms)
    set_step(0,0,0,0)

# Rotate stepper motor in reverse
def rotate_stepper_reverse(revolutions , delay_ms = 5):
    for step in range(revolutions * steps_per_revolution):
        # Calculate which step in the sequence to send
        current_step = step % len(full_step_sequence)
        
        # Apply the current step to the motor
        set_step(*full_step_sequence[-current_step - 1])
        
        # Delay between steps
        time.sleep_ms(delay_ms)
    set_step(0,0,0,0)

# -----------------------------------------------------------------
#                   CODE FOR I2C OLED SCREEN
# -----------------------------------------------------------------

# Macros
SET_CONTRAST        = const(0x81)
SET_ENTIRE_ON       = const(0xa4)
SET_NORM_INV        = const(0xa6)
SET_DISP            = const(0xae)
SET_MEM_ADDR        = const(0x20)
SET_COL_ADDR        = const(0x21)
SET_PAGE_ADDR       = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP       = const(0xa0)
SET_MUX_RATIO       = const(0xa8)
SET_COM_OUT_DIR     = const(0xc0)
SET_DISP_OFFSET     = const(0xd3)
SET_COM_PIN_CFG     = const(0xda)
SET_DISP_CLK_DIV    = const(0xd5)
SET_PRECHARGE       = const(0xd9)
SET_VCOM_DESEL      = const(0xdb)
SET_CHARGE_PUMP     = const(0x8d)

# OLED dimensions
WIDTH = 128
HEIGHT = 64
ADDR = 0x3c  # I2C address for SSD1306

# Buffer for display, here 1 byte represents every 8 vertical pixels
buffer = bytearray((HEIGHT // 8) * WIDTH)

# Function to send command to OLED
def write_cmd(cmd):
    temp = bytearray([0x80, cmd]) 
    i2c.writeto(ADDR, temp)

# Function to send data to OLED
def write_data(data):
    temp = bytearray([0x40, data]) 
    i2c.writeto(ADDR, temp)

# Function to initialize the OLED
def init_display():
    cmds = [
        SET_DISP | 0x00,  # Display off
        SET_MEM_ADDR, 0x00,  # Horizontal addressing mode
        SET_DISP_START_LINE | 0x00,
        SET_SEG_REMAP | 0x01,  # Column address 127 mapped to SEG0
        SET_MUX_RATIO, HEIGHT - 1,
        SET_COM_OUT_DIR | 0x08,  # Scan from COM[N] to COM0
        SET_DISP_OFFSET, 0x00,
        SET_COM_PIN_CFG, 0x12,
        SET_DISP_CLK_DIV, 0x80,
        SET_PRECHARGE, 0xf1,
        SET_VCOM_DESEL, 0x30,  # 0.83*Vcc
        SET_CONTRAST, 0xff,  # Maximum contrast
        SET_ENTIRE_ON,  # Output follows RAM contents
        SET_NORM_INV,  # Not inverted
        SET_CHARGE_PUMP, 0x14,  # Enable charge pump
        SET_DISP | 0x01  # Display on
    ]
    for cmd in cmds:
        write_cmd(cmd)

# Function to clear the display buffer
def clear_display():
    for i in range(len(buffer)):
        buffer[i] = 0x00

# Function to set a pixel in the buffer
def set_pixel(x, y, color):
    if y >= HEIGHT or x < 0 or y < 0:
        return
    if x >= WIDTH:
        #x += 8
        y += 8
    page = y // 8
    bit = y % 8
    index = page * WIDTH + x
    if color:
        buffer[index] |= (1 << bit)
    else:
        buffer[index] &= ~(1 << bit)

# Function to draw a character (simplified 5x8 font)
def draw_char(x, y, char):
    font = {
    'A': [0x7C, 0x12, 0x12, 0x12, 0x7C],
    'B': [0x7E, 0x4A, 0x4A, 0x4A, 0x34],
    'C': [0x3C, 0x42, 0x42, 0x42, 0x24],
    'D': [0x7E, 0x42, 0x42, 0x42, 0x3C],
    'E': [0x7E, 0x4A, 0x4A, 0x42, 0x42],
    'F': [0x7E, 0x0A, 0x0A, 0x0A, 0x02],
    'G': [0x3C, 0x42, 0x4A, 0x4A, 0x38],
    'H': [0x7E, 0x08, 0x08, 0x08, 0x7E],
    'I': [0x00, 0x42, 0x7E, 0x42, 0x00],
    'J': [0x20, 0x40, 0x40, 0x3E, 0x00],
    'K': [0x7E, 0x08, 0x14, 0x22, 0x40],
    'L': [0x7E, 0x40, 0x40, 0x40, 0x00],
    'M': [0x7E, 0x02, 0x0C, 0x02, 0x7E],
    'N': [0x7E, 0x04, 0x08, 0x10, 0x7E],
    'O': [0x3C, 0x42, 0x42, 0x42, 0x3C],
    'P': [0x7E, 0x0A, 0x0A, 0x0A, 0x04],
    'Q': [0x3C, 0x42, 0x52, 0x22, 0x5C],
    'R': [0x7E, 0x0A, 0x1A, 0x2A, 0x44],
    'S': [0x24, 0x4A, 0x4A, 0x4A, 0x30],
    'T': [0x02, 0x02, 0x7E, 0x02, 0x02],
    'U': [0x3E, 0x40, 0x40, 0x40, 0x3E],
    'V': [0x1E, 0x20, 0x40, 0x20, 0x1E],
    'W': [0x7E, 0x20, 0x10, 0x20, 0x7E],
    'X': [0x42, 0x24, 0x18, 0x24, 0x42],
    'Y': [0x06, 0x08, 0x70, 0x08, 0x06],
    'Z': [0x42, 0x62, 0x52, 0x4A, 0x46],

    '0': [0x3C, 0x42, 0x42, 0x42, 0x3C],
    '1': [0x00, 0x44, 0x7E, 0x40, 0x00],
    '2': [0x64, 0x52, 0x52, 0x52, 0x4C],
    '3': [0x24, 0x42, 0x4A, 0x4A, 0x34],
    '4': [0x18, 0x14, 0x12, 0x7E, 0x10],
    '5': [0x2E, 0x4A, 0x4A, 0x4A, 0x32],
    '6': [0x3C, 0x4A, 0x4A, 0x4A, 0x30],
    '7': [0x02, 0x02, 0x72, 0x0A, 0x06],
    '8': [0x34, 0x4A, 0x4A, 0x4A, 0x34],
    '9': [0x0C, 0x52, 0x52, 0x52, 0x3C],

    ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
    '.': [0x00, 0x60, 0x60, 0x00, 0x00],
    '!': [0x00, 0x7A, 0x00, 0x00, 0x00],
    '?': [0x04, 0x02, 0x52, 0x0A, 0x04],
    '-': [0x08, 0x08, 0x08, 0x08, 0x08],
    '_': [0x40, 0x40, 0x40, 0x40, 0x40],

    'g': [0x4C, 0x52, 0x52, 0x52, 0x3E],
    'm': [0x7C, 0x04, 0x18, 0x04, 0x78],

    ':': [0x00, 0x00, 0x12, 0x12, 0x00],
    }

    if char in font:
        data = font[char]
        for i in range(5):
            byte = data[i]
            for j in range(8):
                set_pixel(x + i, y + j, (byte >> j) & 1)

# Function to write "Hello World" on the display
def write_on_disp(text):
    #text = "WASHING MACHINE BROS. 2.0                                        WEIGHT:  5.0 gm "
    x_offset = 0
    for c in text:
        draw_char(x_offset, 0, c)
        x_offset += 6  # Move to next character position

# Function to display the buffer on the OLED
def show():
    write_cmd(SET_COL_ADDR)
    write_cmd(0)
    write_cmd(WIDTH - 1)
    write_cmd(SET_PAGE_ADDR)
    write_cmd(0)
    write_cmd((HEIGHT // 8) - 1)
    for i in range(len(buffer)):
        write_data(buffer[i])

# -----------------------------------------------------------------
#                    CODE FOR PERISTALTIC PUMP
# -----------------------------------------------------------------

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
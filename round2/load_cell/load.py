from machine import enable_irq, disable_irq, idle, Pin
import time

# Setup pins
clock = Pin(18, Pin.OUT)
data = Pin(19, Pin.IN)

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

# Main execution
set_gain(128)  # Set the gain to 128
tare()         # Tare the scale to set the current offset

# Assuming the load cell has a maximum capacity of 1 kg
# Measure raw values with a known weight (calibration process)
known_weight = 1.0  # 1 kg load cell
raw_no_load = read_average(10)  # Average value with no load
print("Raw value with no load: ", raw_no_load)

# Now place a known 1 kg load on the load cell
print("put load now:")
time.sleep(5)  # Time to place the weight
raw_with_load = read_average(10)  # Average value with 1 kg load
print("Raw value with 1 kg load: ", raw_with_load)

# Calculate the scale factor for a 1 kg load cell
scale_factor = (raw_with_load - raw_no_load) / known_weight
print("Calculated scale factor: ", scale_factor)

set_scale(scale_factor)  # Set the calculated scale factor

# Now continuously read weight values in kg
while True:
    print(scale_factor)
    weight = get_units()
    print("Weight: {:.2f} kg".format(weight))
    time.sleep(1)

from lib_test1 import *

total_weight = 0

# Initialize display and clear it
init_display()
clear_display()

# CODE TO CALIBRATE THE LOAD CELL [ONLY ONE TIME]
set_gain(128)  # Set the gain to 128 which gives highest precision
tare()         # Tare the scale to set the current offset

# Assuming the load cell has a maximum capacity of 1 kg
# Measure raw values with a known weight (calibration process)
known_weight = 0.5  # 500 gm load cell
raw_no_load = read_average(10)  # Average value with no load
print("Raw value with no load: ", raw_no_load)

# Now place a known reference load on the load cell
print("put load now:")
time.sleep(5)  # Time to place the weight
raw_with_load = read_average(10)  # Average value with reference load
print("Raw value with 1 kg load: ", raw_with_load)

# Calculate the scale factor for a 1 kg load cell
scale_factor = (raw_with_load - raw_no_load) / known_weight
print("Calculated scale factor: ", scale_factor)

set_scale(scale_factor)  # Set the calculated scale factor

weight = get_units()

# START FOR LOOP HERE FOR 5 CYCLES
open_tube(pwmRED)

while (weight < 5):
    forward(60)
    write_on_disp("WASHING MACHINE BROS. 2.0                                        WEIGHT: {:.2f} mg ".format(weight))
    show()

backwards(60)
time.sleep(3)
stop()

close_tube(pwmRED)
open_tube(pwmBLUE)

total_weight += weight

tare()
weight = get_units()

# STEPPER WILL ROTATE HERE to BLUE cup
# we rotate the stepper one direction to move from blue to red cup, as we dont know the number of rotations
# I'm assuming one rotation = 360degree
revolutions = 1
delay_ms = 5

rotate_stepper_360(revolutions, delay_ms)

#---------------------

while (weight < 10):
    forward(60)
    write_on_disp("WASHING MACHINE BROS. 2.0                                        WEIGHT: {:.2f} mg ".format(weight))
    show()

backwards(60)
time.sleep(3)
stop()

# STEPPER WILL ROTATE HERE to RED cup
# we will do the same as we did before but change the direction for which we call rotate_stepper_reverse function

rotate_stepper_reverse(revolutions, delay_ms)

#---------------------

total_weight += weight

tare()
weight = get_units()

close_tube(pwmBLUE)

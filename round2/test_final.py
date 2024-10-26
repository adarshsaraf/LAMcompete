from lib_test1 import *

total_weight = 0

# Initialize display and clear it
init_display()
clear_display()

# CODE TO CALIBRATE THE LOAD CELL [ONLY ONE TIME]
c = tare()         # Tare the scale to set the current offset

weights = []  # list to store weights

for _ in range(10):  # measure weight 10 times
    raw_wt = read() * 0.001
    weights.append(raw_wt)
    time.sleep(0.001)  # small delay between measurements

weight = ((sum(weights) / len(weights)) - c) * (-0.517)  # calculate average
print(f"Average Weight: {weight:.2f} grams", end="    \r")

# START FOR LOOP HERE FOR 5 CYCLES
open_tube(pwmRED)

while (weight < 5):
    backwards(100)
    for _ in range(10):  # measure weight 10 times
        raw_wt = read() * 0.001
        weights.append(raw_wt)
        time.sleep(0.001)  # small delay between measurements
    
    weight = ((sum(weights) / len(weights)) - c) * (-0.517)  # calculate average

    write_on_disp("WASHING MACHINE BROS. 2.0                                        WEIGHT: {:.2f} mg ".format(weight))
    show()

forward(100)
time.sleep(3)
stop()

close_tube(pwmRED)
open_tube(pwmBLUE)

total_weight += weight

time.sleep(4)

c = tare()

weights = []  # list to store weights

for _ in range(10):  # measure weight 10 times
    raw_wt = read() * 0.001
    weights.append(raw_wt)
    time.sleep(0.001)  # small delay between measurements

weight = ((sum(weights) / len(weights)) - c) * (-0.517)  # calculate average
print(f"Average Weight: {weight:.2f} grams", end="    \r")
write_on_disp("WASHING MACHINE BROS. 2.0                                   TARE   WEIGHT: {:.2f} mg ".format(weight))

# STEPPER WILL ROTATE HERE to BLUE cup
# we rotate the stepper one direction to move from blue to red cup, as we dont know the number of rotations
# I'm assuming one rotation = 360degree
revolutions = 5
delay_ms = 5

rotate_stepper_360(revolutions, delay_ms)

#---------------------

while (weight < 10):
    forward(100)

    for _ in range(10):  # measure weight 10 times
        raw_wt = read() * 0.001
        weights.append(raw_wt)
        time.sleep(0.001)  # small delay between measurements
    
    weight = ((sum(weights) / len(weights)) - c) * (-0.517)  # calculate average

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

c = tare()

weights = []  # list to store weights

for _ in range(10):  # measure weight 10 times
    raw_wt = read() * 0.001
    weights.append(raw_wt)
    time.sleep(0.001)  # small delay between measurements

weight = ((sum(weights) / len(weights)) - c) * (-0.517)  # calculate average
print(f"Average Weight: {weight:.2f} grams", end="    \r")

close_tube(pwmBLUE)

# backwards will suck into the weighing machine..

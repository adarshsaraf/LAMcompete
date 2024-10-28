from lib_total1 import *

total_weight = 0

# Initialize display and clear it
init_display()
clear_display()

# INITITIALIZE PINCH VALVES
close_tube(pwmRED)
close_tube(pwmBLUE)

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
for _ in range (5):
    
    open_tube(pwmRED)

    backwards(100)
    time.sleep(3)

    while (weight < 4.8):
        backwards(35)
        for _ in range(10):  # measure weight 10 times
            raw_wt = read() * 0.001
            weights.append(raw_wt)
            time.sleep(0.001)  # small delay between measurements
        
        weight = ((sum(weights) / len(weights)) - c) * (-0.517)  # calculate average

        write_on_disp("WASHING MACHINE BROS. 2.0                                        WEIGHT: {:.1f} mg     TOTAL WEIGHT: {:.1f} mg".format(weight, total_weight))
        show()

    forward(100)
    time.sleep(14)
    forward(20)
    time.sleep(2)
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
    write_on_disp("WASHING MACHINE BROS. 2.0                                        WEIGHT: {:.1f} mg     TOTAL WEIGHT: {:.1f} mg".format(weight, total_weight))

    # STEPPER WILL ROTATE HERE to BLUE cup
    # we rotate the stepper one direction to move from blue to red cup, as we dont know the number of rotations
    # I'm assuming one rotation = 360degree
    revolutions = 4
    delay_ms = 5

    rotate_stepper_360(revolutions, delay_ms)

    #---------------------

    backwards(100)
    time.sleep(3)
    while (weight < 9.7):
        backwards(35)
        for _ in range(10):  # measure weight 10 times
            raw_wt = read() * 0.001
            weights.append(raw_wt)
            time.sleep(0.001)  # small delay between measurements
        
        weight = ((sum(weights) / len(weights)) - c) * (-0.517)  # calculate average

        write_on_disp("WASHING MACHINE BROS. 2.0                                        WEIGHT: {:.1f} mg     TOTAL WEIGHT: {:.1f} mg".format(weight, total_weight))
        show()

    forward(100)
    time.sleep(14)
    forward(60)
    time.sleep(2)
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
    write_on_disp("WASHING MACHINE BROS. 2.0                                        WEIGHT: {:.1f} mg     TOTAL WEIGHT: {:.1f} mg".format(weight, total_weight))
    close_tube(pwmBLUE)



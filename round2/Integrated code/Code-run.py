# Importing custom library
from Code_Lib import *

# Declaring variable to store total weight of liquids
total_weight = 0

# Initialize display and clear it
init_display()
clear_display()

# Initializing Pinch Valves to closed position
close_tube(pwmRED)
close_tube(pwmBLUE)

# CODE TO CALIBRATE THE LOAD CELL
c = tare()         # Tare the scale to set the current offset

weights = []  # list to store weights

for _ in range(10):  # measure weight 10 times
    raw_wt = read() * 0.001
    weights.append(raw_wt)
    time.sleep_ms(1)  # delay between measurements

# finding average weight
weight = ((sum(weights) / len(weights)) - c) * (-0.517)     # scaling factor and constant found by comparing a known weight
print(f"Average Weight: {weight:.2f} grams", end="    \r")  # printing average weight on terminal for reference

# START executing task for 5 cycles
for _ in range (5):
    
    open_tube(pwmRED)

    # Run at full speed to give initial speed
    backwards(100)
    time.sleep(2)

    while (weight < 4.8):  # Giving value as 4.8 instead of 5 to avoid overshoot

        weights = [] 

        backwards(50)
        
        for _ in range(10):  # measure weight 10 times
            raw_wt = read() * 0.001
            weights.append(raw_wt)
            time.sleep(0.001)  # small delay between measurements
        
        weight = ((sum(weights) / len(weights)) - c) * (-0.517)  # calculate average

        write_on_disp("WASHING MACHINE BROS. 2.0                                        WEIGHT: {:.1f} gm     TOTAL WEIGHT: {:.1f} gm".format(weight, total_weight))
        show()

    # Running peristaltic pump in reverse at different speeds to avoid cross-contamination
    forward(100)
    time.sleep(25)
    forward(40)
    time.sleep(10)
    forward(100)
    time.sleep(25)
    stop()

    # Change pinch valve configuration for the Blue cup 
    close_tube(pwmRED)
    open_tube(pwmBLUE)

    # Updating total weight 
    total_weight += weight

    # Tare the scale to set the current offset
    c = tare()

    weights = []  # list to store weights

    for _ in range(10):  # measure weight 10 times
        raw_wt = read() * 0.001
        weights.append(raw_wt)
        time.sleep_ms(1)  # small delay between measurements

    weight = ((sum(weights) / len(weights)) - c) * (-0.517)  # calculate average
    print(f"Average Weight: {weight:.2f} grams", end="    \r")  # for reference on terminal
    write_on_disp("WASHING MACHINE BROS. 2.0                                        WEIGHT: {:.1f} gm     TOTAL WEIGHT: {:.1f} gm".format(weight, total_weight))

    # STEPPER will MOVE to BLUE cup
    # Here, one revolution = 360 degrees
    revolutions = 4
    delay_ms = 2

    rotate_stepper_360(revolutions, delay_ms)

    # Run at full speed to give initial speed
    backwards(100)
    time.sleep(3)

    while (weight < 9.8):
        weights = []  # list to store weights

        backwards(50)
        for _ in range(10):  # measure weight 10 times
            raw_wt = read() * 0.001
            weights.append(raw_wt)
            time.sleep_ms(1)  # small delay between measurements
        
        weight = ((sum(weights) / len(weights)) - c) * (-0.517)  # calculate average

        write_on_disp("WASHING MACHINE BROS. 2.0                                        WEIGHT: {:.1f} gm     TOTAL WEIGHT: {:.1f} gm".format(weight, total_weight))
        show()

    # Running peristaltic pump in reverse at different speeds to avoid cross-contamination
    forward(100)
    time.sleep(25)
    forward(40)
    time.sleep(10)
    forward(100)
    time.sleep(25)
    stop()


    close_tube(pwmBLUE)

    # STEPPER will MOVE to RED cup
    # we will do the same as we did before but change the direction for which we call rotate_stepper_reverse function
    rotate_stepper_reverse(revolutions, delay_ms)

    # Updating total weight
    total_weight += weight
    
    # Tare the scale to set the current offset
    c = tare()
    
    weights = []  # list to store weights

    for _ in range(10):  # measure weight 10 times
        raw_wt = read() * 0.001
        weights.append(raw_wt)
        time.sleep_ms(1)  # small delay between measurements

    weight = ((sum(weights) / len(weights)) - c) * (-0.517)  # calculate average
    print(f"Average Weight: {weight:.2f} grams", end="    \r")
    write_on_disp("WASHING MACHINE BROS. 2.0                                        WEIGHT: {:.1f} gm     TOTAL WEIGHT: {:.1f} gm".format(weight, total_weight))
    show()
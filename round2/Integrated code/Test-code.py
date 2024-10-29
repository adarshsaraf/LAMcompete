from Code_Lib import *

# ----------------------------------------------------------------------
#               CODE TO TEST WITHOUT MOVING STEPPER
# ----------------------------------------------------------------------

'''total_weight = 0

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

open_tube(pwmRED)

backwards(100)
time.sleep(3)

while (weight < 4.8):
        backwards(60)
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
'''

open_tube(pwmBLUE)
close_tube(pwmRED)
forward(100)
time.sleep(8)
stop()
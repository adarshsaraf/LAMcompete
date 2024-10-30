import machine
import time

# Define the GPIO pins connected to the stepper motor
pin1 = machine.Pin(28, machine.Pin.OUT)
pin2 = machine.Pin(27, machine.Pin.OUT)
pin3 = machine.Pin(26, machine.Pin.OUT)
pin4 = machine.Pin(22, machine.Pin.OUT)

# Full-step sequence (for a 28BYJ-48 stepper motor)
full_step_sequence = [
    [1, 1, 0, 0],  # Step 1
    [0, 1, 1, 0],  # Step 2
    [0, 0, 1, 1],  # Step 3
    [1, 0, 0, 1],  # Step 4
]

# Number of steps for 360-degree rotation (2048 for 28BYJ-48 stepper motor in full-step mode)
steps_per_revolution = 2048

# Function to set the step on the stepper motor
def set_step(p1, p2, p3, p4):
    pin1.value(p1)
    pin2.value(p2)
    pin3.value(p3)
    pin4.value(p4)

# Rotate stepper motor 360 degrees clockwise
def rotate_stepper_360(steps_per_revolution, delay_ms):
    for step in range(steps_per_revolution):
        # Calculate which step in the sequence to send
        current_step = step % len(full_step_sequence)
        
        # Apply the current step to the motor
        set_step(*full_step_sequence[current_step])
        
        # Delay between steps
        time.sleep_ms(delay_ms)

# Rotate stepper motor 360 degrees counterclockwise
def rotate_stepper_reverse(steps_per_revolution, delay_ms):
    for step in range(steps_per_revolution):
        # Calculate which step in the reversed sequence to send
        current_step = step % len(full_step_sequence)
        
        # Apply the current step to the motor in reverse order
        set_step(*full_step_sequence[::-1][current_step])
        
        # Delay between steps
        time.sleep_ms(delay_ms)

# Set delay between steps (controls speed)
delay_ms = 2

# Rotate the motor in clockwise & counter-clockwise direction

#rotate_stepper_360(4*steps_per_revolution, delay_ms)
#print("Stepper rotated anti-clockwise")
#time.sleep(2)
rotate_stepper_reverse(4*steps_per_revolution, delay_ms)
print("Stepper rotated clockwise")

# Turn off all pins after rotation
set_step(0, 0, 0, 0)

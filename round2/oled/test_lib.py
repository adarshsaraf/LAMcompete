import i2c_oled

# Initialize display and clear it
i2c_oled.init_display()
i2c_oled.clear_display()

# Write "Hello World" and show it
i2c_oled.write_on_disp("WASHING MACHINE BROS. 2.0                                        WEIGHT:  5.0 gm                              ಠ_ಠ")
i2c_oled.show()
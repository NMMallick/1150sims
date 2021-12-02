# Simulation for a 2 car system in the event of a 
#   probable rear-end collision

# Car A - speeding vehicle on trajectory to collision
# Car B - vehicle infront of speeding car B

import math 

# 0.8g's (7.84532 m/s^2) is the limit to effective braking of a given vehicle
acc_limit = 7.84532


# Car A variables
vA_init = float(input("Velocity for Car A [ Car A -> Car B ] : (mph) "))/2.237

# Car B variables
vB_init = float(input("Velocity for Car B [ Car A -> Car B ] : (mph) "))/2.237



print("Car A initial velocity: (m/s)", vA_init)
print("Car B initial velocity: (m/s)", vB_init)

vel = vA_init - vB_init

# Limit for successfull braking
xAB = 2 - ((vel**2)/(2*(-acc_limit)))
#  - (vB_init*(vA_init/acc_limit))

print("Minimum distance before braking: (meters) ", xAB)
print("Minimum distance before braking: (feet) ", xAB*3.281)


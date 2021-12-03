# Simulation for a 2 car system in the event of a 
#   probable rear-end collision

# solve for minimum time to avoid collision, take throughput data from system.py, 
# add to time to avoid collision, output new minimum distance to avoid collision

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

#calculate minimum time required to avoid accident given braking distance
d = (vel**2) + (2*acc_limit*xAB)
sol1 = (-vel + math.sqrt(abs(d)))/(acc_limit)
sol2 = (-vel - math.sqrt(abs(d)))/(acc_limit)

if sol1 < 0:
    time = sol2

elif sol2 < 0:
    time = sol1

# take total delay data from system.py and calculate new minimum braking distance to avoid accident
delay = 0.002 # placeholder value for delay
newTime = time + delay
xAB2 = vel*newTime + (acc_limit/2)*(newTime**2)

print("Minimum time required to avoid accident: (s) ", time)
print("Minimum distance before braking with total delay: (meters) ", xAB2)
print("Minimum distance before braking with total delay: (feet) ", xAB2*3.281)


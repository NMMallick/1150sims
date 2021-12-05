# Simulation for a 2 car system in the event of a 
#   probable rear-end collision

# solve for minimum time to avoid collision, take throughput data from system.py, 
# add to time to avoid collision, output new minimum distance to avoid collision

# Car A - speeding vehicle on trajectory to collision
# Car B - vehicle infront of speeding car B

import math
import matplotlib.pyplot as plt
from system import sim

# 0.8g's (7.84532 m/s^2) is the limit to effective braking of a given vehicle
acc_limit = 7.84532


# Car A variables
vA_init = float(input("Velocity for Car B [ Car B -> Car A ] : (mph) "))/2.237

# Car B variables
vB_init = float(input("Velocity for Car A [ Car B -> Car A ] : (mph) "))/2.237



print("Car A initial velocity: (m/s)", vA_init)
print("Car B initial velocity: (m/s)", vB_init)

vel = vA_init - vB_init

# Limit for successfull braking
xAB = 2 - ((vel**2)/(2*(-acc_limit)))

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
# n = number of batches
# m = number slots 
prob, delay = sim()

xAB2 = [] # array to hold values for distances
x_time = [] #array to hold values for total delay values


for i in delay:
    newTime = time + i
    x_time.append(newTime)
    xAB2.append(vel*newTime + (acc_limit/2)*(newTime**2))
    #perChange = ((xAB2 - xAB)/xAB)*100


#print("Minimum time required to avoid accident: (s) ", time)
#print("Minimum distance before braking with total delay: (meters) ", xAB2)
#print("Minimum distance before braking with total delay: (feet) ", xAB2*3.281)
#print("Percent change of distance: ", perChange)

ref = [xAB]*len(xAB2)
plt.figure(figsize=(12,6))

plt.plot(prob, xAB2, 'g', label="Deceleration distance(m)")
plt.plot(prob, x_time, 'b', label="Transmission delay + decelleration time (s)" )
plt.plot(prob, delay, 'r', label="Transmission delays(s)")
plt.plot(prob, ref, 'm', label="Original braking distance(m)")
plt.xticks(rotation=45, fontsize=6)
plt.xlabel("Probability a node will transmit", labelpad=20)

plt.legend()
plt.title("Delta X = Change in Deceleration Distance vs Total Delay")

# Save and show the plot
plt.savefig('kinematics_plot.png')
plt.show()
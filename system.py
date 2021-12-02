from time import sleep
from node import Node
import matplotlib.pyplot as plt


# Variables for simulations
cars = []
slots = 1000

# Variables for plotting
x = []
y_success = []
y_collision = []


# Start of simulation
# The iterator f is used to test every tenth value of m { n = m*(f+1)/10) }
for f in range(10): 

    # Clear out list of vehicle nodes for each test ( wipe all global class data )
    if len(cars) != 0: 
        print("ERR! Not all vehicle nodes were cleared.")
        exit(-1)

    # Load new vehicle nodes 
    for i in range(10): 
        cars.append(Node(id=i))

    Node._n = ((f+1)/10)*Node._m
    
    for itr in range(1000):

        # Update slot for all nodes
        Node._slot = itr

        # Call Node.update() which updates each vehicle nodes backoff timer
        #   or tries to transmit a message.
        for i in cars: 
            i.update()

        # If the list Node._is_transmiting only has one node in it
        #   then we have a successful transmission, greater than 1 is a 
        #   collision and 0 is nobody is transmiting
        if len(Node._is_transmiting) > 1: # Collision 
            Node._num_collisions += 1 
            
            # Creates the list of backoff slots -- {0, 1, ... , 2^k - 1}
            backoff_slots = list(range(1, (2**len(Node._is_transmiting))))  
            
            # Each vehicle node that tried to transmit will pick a spot from the
            #   list of available back off slots
            for j in Node._is_transmiting:  
                cars[j].backoff(backoff_slots)  

        # Only one car is transmitting    
        elif len(Node._is_transmiting) == 1: 
            cars[Node._is_transmiting[0]].success() # Updates stats to increase total successful transmissions
            print("Node", Node._is_transmiting[0], "is successfully transmitting.")

        Node._is_transmiting.clear() # Clear the list for next slot

    ###################################################################################################
    #                       Prints data out from each iteration of n                                  #  
    ###################################################################################################
    # print()
    # for i in cars: 
    #     print("Node", i.id, "has", i.successful_xmissions, "transmissions.")

    # print("Total transmission time for each packet successful packet", Node._time_xmission)
    # print("Total number of collisions after", t_itr, ":", Node._num_collisions)
    # print("Total number of successful transmision: ", Node._num_successful_xmission)
    # print(Node._m)
    # print(Node._n)
    ## exit()
    ###################################################################################################
    
    # Appending data to lists so we can plot
    x.append(str(f+1) + "/10" + "m") # x-axis = (m*1/10, m*2/10, ..... ) 
    y_success.append(Node._num_successful_xmission) # y1-axis = number succesful transmissions 
    y_collision.append(Node._num_collisions)# y2-axis = number of collisions
    cars.clear()

# matplotlib plotting 
plt.plot(x, y_success, 'g', label="Number of Successful Transmissions")
plt.plot(x, y_collision, 'r',label="Number of Collisions")
plt.xticks()
plt.xlabel("Value of n")
plt.ylabel("Successful Transmissions")
plt.legend()
plt.title("m = liftime of useful data/transmission time")

# Show the plot
plt.show()




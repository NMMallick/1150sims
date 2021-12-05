import random 
from node import Node
import numpy as np
import matplotlib.pyplot as plt

def sim(VERBOSE=True, n=40, s=1000): 
    # Variables for simulations
    cars = []
    slots = s
    num_batches = n

    # Variables for plotting
    x = []
    y_success = []
    y_collision = []

    div = 1000
    lim = 0.85

    batch_success = [0]*int(div*lim)
    batch_collision = [0]*int(div*lim)
    total_cars = 0



    ############################ Start of simulation batch ############################
    for batch in range(num_batches):
        
        num_cars = random.randint(0,25)
        total_cars += num_cars

        if VERBOSE: 
            print("Processing simulation for batch", batch)
        
        # F -----> n  where  Pr(transmits) = n/m, 1-Pr(transmit) = 1-(n/m)
        # The iterator f is used to test every tenth value of m { n = m*(f+1)/10) }
        for f in range(int(div*lim)): 

            # Clear out list of vehicle nodes for each test ( wipe all global class data )
            if len(cars) != 0: 
                print("ERR! Not all vehicle nodes were cleared.")
                exit(-1)

            # Load new vehicle nodes 
            # Change range for number of vehicle nodes 
            for i in range(num_cars): 
                cars.append(Node(id=i))

            Node._n = ((f+1)/div)*Node._m
            
            # Change range to simulate number of total slots after a given time
            for itr in range(slots):

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
                    # print("Collision! ", Node._is_transmiting)
                    
                    # Creates the list of backoff slots -- {0, 1, ... , 2^k - 1}
                    backoff_slots = list(range(1, (2**len(Node._is_transmiting))))  
                    
                    # Each vehicle node that tried to transmit will pick a spot from the
                    #   list of available back off slots
                    for j in Node._is_transmiting:  
                        cars[j].backoff(backoff_slots)  

                # Only one car is transmitting    
                elif len(Node._is_transmiting) == 1: 
                    cars[Node._is_transmiting[0]].success() # Updates stats to increase total successful transmissions
                    # print("Node", Node._is_transmiting[0], "is successfully transmitting.")

                Node._is_transmiting.clear() # Clear the list for next slot

            ###################################################################################################
            #                       Prints data out from each iteration of f        
            #                   !!!!!           This gets HEAVY             !!!!!                             #  
            ###################################################################################################
            # print()
            # for i in cars: 
            #     print("Node", i.id, "has", i.successful_xmissions, "transmissions.")

            # print("Total transmission time for each packet successful packet", Node._time_xmission)
            # print("Total number of collisions after", itr, ":", Node._num_collisions)
            # print("Total number of successful transmision: ", Node._num_successful_xmission)
            # print(Node._m)
            # print(Node._n)
            # exit()
            ###################################################################################################
            
            # Appending data to lists so we can plot
            if batch == 0: 
                x.append(Node.getPr())
            
            y_success.append(Node._num_successful_xmission) # y1-axis = number succesful transmissions 
            y_collision.append(Node._num_collisions)# y2-axis = number of collisions   
            
            Node.clearData()
            cars.clear()

        
        batch_success = np.array(y_success) + np.array(batch_success)
        batch_collision = np.array(y_collision) + np.array(batch_collision)
        y_success.clear()
        y_collision.clear()


    avg_cars = total_cars/num_batches
    avg_success = [i / num_batches for i in batch_success]
    avg_collision = [i / num_batches for i in batch_collision]
    avg_succ_per_car = [i / avg_cars for i in avg_success]


    ################################### matplotlib plotting ###################################
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr = '\n'.join(("Tao={}".format(Node._tao),
                        "Packet Size={}Bytes".format(Node._packetsize),
                        "Average # cars={}".format(total_cars/num_batches)))


    plt.figure(figsize=(12,6))
    plt.plot(x, avg_success, 'g', label="Average Successful Transmissions")
    plt.plot(x, avg_collision, 'r',label="Average Collisions")
    plt.plot(x, avg_succ_per_car, 'b', label="Average Transmissions/Average Vehicle")
    plt.xticks(rotation=45, fontsize=6)
    plt.xlabel("Probability of Transmitting", labelpad=20)
    plt.ylabel("Successful Transmissions")
    plt.legend()
    plt.title("m = liftime of useful data/transmission time")
    plt.text(0.7, 60, textstr, bbox=props)

    # Save the plot
    plt.savefig('transmission_plot.png')

    # RETTURN DATA FOR KINEMATICS EQUATIONS
    
    # Assuming that useful data is 90% of packet size 
    pr_succ_xmission = [i / slots for i in avg_succ_per_car]
    throughput = [(i*0.9*Node._packetsize)/Node._transmission_time for i in pr_succ_xmission]
    avg_xmission_delay = [Node._packetsize/i for i in throughput]
    
    return (x, avg_xmission_delay)



# Main function
if __name__ == "__main__": 
    sim()

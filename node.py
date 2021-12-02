import random

class Node: 
    # 27 Mbps  
    _bitrate = 27*(10**6)
    
    # bytes
    _packetsize = 1399

    _transmission_time = (_packetsize*8)/_bitrate
    _tao = .1
    _tNodes = 0
    _slot = 0
    _num_collisions = 0
    _num_successful_xmission = 0
    _is_transmiting = []
    _time_xmission = _transmission_time
    _m = _tao/_transmission_time
    _n = (0.5)*_m

    def __init__(self, id, n=200.0, m=_m): 
        Node._tNodes += 1
        self.id = id
        self.successful_xmissions = 0
        self.attempted_xmissions = 0
        self.next_xmission = -1 # -1 = not transmitting 

    def attempt(self): 
        self.attempted_xmissions += 1
    
    def success(self): 
        Node._num_successful_xmission += 1
        self.successful_xmissions += 1

    def ptransmit(self): 
        list = [0,1]
        dist = [1-(Node._n/Node._m), Node._n/Node._m]
        return random.choices(list, dist)

    def backoff(self, set): 
        self.next_xmission = random.choice(set) + Node._slot
        self.attempt()
        print("Node", self.id, "is backing off til slot", self.next_xmission)
    
    def update(self):
        if self.next_xmission != -1: 
            if self.next_xmission == Node._slot: 
                Node._is_transmiting.append(self.id)
                self.next_xmission = -1
        else: 
            if self.ptransmit()[0] == 1: 
                Node._is_transmiting.append(self.id)

    def __del__(self): 
        Node._tNodes -= 1
        


        
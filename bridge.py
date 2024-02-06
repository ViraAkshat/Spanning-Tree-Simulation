class Lan(object):
    def __init__(self, key):
        self.key = key
        self.bridges = {}
        self.hosts = {}
        
        self.msgs = []
        self.db = None
        self.t = 0

    def add_bridge(self, bridge):               # Add Bridge IDs in Lan
        self.bridges[bridge.key] = bridge
        
    def add_host(self, host):                   # Add Hosts in Lan
        self.hosts[host] = self.key
        
    def send_msg(self):                         # Get Bridge IDs in Lan
        for msg in self.msgs:
            state = msg[0]
            sender = msg[1]
            for bridge in self.bridges:
                if(sender != bridge):
                    self.bridges[bridge].recieve_msg([state, self.key], self.t)
    
    def recieve_msg(self, msg, t):                  # Get Bridge IDs in Lan
        self.t = t
        self.msgs.append(msg)
    
    def transmit(self, sender, reciever, bridge_key):
        if bridge_key is None:
            for bridge in self.bridges:
                 if not (self.bridges[bridge].is_null(self.key)):
                    # print(sender," -->", bridge)
                    self.bridges[bridge].transmit(sender,reciever,self.key)
            return
            
        else:
            for bridge in self.bridges:
                if not (self.bridges[bridge].is_null(self.key) or bridge == bridge_key):
                    # print(sender," -->", bridge)
                    self.bridges[bridge].transmit(sender, reciever, self.key)
            return

        return
        
    def update(self):
        self.msgs.sort(key=order)
        
        if len(self.msgs) != 0:
            best_config = self.msgs[0]
            bridge_key = best_config[1]
            
            if self.db is not None:
                if (bridge_key[1] < self.db[1]):
                    self.db = bridge_key
            else:
                self.db = bridge_key
                
        self.msgs = []
        return self.db
        
    def get_connections(self):                  # Get Bridge IDs in Lan
        return self.bridges.keys()
    
    def get_hosts(self):                        # Get Host IDs in Lan
        return self.hosts.keys()


class Bridge(object):
    def __init__(self, key):
        self.key = key    
        self.root = key
        self.d = 0
        
        self.lans = {}
        self.state = [self.root, self.d, self.key]
        self.msgs = []
        
        self.trace = []
        self.change = False
        
        self.forward = {}

    def add_lan(self, lan):                     # Add Lan in Bridge
        self.lans[lan.key] = [lan,"DP"]

    def get_connections(self):                  # Get Lan IDs in Bridge
        return self.lans.keys()
    
    def port(self, lan_key):                    # Get Lan IDs in Bridge
        return [self.key, lan_key, self.lans[lan_key][1]]
    
    def status(self):                           # Get Bridge Status
        return self.state
    
    def send_msg(self, t):
        self.trace.append(str(t) + " s " + self.key + " (" +self.root+", " + str(self.d)+", " +self.key + ")")
        for lan in self.lans:
            self.lans[lan][0].recieve_msg([self.state, self.key], t)

    def recieve_msg(self, msg, t):                      # Receiver Bridge Status
        self.trace.append(str(t+1)+" r " +self.key+" (" + msg[0][0]+", " + str(msg[0][1])+", " + msg[0][2]+")")
        self.msgs.append(msg)
    
    def transmit(self, sender, reciever, lan_key):
        # print(self.forward)
        if reciever not in self.forward:
            self.forward[sender] = lan_key
            
            for lan in self.lans:
                if not (lan == lan_key or self.is_null(lan)):
                    # print(sender," -->", lan)
                    self.lans[lan][0].transmit(sender, reciever, self.key)
            return
        
        else:
            if sender not in self.forward:
                self.forward[sender] = lan_key
                
                lan = self.forward[reciever]
                
                if not (lan == lan_key):
                    # print(sender," -->", lan)
                    self.lans[lan][0].transmit(sender, reciever, self.key)
                
                return
            
            else:
                lan = self.forward[reciever]
                
                if not (lan == lan_key):
                    # print(sender," -->", lan)
                    self.lans[lan][0].transmit(sender, reciever, self.key)
                
                return
                
    def update(self):
        self.msgs.sort(key=order)
        
        if len(self.msgs) != 0:
            best_config = self.msgs[0]
            
            if(self.root > best_config[0][0]):
                self.root = best_config[0][0]
                self.d = int(best_config[0][1]) + 1

                lan_key = best_config[1]
                self.lans[lan_key][1] = 'RP'
                
                self.state = [self.root, self.d, self.key]
                self.change = True
                
            else:
                self.change = False
            
        self.msgs = []    
        return self.state
    
    def null_port(self):
        for lan in self.lans:
            if self.lans[lan][1] != 'RP':
                if self.lans[lan][0].db != self.key:
                    self.lans[lan][1] = 'NP'
    
    def is_null(self,lan_key):
        return self.lans[lan_key][1] == 'NP'
        
    def is_root(self):
        return self.root == self.key

def order(msg):
    return int(msg[0][0][1])**2 + int(msg[0][1])**2 + int(msg[0][2][1])**2

class Network(object):
    def __init__(self):
        self.bridges = {}   # Bridges in Network
        self.lans = {}      # Lans in Network
        self.hosts = {}
        self.update = True
        
    def add_bridge(self, bridge):                   # Add Bridge in Network
        self.bridges[bridge.key] = bridge
        
    def add_lan(self, lan):                         # Add Lan in Network
        self.lans[lan.key] = lan
        
    def add_host(self, host, lan):                  # Add Host in Network
        self.hosts[host] = lan
        self.lans[lan].hosts[host] = lan
        
    def add_port(self, lan_key, bridge_key):        # Add Port in resp Bridge and Lan
        if lan_key not in self.lans:
            self.add_lan(Lan(lan_key))
            
        if lan_key not in self.bridges[bridge_key].lans:
            self.bridges[bridge_key].add_lan(self.lans[lan_key])
            
        if bridge_key not in self.lans[lan_key].bridges:
            self.lans[lan_key].add_bridge(self.bridges[bridge_key])
    
    def transmit(self, sender, reciever):
        lan_key = self.hosts[sender]
        self.lans[lan_key].transmit(sender,reciever, None)
        
        return
        
    def get_bridges(self):                          # Get Bridges IDs in Network
        return self.bridges.keys()
    
    def get_lans(self):                             # Get Lans IDs in Network
        return self.lans.keys()
    
    def change(self):
        for bridge in self.bridges:
            if self.bridges[bridge].change == True:
                self.update = True
                break
                
        return self.update
    
    def __iter__(self):
        return iter(self.bridges.values())
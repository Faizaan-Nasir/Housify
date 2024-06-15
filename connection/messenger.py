import pickle

class Messenger : 

    HEADER_LENGTH = 10

    def __init__(self, _type, dest = "") :
        self.msg = []
        self.dest = dest
        self.type = _type

    def send(self, msg) : 
        self.msg.append(msg)

    def release(self) :
        if len(self.msg) == 0 : 
            return
        msg = self.msg.pop(0)
        msg = pickle.dumps(msg)
        header = f"{len(msg):<{self.HEADER_LENGTH}}"
        final = bytes(header, "utf-8") + msg
        return final
    

class MessengerGroup :

    def __init__(self) : 
        self.messengers = {}
    
    def add(self, m) : 
        self.messengers[m.dest] = m
    
    def remove(self, addr) : 
        del self.messengers[addr]

    def broadcast(self, msg) : 
        for m in self.messengers : 
            m.send(msg)

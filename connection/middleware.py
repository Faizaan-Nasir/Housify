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
        return msg

class Triggers : 

    def __init__(self) : 
        pass
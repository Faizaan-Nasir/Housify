
class Messenger : 

    def __init__(self, _type) : 
        self.msg = []
        self.dest = ""
        self.type = _type

    def send(self, msg) : 
        self.msg.append(msg)

    def release(self) :
        if len(self.msg) == 0 : 
            return
        msg = self.msg.pop(0)
        return msg
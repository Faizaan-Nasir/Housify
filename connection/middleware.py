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
        self.HOST_FR_CALL   = lambda x: x
        self.HOST_SR_CALL   = lambda x: x
        self.HOST_TR_CALL   = lambda x: x
        self.HOST_FH_CALL   = lambda x: x
        self.PLAYER_PAUSE   = lambda x: x
        self.NEW_NUMBER     = lambda x: x
        self.STATUS_CHANGE  = lambda x: x

class Game : 

    def __init__(self, code, hostname, host_client) : 
        self.code = code
        self.hostname = hostname
        self.host_client = host_client
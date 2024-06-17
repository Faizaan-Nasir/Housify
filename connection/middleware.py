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

    def __init__(
        self, 
        HOST_FR_CALL,
        HOST_SR_CALL,
        HOST_TR_CALL,
        HOST_FH_CALL,
        PLAYER_PAUSE,
        NEW_NUMBER,
        STATUS_CHANGE
    ) : 
        self.HOST_FR_CALL   = lambda x: HOST_FR_CALL(x)
        self.HOST_SR_CALL   = lambda x: HOST_SR_CALL(x)
        self.HOST_TR_CALL   = lambda x: HOST_TR_CALL(x)
        self.HOST_FH_CALL   = lambda x: HOST_FH_CALL(x)
        self.PLAYER_PAUSE   = lambda x: PLAYER_PAUSE(x)
        self.NEW_NUMBER     = lambda x: NEW_NUMBER(x)
        self.STATUS_CHANGE  = lambda x: STATUS_CHANGE(x)
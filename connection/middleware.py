class Game : 

    def __init__(self, code, hostname, host_client) : 
        self.code = code
        self.hostname = hostname
        self.host_client = host_client
        self.players = {}

    def add_player(self, name, socket) :
        self.players[name] = socket
    
    def remove_player(self, socket) : 
        if self.host_client == socket : 
            return 2
        elif socket in list(self.players.values()) : 
            for n, c in self.players.items() : 
                if c == socket : 
                    del self.players[n]
                    return 1
        else : 
            return 0
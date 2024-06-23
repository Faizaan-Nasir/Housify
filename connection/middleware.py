class Game : 

    def __init__(self, code, hostname, host_client) : 
        self.code = code
        self.hostname = hostname
        self.host_client = host_client
        self.players = {}

    def add_player(self, name, socket) :
        self.players[name] = socket
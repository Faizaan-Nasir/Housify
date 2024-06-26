import socket
import pickle
import select
from connection import Game

class Server : 
    
    HEADER_LENGTH = 10
    BUFFER_SIZE = 16
    FORMATTING = "utf-8"

    def __init__(self) : 
        self.port = 4040
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host_ip, self.port))

        self.sockets_list = [self.socket]
        self.clients = {}
        # gamecode : Game
        self.games = {}

        self.socket.listen()
        print(f"Listening on port {self.port}")

    def _encode(self, msg) : 
        msg = pickle.dumps(msg)
        header = f"{len(msg):<{self.HEADER_LENGTH}}".encode("utf-8")
        return header + msg
    
    def start(self) :
        while True : 
            read_sockets, _, except_sockets = select.select(self.sockets_list, [], self.sockets_list)
            
            for n_socket in read_sockets : 
                if n_socket == self.socket : # Connection request
                    conn, addr = self.socket.accept()
                    print(f"[NEW CONN]\tNew connection from {addr}")
                    msg = self.receive_client(conn)
                    print(f"[NEW PLAYER]\t{msg} joined the game")
                    if msg is False : 
                        continue
                    self.clients[conn] = msg
                    self.sockets_list.append(conn)
                else : # Received a message from client
                    msg = self.receive_client(n_socket)
                    if msg is False : # Client disconnect 
                        print(f"Closed connection")
                        self.handle_leave_game(n_socket)
                        del self.clients[n_socket]
                        self.sockets_list.remove(n_socket)
                        continue

                    print(f"[MSG RECVD]\tReceived '{msg}' from {self.clients[n_socket]}")
                    self._handle_event(msg, n_socket)

            for n_sockets in except_sockets :
                self.sockets_list.remove(n_sockets)
                del self.clients[n_sockets]
    
    def handle_leave_game(self, socket, gcode = None, host = False) : 
        name = self.clients[socket]
        # Specific game is known
        if gcode :
            g = self.games[gcode]
            g.remove_player(socket)
            if host: 
                self.on_remove_host(g, gcode)
            else : 
                self.on_remove_player(g, name)
            return

        # Specific game is not known. Linear search to find the game. See implementation of remove_player for Game
        for gcode, g in self.games.items() : 
            r = g.remove_player(socket)
            if r == 2 : # Host left the game 
                self.on_remove_host(g, gcode)
                break
            elif r == 1 : # Just a player left the game
                self.on_remove_player(g, name)
                break

    def on_remove_player(self, g, name) : 
        g.host_client.send(self._encode({"event" : "PLAYER LEAVE", "player" : name}))
        
    def on_remove_host(self, g, gcode) : 
        for p in g.players.values() : 
            p.send(self._encode({"event" : "END GAME", "reason" : "Host ended the game or has disconnected."}))
        del self.games[gcode]

    def receive_client(self, socket) : 
        try : 
            header = socket.recv(self.HEADER_LENGTH).decode(self.FORMATTING)

            if len(header) == 0 : 
                return False
            
            mlen = int(header)
            msg = socket.recv(mlen)
            msg = pickle.loads(msg)
            return msg
        except : 
            return False
        
    
    def _handle_event(self, msg, c) :
        code = msg["code"]
        if msg["event"] == "CREATE GAME" : 
            uname = msg["username"]
            g = Game(code, uname, c)
            self.games[code] = g
            print(f"[NEW GAME]\tGame with code {code} was created by {uname}")
        elif msg["event"] == "JOIN GAME" : 
            reply = "SUCCESS"
            uname = msg["username"]
            if code in self.games :
                g = self.games[code]
                g.add_player(uname, c)
                h_reply = {"event" : "PLAYER JOIN", "player_name" : uname}
                print(f"Sent {h_reply} to {g.hostname}")
                g.host_client.send(self._encode(h_reply))
            else : 
                print(self.games)
                reply = "FAILED"              
            c.send(self._encode({"msg" : reply}))
        elif msg["event"] == "START GAME" : 
            g = self.games[code]
            for n, p in g.players.items() :
                reply = {"event" : "START GAME", "name" : n}
                p.send(self._encode(reply))
        elif msg["event"] == "CALL NUMBER" : 
            reply = msg
            g = self.games[code]
            for p in g.players.values() : 
                p.send(self._encode(reply))
        elif msg["event"] == "LEAVE GAME" :
            self.handle_leave_game(c, code)
        elif msg["event"] == "END GAME" :
            # TODO: Consult with everyone and decide on the actual function of END GAME button 
            self.handle_leave_game(c, code, host = True)


# USAGE EXAMPLE
if __name__ == "__main__" : 
    s = Server()
    s.start()
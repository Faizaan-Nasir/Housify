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
                    if msg is False : 
                        print(f"Closed connection")
                        del self.clients[n_socket]
                        self.sockets_list.remove(n_socket)
                        continue
                    print(f"[MSG RECVD]\tReceived '{msg}' from {self.clients[n_socket]}")
                    self._handle_event(msg, n_socket)

            for n_sockets in except_sockets : 
                self.sockets_list.remove(n_sockets)
                del self.clients[n_sockets]

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
        if msg["event"] == "CREATE GAME" : 
            code = msg["code"]
            uname = msg["username"]
            g = Game(code, uname, c)
            self.games[code] = g
            print(f"[NEW GAME]\tGame with code {code} was created by {uname}")
        elif msg["event"] == "JOIN GAME" : 
            code = msg["code"]
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
            code = msg["code"]
            g = self.games[code]
            for n, p in g.players.items() :
                reply = {"event" : "START GAME", "name" : n}
                p.send(self._encode(reply))

# USAGE EXAMPLE
if __name__ == "__main__" : 
    s = Server()
    s.start()
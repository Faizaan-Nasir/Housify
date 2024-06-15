import socket
import pickle
import select

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
        self.socket.listen()
        print(f"Listening on port {self.port}")
    
    def start(self) :
        while True : 
            read_sockets, _, except_sockets = select.select(self.sockets_list, [], self.sockets_list)
            
            for n_socket in read_sockets : 
                if n_socket == self.socket : # Connection request
                    conn, addr = self.socket.accept()
                    print(f"[NEW CONN]\tNew connection from {addr}")
                    msg = self.receive_client(conn)
                    if not msg : 
                        continue
                    print(msg)
                    self.clients[conn] = addr
                    self.sockets_list.append(conn)
                else : # Received a message from client
                    msg = self.receive_client(n_socket)
                    if msg is False : 
                        print(f"Closed connection")
                        del self.clients[n_socket]
                        self.sockets_list.remove(n_socket)
                        continue
                    
                    print(f"[MSG RECVD]\tReceived '{msg}' from {self.clients[n_socket]}")

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
            # TODO: Do something with the message
            return msg
        except : 
            return False


# USAGE EXAMPLE
if __name__ == "__main__" : 
    s = Server()
    s.start()
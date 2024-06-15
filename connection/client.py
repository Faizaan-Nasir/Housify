import socket
import pickle
import errno
import sys

class Client : 

    BUFFER_SIZE = 16
    HEADER_LENGTH = 10
    FORMATTING = "utf-8"

    def __init__(self, ip = socket.gethostbyname(socket.gethostname()), port = 4040) : 
        self.b_ip = ip
        self.b_port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.b_ip, self.b_port))
        self.socket.setblocking(False)

    def run(self) : 
        while True :
            msg = input("> ") 
            msg = pickle.dumps(msg)
            header = f"{len(msg):<{self.HEADER_LENGTH}}".encode("utf-8")
            self.socket.send(header + msg)
            try : 
                while True : 
                    header = self.socket.recv(self.HEADER_LENGTH).decode(self.FORMATTING)
                    if not len(header) : 
                        print("Connection closed by the server")
                        sys.exit()
                    
                    msg = self.socket.recv(int(header))
                    msg = pickle.loads(msg)
                    print(msg)

            except IOError as e: 

                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK : 
                    print(f"Reading error: {str(e)}")
                    sys.exit()


# USAGE EXAMPLE
if __name__ == "__main__" : 
    c = Client()
    c.run()

import socket
import pickle
import errno
import sys
import time
import threading
from middleware import Messenger

class Client : 

    BUFFER_SIZE = 16
    HEADER_LENGTH = 10
    FORMATTING = "utf-8"

    def __init__(self, ip = socket.gethostbyname(socket.gethostname()), port = 4040) : 
        self.b_ip = ip
        self.b_port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msgr = m

    def _encode(self, msg) : 
        msg = pickle.dumps(msg)
        header = f"{len(msg):<{self.HEADER_LENGTH}}".encode("utf-8")
        return header + msg
    
    def connect(self, username) : 
        self.socket.connect((self.b_ip, self.b_port))
        self.socket.setblocking(False)
        usr = self._encode(username)
        self.socket.send(usr)
        
    def run(self) : 
        t = threading.Thread(target = self._run)
        t.start()

    def _run(self) : 
        while True :
            self._send()
            self._receive()
            
    def _send(self) : 
        msg = self.msgr.release()
        if msg : 
            msg = self._encode(msg)
            self.socket.send(msg)
    
    def _receive(self) : 
        try : 
            while True : 
                header = self.socket.recv(self.HEADER_LENGTH).decode(self.FORMATTING)
                if not len(header) : 
                    print("Connection closed by the server")
                    self.socket.close()
                    sys.exit()
            
                msg = self.socket.recv(int(header))
                msg = pickle.loads(msg)

        except IOError as e: 
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK : 
                print(f"Reading error: {str(e)}")
                self.socket.close()
                sys.exit()
                

# USAGE EXAMPLE
if __name__ == "__main__" : 
    m = Messenger(_type = "CLIENT")
    c = Client(m)
    username = input("Enter your username: ")
    c.connect(username)
    c.run()
    time.sleep(10)
    m.send("Hello")
    

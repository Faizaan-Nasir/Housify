import socket
import threading

class Server : 
    
    HEADER_LENGTH = 10
    FORMATTING = "utf-8"
    INITIAL_MESSAGE = "Hello, world"

    def __init__(self) : 
        self.port = 4040
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host_ip, self.port))
        self.msg = ""
    
    def start(self) :
        self.socket.listen(5)
        print(f"[SERVER STARTED] Listening on port {self.port}")
        while True :
            conn, addr = self.socket.accept()
            print(f"[NEW CONNECTION] Received connection from {addr}")
            conn.sendall(self.INITIAL_MESSAGE.encode(self.FORMATTING))
            t = threading.Thread(target = self._handle_client, args=(conn, addr))
            t.start()

    def _handle_client(self, conn, addr) : 
        msg = ""
        while True : 
            if self.msg : 
                conn.sendall(self.msg.encode(self.FORMATTING))
                print(f"[MSG SENT] Message sent to {addr}")
                self.msg = ""
            msg = conn.recv(1024).decode(self.FORMATTING)
            if msg : 
                print(f"[MSG RECIEVED] {msg} {len(msg)}")
                msg = ""


if __name__ == "__main__" : 
    s = Server()
    s.start()
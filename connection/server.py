import socket

class Server : 
    
    HEADER_LENGTH = 10
    FORMATTING = "utf-8"

    def __init__(self) : 
        self.port = 4040
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host_ip, self.port))
    
    def start(self) :
        self.socket.listen(5)
        print(f"[SERVER STARTED] Listening on port {self.port}")
        while True :
            conn, addr = self.socket.accept()
            print(f"[NEW CONNECTION] Received connection from {addr}")
            msg = "Hello world"
            conn.send(msg.encode(self.FORMATTING))
            print(f"[MSG SENT] Message sent to {addr}")
            conn.close()
            print(f"[CONNECTION CLOSED] Connection closed: {addr}")

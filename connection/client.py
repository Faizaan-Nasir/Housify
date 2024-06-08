import socket

class Client : 

    HEADER_LENGTH = 10
    FORMATTING = "utf-8"

    def __init__(self, ip = socket.gethostbyname(socket.gethostname()), port = 4040) : 
        self.b_ip = ip
        self.b_port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) : 
        self.socket.connect((self.b_ip, self.b_port))
        print("[CLIENT CONN] Client connected successfully")
        msg = self.socket.recv(1024).decode("")
        print(f"[MSG RECIEVED] {msg}")
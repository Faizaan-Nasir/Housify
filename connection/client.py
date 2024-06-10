import socket, threading

class Client : 

    HEADER_LENGTH = 10
    FORMATTING = "utf-8"

    def __init__(self, ip = socket.gethostbyname(socket.gethostname()), port = 4040) : 
        self.b_ip = ip
        self.b_port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msg = ""

    def run(self) : 
        self.socket.connect((self.b_ip, self.b_port))
        print("CLIENT CONNECTED")
        t = threading.Thread(target=self._run)
        t.start()
        # t.join()
    
    def _run(self) : 
        while True : 
            msg = self.socket.recv(1024).decode(self.FORMATTING)
            if msg : 
                print(f"[MSG RECIEVED] {msg} {len(msg)}")
            # Handle sending message

if __name__ == "__main__" : 
    c = Client()
    c.run()

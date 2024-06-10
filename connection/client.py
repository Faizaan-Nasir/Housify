import socket, threading
from messenger import Messenger

class Client : 

    HEADER_LENGTH = 10
    FORMATTING = "utf-8"

    def __init__(self, ip = socket.gethostbyname(socket.gethostname()), port = 4040) : 
        self.b_ip = ip
        self.b_port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msg = ""

    def run(self, messenger) : 
        self.socket.connect((self.b_ip, self.b_port))
        self.socket.setblocking(1)
        self.socket.settimeout(1)
        print("CLIENT CONNECTED")
        t = threading.Thread(target=self._run, args = (messenger,))
        t.start()
    
    def _run(self, messenger) : 
        while True : 
            try:
                msg = self.socket.recv(1024).decode(self.FORMATTING)
                if msg : 
                    print(f"[MSG RECIEVED] {msg} {len(msg)}")
            except TimeoutError : 
                pass
            except Exception as e: 
                print(e)
                break
            # Handle sending message
            n_msg = messenger.release()
            if n_msg: 
                print(f"SENDING '{msg}'")
                self.socket.sendall(n_msg.encode(self.FORMATTING))

if __name__ == "__main__" : 
    c = Client()
    m = Messenger(_type="CLIENT")
    c.run(m)
    m.send("Hello, back")
    m.send("How are you?")
    m.send("I am a client")

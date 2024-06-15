import socket, threading
import pickle
from messenger import Messenger

class Client : 

    BUFFER_SIZE = 16
    HEADER_LENGTH = 10
    FORMATTING = "utf-8"

    def __init__(self, ip = socket.gethostbyname(socket.gethostname()), port = 4040) : 
        self.b_ip = ip
        self.b_port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msg = ""

    def run(self, messenger) : 
        self.socket.connect((self.b_ip, self.b_port))
        self.socket.setblocking(False)
        self.socket.settimeout(1)
        print("CLIENT CONNECTED")
        t = threading.Thread(target=self._run, args = (messenger,))
        t.start()
    
    def _run(self, messenger) : 
        msg = b""
        mlen = 0
        flag = True
        while True : 
            try:
                rmsg = self.socket.recv(self.BUFFER_SIZE)
                if flag and rmsg: 
                    flag = False
                    mlen = int(rmsg[:self.HEADER_LENGTH])
                msg += rmsg
                if len(msg) - self.HEADER_LENGTH == mlen : 
                    obj = pickle.loads(msg[self.HEADER_LENGTH:])
                    print(f"[MSG RECEIVED] {obj}")
                    mlen = 0
                    msg = b""
                    flag = True
            except TimeoutError : 
                pass
            except Exception as e: 
                print(e)
                break
            # Handle sending message
            n_msg = messenger.release()
            if n_msg:
                self.socket.sendall(n_msg)
                print(f"SENDING '{pickle.loads(n_msg[self.HEADER_LENGTH:])}'")

# USAGE EXAMPLE
if __name__ == "__main__" : 
    c = Client()
    m = Messenger(_type="CLIENT")
    c.run(m)
    m.send("Hello, back")
    m.send("How are you?")
    m.send("I am a client")

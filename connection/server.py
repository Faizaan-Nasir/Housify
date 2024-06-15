import socket
import threading
from messenger import Messenger, MessengerGroup

class Server : 
    
    HEADER_LENGTH = 10
    BUFFER_SIZE = 16
    FORMATTING = "utf-8"

    def __init__(self, mg) : 
        self.port = 4040
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host_ip, self.port))
        self.mg = mg
    
    def start(self) :
        self.socket.listen(5)
        print(f"[SERVER STARTED] Listening on port {self.port}")
        while True :
            conn, addr = self.socket.accept()
            print(f"[NEW CONNECTION] Received connection from {addr}")
            m = Messenger(_type = "SERVER", dest = addr)
            m.send("Hello! Welcome to the server!")
            self.mg.add(m)
            t = threading.Thread(target = self._handle_client, args=(conn, addr, m))
            t.start()
        

    def _handle_client(self, conn, addr, messenger:Messenger) : 
        msg = ""
        mlen = 0
        flag = True
        while True : 
            # Send message
            nmsg = messenger.release()
            if nmsg : 
                conn.sendall(nmsg.encode(self.FORMATTING))
                print(f"[MSG SENT] '{nmsg[self.HEADER_LENGTH:]}' sent to {addr}")

            # Receiving message
            rmsg = conn.recv(self.BUFFER_SIZE).decode(self.FORMATTING)
            if flag and rmsg: 
                flag = False
                mlen = int(rmsg[:self.HEADER_LENGTH])
            msg += rmsg
            if len(msg) - self.HEADER_LENGTH == mlen : 
                print(f"[MSG RECEIVED] {msg[self.HEADER_LENGTH:]}")
                mlen = 0
                msg = ""
                flag = True
            
            
            # TODO: Manage disconnect


# USAGE EXAMPLE
if __name__ == "__main__" : 
    mg = MessengerGroup()
    s = Server(mg)
    s.start()
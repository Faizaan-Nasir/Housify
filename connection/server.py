import socket
import threading
from messenger import Messenger, MessengerGroup

class Server : 
    
    HEADER_LENGTH = 10
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
            conn.sendall("Hello, world".encode(self.FORMATTING))
            m = Messenger(_type = "SERVER", dest = addr)
            self.mg.add(m)
            t = threading.Thread(target = self._handle_client, args=(conn, addr, m))
            t.start()
        

    def _handle_client(self, conn, addr, messenger:Messenger) : 
        msg = ""
        messenger.send(f"Hey there, {addr}, welcome from your personal messenger instance")
        while True : 
            nmsg = messenger.release()
            if nmsg : 
                conn.sendall(nmsg.encode(self.FORMATTING))
                print(f"[MSG SENT] '{nmsg}' sent to {addr}")
            msg = conn.recv(1024).decode(self.FORMATTING)
            if msg : 
                print(f"[MSG RECIEVED] {msg} {len(msg)}")
                msg = ""
            # TODO: On disconnect, self.mg.remove(addr)


# USAGE EXAMPLE
if __name__ == "__main__" : 
    mg = MessengerGroup()
    s = Server(mg)
    s.start()
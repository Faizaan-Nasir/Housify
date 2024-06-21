import socket
import pickle
import errno
import sys
import threading

class Client : 

    BUFFER_SIZE = 16
    HEADER_LENGTH = 10
    FORMATTING = "utf-8"

    def __init__(self, m, t, status = "PLAYER", ip = socket.gethostbyname(socket.gethostname()), port = 4040) : 
        self.b_ip = ip
        self.b_port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msgr = m
        self.trigger = t
        self.status = status

    def _encode(self, msg) : 
        msg = pickle.dumps(msg)
        header = f"{len(msg):<{self.HEADER_LENGTH}}".encode("utf-8")
        return header + msg
    
    def connect(self, username) : 
        self.socket.connect((self.b_ip, self.b_port))
        self.socket.setblocking(False)
        usr = self._encode(username)
        self.socket.send(usr)

    def disconnect(self) : 
        self.socket.close()
        
    def run(self) : 
        t = threading.Thread(target = self._run)
        t.start()

    def disconnect(self) : 
        self.socket.close()

    def _run(self) : 
        while True :
            try : 
                self._send()
                self._receive()
            except Exception as e : 
                if str(e) == "APPLICATION EXIT" :
                    print("[DISCONNECT]\tCLOSING APPLICATION")
                    self.disconnect() 
                    break
        return
                    
            
    def _send(self) :
        # print("Called") 
        msg = self.msgr.release()
        if msg : 
            if msg == "CLOSE APP" : 
                raise Exception("APPLICATION EXIT")
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
                self._handle_events(msg)

        except IOError as e: 
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK : 
                print(f"Reading error: {str(e)}")
                self.socket.close()
                sys.exit()

    def _handle_events(self, msg) : 
        # This is for the player who is the host
        if self.status == "HOST" :
            if msg["msg"] == "FIRST ROW" :
                self.trigger.HOST_FR_CALL(msg)
            elif msg["msg"] == "SECOND ROW" :
                self.trigger.HOST_SR_CALL(msg)
            elif msg["msg"] == "THIRD ROW" :
                self.trigger.HOST_TR_CALL(msg)
            elif msg["msg"] == "FULL HOUSIE" : 
                self.trigger.HOST_FH_CALL(msg)

        # This is for a simple player
        elif self.status == "PLAYER" : 
            if msg["msg"] == "PAUSE GAME" : 
                self.trigger.PLAYER_PAUSE(msg)
            elif msg["msg"] == "NEW NUMBER" : 
                self.trigger.NEW_NUMBER(msg)
            elif msg["msg"] == "STATUS CHANGE" : 
                self.trigger.STATUS_CHANGE(msg)    

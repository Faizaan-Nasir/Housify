import socket
client_socket=socket.socket()
port=7000
client_socket.connect((socket.gethostname(),port))
msg='H$O$S$T'
client_socket.send(msg.encode())    
def sendNewMes(msg):
    client_socket.send(msg.encode())
def endCon():
    client_socket.close()
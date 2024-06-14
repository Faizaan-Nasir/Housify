import mysql.connector as sql
import os
import random
from dotenv import load_dotenv

load_dotenv()

try:
    con=sql.connect(host=os.getenv("HOST"),port=int(os.getenv("PORT")),user=os.getenv("USER"),charset="utf8mb4",password=os.getenv("PASSWORD"),database='defaultdb')
except Exception as error:
    with open('connection-error.txt','w') as file:
        file.write(error)
cur=con.cursor()
try:
    cur.execute("create table CurrentGames(GameID varchar(7) primary key,HostID varchar(25))")
    cur.execute("create table GamePlayers(GameID varchar(7),PlayerID varchar(20),TicketID varchar(6), primary key(GameID,PlayerID))")
except:
    print('table already exists')

try:
    with open('./temp/gamerid.txt','r') as file:
        gamerid=file.read()
except:
    gamerid=str(random.randint(10000,99999))
    with open('./temp/gamerid.txt','w') as file:
        file.write(gamerid)

def createGame():
    gameid=str(random.randint(10000,99999))
    cur.execute(f"insert into CurrentGames values('{gameid}','{gamerid}')")
    return gameid

# need to fix the fact that a random game id could already exist too

def joinGame(gameid):
    def generate():
        x=random.randint(1,9)
        coor=(x,i+1)
        if coor in l:
            generate()
        else:
            l.append(coor)
    ticketid='T'+str(random.randint(10000,99999))
    cur.execute(f"insert into GamePlayers values ('{gameid}','{gamerid}','{ticketid}')")
    random.seed(int(ticketid[1:]))
    ticket={}
    l=[]
    for i in range(3):
        for j in range(5):
            generate()
    def genNum():
        if coordinate[0]==1:
            number=random.randint(coordinate[0],coordinate[0]+10)
        else:
            number=random.randint((coordinate[0]-1)*10,(coordinate[0]-1)*10+10)
        return number
    for coordinate in l:
        value=genNum()
        while value in ticket.values():
            value=genNum()
        else:
            ticket[coordinate]=value
    # makeTicket()
    return ticket
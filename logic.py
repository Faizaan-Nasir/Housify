import mysql.connector as sql
import os
import random
from dotenv import load_dotenv
import ticket

load_dotenv()

def getName():
    with open('username.txt','r') as file:
        return file.read()

def connectMe():
    global con,cur
    try:
        con=sql.connect(host=os.getenv("HOST"),port=int(os.getenv("PORT")),user=os.getenv("USER"),charset="utf8mb4",password=os.getenv("PASSWORD"),database='defaultdb')
    except Exception as error:
        with open('connection-error.txt','w') as file:
            file.write(error)
    cur=con.cursor()
# try:
#     cur.execute("create table CurrentGames(GameID varchar(7) primary key,HostID varchar(25))")
#     cur.execute("create table GamePlayers(GameID varchar(7),PlayerID varchar(20),TicketID varchar(6), primary key(GameID,PlayerID))")
# except:
#     print('table already exists')

def createGame():
    gameid=str(random.randint(10000,99999))
    with open('username.txt','r') as file:
        gamerid=file.read()
    cur.execute(f"insert into CurrentGames values('{gameid}','{gamerid}')")
    return gameid
# connectMe()
# createGame()
# need to fix the fact that a random game id could already exist too

def generateTicket(ticketid):
    def generate(x,y):
        a,b=x,y
        if x=='':
            x=random.randint(1,9)
        if y=='':
            while True:
                count=0
                y=random.randint(1,3)
                for k in l:
                    if k[1]==y:
                        count+=1
                if count<5:
                    break
        coor=(x,y)
        if coor in l:
            generate(a,b)
        else:
            l.append(coor)
    random.seed(int(ticketid[1:]))
    ticket={}
    l=[]
    for i in range(9):
        generate(i+1,'')

    for i in range(3):
        count=0
        for k in l:
            if k[1]==(i+1):
                count+=1
        for j in range(5-count):
            generate('',i+1)
    def genNum():
        if coordinate[0]==1:
            number=random.randint(coordinate[0],coordinate[0]+9)
        else:
            number=random.randint((coordinate[0]-1)*10+1,(coordinate[0]-1)*10+10)
        return number
    for coordinate in l:
        value=genNum()
        while value in ticket.values():
            value=genNum()
        else:
            ticket[coordinate]=value
    # print(ticket)
    keys=sorted(list(ticket.keys()))
    values=sorted(list(ticket.values()))
    index=0
    acticket={}
    for key in keys:
        acticket[key]=values[index]
        index+=1
    # print(acticket)
    return acticket

def joinGame(gameid,gamerid):
    ticketid='T'+str(random.randint(10000,99999))
    # cur.execute('ALTER TABLE GamePlayers add foreign key (GameID) references CurrentGames(GameID)')
    try:
        cur.execute(f"insert into GamePlayers values ('{gameid}','{gamerid}','{ticketid}')")
        ticket.ticketMain(generateTicket(ticketid[1:])).show()
    except sql.errors.IntegrityError:
        print('''One of the two errors occurred:
              1. A game with the entered Game Code does not exist
              2. You have already joined this game before''')
import mysql.connector as sql
import os
import random
from dotenv import load_dotenv

# to open the .env file
load_dotenv()

def getName():
    with open('username.txt','r') as file:
        return file.read()

# establishing connection to the online database
def connectMe():
    global con,cur
    try:
        con=sql.connect(host=os.getenv("HOST"),port=int(os.getenv("PORT")),user=os.getenv("USERNAME"),charset="utf8mb4",password=os.getenv("PASSWORD"),database='defaultdb')
    except Exception as error:
        with open('connection-error.txt','w') as file:
            file.write(str(error))
    cur=con.cursor()

# the following bit is for reference only, may be used to create a database locally
# try:
#     cur.execute("create table CurrentGames(GameID varchar(7) primary key,HostID varchar(25))")
#     cur.execute("create table GamePlayers(GameID varchar(7),PlayerID varchar(20),TicketID varchar(6), primary key(GameID,PlayerID))")
# except:
#     print('table already exists')

# creates a game
def createGame():
    gameid=str(random.randint(10000,99999))
    with open('username.txt','r') as file:
        gamerid=file.read()
    cur.execute(f"insert into CurrentGames values('{gameid}','{gamerid}')")
    con.commit()
    return gameid
# need to fix the fact that a random game id could already exist too

# this function creates a dictionary with keys as coordinates and values as the corresponding numbers for the ticket
# following all rules of a housie ticket
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
    keys=sorted(list(ticket.keys()))
    values=sorted(list(ticket.values()))
    index=0
    acticket={}
    for key in keys:
        acticket[key]=values[index]
        index+=1
    return acticket

# performs the following functions:
# 1. generates a ticketid (seed)
# 2. joins a game in the database
def joinGame(gameid,gamerid):
    ticketid='T'+str(random.randint(10000,99999))
    # cur.execute('ALTER TABLE GamePlayers add foreign key (GameID) references CurrentGames(GameID)')
    try:
        cur.execute(f"insert into GamePlayers values ('{gameid}','{gamerid}','{ticketid}')")
        con.commit()
        return ticketid[1:]
    except sql.errors.IntegrityError:
        print('''One of the two errors occurred:
              1. A game with the entered Game Code does not exist
              2. You have already joined this game before''')
        # we need to put this error in some sort of a window
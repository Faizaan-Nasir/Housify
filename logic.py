import random

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
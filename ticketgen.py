import random
ticket={}
ticketnum=int(input("Enter ticket number: "))
random.seed(ticketnum)
def gencolnum():
    num=random.randint(col*10-9,col*10)
    if num not in ticket[col]:
        ticket[col].append(num)
    else:
        gencolnum()
def generate():
    x=random.randint(1,9)
    coor=(x,i+1)
    if coor in l:
        generate()
    else:
        l.append(coor)
for col in range(1,10):
    ticket[col]=[]
    for j in range(3):
        gencolnum()
    else:
        ticket[col].sort()
l=[]
for i in range(3):
    for j in range(5):
        generate()
l.sort()
finticket={}
for i in l:
    finticket[i]=ticket[i[0]][i[1]-1]
print(finticket)
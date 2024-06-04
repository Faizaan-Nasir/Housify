import random
import hostCon
import time
l=[]
def callNum():
    newnum=random.randint(1,90)
    if newnum not in l:
        l.append(newnum)
        hostCon.sendNewMes(str(newnum))
    else:
        callNum()
for i in range(10):
    time.sleep(5)
    callNum()
hostCon.endCon()
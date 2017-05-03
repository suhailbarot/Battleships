import socket,time


cs = socket.socket()

ss = socket.socket()
ss.bind(('127.0.0.1',12345))
ss.listen(5)



mysea = [[0 for x in range(8)] for x in range(8)]
trysea = [[0 for x in range(8)] for x in range(8)]
ships = []


def ship_check(row,col,x):
    if mysea[row][col]==1:
        client.send("1")
        print("YOUR OPPONENT HIT!")

        m=sink_ship(row,col)
        if m==1:
            x=1
            print("YOU LOSE!")
    else:
        client.send("0")
        print("YOUR OPPONENT MISSED!")

    time.sleep(0.5)
    return x

def display(array):
    m=0
    print("\t"),
    for row in array:
        print(str(m)+" "),
        m+=1
    m=0
    print("\n")
    for row in array:
        print(str(m)+"\t"),
        for val in row:
            print str(val)+" ",
        m+=1
        print("")

#ships are of length 4, total 4 ships
def sink_ship(row,col):
    for ship in ships:
        if (ship[0]<=row<=ship[2] or ship[2]<=row<=ship[0])  and (ship[1]<=col<=ship[3] or ship[3]<=col<=ship[1]):
            print("in")
            if ship[0]<=ship[2]:
                for i in range(ship[0],ship[2]+1):
                    mysea[i][ship[1]]=0
            else:
                for i in range(ship[2],ship[0]+1):
                    mysea[i][ship[1]]=0
            if ship[1]<=ship[3]:
                for i in range(ship[1],ship[3]+1):
                    mysea[ship[0]][i]=0
            else:
                for i in range(ship[3],ship[1]+1):
                    mysea[ship[0]][i]=0
            ships.remove(ship)


    print("Number of ships you have left:")
    print(len(ships))
    if len(ships)==0:
        p=1
    else:
        p=0
    return p

def check(st_row,st_col,end_row,end_col):
    ch=1
    if (abs(st_row - end_row)==3 and abs(st_col - end_col)==0) or (abs(st_col - end_col)==3 and abs(st_row - end_row)==0):
        ch=0
    for ship in ships:
        if ship[0]<=ship[2]:
            for n in range(ship[0],ship[2]+1):
                if st_row<=n<=end_row or end_row<=n<=st_row:
                    if ship[1]<=ship[3]:
                        for p in range(ship[1],ship[3]+1):
                            if st_col<=p<=end_col or end_col<=p<=st_col:
                                ch=1
                    else:
                        for p in range(ship[3],ship[1]+1):
                            if st_col<=p<=end_col or end_col<=p<=st_col:
                                ch=1

        else:
            for n in range(ship[2],ship[0]+1):
                if st_row<=n<=end_row or end_row<=n<=st_row:
                    if ship[1]<=ship[3]:
                        for p in range(ship[1],ship[3]+1):
                            if st_col<=p<=end_col or end_col<=p<=st_col:
                                ch=1
                    else:
                        for p in range(ship[3],ship[1]+1):
                            if st_col<=p<=end_col or end_col<=p<=st_col:
                                ch=1
    return ch

def place_ship():
    n=0
    while n==0:
        try:
            st_row,st_col,end_row,end_col = map(int,raw_input("Enter Start row, start column,end row,end column : ").split())
            n=1
        except:
            print("Please enter valid numbers")

    ch = check(st_row,st_col,end_row,end_col)
    if ch == 1:
        print("Your ship length must be 4 and it must be either horizontal or vertical OR your ships are clashing try again\n")
        place_ship()
    if st_row<=end_row:
        for i in range(st_row,end_row+1):
            mysea[i][st_col] = 1
    else:
        for i in range(end_row,st_row+1):
            mysea[i][st_col] = 1
    if st_col<=end_col:
        for i in range(st_col,end_col+1):
            mysea[st_row][i] = 1
    else:
        for i in range(end_col,st_col+1):
            mysea[st_row][i] = 1
    ships.append([st_row,st_col,end_row,end_col])



def guess(x):
    n=0
    while n==0:
        try:
            row,col= map(int,raw_input("Enter row and column number: ").split())
            n=1
        except:
            print("Please enter valid numbers")
    while row not in range(0,8) or col not in range(0,8):
        print("Enter values from 0 to 7!")
        n=0
        while n==0:
            try:
                row,col= map(int,raw_input("Enter row and column number: ").split())
                n=1
            except:
                print("Please enter valid numbers")
    while trysea[row][col] == 'X' or trysea[row][col]=='S':
        print("You already guessed this,try again")
        n=0
        while n==0:
            try:
                row,col= map(int,raw_input("Enter row and column number: ").split())
                n=1
            except:
                print("Please enter valid numbers")

    client.send(str(row))
    time.sleep(0.5)
    client.send(str(col))
    v = cs.recv(1000)
    x=cs.recv(1000)
    if x=="1":
        print("YOU WIN!")
        return x


    if trysea[row][col] == 0:
        if v=="1":
            trysea[row][col]='S'
            print("\nYOU HIT!\n")
        else:
            trysea[row][col]='X'
            print("\nYOU MISSED!\n")

    return x

#Game starts here.
print("You have 4 battleships of length 4 each on an 8x8 board")

for i in range(4):
    print("Place a ship:")
    place_ship()
    print("Your placements:\n")
    display(mysea)

print("ships placed!\n")

print("Start guessing!\n")
cs.connect(('127.0.0.1',12346))
client,address = ss.accept()
x=0
while x==0:
    print("Your opponent's sea : \n")
    display(trysea)

    row= cs.recv(2000)
    col=cs.recv(2000)
    row=int(row)
    col=int(col)
    x=int(ship_check(row,col,x))
    client.send(str(x))
    if x==1:
        break
    x=int(guess(x))
    if x==1:
        break

cs.close()
ss.close()


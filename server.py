import socket
import threading
import time
import random


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
MONEY=5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

easydict={
    "Who I am?" : "the server",
    "Are you stupid?" : "yes",
    "This is cool?" : "yes",
    "Are you pretty?" : "no",
    "Am I pretty?" : "yes",
    "hiii" : "hiii",
    "friends" : "joey",
    "Am I old?" : "no",
    "Are you old?" : "yes",
    "This is fun?" : "of course",
    "Who is the king?" : "Hadar Ashoach"
}


hardict={
   "What is israel?" : "a country",
    "What is god" : "everything",
    "When did world war 2 started?" : "1940",
    "What is 'A'" : "a letter",
}


class question():
    def __init__(self, dic):
        self.quest,self.answer =random.choice(list(dic.items()))
        self.self = self.answer,self.quest
        dic.pop(self.quest,self.answer)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")
            if msg == DISCONNECT_MESSAGE:
                conn.send('Bye'.encode(FORMAT))
                conn.close()
                connected = False
            elif msg.lower() == 'start':
                game(conn, addr)
            else:
                conn.send("no function".encode(FORMAT))

    conn.close()

def check(q ,player_answer):
    if q.answer==player_answer:
        message="correct"
    else:
        message="incorrect"
        if player_answer == '*':
            conn.send('Bye'.encode(FORMAT))
            conn.close()
    return message

def game(conn, addr):
    r_count, w_count = 0, 0
    r_hardcount,w_hardcount=0,0
    start_time = time.time()

    print(f"[TIME] player started first round at {start_time}")
    conn.send("welcome to our game!".encode(FORMAT))

    for i in range(len(easydict)):
        current_time = time.time()

        qna = question(easydict)
        conn.send(qna.quest.encode(FORMAT))
        time.sleep(0.1)

        conn.send((str(60 - (current_time-start_time))).encode(FORMAT))
        player_answer = conn.recv(1024).decode(FORMAT)
        message = check(qna ,player_answer)
        current_time = time.time()

        if message == 'correct':
            r_count += 1
            if current_time-start_time >= 61:
                r_count -= 1
                w_count += 1
                message = "incorrect. your time is over"
        else:
            w_count += 1
        
        print(f"[SCORING {addr}] right:{r_count} wrong:{w_count}")

        if current_time - start_time >= 60:
            amount = r_count*MONEY
            conn.send(f"{message}, you won {amount}₪".encode())
            print(f"[MONEY]{addr} won {amount}₪")
            break
        else:
            conn.send(message.encode(FORMAT))
    
    '''
    howmuch = int(conn.recv(1024).decode())
    for i in range(howmuch):
        ran1 = random.choice(hardquest)
        conn.send(ran1.question.encode(FORMAT))
        hardquest.remove(ran1)
        player1_hardanswer = conn.recv(1024).decode(FORMAT)
        messege = check(ran1, player1_hardanswer)
        if messege == 'correct':
            r_hardcount += 1
        else:
            w_hardcount += 1
    total=r_hardcount * MONEY
    string = str(f"you erend in this round: {total}")
    conn.send(string.encode())
    print(f"[MONEY] {addr} won {total}₪")
    '''



def start():
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        thread_list=[]
        thread_list.append(thread)
        print(f"[ACTIVE CINECTION] {threading.activeCount() - 1}")
print('[STARTING] server is starting...')
start()


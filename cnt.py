import socket
import time
import pygame
import os

pygame.init()
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hamerdaf!!!")

DavidFont = pygame.font.SysFont('David', 26)

BACKGROND = pygame.image.load(os.path.join('Assets', 'background.jpg'))

FPS = 1


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    massage = msg.encode(FORMAT)
    msg_length = len(massage)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(massage)
    re = client.recv(2048).decode(FORMAT)
    print(re)

msg = input('to start, type start. to disconnect press * ')
if msg == '*':
    send(DISCONNECT_MESSAGE)
else:
    send(msg)



def round1(message):
    WIN.blit(BACKGROND, (0, 0))
    question = client.recv(1024).decode(FORMAT)
    time_left = client.recv(1024).decode(FORMAT)
    question = DavidFont.render(question, 1, (0, 0, 0))
    time_left = DavidFont.render(time_left, 1, (0, 0, 0))
    answer = DavidFont.render(f"your answer: {message}", 1, (0, 0, 0))
    WIN.blit(time_left, (10, 10))
    WIN.blit(question, (10, 100))
    WIN.blit(answer, (200, 200))
    pygame.display.update()
    if message == "*":
        send(DISCONNECT_MESSAGE)
    elif message[-1] == ':':
        client.send(answer.encode())
        re = client.recv(2048).decode(FORMAT)
        re = DavidFont.render(re, 1, (0, 0, 0))




def main():
    run = True
    round_num = 1
    message = ' '
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == DISCONNECT_MESSAGE:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    message += 'a'
                elif event.key == pygame.K_b:
                    message += 'b'
                elif event.key == pygame.K_c:
                    message += 'c'
                elif event.key == pygame.K_d:
                    message += 'd'
                elif event.key == pygame.K_e:
                    message += 'e'
        WIN.blit(BACKGROND, (0, 0))
        round1(message)
        pygame.display.update()


if __name__ =='__main__':
    main()
 

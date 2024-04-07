from socket import *
import threading
import pygame
import sys
import pyscreenshot
import base64
import os
import cv2 as cv
import PIL

serv=("26.148.102.119",27015)

server=socket(AF_INET,SOCK_STREAM)
server.bind(serv)
server.listen(5)
user, addres = server.accept()

pygame.init()

width = 1280
height = 720
BLACK = (0, 0, 0)
GRAY = (76, 76, 76)
FPS = 144

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


def Label(text,pos,color=(255,255,255),size=36):
    font = pygame.font.Font(None, size)
    text_render = font.render(text, False, color)
    screen.blit(text_render, pos)

class Button:
    def __init__(self, rect, text, func=None):
        self.rect = rect
        self.text = text
        self.func = func

    def draw(self):
        pygame.draw.rect(screen, (200, 0, 255), self.rect)
        Label(self.text,[self.rect.x,self.rect.y])

    def check(self, mrect):
        if self.rect.colliderect(mrect):
            self.func()

button_close=Button(pygame.Rect(100,100,100,40),"Close",exit)

#threading.Thread(target=receive).start()

run = True
while run:
    screen.fill((0,0,0))
    pygame.display.set_caption(str(clock.get_fps()))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            msg = str(x) + "/" + str(y)
            #user.send(msg.encode("utf-8"))
            mrect = pygame.Rect(x, y, 1, 1)
            button_close.check(mrect)
    msg = user.recv(1024 * 20 * 1024)
    with open("screen.png", 'wb') as f:
        f.write(msg)
    try:
        img = pygame.image.load(os.path.join('screen.png'))
        screen.blit(img, (0, 0))
    except:
        print("Error")
    button_close.draw()
    pygame.display.flip()
    clock.tick(FPS)

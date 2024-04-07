from socket import *
import threading
import keyboard
from mss import mss

from PIL import Image

run=True


class Client:
    def __init__(self):
        self.addr = ('26.148.102.119', 27015)
        self.client = socket(AF_INET, SOCK_STREAM)

    def connecting(self):
        try:
            self.client.connect(self.addr)
        except:
            return 0
        return 1

    def send(self, encoded_photo):
        try:
            self.client.send(encoded_photo)
        except:
            return 0
        return 1


def close():
    global run
    while True:
        if keyboard.is_pressed("q+ctrl"):
            run=False
            exit(69)


threading.Thread(target=close).start()


def start():
    global run

    client = Client()
    while True:
        code = client.connecting()
        if code == 1:
            break
    while run:
        mss().shot(mon=0)
        img = Image.open('monitor-1.png')
        img.thumbnail((1280, 720))
        img.save("monitor-1.png")
        f = open("monitor-1.png", 'rb')
        encoded_photo = f.read()
        f.close()
        code = client.send(encoded_photo)
        if code == 0:
            start()


start()

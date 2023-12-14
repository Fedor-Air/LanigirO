import random

import pygame
import sqlite3
import csv

fps = 50  # количество кадров в секунду
clock = pygame.time.Clock()
running = True

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['000'] * width for _ in range(height)]
        used_coor = []
        for i in range(self.width):
            for j in range(self.width):
                used_coor.append((j, i))  # пустая карта, карта всегда квадрат, для удобства


        con = sqlite3.connect("rooms_bd.sqlite")
        cur = con.cursor()
        c = cur.execute("""SELECT * FROM rooms WHERE type=?""", ('ess_room',)).fetchall()  # осн генерация
        for room in c:
            rcoor = random.choice(used_coor)
            used_coor.remove(rcoor)
            self.board[rcoor[0]][rcoor[1]] = room[2]

        if self.width >= 5 and self.height >= 5:
            c = cur.execute("""SELECT * FROM rooms WHERE type=?""", ('room',)).fetchall()  # генерация доп комнат
            for i in range(self.width - 3):
                rroom = random.randint(0, len(c) - 1)
                rcoor = random.choice(used_coor)
                used_coor.remove(rcoor)
                self.board[rcoor[0]][rcoor[1]] = c[rroom][2]
            c = cur.execute("""SELECT * FROM rooms WHERE type=?""", ('monstr',)).fetchall()  # генерация монстров (пока только 1((()
            for i in range(self.width - 3):
                rmon = random.randint(0, len(c) - 1)
                rcoor = random.choice(used_coor)
                used_coor.remove(rcoor)
                self.board[rcoor[0]][rcoor[1]] = c[rmon][2]

        print(*self.board, sep='\n')

# while running:  # главный игровой цикл
    # for event in pygame.event.get():
        # if event.type == pygame.QUIT:
            # running = False
        # обработка остальных событий
    # ...
    # формирование кадра
    # ...
    # pygame.display.flip()  # смена кадра
    # изменение игрового мира
    # ...
    # временная задержка
    # clock.tick(fps) # тут впринципе для федора все
cc = Board(10, 10)  # оно в принте отображает созданный лабиринт, цифры - айди комнаты в бд

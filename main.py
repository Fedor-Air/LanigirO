import random
import pygame
import os
import sys
import sqlite3
import csv

if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode(size)
    FPS = 50  # количество кадров в секунду
    clock = pygame.time.Clock()
    running = True


class Board:
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.board = [['000'] * WIDTH for _ in range(HEIGHT)]
        used_coor = []
        for i in range(self.WIDTH):
            for j in range(self.WIDTH):
                used_coor.append((j, i))  # пустая карта, карта всегда квадрат, для удобства

        con = sqlite3.connect("rooms_bd.sqlite")
        cur = con.cursor()
        c = cur.execute("""SELECT * FROM rooms WHERE type=?""", ('ess_room',)).fetchall()  # осн генерация
        for room in c:
            rcoor = random.choice(used_coor)
            used_coor.remove(rcoor)
            self.board[rcoor[0]][rcoor[1]] = room[2]

        if self.WIDTH >= 5 and self.HEIGHT >= 5:
            c = cur.execute("""SELECT * FROM rooms WHERE type=?""", ('room',)).fetchall()  # генерация доп комнат
            for i in range(self.WIDTH - 3):
                rroom = random.randint(0, len(c) - 1)
                rcoor = random.choice(used_coor)
                used_coor.remove(rcoor)
                self.board[rcoor[0]][rcoor[1]] = c[rroom][2]
            c = cur.execute("""SELECT * FROM rooms WHERE type=?""", ('monstr',)).fetchall()  # генерация монстров (пока только 1((()
            for i in range(self.WIDTH - 3):
                rmon = random.randint(0, len(c) - 1)
                rcoor = random.choice(used_coor)
                used_coor.remove(rcoor)
                self.board[rcoor[0]][rcoor[1]] = c[rmon][2]

        print(*self.board, sep='\n')


def load_image(name, transparent=False):
    fullname = os.path.join('resources', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if transparent:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image


# Функция закрытия приложения
def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["LanigirO", "",
                  "Одиночная игра",
                  "Сетевая игра",
                  "Настройки",
                  "Выход"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 30)
    text_coord = 50
    text_out = []
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        text_out.append((string_rendered, intro_rect))
    # Отрисовка
    while True:
        mouse = pygame.mouse.get_pos()
        for i in text_out:
            screen.blit(i[0], i[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on the
                # button the game is terminated
                if 10 <= mouse[0] <= 115 and 180 <= mouse[1] <= 200:
                    settings()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(int(FPS))


def settings():
    intro_text = ["FPS",
                  "Разрешение",
                  "Звук",
                  "Музыка",
                  "Эффекты"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 30)
    text_coord = 50
    text_out = []
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        text_out.append((string_rendered, intro_rect))
    # Отрисовка
    while True:
        mouse = pygame.mouse.get_pos()
        for i in text_out:
            screen.blit(i[0], i[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(int(FPS))

cc = Board(10, 10)  # оно в принте отображает созданный лабиринт, цифры - айди комнаты в бд
start_screen()

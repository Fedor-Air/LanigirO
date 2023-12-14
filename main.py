import pygame
import sqlite3
import csv

fps = 50  # количество кадров в секунду
clock = pygame.time.Clock()
running = True

def generate_level(x, y):
    con = sqlite3.connect("rooms_bd.sqlite")
    cur = con.cursor()
    with open('generated_map.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        row_dull = '000'
        row_wall = '002'
        row_list = []
        for i in range(y + 2):
            lisik = []
            if i == 0 or i == y + 2:
                for j in range(x + 2):
                    lisik.append('002')
                row_list.append(listik)
            else:
                for j in range(x + 2):
                    if j == 0 or j == y + 2:
                        lisik.append('002')
                    else:
                        lisik.append('000')
                    listik.append(row)

        writer.writerow(row_list)
        # тут будут генерации по созданной пустой карте

while running:  # главный игровой цикл
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # обработка остальных событий
    # ...
    # формирование кадра
    # ...
    pygame.display.flip()  # смена кадра
    # изменение игрового мира
    # ...
    # временная задержка
    clock.tick(fps) # тут впринципе для федора все

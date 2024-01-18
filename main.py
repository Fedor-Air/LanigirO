import random
import pygame
import os
import sys
import sqlite3
import copy


musicon = True

class Board:
    def __init__(self, WIDTH, HEIGHT, col_st):
        self.walls_coor = []
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.board = [['000'] * WIDTH for _ in range(HEIGHT)]
        self.unused_coor = []
        self.cell_size = 30
        self.color_board = []
        self.left = (1200 - self.WIDTH * self.cell_size) // 2
        self.top = (700 - self.WIDTH * self.cell_size) // 2

        col_sten = col_st

        def walls_gen():
            self.color_board = []
            self.unused_coor = []
            self.board = [['000'] * WIDTH for _ in range(HEIGHT)]
            self.walls_coor = []
            for i in range(self.WIDTH):
                a = []
                for j in range(self.WIDTH):
                    a.append("black")
                self.color_board.append(a)
            for i in range(self.WIDTH):
                for j in range(self.WIDTH):
                    self.unused_coor.append((i, j))
            self.board = [['000'] * WIDTH for _ in range(HEIGHT)]
            for i in range(col_sten):
                x = random.randint(0, self.WIDTH - 1)
                y = random.randint(0, self.WIDTH - 1)
                while self.board[x][y] == '002':
                    x = random.randint(0, self.WIDTH - 1)
                    y = random.randint(0, self.WIDTH - 1)
                self.unused_coor.remove((x, y))
                self.walls_coor.append((x, y))
                self.color_board[x][y] = "red"
                self.board[x][y] = '002'

        def generate():
            con = sqlite3.connect("rooms_bd.sqlite")
            cur = con.cursor()
            c = cur.execute("""SELECT * FROM rooms WHERE type=?""", ('ess_room',)).fetchall()  # осн генерация
            for room in c:
                rcoor = random.choice(self.unused_coor)
                self.unused_coor.remove(rcoor)
                self.board[rcoor[0]][rcoor[1]] = room[2]
            if self.WIDTH >= 5 and self.HEIGHT >= 5:
                c = cur.execute("""SELECT * FROM rooms WHERE type=?""", ('room',)).fetchall()  # генерация доп комнат
                for i in range(self.WIDTH - 3):
                    rroom = random.randint(0, len(c) - 1)
                    rcoor = random.choice(self.unused_coor)
                    self.unused_coor.remove(rcoor)
                    self.board[rcoor[0]][rcoor[1]] = c[rroom][2]
                if len(self.walls_coor) > 4:
                    for i in range(len(self.walls_coor) // 3):
                        rcoor = random.choice(self.walls_coor)
                        self.board[rcoor[0]][rcoor[1]] = "004"
                        self.walls_coor.remove(rcoor)
                    for i in range(len(self.walls_coor) // 3):
                        rcoor = random.choice(self.walls_coor)
                        self.board[rcoor[0]][rcoor[1]] = "003"
                        self.walls_coor.remove(rcoor)

        def spawn(r):
            for i in range(r):
                for j in range(r):
                    if self.board[j][i] == '000':
                        return i, j

        def osmotr(x, y, r):
            print(x, y)
            if 0 <= x < r and 0 <= y - 1 < r and w[x][y - 1] == '000':
                w[x][y - 1] = '1'
                edinici.append([x, y - 1])
                # print('1')
            if 0 <= x + 1 < r and 0 <= y < r and w[x + 1][y] == '000':
                w[x + 1][y] = '1'
                edinici.append([x + 1, y])
                # print('2')

            if 0 <= x < r and 0 <= y + 1 < r and w[x][y + 1] == '000':
                w[x][y + 1] = '1'
                edinici.append([x, y + 1])

                # print('3')

            if 0 <= x - 1 < r and 0 <= y < r and w[x - 1][y] == '000':
                w[x - 1][y] = '1'
                edinici.append([x - 1, y])

        def vivod(q):
            for i in q:
                print(*i)
            print()

        nice_gen = True
        walls_gen()
        while nice_gen:
            result = self.WIDTH * self.WIDTH - col_sten
            edinici = list()
            x, y = spawn(self.WIDTH)
            w = copy.deepcopy(self.board)
            w[y][x] = '  2'
            osmotr(y, x, self.WIDTH)
            while len(edinici) != 0:
                y2, x2 = edinici[0]
                osmotr(y2, x2, self.WIDTH)
                w[y2][x2] = '  2'
                r_lis = [y2, x2]
                edinici.remove(r_lis)
            vivod(w)
            check = True
            for i in range(self.WIDTH):
                for j in range(self.WIDTH):
                    if w[i][j] == '000':
                        check = False
            if check:
                nice_gen = False
                generate()
            else:
                walls_gen()
        print(*self.board, sep='\n')
        print(*self.color_board, sep='\n')

    def color_remove(self, cell):
        rx = cell[0]
        ry = cell[1]
        self.color_board[rx][ry] = "black"

    def render(self, screen):
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                pygame.draw.rect(screen, pygame.Color("white"),
                                 pygame.Rect(self.left + i * self.cell_size, self.top + j * self.cell_size,
                                             self.cell_size, self.cell_size), 1)
                if self.color_board[j][i] == "white":
                    pygame.draw.rect(screen, pygame.Color(self.color_board[j][i]),
                                     pygame.Rect(self.left + i * self.cell_size + 1, self.top + j * self.cell_size + 1,
                                                 self.cell_size - 1, self.cell_size - 1))

    def on_click(self, cell):
        if cell:
            color = "white"
            if self.color_board[cell[1]][cell[0]] != "red":
                self.color_board[cell[1]][cell[0]] = color

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if self.left <= x < self.left + self.WIDTH * self.cell_size and self.top <= y < self.top + self.HEIGHT * self.cell_size:
            column = (x - self.left) // self.cell_size
            row = (y - self.top) // self.cell_size
            return (column, row)
        return None

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            return True
        else:
            return False

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


def load_image(name, transparent=False):
    fullname = os.path.join('resources', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


    return image


# Функция закрытия приложения
def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global musicon
    intro_text = ["LanigirO", "",
                  "Оффлайн игра",
                  "Настройки",
                  "Выход"]
    if musicon:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("resources/music1.mp3")
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    size = WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))

    pygame.display.set_caption('LanigirO')
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
                if text_out[3][1].x <= mouse[0] <= text_out[3][1].x + text_out[3][1].w and \
                        text_out[3][1].y <= mouse[1] <= text_out[3][1].y + text_out[3][1].h:
                    settings()
                elif text_out[-1][1].x <= mouse[0] <= text_out[-1][1].x + text_out[-1][1].w and \
                        text_out[-1][1].y <= mouse[1] <= text_out[-1][1].y + text_out[-1][1].h:
                    terminate()
                elif text_out[2][1].x <= mouse[0] <= text_out[2][1].x + text_out[2][1].w and \
                        text_out[2][1].y <= mouse[1] <= text_out[2][1].y + text_out[2][1].h:
                    level_settings()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(int(FPS))


def settings():
    global musicon
    intro_text = ["Музыка ВКЛ/ВЫКЛ",
                  "Выход"]

    size = WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 50)
    text_coord = 90
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
        if not musicon:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if text_out[-1][1].x <= mouse[0] <= text_out[-1][1].x + text_out[-1][1].w and \
                        text_out[-1][1].y <= mouse[1] <= text_out[-1][1].y + text_out[-1][1].h:
                    screen.fill(pygame.Color("black"))
                    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
                    screen.blit(fon, (0, 0))
                    return
                elif text_out[0][1].x <= mouse[0] <= text_out[0][1].x + text_out[0][1].w and \
                        text_out[0][1].y <= mouse[1] <= text_out[0][1].y + text_out[0][1].h:
                    if musicon:
                        musicon = False
                    else:
                        musicon = True

        pygame.display.flip()
        clock.tick(int(FPS))


def level_settings():
    intro_text = ["Размеры лабиринта:", "<", "7x7", ">",
                  "Количество стен:", "<", "10", ">",
                  "Количество игроков:", "<", "1", ">",
                  "Назад"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 30)
    text_coordy = 50
    text_coordx = 10
    text_out = []
    for line in intro_text:
        if intro_text.index(line) % 4 == 0:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coordy += 10
            intro_rect.x = 10
            if intro_text.index(line) != 0:
                text_coordy += intro_rect.height
            intro_rect.top = text_coordy
            text_coordx = intro_rect.width
            screen.blit(string_rendered, intro_rect)
            text_out.append((string_rendered, intro_rect))
        else:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coordx += 30
            intro_rect.top = text_coordy
            intro_rect.x = text_coordx
            text_coordx += intro_rect.width
            screen.blit(string_rendered, intro_rect)
            text_out.append([string_rendered, intro_rect])

    font2 = pygame.font.Font(None, 50)
    start_button = font2.render("Начать игру!", 1, pygame.Color('red'))
    intro_rect2 = start_button.get_rect()
    text_coordy += 10
    intro_rect2.x = 10
    text_coordy += intro_rect2.height
    intro_rect2.top = text_coordy
    text_coordx = intro_rect2.width
    screen.blit(start_button, intro_rect2)
    players_amount = int(intro_text[10])
    walls_amount = int(intro_text[6])
    dimensions_board = int(intro_text[2][0])
    while True:
        if not musicon:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if text_out[-1][1].x <= mouse[0] <= text_out[-1][1].x + text_out[-1][1].w and \
                        text_out[-1][1].y <= mouse[1] <= text_out[-1][1].y + text_out[-1][1].h:
                    screen.fill(pygame.Color("black"))
                    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
                    screen.blit(fon, (0, 0))
                    return

                #  размер доски
                elif text_out[1][1].x <= mouse[0] <= text_out[1][1].x + text_out[1][1].w and \
                        text_out[1][1].y <= mouse[1] <= text_out[1][1].y + text_out[1][1].h:
                    if dimensions_board - 1 != 6:
                        dimensions_board -= 1
                        screen.fill(pygame.Color("white"),
                                    (text_out[2][1].x, text_out[2][1].y, text_out[2][1].w, text_out[2][1].h))
                        text_out[2][0] = font.render(f"{dimensions_board}x{dimensions_board}", 1, pygame.Color('black'))
                        text_out[2][1].w = text_out[2][0].get_width()
                        text_out[2][1].h = text_out[2][0].get_height()
                        if walls_amount > dimensions_board ** 2 // 2:
                            walls_amount = dimensions_board ** 2 // 2
                            screen.fill(pygame.Color("white"),
                                        (text_out[6][1].x, text_out[6][1].y, text_out[6][1].w, text_out[6][1].h))
                            text_out[6][0] = font.render(f"{walls_amount}", 1, pygame.Color('black'))
                            text_out[6][1].w = text_out[6][0].get_width()
                            text_out[6][1].h = text_out[6][0].get_height()
                            screen.blit(text_out[6][0], text_out[6][1])

                        if players_amount > dimensions_board ** 2 // 5:
                            players_amount = dimensions_board ** 2 // 5
                            screen.fill(pygame.Color("white"),
                                        (text_out[10][1].x, text_out[10][1].y, text_out[10][1].w, text_out[10][1].h))
                            text_out[10][0] = font.render(f"{players_amount}", 1, pygame.Color('black'))
                            text_out[10][1].w = text_out[10][0].get_width()
                            text_out[10][1].h = text_out[10][0].get_height()
                            screen.blit(text_out[10][0], text_out[10][1])

                        screen.blit(text_out[2][0], text_out[2][1])

                elif text_out[3][1].x <= mouse[0] <= text_out[3][1].x + text_out[3][1].w and \
                        text_out[3][1].y <= mouse[1] <= text_out[1][1].y + text_out[3][1].h:
                    if dimensions_board + 1 != 16:
                        dimensions_board += 1
                        screen.fill(pygame.Color("white"),
                                    (text_out[2][1].x, text_out[2][1].y, text_out[2][1].w, text_out[2][1].h))
                        text_out[2][0] = font.render(f"{dimensions_board}x{dimensions_board}", 1, pygame.Color('black'))
                        text_out[2][1].w = text_out[2][0].get_width()
                        text_out[2][1].h = text_out[2][0].get_height()
                        screen.blit(text_out[2][0], text_out[2][1])

                #  количество стен
                elif text_out[5][1].x <= mouse[0] <= text_out[5][1].x + text_out[5][1].w and \
                        text_out[5][1].y <= mouse[1] <= text_out[5][1].y + text_out[5][1].h:
                    if walls_amount - 1 != -1:
                        walls_amount -= 1
                        screen.fill(pygame.Color("white"),
                                    (text_out[6][1].x, text_out[6][1].y, text_out[6][1].w, text_out[6][1].h))
                        text_out[6][0] = font.render(f"{walls_amount}", 1, pygame.Color('black'))
                        text_out[6][1].w = text_out[6][0].get_width()
                        text_out[6][1].h = text_out[6][0].get_height()
                        screen.blit(text_out[6][0], text_out[6][1])

                elif text_out[7][1].x <= mouse[0] <= text_out[7][1].x + text_out[7][1].w and \
                        text_out[7][1].y <= mouse[1] <= text_out[7][1].y + text_out[7][1].h:
                    if walls_amount + 1 < dimensions_board ** 2 // 2:
                        walls_amount += 1
                        screen.fill(pygame.Color("white"),
                                    (text_out[6][1].x, text_out[6][1].y, text_out[6][1].w, text_out[6][1].h))
                        text_out[6][0] = font.render(f"{walls_amount}", 1, pygame.Color('black'))
                        text_out[6][1].w = text_out[6][0].get_width()
                        text_out[6][1].h = text_out[6][0].get_height()
                        screen.blit(text_out[6][0], text_out[6][1])

                #  Кол-во игроков
                elif text_out[9][1].x <= mouse[0] <= text_out[9][1].x + text_out[9][1].w and \
                        text_out[9][1].y <= mouse[1] <= text_out[9][1].y + text_out[9][1].h:
                    if players_amount - 1 != 0:
                        players_amount -= 1
                        screen.fill(pygame.Color("white"),
                                    (text_out[10][1].x, text_out[10][1].y, text_out[10][1].w, text_out[10][1].h))
                        text_out[10][0] = font.render(f"{players_amount}", 1, pygame.Color('black'))
                        text_out[10][1].w = text_out[10][0].get_width()
                        text_out[10][1].h = text_out[10][0].get_height()
                        screen.blit(text_out[10][0], text_out[10][1])

                elif text_out[11][1].x <= mouse[0] <= text_out[11][1].x + text_out[11][1].w and \
                        text_out[11][1].y <= mouse[1] <= text_out[11][1].y + text_out[11][1].h:
                    if players_amount + 1 < dimensions_board ** 2 // 5:
                        players_amount += 1
                        screen.fill(pygame.Color("white"),
                                    (text_out[10][1].x, text_out[10][1].y, text_out[10][1].w, text_out[10][1].h))
                        text_out[10][0] = font.render(f"{players_amount}", 1, pygame.Color('black'))
                        text_out[10][1].w = text_out[10][0].get_width()
                        text_out[10][1].h = text_out[10][0].get_height()
                        screen.blit(text_out[10][0], text_out[10][1])

                #  начало игры
                elif intro_rect2.x <= mouse[0] <= intro_rect2.x + intro_rect2.w and \
                        intro_rect2.y <= mouse[1] <= intro_rect2.y + intro_rect2.h:
                    ss = Game(dimensions_board, walls_amount, players_amount)
                    ss.spawn_choose()

        pygame.display.flip()
        clock.tick(int(FPS))


class Knight(pygame.sprite.Sprite):


    def __init__(self):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__()
        Idle_image = load_image("_Idle.png")
        self.image = Idle_image
        self.rect = self.image.get_rect()
        self.rect.x = 180
        self.rect.y = 160

        self.run_images = []
        self.run_images.append(pygame.image.load('resources/Run_images/_Run_0.png'))
        self.run_images.append(pygame.image.load('resources/Run_images/_Run_1.png'))
        self.run_images.append(pygame.image.load('resources/Run_images/_Run_2.png'))
        self.run_images.append(pygame.image.load('resources/Run_images/_Run_3.png'))
        self.run_images.append(pygame.image.load('resources/Run_images/_Run_4.png'))
        self.run_images.append(pygame.image.load('resources/Run_images/_Run_5.png'))
        self.run_images.append(pygame.image.load('resources/Run_images/_Run_6.png'))
        self.run_images.append(pygame.image.load('resources/Run_images/_Run_7.png'))
        self.run_images.append(pygame.image.load('resources/Run_images/_Run_8.png'))
        self.run_images.append(pygame.image.load('resources/Run_images/_Run_9.png'))
        self.run_index = 0

    def update(self, state):
        if state == "runs":
            self.run_index += 1
            if self.run_index >= len(self.run_images):
                self.run_index = 0
            self.image = self.run_images[self.run_index]
        elif state == "run":
            self.image = load_image("_Run.png")
        elif state == "ok":
            self.image = load_image("_Idle.png")
        else:
            self.image = load_image("_Death.png")


class Game:

    def __init__(self, dim, walls, players):
        global musicon
        self.diff_out = []
        self.dim = dim
        self.walls = walls
        self.chat_coordy = 520
        self.players = players
        self.endgame = False
        self.main_field = Board(self.dim, self.dim, self.walls)
        print(*self.main_field.board, sep="\n")
        self.players_info = []
        if musicon:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load("resources/music2.mp3")
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        for i in range(1, self.players + 1):
            pl_pos = (None, None)
            items = []
            status = "ok"
            self.players_info.append([f'Игрок {i}', pl_pos, items, status])
        self.choosing_player = 1

    def spawn_choose(self):
        size = WIDTH, HEIGHT = 1200, 700
        screen = pygame.display.set_mode(size)
        fon = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(f"Игрок {self.choosing_player} выбирает точку появления", 1,
                                      pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coordx = (1200 - intro_rect.width) // 2
        intro_rect.top = 30
        intro_rect.x = text_coordx
        text_coordx += intro_rect.width
        screen.blit(string_rendered, intro_rect)
        self.main_field.render(screen)
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.main_field.get_click(event.pos):
                        celling = self.main_field.get_cell(event.pos)
                        if self.main_field.color_board[celling[1]][celling[0]] != "red" and celling:
                            self.players_info[self.choosing_player - 1][1] = celling
                            screen.blit(fon, (0, 0))
                            self.choosing_player += 1
                            if self.choosing_player > self.players:
                                self.main_gameprocess()
                            else:
                                string_rendered = font.render(f"Игрок {self.choosing_player} выбирает точку появления",
                                                              1, pygame.Color('white'))
                                intro_rect = string_rendered.get_rect()
                                text_coordx = (1200 - intro_rect.width) // 2
                                intro_rect.top = 30
                                intro_rect.x = text_coordx
                                text_coordx += intro_rect.width
                                screen.blit(string_rendered, intro_rect)
                                self.main_field.render(screen)
                                pygame.display.flip()
                pygame.display.flip()

    def respawn(self, player):
        for i in range(self.dim):
            for j in range(self.dim):
                if self.main_field.board[i][j] == "005":
                    player[1] = (j, i)
                    self.chat.append(f"{player[0]} был убит монстром.")
                    my_group.update("death")
                    rect_1 = pygame.Rect(240, 240, 100, 80)
                    pygame.draw.rect(screen, (255, 255, 255), rect_1)
                    my_group.draw(screen)
                    if player[2]:
                        new_coor = random.choice(self.main_field.unused_coor)
                        self.main_field.board[new_coor[0]][new_coor[1]] = "006"
                        self.chat.append(f"{player[0]} потерял ключ. Ключ появился в случайной клетке.")

    def win_screen(self):
        if musicon:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load("resources/music3.mp3")
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        size = WIDTH, HEIGHT = 1200, 700
        screen = pygame.display.set_mode(size)
        fon = pygame.transform.scale(load_image('fon3.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        pygame.display.flip()
        font = pygame.font.Font(None, 100)
        string_rendered1 = font.render(f"Игрок {self.choosing_player} Выбрался!", 1,
                                      pygame.Color('white'))
        intro_rect1 = string_rendered1.get_rect()
        text_coordx = (1200 - intro_rect1.width) // 2
        intro_rect1.top = 30
        intro_rect1.x = text_coordx
        screen.blit(string_rendered1, intro_rect1)
        pygame.display.flip()
        self.endgame = True
        font = pygame.font.Font(None, 70)
        string_rendered2 = font.render(f"Выйти в меню", 1,
                                      pygame.Color('white'))
        intro_rect2 = string_rendered2.get_rect()
        text_coordx = (1200 - intro_rect2.width) // 2
        intro_rect2.top = 600
        intro_rect2.x = text_coordx
        screen.blit(string_rendered2, intro_rect2)
        text_out = []
        text_out.append((string_rendered2, intro_rect2))
        pygame.display.flip()
        while True:
            pygame.display.flip()
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if text_out[0][1].x <= mouse[0] <= text_out[0][1].x + text_out[0][1].w and \
                            text_out[0][1].y <= mouse[1] <= text_out[0][1].y + text_out[0][1].h:
                        start_screen()
                        return
            my_group.update("runs")
            screen.blit(fon, (0, 0))
            screen.blit(string_rendered1, intro_rect1)
            screen.blit(string_rendered2, intro_rect2)
            my_sprite.rect = pygame.Rect((1200 - my_sprite.rect.width) // 2 - 95, 100, 280, 180)
            my_group.draw(screen)
            clock.tick(20)

    def check_tile(self, player, tile, dir_ind):
        pos = tile
        if self.main_field.board[pos[1]][pos[0]] == "003":
            if player[3] == "rubber":
                player[3] = "ok"
            self.respawn(player)
        elif self.main_field.board[pos[1]][pos[0]] == "004":
            if dir_ind == 0:
                exit_dir = 3
                player[3] = "rubber"
                player.append(exit_dir)
            elif dir_ind == 1:
                exit_dir = 2
                player[3] = "rubber"
                player.append(exit_dir)
            elif dir_ind == 2:
                exit_dir = 1
                player[3] = "rubber"
                player.append(exit_dir)
            elif dir_ind == 3:
                exit_dir = 0
                player[3] = "rubber"
                player.append(exit_dir)
            my_group.update("run")
            rect_1 = pygame.Rect(240, 240, 100, 80)
            pygame.draw.rect(screen, (255, 255, 255), rect_1)
            my_group.draw(screen)
        elif self.main_field.board[pos[1]][pos[0]] == "006":
            if player[3] == "rubber":
                player[3] = "ok"
            player[2].append("key")
            self.chat.append(f"{player[0]} нашел ключ.")
            self.chat_render()
            self.main_field.board[pos[1]][pos[0]] = "000"
            my_group.update("run")
            rect_1 = pygame.Rect(240, 240, 100, 80)
            pygame.draw.rect(screen, (255, 255, 255), rect_1)
            my_group.draw(screen)
        elif self.main_field.board[pos[1]][pos[0]] == "007":
            if player[3] == "rubber":
                player[3] = "ok"
            if player[2]:  # win четотам
                self.win_screen()
                return True
            else:
                self.chat.append(f"{player[0]} нашел выход, но нету ключа...")
                self.chat_render()
                my_group.update("run")
                rect_1 = pygame.Rect(240, 240, 100, 80)
                pygame.draw.rect(screen, (255, 255, 255), rect_1)
                my_group.draw(screen)
        elif self.main_field.board[pos[1]][pos[0]] == "008":
            if player[3] == "rubber":
                player[3] = "ok"
            self.chat.append(f"{player[0]} угодил в тюрьму. (Пропуск 1 хода)")
            my_group.update("death")
            rect_1 = pygame.Rect(240, 240, 100, 80)
            pygame.draw.rect(screen, (255, 255, 255), rect_1)
            my_group.draw(screen)
            self.chat_render()
            player[3] = "jail"
        else:
            my_group.update("run")
            rect_1 = pygame.Rect(240, 240, 100, 80)
            pygame.draw.rect(screen, (255, 255, 255), rect_1)
            my_group.draw(screen)

    def chat_render(self):
        self.chat_coordy = 520
        pygame.draw.rect(screen, (0, 0, 0),
                         (700, 150, 500, 400))
        font = pygame.font.Font(None, 30)
        rendered_chat = 0
        for line in self.chat[::-1]:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 700
            intro_rect.top = self.chat_coordy
            self.chat_coordy -= 40
            rendered_chat += 1
            screen.blit(string_rendered, intro_rect)
            pygame.display.flip()
            if rendered_chat + 1 > 10:
                pygame.display.flip()
                return
        pygame.display.flip()

    def turn_change(self):
        if self.choosing_player + 1 > self.players:
            pygame.time.wait(2000)
            self.choosing_player = 1
            pygame.draw.rect(screen, (0, 0, 0),
                             (0, 0, 1200, 700))
            font = pygame.font.Font(None, 100)
            string_rendered = font.render(f"Переход хода..", 1,
                                          pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coordx = (1200 - intro_rect.width) // 2
            text_coordy = (700 - intro_rect.h) // 2
            intro_rect.top = text_coordy
            intro_rect.x = text_coordx
            screen.blit(string_rendered, intro_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            self.scr_render()
            self.chat_render()
            pygame.display.flip()
        else:
            pygame.time.wait(2000)
            self.choosing_player += 1
            pygame.draw.rect(screen, (0, 0, 0),
                             (0, 0, 1200, 700))
            font = pygame.font.Font(None, 100)
            string_rendered = font.render(f"Переход хода..", 1,
                                          pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coordx = (1200 - intro_rect.width) // 2
            text_coordy = (700 - intro_rect.h) // 2
            intro_rect.top = text_coordy
            intro_rect.x = text_coordx
            screen.blit(string_rendered, intro_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            self.scr_render()
            self.chat_render()
            pygame.display.flip()

    def scr_render(self):
        WIDTH, HEIGHT = 1200, 700
        fon = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 80)
        string_rendered = font.render(f"Игрок {self.choosing_player} делает ход", 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coordx = (1200 - intro_rect.width) // 2
        intro_rect.top = 30
        intro_rect.x = text_coordx
        text_coordx += intro_rect.width
        screen.blit(string_rendered, intro_rect)
        string_rendered = font.render(f"Пауза", 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 500
        intro_rect.x = 50
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        intro_text = ["Вверх",
                      "Влево", "Вправо",
                      "Вниз"]
        font = pygame.font.Font(None, 90)
        pygame.display.flip()
        self.text_out = []
        self.diff_out = []
        self.diff_out.append((string_rendered, intro_rect))
        text_coordy = 150
        text_coordx = 200
        for line in intro_text:
            if intro_text.index(line) == 0:
                string_rendered = font.render(line, 1, pygame.Color('black'))
                intro_rect = string_rendered.get_rect()
                intro_rect.x = text_coordx
                intro_rect.top = text_coordy
                pygame.draw.rect(screen, (255, 255, 255),
                                 (intro_rect.x, intro_rect.y, intro_rect.w, intro_rect.h))
                screen.blit(string_rendered, intro_rect)
                self.text_out.append((string_rendered, intro_rect))
                pygame.display.flip()
            elif intro_text.index(line) == 1:
                string_rendered = font.render(line, 1, pygame.Color('black'))
                intro_rect = string_rendered.get_rect()
                intro_rect.x = text_coordx - intro_rect.w
                text_coordy += intro_rect.height + 50
                intro_rect.top = text_coordy
                pygame.draw.rect(screen, (255, 255, 255),
                                 (intro_rect.x, intro_rect.y, intro_rect.w, intro_rect.h))
                screen.blit(string_rendered, intro_rect)
                self.text_out.append((string_rendered, intro_rect))
                pygame.display.flip()
            elif intro_text.index(line) == 2:
                string_rendered = font.render(line, 1, pygame.Color('black'))
                intro_rect = string_rendered.get_rect()
                intro_rect.x = text_coordx + self.text_out[1][1].w
                intro_rect.top = text_coordy
                pygame.draw.rect(screen, (255, 255, 255),
                                 (intro_rect.x, intro_rect.y, intro_rect.w, intro_rect.h))
                screen.blit(string_rendered, intro_rect)
                self.text_out.append((string_rendered, intro_rect))
                pygame.display.flip()
            elif intro_text.index(line) == 3:
                string_rendered = font.render(line, 1, pygame.Color('black'))
                intro_rect = string_rendered.get_rect()
                intro_rect.x = text_coordx + ((self.text_out[0][1].w - intro_rect.w) // 2)
                intro_rect.top = text_coordy + intro_rect.h + 50
                pygame.draw.rect(screen, (255, 255, 255),
                                 (intro_rect.x, intro_rect.y, intro_rect.w, intro_rect.h))
                screen.blit(string_rendered, intro_rect)
                self.text_out.append((string_rendered, intro_rect))
                pygame.display.flip()
        my_group.update("ok")
        rect_1 = pygame.Rect(240, 240, 100, 80)
        pygame.draw.rect(screen, (255, 255, 255), rect_1)
        my_group.draw(screen)

    def main_gameprocess(self):
        self.choosing_player = 1
        self.chat = []

        def move_up(pos):
            self.chat.append(f"{player[0]} прошел клетку.")
            self.chat_render()
            self.players_info[self.choosing_player - 1][1] = (pos[0], pos[1] - 1)
            pos = self.players_info[self.choosing_player - 1][1]
            self.check_tile(player, pos, self.text_out.index(direction))
            if self.endgame:
                return
            self.chat_render()
            self.turn_change()

        def move_left(pos):
            self.chat.append(f"{player[0]} прошел клетку.")
            self.chat_render()
            self.players_info[self.choosing_player - 1][1] = (pos[0] - 1, pos[1])
            pos = self.players_info[self.choosing_player - 1][1]
            self.check_tile(player, pos, self.text_out.index(direction))
            if self.endgame:
                return
            self.chat_render()
            self.turn_change()

        def move_right(pos):
            self.chat.append(f"{player[0]} прошел клетку.")
            self.chat_render()
            self.players_info[self.choosing_player - 1][1] = (pos[0] + 1, pos[1])
            pos = self.players_info[self.choosing_player - 1][1]
            self.check_tile(player, pos, self.text_out.index(direction))
            if self.endgame:
                return
            self.chat_render()
            self.turn_change()

        def move_down(pos):
            self.chat.append(f"{player[0]} прошел клетку.")
            self.chat_render()
            self.players_info[self.choosing_player - 1][1] = (pos[0], pos[1] + 1)
            pos = self.players_info[self.choosing_player - 1][1]
            self.check_tile(player, pos, self.text_out.index(direction))
            if self.endgame:
                return
            self.chat_render()
            self.turn_change()

        def skip_turn():
            pygame.draw.rect(screen, (0, 0, 0),
                             (0, 0, 1200, 700))
            font = pygame.font.Font(None, 100)
            string_rendered = font.render(f"{player[0]} пропускает ход.", 1,
                                          pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coordx = (1200 - intro_rect.width) // 2
            text_coordy = (700 - intro_rect.h) // 2
            intro_rect.top = text_coordy
            intro_rect.x = text_coordx
            screen.blit(string_rendered, intro_rect)
            pygame.display.flip()
            player[3] = "ok"
            self.turn_change()

        def pause_menu():
            intro_text = ["Вернуться в игру",
                          "В меню"]

            WIDTH, HEIGHT = 1200, 700
            font = pygame.font.Font(None, 90)
            fon = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))
            text_coordyy = 50
            text_coordxx = 10
            text_out = []
            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coordxx += 10
                intro_rect.top = text_coordyy
                intro_rect.x = 10
                text_coordyy += intro_rect.height
                screen.blit(string_rendered, intro_rect)
                text_out.append((string_rendered, intro_rect))
            pygame.display.flip()
            while True:
                pygame.display.flip()
                mouse = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if text_out[0][1].x <= mouse[0] <= text_out[0][1].x + text_out[0][1].w and \
                                text_out[0][1].y <= mouse[1] <= text_out[0][1].y + text_out[0][1].h:
                            return
                        elif text_out[1][1].x <= mouse[0] <= text_out[1][1].x + text_out[1][1].w and \
                                text_out[1][1].y <= mouse[1] <= text_out[1][1].y + text_out[1][1].h:
                            start_screen()
                pygame.display.flip()

        def get_button(pos):
            x, y = pos
            for line in self.text_out:
                if line[1].left <= x < line[1].left + line[1].w and line[1].top <= y < line[1].top + line[1].h:
                    button = line
                    return button
            return None

        self.scr_render()
        self.chat_render()
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                pygame.display.flip()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    direction = get_button(event.pos)
                    if direction:
                        if self.text_out.index(direction) == 0:
                            player = self.players_info[self.choosing_player - 1]
                            pos = self.players_info[self.choosing_player - 1][1]
                            if player[3] == "ok":
                                if self.main_field.board[pos[1] - 1][pos[0]] != "002" and pos[1] - 1 >= 0:
                                    move_up(pos)
                                    if self.endgame:
                                        return
                            elif player[3] == "jail":
                                skip_turn()
                            elif player[3] == "rubber":
                                if self.text_out.index(direction) == player[4]:
                                    pos = self.players_info[self.choosing_player - 1][1]
                                    self.chat.append(f"{player[0]} вышел из резиновой комнаты...")
                                    move_up(pos)
                                    if self.endgame:
                                        return
                                else:
                                    self.chat.append(f"{player[0]} прошел клетку.")
                                    my_group.update("run")
                                    rect_1 = pygame.Rect(240, 240, 100, 80)
                                    pygame.draw.rect(screen, (255, 255, 255), rect_1)
                                    my_group.draw(screen)
                                    self.chat_render()
                                    self.turn_change()

                        elif self.text_out.index(direction) == 1:
                            player = self.players_info[self.choosing_player - 1]
                            pos = self.players_info[self.choosing_player - 1][1]
                            if player[3] == "ok":
                                if self.main_field.board[pos[1]][pos[0] - 1] != "002" and pos[0] - 1 >= 0:
                                    move_left(pos)
                                    if self.endgame:
                                        return
                            elif player[3] == "jail":
                                skip_turn()
                            elif player[3] == "rubber":
                                if self.text_out.index(direction) == player[4]:
                                    pos = self.players_info[self.choosing_player - 1][1]
                                    self.chat.append(f"{player[0]} вышел из резиновой комнаты...")
                                    move_left(pos)
                                    if self.endgame:
                                        return
                                else:
                                    self.chat.append(f"{player[0]} прошел клетку.")
                                    my_group.update("run")
                                    rect_1 = pygame.Rect(240, 240, 100, 80)
                                    pygame.draw.rect(screen, (255, 255, 255), rect_1)
                                    my_group.draw(screen)
                                    self.chat_render()
                                    self.turn_change()

                        elif self.text_out.index(direction) == 2:
                            player = self.players_info[self.choosing_player - 1]
                            pos = self.players_info[self.choosing_player - 1][1]
                            if player[3] == "ok":
                                if pos[0] + 1 < self.dim:
                                    if self.main_field.board[pos[1]][pos[0] + 1] != "002":
                                        move_right(pos)
                                        if self.endgame:
                                            return
                            elif player[3] == "jail":
                                skip_turn()
                            elif player[3] == "rubber":
                                if self.text_out.index(direction) == player[4]:
                                    pos = self.players_info[self.choosing_player - 1][1]
                                    self.chat.append(f"{player[0]} вышел из резиновой комнаты...")
                                    move_right(pos)
                                    if self.endgame:
                                        return
                                else:
                                    self.chat.append(f"{player[0]} прошел клетку.")
                                    my_group.update("run")
                                    rect_1 = pygame.Rect(240, 240, 100, 80)
                                    pygame.draw.rect(screen, (255, 255, 255), rect_1)
                                    my_group.draw(screen)
                                    self.chat_render()
                                    self.turn_change()

                        elif self.text_out.index(direction) == 3:
                            player = self.players_info[self.choosing_player - 1]
                            pos = self.players_info[self.choosing_player - 1][1]
                            if player[3] == "ok":
                                if pos[1] + 1 < self.dim:
                                    if self.main_field.board[pos[1] + 1][pos[0]] != "002":
                                        move_down(pos)
                                        if self.endgame:
                                            return
                            elif player[3] == "jail":
                                skip_turn()
                            elif player[3] == "rubber":
                                if self.text_out.index(direction) == player[4]:
                                    pos = self.players_info[self.choosing_player - 1][1]
                                    self.chat.append(f"{player[0]} вышел из резиновой комнаты...")
                                    move_down(pos)
                                    if self.endgame:
                                        return
                                else:
                                    self.chat.append(f"{player[0]} прошел клетку.")
                                    my_group.update("run")
                                    rect_1 = pygame.Rect(240, 240, 100, 80)
                                    pygame.draw.rect(screen, (255, 255, 255), rect_1)
                                    my_group.draw(screen)
                                    self.chat_render()
                                    self.turn_change()
                    elif self.diff_out[0][1].x <= mouse[0] <= self.diff_out[0][1].x + self.diff_out[0][1].w and \
                            self.diff_out[0][1].y <= mouse[1] <= self.diff_out[0][1].y + self.diff_out[0][1].h:
                        pause_menu()
                        self.scr_render()
                        self.chat_render()
            clock.tick(20)

if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode(size)
    my_sprite = Knight()
    my_group = pygame.sprite.Group(my_sprite)
    FPS = 50  # количество кадров в секунду
    clock = pygame.time.Clock()

start_screen()

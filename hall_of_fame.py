import os
import sqlite3

import pygame

FPS = 10
all_sprites = pygame.sprite.Group()

class Table:
    # создание поля
    def __init__(self, width, height, output, gamer, score,):
        self.width = width
        self.height = height
        self.data = output
        self.gamer = gamer
        self.score = score
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 80
        self.top = 80
        self.cell_size = 65

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render_pic(self, gamer, score):  # рендерим все строчки в таблице
        font = pygame.font.Font('./font/CoreSans.ttf', 40)
        rendered = font.render(gamer + str(score), True, pygame.Color('#3C6371'))
        return rendered

    def render(self, screen):
        f1 = pygame.font.Font('./font/CoreSans.ttf', 32)
        screen.blit(self.render_pic('Результат: ' + self.gamer[:20] + ', ', self.score), (40, 20))
        for y in range(self.height):
            x = 0

            screen.blit(f1.render(str(self.data[y][x]), True, pygame.Color('#3C6371')),
                        (x * self.cell_size + 10 + self.left, y * self.cell_size + self.cell_size // 3 + self.top,
                         self.cell_size, self.cell_size))
            x = 1
            screen.blit(f1.render(str(self.data[y][x]), True, pygame.Color('#3C6371')),
                        (x * self.cell_size + 28 + self.left, y * self.cell_size + self.cell_size // 3 + self.top,
                         self.cell_size, self.cell_size))
            if str(self.data[y][x]) == self.gamer:
                pygame.draw.rect(screen, pygame.Color(50, 155, 55), (
                    0, y * self.cell_size + self.top, 730,
                    self.cell_size), 5, border_radius=10)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def load_image(name, color_key=None):
    fullname = os.path.join('img', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def main(score, gamer='Unknown'):
    connection = sqlite3.connect("./db/bingame2_score.db")
    cur = connection.cursor()

    # insert/update value
    if (gamer,) not in cur.execute(f"SELECT name FROM users").fetchall():
        cur.execute("INSERT INTO users VALUES (?,?)",
                    (cur.execute("SELECT max(id) FROM users").fetchone()[0] + 1, gamer))
        next_id = cur.execute("SELECT max(id) FROM userscore").fetchone()[0] + 1
        # max(id) не для сетевой версии из-за одновременных запросов пользователей
        name_to_insert = cur.execute(f'SELECT id FROM users WHERE name = "{gamer}"').fetchone()[0]
        cur.execute("INSERT INTO userscore VALUES (?,?,?)", (next_id, name_to_insert, score))

    name_to_update = cur.execute(f'SELECT id FROM users WHERE name = "{gamer}"').fetchone()[0]
    if score > cur.execute(f'SELECT * FROM userscore WHERE username = {name_to_update}').fetchone()[2]:
        cur.execute(f'UPDATE userscore SET userscore = {score} WHERE username = {name_to_update}')

    connection.commit()
    output = cur.execute('SELECT * FROM userscore ORDER BY userscore DESC').fetchall()
    data = []
    for e in range(len(output)):
        name = cur.execute(f'SELECT name FROM users WHERE id = {output[e][1]}').fetchone()[0]
        data.append((output[e][2], name,))

    connection.close()
    clock = pygame.time.Clock()
    board = Table(2, min(9, len(output)), data, gamer, score)
    size = 730, 730
    pygame.init()
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption('Binary Game FameHall')
    sprt = AnimatedSprite(load_image("pngegg.png"), 5, 5, 500, 500)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        fon = pygame.image.load('./img/ice_1.png')
        all_sprites.draw(screen)
        all_sprites.update()
        screen.blit(fon, (200, 0))
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main(333)

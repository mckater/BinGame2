import sqlite3

import pygame


class Table:
    # создание поля
    def __init__(self, width, height, output, gamer):
        self.width = width
        self.height = height
        self.data = output
        self.gamer = gamer
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

    def render(self, screen):
        for y in range(self.height):
            x = 0
            f1 = pygame.font.Font('./font/CoreSans.ttf', 32)
            screen.blit(f1.render(str(self.data[y][x]), 1, pygame.Color('#3C6371')),
                        (x * self.cell_size + 10 + self.left, y * self.cell_size + self.cell_size // 3 + self.top,
                         self.cell_size, self.cell_size))
            # pygame.draw.rect(screen, pygame.Color(50, 155, 55), (
            #     x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size + 15,
            #     self.cell_size), 2)
            x = 1
            f1 = pygame.font.Font('./font/CoreSans.ttf', 32)
            screen.blit(f1.render(str(self.data[y][x]), 1, pygame.Color('#3C6371')),
                        (x * self.cell_size + 28 + self.left, y * self.cell_size + self.cell_size // 3 + self.top,
                         self.cell_size, self.cell_size))
            if str(self.data[y][x]) == self.gamer:
                pygame.draw.rect(screen, pygame.Color(50, 155, 55), (
                    0, y * self.cell_size + self.top, 730,
                    self.cell_size), 5, border_radius=10)


def main(score, gamer):
    connection = sqlite3.connect("./db/bingame2_score.db")
    cur = connection.cursor()

    # insert/update value

    if (gamer,) not in cur.execute(f"SELECT name FROM users").fetchall():
        # решение школярское, рекомендуется использовать EXISTS
        cur.execute("INSERT INTO users VALUES (?,?)",
                    (cur.execute("SELECT max(id) FROM users").fetchone()[0] + 1, gamer))
        next_id = cur.execute("SELECT max(id) FROM userscore").fetchone()[0] + 1
        # max(id) не подойдёт для сетевой версии из-за одновременных запросов пользователей
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
    board = Table(2, min(9, len(output)), data, gamer)
    size = 730, 730
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption('Binary Game hello')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        fon = pygame.image.load('./img/metal.png')
        screen.blit(fon, (200, 0))
        board.render(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main(164, 'Student')

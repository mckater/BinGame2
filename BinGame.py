import sys

import hards
import itertools
import pygame
import random

import hello_user, hall_of_fame


class Board:
    # создание поля
    def __init__(self, width, height, level, username):
        self.level = level
        self.width = width
        self.height = height
        self.username = username
        self.board = [[0] * width for _ in range(height)]
        self.ii_matrix = [['0'] * width for _ in range(height)]
        # значения по умолчанию
        self.game_over = False
        self.cell_stop_list = list()  # блокируем уже решённые строки
        self.ones = pygame.sprite.Group()
        self.left = 35
        self.top = 100
        self.cell_size = 66
        self.colors = [pygame.Color("#006400"), pygame.Color("#fcbdcb"), pygame.Color("black"),
                       pygame.Color('#E0FFFF'), pygame.Color('#EEE8AA')]
        self.images = ['./img/ice_small.png', './img/2_7_128.png', './img/2_6_64.png', './img/2_5_32.png',
                       './img/2_4_16.png', './img/2_3_8.png', './img/2_2_4.png', './img/2_1_2.png', './img/2_0_1.png',
                       './img/ice_small.png']

    def render(self, screen):
        for y in range(1, self.height - 1):
            if self.board[y][9] != 0:
                flag = False
                for x in range(1, self.width - 1):
                    if self.board[y][x] == 1:
                        flag = True
                    if flag:
                        pygame.draw.rect(screen, self.colors[1], (
                            x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                            self.cell_size))
                    else:
                        pygame.draw.rect(screen, self.colors[self.board[y][x]], (
                            x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                            self.cell_size))

            else:
                for x in range(1, self.width - 1):
                    pygame.draw.rect(screen, self.colors[self.board[y][x]], (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                        self.cell_size))
        for x, y in itertools.product(range(1, self.width - 1), range(1, self.height - 1)):
            one_or_zero = './img/' + str(self.board[y][x]) + '.png'
            screen.blit(pygame.image.load(one_or_zero), (x * self.cell_size + self.left, y * self.cell_size + self.top))

        for x in range(0, self.width):
            if self.level < 4:
                pica = pygame.image.load(self.images[x])  # подсказки степени двойки
                x_pos = self.left + self.cell_size * x
                y_pos = self.top
                screen.blit(pica, (x_pos, y_pos))
                y_pos = self.top + self.cell_size * 8
                screen.blit(pica, (x_pos, y_pos))
        for y in range(1, self.height - 1):
            x = 0  # слева загаданные числа
            leftpic = self.render_pic(self.ii_matrix[y][x], self.colors[3])
            screen.blit(leftpic[0],
                        (self.left + self.cell_size - leftpic[1] - 10, y * self.cell_size + self.top))
            x = 9  # справа числа игрока
            screen.blit(self.render_pic(self.board[y][x], self.colors[4])[0],
                        (x * self.cell_size + self.left + 10, y * self.cell_size + self.top))
        # инфо-панель пользователя
        render_score = self.render_score()
        screen.blit(render_score[0], (730 - render_score[1] - 10, 20))
        if self.username:
            screen.blit(self.render_pic('Игрок: ' + self.username[:15], self.colors[4])[0], (20, 20))
        else:
            screen.blit(self.render_pic('Нет имени игрока', self.colors[4])[0], (730 // 4, 20))

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # cell - кортеж (x, y)
    def on_click(self, cell):  # с каждым кликом
        if cell not in self.cell_stop_list:
            self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2
            self.count_user_digit(cell[1])  # кликнул - пересчитывается его число
            if all([int(self.ii_matrix[cell[1]][i]) == self.board[cell[1]][i] for i in range(1, self.width - 1)]):
                self.ii_matrix[cell[1]][0] = '+'
                self.cell_stop_list.extend([(stop, cell[1]) for stop in range(1, self.width - 1)])
                for i in range(1, self.width - 1):
                    if self.board[cell[1]][i]:
                        x, y = i, cell[1]
                        hards.One(x * self.cell_size + self.left, y * self.cell_size + self.top, self.ones)
                        hards.score += 2 + 2 * self.level

            else:
                self.ii_matrix[cell[1]][0] = int(''.join(self.ii_matrix[cell[1]][1:9]), 2)
            if all([self.ii_matrix[y][0] == '+' for y in range(1, self.height - 1)]):
                pygame.draw.rect(pygame.display.set_mode((self.width * self.cell_size + self.left,
                                                          self.height * self.cell_size + self.top)), '#2F4F4F',
                                 (0, 0, self.width * self.cell_size + self.left,
                                  self.height * self.cell_size + self.top))
                main(self.level, self.username)  # отправляем игрока на старт_скрин, но с очками

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 1 or cell_x >= self.width - 1 or cell_y < 1 or cell_y >= self.height - 1:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def ii(self):
        for y in range(1, 9):
            if self.ii_matrix[y][0] != '+':
                if self.level > 1:
                    ones = random.randint(1, 6)
                else:
                    ones = self.level + 1
                while True:
                    new_digit = ['1'] * ones + ['0'] * (self.width - 2 - ones)
                    random.shuffle(new_digit)
                    if self.ii_matrix[y][1:9] not in self.ii_matrix:
                        self.ii_matrix[y][1:9] = new_digit
                        self.ii_how_many(y)  # десятичное загаданное число
                    if [['0'] * self.width for _ in range(self.height)] not in self.ii_matrix:
                        break

    def ii_how_many(self, y):
        self.ii_matrix[y][0] = int(''.join(self.ii_matrix[y][1:9]), 2)

    def count_user_digit(self, y):
        sm = ''
        for x in range(1, self.width - 1):
            sm += str(self.board[y][x])
        self.board[y][-1] = int(sm, 2)

    def render_pic(self, digit, color):
        font = pygame.font.Font(None, 64)
        rendered = font.render(str(digit), True, color)
        return rendered, rendered.get_width()

    def render_score(self):
        font = pygame.font.Font(None, 80)
        rendered_score = font.render(str(hards.score), True, '#E0FFFF')
        return rendered_score, rendered_score.get_width()


def terminate():
    pygame.quit()
    sys.exit()

def main(level, username):
    if level == 4:
        hall_of_fame.main(hards.score, username)
        terminate()
    level, username = hello_user.start_screen(level + 1, username)
    board = Board(10, 9, level, username)

    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    size = 730, 730
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Binary Game')

    board.ii()
    ices = pygame.sprite.Group()
    ices_to_add = [hards.Ice(board.left, board.top),
                   hards.Ice(board.left + board.cell_size * (board.width - 1), board.top),
                   hards.Ice(board.left, board.top + board.cell_size * (board.height - 1)),
                   hards.Ice(board.left + board.cell_size * (board.width - 1),
                             board.top + board.cell_size * (board.height - 1))]
    if level:
        for i in range(level):
            ices.add(ices_to_add[i])
    ices.draw(screen)

    running = True
    while running and not board.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
            if event.type == pygame.KEYUP:  # KEYUP удалит летающие льдышки
                ices.remove(*ices_to_add)  # раскомментировать, лазейка для тестировщика

        screen.fill(pygame.Color('#2F4F4F'))
        board.render(screen)
        ices.draw(screen)
        ices.update(size)
        board.ones.update(ices, board)
        board.ones.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


if __name__ == '__main__':
    main(-1, '')

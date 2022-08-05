import pygame, itertools, datetime, random


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.ii_matrix = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.game_over = False
        self.left = 35
        self.top = 50
        self.cell_size = 66
        self.images = [None, './img/2_7_128.png', './img/2_6_64.png', './img/2_5_32.png', './img/2_4_16.png',
                       './img/2_3_8.png', './img/2_2_4.png',  './img/2_1_2.png', './img/2_0_1.png', None]

    def render(self, screen):
        colors = [pygame.Color("#006400"), pygame.Color("#3CB371"), pygame.Color("black")]
        for y in range(1, self.height - 1):
            if self.board[y][9] != 0:
                flag = False
                for x in range(1, self.width - 1):
                    if self.board[y][x] == 1:
                        flag = True
                    if flag:
                        pygame.draw.rect(screen, colors[1], (
                            x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                            self.cell_size))
                    else:
                        pygame.draw.rect(screen, colors[self.board[y][x]], (
                            x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                            self.cell_size))

            else:
                for x in range(1, self.width - 1):
                    pygame.draw.rect(screen, colors[self.board[y][x]], (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                        self.cell_size))
        for x, y in itertools.product(range(1, self.width - 1), range(1, self.height - 1)):
            # pygame.draw.rect(screen, colors[self.board[y][x]], (
            #     x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
            #     self.cell_size))
            # pygame.draw.rect(screen, pygame.Color("white"), (
            #     x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
            #     self.cell_size), 1)
            one_or_zero = './img/' + str(self.board[y][x]) + '.png'
            screen.blit(pygame.image.load(one_or_zero), (x * self.cell_size + self.left, y * self.cell_size + self.top))

        for x in range(1, self.width - 1):
            pica = pygame.image.load(self.images[x])
            x_pos = self.left + self.cell_size * x
            y_pos = self.top
            screen.blit(pica, (x_pos, y_pos))
            y_pos = self.top + self.cell_size * 8
            screen.blit(pica, (x_pos, y_pos))
        for y in range(1, self.height - 1):
            x = 0
            screen.blit(self.render_digit_pic(self.ii_matrix[y][x], '#E0FFFF'),
                        (self.left, y * self.cell_size + self.top))
            x = 9
            screen.blit(self.render_digit_pic(self.board[y][x], '#EEE8AA'),
                        (x * self.cell_size + self.left, y * self.cell_size + self.top))


    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # cell - кортеж (x, y)
    def on_click(self, cell):
        self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2
        self.count_user_digit(cell[1])  # кликнул - пересчитывается его число
        print(cell[1])
        print(self.ii_matrix[cell[1]][0])
        print(self.board[cell[1]][-1])
        if self.ii_matrix[cell[1]][0] == self.board[cell[1]][-1]:
            self.ii_matrix[cell[1]] = ['~~'] + ['0'] * 8

        # self.ii()  # с каждым кликом формируем задание
        if self.board[cell[1]][cell[0]] == 1:
            print('Gotcha 1!')
        if self.board[cell[1]][cell[0]] == 0:
            print('Gotcha 0000000000!')

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
            if self.ii_matrix[y][0] == 0:
                new_digit = ['0', '0', '0', '0', '0', '1', '1', '1']  # усложнить, не 0
                random.shuffle(new_digit)
                self.ii_matrix[y] = new_digit
                self.ii_matrix[y][0] = int(''.join(self.ii_matrix[y][1:9]), 2)

    def count_user_digit(self, y):
        sm = ''
        for x in range(1, self.width - 1):
            sm += str(self.board[y][x])
        # print(y, self.ii_matrix[y], sm, int(sm, 2))
        self.board[y][-1] = int(sm, 2)

    def render_digit_pic(self, digit, color):
        font = pygame.font.Font(None, 80)
        return font.render(str(digit), True, color)


def main():
    pygame.init()
    start = datetime.datetime.now()
    size = 730, 730
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Binary Game +')

    board = Board(10, 9)
    board.ii()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill('#2F4F4F')
        board.render(screen)

        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()

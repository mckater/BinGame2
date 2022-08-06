import sys

import pygame

class Levels:
    # создание кнопок
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 470
        self.top = 80
        self.cell_size = 110

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                font = pygame.font.Font(None, 60)
                screen.blit(font.render(str(y) + '.lvl', 1, pygame.Color('orange')), (x * self.cell_size + 18 + self.left, y * self.cell_size + self.cell_size // 3 + self.top, self.cell_size,
                    self.cell_size))
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 3)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            return sum(cell)
        else:
            pass

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["Binary Game", "",
                  "Правила игры:",
                  "собирайте двоичные числа,",
                  "и будет Вам счастье",
                  "ВЫБОР УРОВНЯ - 0...4"]

    fon = pygame.image.load('./img/metal.png')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 36)
    text_coord = 60
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    levels = Levels(1, 5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = levels.get_click(event.pos)
                if click is None:
                    pass
                else:
                    return click
        levels.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


WIDTH, HEIGHT = size = 730, 730
pygame.init()
clock = pygame.time.Clock()
FPS = 50
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Binary Game')
start_screen()
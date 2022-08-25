import random
import pygame

ice_sprites = pygame.sprite.Group()
ones_sprites = pygame.sprite.Group()
score = 0

class One(pygame.sprite.Sprite):
    def __init__(self, x, y, group_of_ones):
        super().__init__(ones_sprites)
        self.image = pygame.image.load('./img/1_red.png')
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.rect = self.image.get_rect()
# перехватываем расположение каждой единички в угаданных числах
        self.rect.left = x
        self.rect.top = y
# 35, 66 и 100 можно бы передать из борды, но мы не собираемся менять размеры
# Можно так.
        self.cell_x = (x - 35) // 66
        self.cell_y = (y - 100) // 66

        self.add(group_of_ones)

    def update(self, group_of_ice, board):
        global score
        if pygame.sprite.spritecollideany(self, group_of_ice):

# заново считаем загаданное число
            board.ii_how_many(self.cell_y)
# разблокируем эту клетку для пользователя
            board.cell_stop_list.remove((self.cell_x, self.cell_y))
# у игрока эта его клетка - снова ноль
            board.board[self.cell_y][self.cell_x] = 0
            self.kill()
            score -= 5


class Ice(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(ice_sprites)
        self.ice_image = pygame.image.load('./img/ice.png')
        self.w = self.ice_image.get_width() // 30
        self.h = self.ice_image.get_height() // 30
        self.image = pygame.transform.scale(self.ice_image, (self.w, self.h))
        self.rect = self.image.get_rect()
# шаг спрайта определяем случайно, по сути это скорость
        self.vx = random.randint(-1, 1)
        self.vy = random.randrange(-1, 1)
# в начале льды в по углам
        self.rect.left = x
        self.rect.top = y

    def update(self, size):
        w, h = size
        self.rect = self.rect.move(self.vx, self.vy)  # шаг спрайта
        if self.rect.x > w - self.w or self.rect.x <= 0:
            self.vx = -self.vx
            self.image = pygame.transform.flip(self.image, True, False)
        if self.rect.y > h - self.h or self.rect.y <= 0:
            self.vy = -self.vy
            self.image = pygame.transform.flip(self.image, False, True)

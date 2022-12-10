import random
import pygame

ice_sprites = pygame.sprite.Group()
ones_sprites = pygame.sprite.Group()
score = 0


class One(pygame.sprite.Sprite):  # единичка
    def __init__(self, x, y, group_of_ones):
        super().__init__(ones_sprites)
        self.image = pygame.image.load('./img/1_red.png')
        self.collide_mask_pic = pygame.image.load('./img/collide_mask.png')
        self.collide_mask = pygame.mask.from_surface(self.collide_mask_pic)
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.rect = self.image.get_rect()
        # перехватываем расположение каждой единички в угаданных числах
        self.rect.left = x
        self.rect.top = y
        # 35, 66 и 100 можно бы передать из борды, но мы не собираемся менять размеры
        # Можно и так.
        self.cell_x = (x - 35) // 66
        self.cell_y = (y - 100) // 66

        self.add(group_of_ones)

    def update(self, group_of_ice, board):
        global score
        # if pygame.sprite.spritecollideany(self, group_of_ice):
        for el in group_of_ice:  # по льдинкам проверяем на столкновение
            if pygame.sprite.collide_mask(self, el):  # если столкнулось с 1-кой
                # заново считаем загаданное число
                board.ii_matrix[self.cell_y][0] = board.ii_how_many(board.ii_matrix[self.cell_y][1:9])
                # разблокируем эту клетку для пользователя
                board.cell_stop_list.remove((self.cell_x, self.cell_y))
                # у игрока эта его клетка - снова ноль
                board.board[self.cell_y][self.cell_x] = 0
                # и число игрока справа - пересчитывается
                board.count_user_digit(self.cell_y)
                self.kill()
                score -= 5


class Ice(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(ice_sprites)
        self.ice_image = pygame.image.load('./img/ice.png')
        self.w = self.ice_image.get_width() // 6
        self.h = self.ice_image.get_height() // 6
        self.image = pygame.transform.scale(self.ice_image, (self.w, self.h))
        self.rect = self.image.get_rect()
        # шаг спрайта - скорость
        self.vx = random.choice((-1.5, -1, 1, 1.5))
        self.vy = random.choice((-1.5, -1, 1, 1.5))
        print(self.vx, self.vy)
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

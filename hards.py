import random
import pygame

ice_sprites = pygame.sprite.Group()
ones_sprites = pygame.sprite.Group()


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
        self.add(group_of_ones)

    def update(self, group_of_ice):
        if pygame.sprite.spritecollideany(self, group_of_ice):
            self.kill()
            return False


class Ice(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(ice_sprites)
        self.ice_image = pygame.image.load('./img/ice.png')
        self.w = self.ice_image.get_width() // 20
        self.h = self.ice_image.get_height() // 20
        self.image = pygame.transform.scale(self.ice_image, (self.w, self.h))
        self.rect = self.image.get_rect()
# шаг спрайта определяем случайно, по сути это скорость
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)
# в начале льды в по углам
        self.rect.left = x
        self.rect.top = y

    def update(self, size):
        w, h = size
        self.rect = self.rect.move(self.vx, self.vy)  # шаг спрайта
        if self.rect.x > w - self.w or self.rect.x <= 0:
            self.vx = -self.vx
        if self.rect.y > h - self.h or self.rect.y <= 0:
            self.vy = -self.vy
        # if pygame.sprite.spritecollideany(self, other_group): # проверяем столкновение мяча с группой спрайтов
        #     self.vy = -self.vy
        #     self.vx = -self.vx
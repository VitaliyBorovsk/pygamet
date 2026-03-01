import pygame as pg

TILE_SCALE = 1


class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super(Player, self).__init__()

        self.image = pg.Surface((50, 50))
        self.image.fill("yellow")

        # Рисуем веселый смайлик на желтом кубе
        # Глаза (побольше и веселее)
        pg.draw.circle(self.image, "black", (15, 15), 6)
        pg.draw.circle(self.image, "black", (35, 15), 6)
        # Зрачки (большие белые точки для выразительности)
        pg.draw.circle(self.image, "white", (13, 13), 3)
        pg.draw.circle(self.image, "white", (33, 13), 3)
        # Большая широкая улыбка (перевернутая - правильная улыбка)
        pg.draw.arc(self.image, "black", (10, 25, 30, 20), 3.1415926535, 0, 4)

        # Две брови над глазами
        pg.draw.arc(self.image, "black", (8, 5, 14, 8), 0.2, 2.9, 2)  # Левая бровь
        pg.draw.arc(self.image, "black", (28, 5, 14, 8), 0.2, 2.9, 2)  # Правая бровь

        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)  # Начальное положение персонажа

        # Начальная скорость и гравитация
        self.hp = 5
        self.damage_timer = pg.time.get_ticks()
        self.damage_interval = 1000
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 1
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

    def update(self, platforms):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and not self.is_jumping:
            self.jump()
        if keys[pg.K_a]:
            self.velocity_x = -10
        elif keys[pg.K_d]:
            self.velocity_x = 10
        else:
            self.velocity_x = 0
        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
            if platform.rect.collidepoint(self.rect.midright):
                self.rect.right = platform.rect.left

            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left = platform.rect.right

    def jump(self):
        self.velocity_y = -15
        self.is_jumping = True

    def get_damage(self):
        if pg.time.get_ticks() > self.damage_timer + self.damage_interval:
            self.hp -=1
            self.damage_timer = pg.time.get_ticks()

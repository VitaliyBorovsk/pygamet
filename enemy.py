import pygame as pg

TILE_SCALE = 1


class Enemy(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super(Enemy, self).__init__()

        self.image = pg.Surface((50, 50))
        self.image.fill("red")

        # Рисуем грустный смайлик на красном кубе
        # Глаза (такие же большие)
        pg.draw.circle(self.image, "black", (15, 15), 6)
        pg.draw.circle(self.image, "black", (35, 15), 6)
        # Зрачки (большие белые точки)
        pg.draw.circle(self.image, "white", (13, 13), 3)
        pg.draw.circle(self.image, "white", (33, 13), 3)

        # Грустный рот (перевернутая улыбка)
        pg.draw.arc(self.image, "black", (10, 25, 30, 20), 0, 3.1415926535, 4)

        # Злые брови (острые, наклоненные вниз к переносице)
        # Левая бровь (наклонена вниз вправо)
        pg.draw.line(self.image, "black", (8, 5), (22, 12), 3)
        # Правая бровь (наклонена вниз влево)
        pg.draw.line(self.image, "black", (42, 5), (28, 12), 3)

        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)  # Начальное положение персонажа

        # Начальная скорость и гравитация
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
            self.velocity_x = -9
        elif keys[pg.K_d]:
            self.velocity_x = 9
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
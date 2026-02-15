import pygame as pg
import pytmx

from player import Player

pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 80
TILE_SCALE = 4
class Platform(pg.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super(Platform, self).__init__()

        self.image = pg.transform.scale(image,(width * TILE_SCALE, height * TILE_SCALE))
        self.rect = self.image.get_rect()
        self.rect.x = x*TILE_SCALE
        self.rect.y = y * TILE_SCALE
class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Платформер")
        self.clock = pg.time.Clock()
        self.is_running = False
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 4
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.tmx_map = pytmx.load_pygame("maps/map.tmx")

        map_pixel_width = self.tmx_map.width * self.tmx_map.tilewidth * TILE_SCALE
        map_pixel_height = self.tmx_map.height * self.tmx_map.tileheight * TILE_SCALE

        self.player = Player(map_pixel_width, map_pixel_height)
        self.all_sprites.add(self.player)

        for layer in self.tmx_map:
            for x,y,gid in layer:
                tile = self.tmx_map.get_tile_image_by_gid(gid)

                if tile:
                    platform = Platform(tile,x*self.tmx_map.tilewidth, y*self.tmx_map.tileheight, self.tmx_map.tilewidth, self.tmx_map.tileheight)
                    self.screen.blit(tile,(x*self.tmx_map.tilewidth, y*self.tmx_map.tileheight))
                    self.all_sprites.add(platform)
                    self.platforms.add(platform)
        self.run()






    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pg.quit()
        quit()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.camera_x += self.camera_speed
        if keys[pg.K_RIGHT]:
            self.camera_x -= self.camera_speed
        if keys[pg.K_UP]:
            self.camera_y += self.camera_speed
        if keys[pg.K_DOWN]:
            self.camera_y -= self.camera_speed

    def update(self):
        self.player.update(self.platforms)

    def draw(self):
        self.screen.fill("light blue")

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(self.camera_x, self.camera_y))

        pg.display.flip()
if __name__ == "__main__":
    game = Game()
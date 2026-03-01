import pygame as pg
import pytmx

from player import Player
from enemy import Enemy
pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 60
TILE_SCALE = 5
font = pg.font.Font(None, 96)
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
        self.setup()
    # noinspection PyAttributeOutsideInit
    def setup(self):
        self.mode = "game"
        self.clock = pg.time.Clock()
        self.is_running = False
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 4
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.tmx_map = pytmx.load_pygame("maps/map.tmx")
        self.enemies = pg.sprite.Group()
        self.map_pixel_width = self.tmx_map.width * self.tmx_map.tilewidth * TILE_SCALE
        self.map_pixel_height = self.tmx_map.height * self.tmx_map.tileheight * TILE_SCALE
        self.end_game_timer = pg.time.get_ticks()
        self.end_game_timer_interval = 3000
        self.player = Player(self.map_pixel_width, self.map_pixel_height)
        self.all_sprites.add(self.player)
        self.enemy = Enemy(self.map_pixel_width, self.map_pixel_height)
        self.enemies.add(self.enemy)
        self.all_sprites.add(self.enemy)

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
        while True:
            if self.is_running:
                self.update()
                self.draw()
                self.clock.tick(FPS)
            self.event()
        pg.quit()
        quit()

    def event(self):
        if pg.time.get_ticks() > self.end_game_timer + self.end_game_timer_interval:
            if self.mode == "game over":
                pg.quit()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            if self.mode == "game over":
                print(232)


                if event.type == pg.KEYDOWN:
                    self.setup()

        keys = pg.key.get_pressed()

        # if keys[pg.K_LEFT]:
        #     self.camera_x += self.camera_speed
        # if keys[pg.K_RIGHT]:
        #     self.camera_x -= self.camera_speed
        # if keys[pg.K_UP]:
        #     self.camera_y += self.camera_speed
        # if keys[pg.K_DOWN]:
        #     self.camera_y -= self.camera_speed

    def update(self):

        if self.player.hp <= 0:
            self.end_game_timer = pg.time.get_ticks()
            self.mode = "game over"



            return

        for enemy in self.enemies.sprites():
            if pg.sprite.collide_mask(self.player, enemy):
                self.player.get_damage()

        self.player.update(self.platforms)
        self.enemies.update(self.platforms)
        self.camera_x = self.player.rect.x - SCREEN_WIDTH //2
        self.camera_y = self.player.rect.y - SCREEN_HEIGHT //2

        self.camera_x = max(0, min(self.camera_x, self.map_pixel_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.map_pixel_width - SCREEN_HEIGHT))
    def draw(self):
        self.screen.fill("light blue")

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, -self.camera_y))
        pg.draw.rect(self.screen, pg.Color("red"), (10, 10, self.player.hp * 20, 10))
        pg.draw.rect(self.screen, pg.Color("black"), (9, 9, 102, 12), 1)
        if self.mode == "game over":
            text = font.render("Вы проиграли", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2 , SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
        pg.display.flip()
if __name__ == "__main__":
    game = Game()
import pygame
import sys
from pygame.locals import *
import random
import time
import os

folder = os.path.dirname(__file__)
pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

# COLORS
WHITE = (255, 255, 255)

font_large = pygame.font.Font('freesansbold.ttf', 60)
font_small = pygame.font.Font('freesansbold.ttf', 28)
game_over = font_large.render("Game Over", True, WHITE)

DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY.fill(WHITE)

pygame.display.set_caption("Space Explorer")


class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(folder, "images/enemy.png"))
        self.surf = pygame.Surface((64, 32))
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH, random.randint(35, SCREEN_HEIGHT-35)))

    def move(self):
        global SCORE
        self.rect.move_ip(-SPEED, 0)
        if (self.rect.left < 0):
            SCORE += 1
            self.rect.left = SCREEN_WIDTH
            self.rect.center = (
                SCREEN_WIDTH, random.randint(35, SCREEN_HEIGHT-35))

    def addNPC(self):
        global SCORE
        if (self.rect.left < 0):
            INC_ENEMIES += 1
            E = NPC()
            enemies.add(E)
            all_sprites.add(E)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(folder, "images/player.png"))
        self.surf = pygame.Surface((37, 32))
        self.rect = self.surf.get_rect(center=(150, 350))

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)


class Background():
    def __init__(self):
        self.bg_image = pygame.image.load(
            os.path.join(folder, "images/stars_texture.png"))
        self.rectBGimg = self.bg_image.get_rect()
        self.bg_X1 = 0
        self.bg_Y1 = 0
        self.bg_X2 = self.rectBGimg.width
        self.bg_Y2 = 0
        self.moving_speed = 5

    def update(self):
        self.bg_X1 -= self.moving_speed
        self.bg_X2 -= self.moving_speed
        if self.bg_X1 <= -self.rectBGimg.width:
            self.bg_X1 = self.rectBGimg.width
        if self.bg_X2 <= -self.rectBGimg.width:
            self.bg_X2 = self.rectBGimg.width

    def render(self):
        DISPLAY.blit(self.bg_image, (self.bg_X1, self.bg_Y1))
        DISPLAY.blit(self.bg_image, (self.bg_X2, self.bg_Y2))


P1 = Player()
E1 = NPC()

back_ground = Background()

enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

INC_ENEMIES = 1

while True:

    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    back_ground.update()
    back_ground.render()

    scores = font_small.render(str(SCORE), True, WHITE)
    DISPLAY.blit(scores, (395, 10))

    for entity in all_sprites:
        DISPLAY.blit(entity.image, entity.rect)
        entity.move()
        for enemy in enemies:
            enemy.addNPC()

    if pygame.sprite.spritecollideany(P1, enemies):
        time.sleep(0.8)

        DISPLAY.fill((255, 0, 0))
        DISPLAY.blit(game_over, (300, 275))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(1.5)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)

#!/usr/bin/python2
import pygame
import random

# Colors
BLACK = (0, 0, 0)
BROWN = (99, 66, 33)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

GRAVITY = 3

#Screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#This code sucks donkey cock
class Banana(pygame.sprite.Sprite):
    width = 45
    height = 45

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.width, self.height])

        self.rect = self.image.get_rect()

        self.reset()

    def reset(self):
        # There is a 1 in 10 chance of a bad banana
        self.good = random.randint(0, 10)

        if self.good != 0:
            self.image.fill(YELLOW)
            self.is_good = True
        else:
            self.image.fill(BROWN)
            self.is_good = False

        self.rect.x = SCREEN_WIDTH - self.width
        self.rect.y = SCREEN_HEIGHT / 3

        self.vel_x = random.randint(10, 30)
        self.vel_y = random.randint(-20, -10)

    def update(self, buckets):
        self.rect.x -= self.vel_x
        self.rect.y += self.vel_y

        self.vel_y += GRAVITY

        if self.rect.x < 0 or self.rect.y > SCREEN_HEIGHT:
            self.reset()
 #Bucket
class Bucket(pygame.sprite.Sprite):
    width = 100
    height = 150

    vel_y = 0
    is_jumping = False
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y - self.height

        self.hitbox = pygame.Rect(self.rect.left, self.rect.top, self.width, self.height/3)

    def jump(self):
        if self.rect.bottom == SCREEN_HEIGHT:
            self.vel_y = -20
            self.is_jumping = True

    def update(self, banana):
        self.rect.y += self.vel_y

        if self.rect.bottom < SCREEN_HEIGHT:
            self.vel_y += GRAVITY
        else:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0
            self.is_jumping = False

        self.hitbox.y = self.rect.y

class Game():
    def start(self):

        pygame.init()

        size = [SCREEN_WIDTH, SCREEN_HEIGHT]
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Adventure Banana")

        done = False

        clock = pygame.time.Clock()

        score = 0
        combo = 0

        all_sprites = pygame.sprite.RenderPlain()
        all_buckets = pygame.sprite.RenderPlain()

        buckets = []

        start = 100
        for i in range(0, 3):
            buckets.append(Bucket(start + 2*start*i, SCREEN_HEIGHT))
            all_buckets.add(buckets[i])
            all_sprites.add(buckets[i])

        banana = Banana()
        all_sprites.add(banana)

        while done == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    for bucket in buckets:
                        if bucket.rect.collidepoint(pos):
                            bucket.jump()
                            break

            screen.fill(WHITE)

            banana.update(buckets)
            all_buckets.update(banana)

            for bucket in buckets:
                collide = pygame.Rect.colliderect(banana.rect, bucket.hitbox)

                if collide:
                    if bucket.is_jumping:
                        if banana.is_good:
                            score += 20
                        else:
                            score -= 20

                        banana.reset()
                        print score

            all_sprites.draw(screen)

            clock.tick(20)

            pygame.display.flip()

        pygame.quit()

g = Game()
g.start()

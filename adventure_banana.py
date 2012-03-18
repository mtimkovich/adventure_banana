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
PINK = (255, 128, 128)

GRAVITY = 2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Banana(pygame.sprite.Sprite):
    width = 45
    height = 45

    def __init__(self, num_of_buckets):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.width, self.height])

        self.rect = self.image.get_rect()

        # There is a 1 in 10 chance of a bad banana
#         self.good = random.randint(0, 10)
        r = random.randint(0, 3)

        if num_of_buckets < 3 and r == 1:
            self.image.fill(PINK)
            self.type = "heart"
        elif r == 0:
            self.image.fill(BROWN)
            self.type = "bad"
        else:
            self.image.fill(YELLOW)
            self.type = "good"

        self.rect.x = SCREEN_WIDTH - self.width
        self.rect.y = SCREEN_HEIGHT / 1.8

#         self.vel_x = random.randint(10, 30)
#         self.vel_y = random.randint(-20, -10)
        self.vel_x = 25
        self.vel_y = -20

    def update(self):
        self.rect.x -= self.vel_x
        self.rect.y += self.vel_y

        self.vel_y += GRAVITY

        if self.rect.x < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()

            if self.type != "bad":
                return False

        return True

class Bucket(pygame.sprite.Sprite):
    width = 100
    height = 150

    vel_y = 0
    is_jumping = False
    dead = False

    points = 10
    
    def __init__(self, x, offset = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.bottom = SCREEN_HEIGHT - offset

        self.hitbox = pygame.Rect(self.rect.left, self.rect.top, self.width, self.height/3)

        self.value = Bucket.points
        Bucket.points += 10

    def die(self):
        self.dead = True
        self.is_jumping = False

    def jump(self):
        if self.rect.bottom == SCREEN_HEIGHT:
            self.vel_y = -25
            self.is_jumping = True

    def update(self):
        self.rect.y += self.vel_y

        if self.rect.bottom < SCREEN_HEIGHT:
            self.vel_y += GRAVITY
        else:
            if not self.dead:
                self.rect.bottom = SCREEN_HEIGHT
                self.vel_y = 0
                self.is_jumping = False
            else:
                self.vel_y += GRAVITY

                if self.rect.top > SCREEN_HEIGHT:
                    self.kill()

        self.hitbox.top = self.rect.top

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

        buckets = pygame.sprite.RenderPlain()
        bananas = pygame.sprite.RenderPlain()

        # Create the buckets
        start = 100
        for i in range(0, 3):
            buckets.add(Bucket(start/2 + 2*start*i))

        dead_bucket_coor = []

        tick = 0

        # Main game loop
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

            if tick == 0:
                banana = Banana(len(buckets))
                bananas.add(banana)

            for banana in bananas:
                r = banana.update()

                if r == False:
                    combo = 0

            buckets.update()

            for bucket in buckets:
                for banana in bananas:
                    collide = pygame.Rect.colliderect(banana.rect, bucket.hitbox)

                    if collide:
                        if bucket.is_jumping:
                            if banana.type == "good":
                                combo += 1
                                score += bucket.value + combo
                            elif banana.type == "bad":
                                dead_bucket_coor.append(bucket.rect.x)

                                bucket.die()

                                combo = 0
                            elif banana.type == "heart":
                                if len(buckets) < 3:
                                    buckets.add(Bucket(dead_bucket_coor[0], 100))

                                    dead_bucket_coor.pop(0)

                            banana.kill()

            buckets.draw(screen)
            bananas.draw(screen)

            font = pygame.font.Font("DroidSans.ttf", 20)

            if combo >= 0:
                text = font.render("Combo: " + str(combo), True, RED)
                screen.blit(text, [SCREEN_WIDTH/3, SCREEN_HEIGHT/3])

            font = pygame.font.Font("DroidSans.ttf", 30)

            # Print the score on to the screen
            text = font.render("Score: " + str(score), True, BLACK)
            screen.blit(text, [20, 20])

            clock.tick(20)

            pygame.display.flip()

            tick += 1

            if tick > 15:
                tick = 0

        pygame.quit()

g = Game()
g.start()

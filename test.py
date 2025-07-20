import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Enemy:
    def __init__(self, x, y, left_bound, right_bound):  # КОНСТРУКТОР С ПАРАМЕТРАМИ
        self.rect = pygame.Rect(x, y, 40, 60)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = 2
        self.direction = 1
        self.health = 1

        # Состояния
        self.STATE_IDLE = 0
        self.STATE_WALK1 = 1
        self.STATE_WALK2 = 2
        self.state = self.STATE_IDLE

        # Таймеры
        self.idle_timer = 0
        self.idle_duration = 30
        self.animation_timer = 0
        self.animation_speed = 10

        # Цвета
        self.state_colors = {
            self.STATE_IDLE: (255, 0, 0),
            self.STATE_WALK1: (255, 255, 0),
            self.STATE_WALK2: (0, 255, 0)
        }

    def update(self):
        if self.direction > 0 and self.rect.right >= self.right_bound:
            self._start_idle()
        elif self.direction < 0 and self.rect.left <= self.left_bound:
            self._start_idle()

        if self.state == self.STATE_IDLE:
            self.idle_timer -= 1
            if self.idle_timer <= 0:
                self.direction *= -1
                self.state = self.STATE_WALK1
        else:
            self.rect.x += self.speed * self.direction
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                if self.state == self.STATE_WALK1:
                    self.state = self.STATE_WALK2
                else:
                    self.state = self.STATE_WALK1

    def _start_idle(self):
        if self.state != self.STATE_IDLE:
            self.state = self.STATE_IDLE
            self.idle_timer = self.idle_duration

    def draw(self, surface):
        pygame.draw.rect(surface, self.state_colors[self.state], self.rect)

enemy = Enemy(100, 300, 100, 400)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    enemy.update()

    screen.fill((30, 30, 50))
    enemy.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
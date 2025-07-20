import pygame
import sys

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Платформер")
clock = pygame.time.Clock()
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)  # Хитбокс игрока
        self.x_speed = 0  # Горизонтальная скорость
        self.y_speed = 0  # Вертикальная скорость
        self.jump_power = -15  # Сила прыжка
        self.speed = 5  # Скорость движения
        self.on_ground = False

    def update(self, platforms):
        # гравитация
        self.y_speed += 0.8
        self.rect.y += self.y_speed

        # Движение по горизонтали
        self.rect.x += self.x_speed



        # Проверка коллизий с платформами
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.y_speed > 0:  # Падаем вниз
                    self.rect.bottom = platform.top
                    self.y_speed = 0
                    self.on_ground = True
                elif self.y_speed < 0:  # Движемся вверх
                    self.rect.top = platform.bottom
                    self.y_speed = 0

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)


def main():
    # игрок
    player = Player(100, 300)

    # платформы
    platforms = [
        pygame.Rect(0, 550, 800, 50),  # Основной пол
        pygame.Rect(100, 450, 200, 20),
        pygame.Rect(400, 350, 200, 20),
        pygame.Rect(200, 250, 100, 20),
        pygame.Rect(600, 400, 150, 20)
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # прыжок
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.on_ground:
                    player.y_speed = player.jump_power

        # Управление движением
        keys = pygame.key.get_pressed()
        player.x_speed = (keys[pygame.K_d] - keys[pygame.K_a]) * player.speed

        # Обновление игрока
        player.update(platforms)

        # Отрисовка
        display.fill(SKY_BLUE)  # Фон


        for platform in platforms:
            pygame.draw.rect(display, (0, 255, 0), platform)


        player.draw(display)



        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Платформер!")
clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
DARK_BG = (30, 30, 50)


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.SysFont(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect)
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.current_color = self.hover_color if self.rect.collidepoint(pos) else self.color

    def is_clicked(self, pos, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos)


class Spikes:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = (194, 190, 190)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)


class Enemy:
    def __init__(self, x, y, left_bound, right_bound):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = 2
        self.direction = 1
        self.health = 1
        self.STATE_IDLE = 0
        self.STATE_WALK1 = 1
        self.STATE_WALK2 = 2
        self.state = self.STATE_IDLE
        self.idle_timer = 0
        self.idle_duration = 30
        self.animation_timer = 0
        self.animation_speed = 10
        self.idle_image = self._load_image('12.png')
        self.walk1_image = self._load_image('12.png')
        self.walk2_image = self._load_image('12.png')
        self.idle_image_left = pygame.transform.flip(self.idle_image, True, False)
        self.walk1_image_left = pygame.transform.flip(self.walk1_image, True, False)
        self.walk2_image_left = pygame.transform.flip(self.walk2_image, True, False)
        self.current_image = self.idle_image

    def _load_image(self, path):
        try:
            return pygame.image.load(path).convert_alpha()
        except:
            surface = pygame.Surface((40, 60))
            surface.fill((255, 0, 0))
            return surface

    def update(self):
        if self.rect.right >= self.right_bound and self.direction > 0:
            self._start_idle()
        elif self.rect.left <= self.left_bound and self.direction < 0:
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

        if self.direction > 0:
            if self.state == self.STATE_IDLE:
                self.current_image = self.idle_image
            elif self.state == self.STATE_WALK1:
                self.current_image = self.walk1_image
            else:
                self.current_image = self.walk2_image
        else:
            if self.state == self.STATE_IDLE:
                self.current_image = self.idle_image_left
            elif self.state == self.STATE_WALK1:
                self.current_image = self.walk1_image_left
            else:
                self.current_image = self.walk2_image_left

    def _start_idle(self):
        if self.state != self.STATE_IDLE:
            self.state = self.STATE_IDLE
            self.idle_timer = self.idle_duration

    def draw(self, surface):
        surface.blit(self.current_image, self.rect)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.x_speed = 0
        self.y_speed = 0
        self.jump_power = -15
        self.speed = 5
        self.on_ground = False
        self.max_health = 3
        self.health = self.max_health
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 90

    def update(self, platforms):
        self.y_speed += 0.8
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed

        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.y_speed > 0:
                    self.rect.bottom = platform.top
                    self.y_speed = 0
                    self.on_ground = True
                elif self.y_speed < 0:
                    self.rect.top = platform.bottom
                    self.y_speed = 0

    def jump(self):
        if self.on_ground:
            self.y_speed = self.jump_power
            self.on_ground = False

    def draw(self, surface):
        if self.invincible and (pygame.time.get_ticks() // 200) % 2 == 0:
            pygame.draw.rect(surface, (255, 255, 255), self.rect)
        else:
            pygame.draw.rect(surface, BLUE, self.rect)

    def take_damage(self):
        if not self.invincible:
            self.health -= 1
            self.invincible = True
            self.invincible_timer = self.invincible_duration
            return True
        return False


class Game:
    def __init__(self):
        self.state = "main_menu"
        self.platforms = [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(100, 450, 200, 20),
            pygame.Rect(400, 350, 200, 20),
            pygame.Rect(200, 250, 100, 20),
            pygame.Rect(600, 400, 150, 20)
        ]
        self.player = Player(100, 300)
        self.enemy = Enemy(100, 500, 100, 400)
        self.spikes = Spikes(700, 520)
        self.title_font = pygame.font.SysFont(None, 72)
        self.start_button = Button(300, 300, 200, 50, "Start", (100, 200, 100), (150, 255, 150))
        self.exit_button = Button(300, 400, 200, 50, "Exit", (200, 100, 100), (255, 150, 150))
        self.continue_button = Button(300, 300, 200, 50, "Continue", (100, 200, 100), (150, 255, 150))
        self.menu_button = Button(300, 400, 200, 50, "Main Menu", (200, 200, 100), (255, 255, 150))
        self.game_over_font = pygame.font.SysFont(None, 48)
        self.heart_image = self._load_heart_image()

    def _load_heart_image(self):
        heart_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(heart_surface, (255, 0, 0), (10, 10), 10)
        pygame.draw.circle(heart_surface, (255, 0, 0), (20, 10), 10)
        pygame.draw.polygon(heart_surface, (255, 0, 0), [(5, 15), (15, 25), (25, 15)])
        return heart_surface

    def draw_health(self, surface):
        for i in range(self.player.max_health):
            if i < self.player.health:
                surface.blit(self.heart_image, (10 + i * 35, 10))
            else:
                empty_heart = pygame.Surface((30, 30), pygame.SRCALPHA)
                pygame.draw.circle(empty_heart, (200, 0, 0), (10, 10), 10, 2)
                pygame.draw.circle(empty_heart, (200, 0, 0), (20, 10), 10, 2)
                pygame.draw.polygon(empty_heart, (200, 0, 0), [(5, 15), (15, 25), (25, 15)], 2)
                surface.blit(empty_heart, (10 + i * 35, 10))

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.state == "main_menu":
                self.start_button.check_hover(mouse_pos)
                self.exit_button.check_hover(mouse_pos)
                if self.start_button.is_clicked(mouse_pos, event):
                    self.state = "game"
                elif self.exit_button.is_clicked(mouse_pos, event):
                    return False

            elif self.state == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "pause"
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.player.jump()

            elif self.state == "pause":
                self.continue_button.check_hover(mouse_pos)
                self.menu_button.check_hover(mouse_pos)
                if self.continue_button.is_clicked(mouse_pos, event):
                    self.state = "game"
                elif self.menu_button.is_clicked(mouse_pos, event):
                    self.state = "main_menu"

            elif self.state == "game_over":
                self.menu_button.check_hover(mouse_pos)
                if self.menu_button.is_clicked(mouse_pos, event):
                    self.__init__()
        return True

    def update(self):
        if self.state == "game":
            keys = pygame.key.get_pressed()
            self.player.x_speed = (keys[pygame.K_d] - keys[pygame.K_a]) * self.player.speed
            self.player.update(self.platforms)
            self.enemy.update()

            if self.enemy.check_collision(self.player.rect):
                if self.player.take_damage() and self.player.health <= 0:
                    self.state = "game_over"

            if self.spikes.check_collision(self.player.rect):
                if self.player.take_damage() and self.player.health <= 0:
                    self.state = "game_over"

    def draw(self):
        if self.state == "main_menu":
            display.fill(DARK_BG)
            title = self.title_font.render("Название Игры", True, (255, 255, 255))
            display.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
            self.start_button.draw(display)
            self.exit_button.draw(display)
        else:
            display.fill(SKY_BLUE)
            for platform in self.platforms:
                pygame.draw.rect(display, GREEN, platform)

            if self.state in ["game", "pause"]:
                self.player.draw(display)
                self.enemy.draw(display)
                self.spikes.draw(display)
                self.draw_health(display)

            if self.state == "pause":
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                display.blit(overlay, (0, 0))
                pause_text = self.title_font.render("PAUSED", True, (255, 255, 255))
                display.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, 150))
                self.continue_button.draw(display)
                self.menu_button.draw(display)

            elif self.state == "game_over":
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                display.blit(overlay, (0, 0))
                game_over_text = self.game_over_font.render("GAME OVER", True, (255, 0, 0))
                display.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
                self.menu_button.draw(display)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)


def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
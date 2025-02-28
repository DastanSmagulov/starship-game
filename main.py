import pygame
import random
 
# Инициализация Pygame
pygame.init()
 
# экран
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Космическое приключение")
 
# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
 
# космический корабль
class Spaceship:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.speed = 3
        self.boost_speed = 6  # Скорость при ускорении
        self.is_boosting = False  # Флаг ускорения
 
    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
 
    def move(self, direction):
        current_speed = self.boost_speed if self.is_boosting else self.speed  # Выбор скорости
 
        if direction == "left" and self.x > 0:
            self.x -= current_speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += current_speed
        if direction == "up" and self.y > 0:
            self.y -= current_speed
        if direction == "down" and self.y < SCREEN_HEIGHT - self.height:
            self.y += current_speed
 
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
        if self.y < 0:
            self.y = 0
        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
 
# астероиды
class Asteroid:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.speed = random.randint(2, 4)
 
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
 
    def move(self):
        self.y += self.speed
 
# Кнопка рестарта
def draw_restart_button():
    font = pygame.font.Font(None, 36)
    text = font.render("Рестарт", True, WHITE)
    button_width = 110
    button_height = 50
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    button_y = SCREEN_HEIGHT // 2 - button_height // 2
    pygame.draw.rect(screen, RED, (button_x, button_y, button_width, button_height))
    screen.blit(text, (button_x + 10, button_y + 10))
    return pygame.Rect(button_x, button_y, button_width, button_height)
 
# Вывод счёта
def draw_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Счёт: {score}", True, WHITE)
    screen.blit(text, (10, 10))
 
# процесс игры
def main():
    clock = pygame.time.Clock()
    spaceship = Spaceship()
    asteroids = []
    game_over = False
    score = 0
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
 
            # Обработка нажатия на кнопку рестарта
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    # Рестарт игры
                    game_over = False
                    spaceship = Spaceship()
                    asteroids = []
                    score = 0
 
        if not game_over:
            # Управление кораблём
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                spaceship.move("left")
            if keys[pygame.K_d]:
                spaceship.move("right")
            if keys[pygame.K_s]:
                spaceship.move("down")
            if keys[pygame.K_w]:
                spaceship.move("up")
 
            mouse_x, mouse_y = pygame.mouse.get_pos()
            spaceship.x += (mouse_x - spaceship.x) * 0.5  # Плавное движение по оси X
            spaceship.y += (mouse_y - spaceship.y) * 0.5  # Плавное движение по оси Y
 
 
 
 
 
            # Ускорение на левый Shift
            spaceship.is_boosting = keys[pygame.K_LSHIFT]
 
            # Создание новых астероидов
            if random.randint(1, 100) < 5:
                asteroids.append(Asteroid())
 
            # Очистка экрана
            screen.fill(BLACK)
 
            print(spaceship.x, spaceship.y)
 
            # Движение и отрисовка астероидов
            for asteroid in asteroids[:]:
                asteroid.move()
                asteroid.draw()
 
                # Удаление астероидов, которые улетели за пределы экрана
                if asteroid.y > SCREEN_HEIGHT:
                    asteroids.remove(asteroid)
                    score += 1
 
                # Проверка столкновения
                if (spaceship.x < asteroid.x + asteroid.width and
                    spaceship.x + spaceship.width > asteroid.x and
                    spaceship.y < asteroid.y + asteroid.height and
                    spaceship.y + spaceship.height > asteroid.y or (spaceship.x == 750 or spaceship.x == 0 or spaceship.y == 0 or spaceship.x <= 0.1  or spaceship.y >=550 or spaceship.x>=750 or spaceship.y <= 0.1)):
                    game_over = True
 
            # Отрисовка корабля
            spaceship.draw()
 
 
            # Вывод счёта
            draw_score(score)
 
        else:
            # Экран завершения игры
            screen.fill(BLACK)
            draw_score(score)
            restart_button = draw_restart_button()
 
        # Обновление экрана
        pygame.display.flip()
 
        # Управление частотой обновления экрана
        clock.tick(60)
 
# Запуск игры
if __name__ == "__main__":
    main()
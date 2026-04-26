import pygame
import random
import sys

# ---------------------------------
# ИНИЦИАЛИЗАЦИЯ
# ---------------------------------
pygame.init()

# Размер окна
WIDTH = 400
HEIGHT = 600

# Создаем окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

# Часы для FPS
clock = pygame.time.Clock()
FPS = 60

# ---------------------------------
# ЦВЕТА
# ---------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
DARK_GRAY = (60, 60, 60)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 215, 0)

# ---------------------------------
# ШРИФТЫ
# ---------------------------------
font_small = pygame.font.SysFont("Arial", 24)
font_big = pygame.font.SysFont("Arial", 48)

# ---------------------------------
# НАСТРОЙКИ ДОРОГИ
# ---------------------------------
ROAD_LEFT = 80
ROAD_RIGHT = 320
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT

# Полосы разметки
lane_line_y = 0
lane_line_speed = 6

# ---------------------------------
# ИГРОК
# ---------------------------------
player_width = 40
player_height = 70
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 100
player_speed = 6

# ---------------------------------
# ВРАГИ
# ---------------------------------
enemy_width = 40
enemy_height = 70
enemy_speed = 5

# Список врагов
enemies = []

# Таймер для добавления врагов
enemy_spawn_delay = 1200  # миллисекунды
last_enemy_spawn = pygame.time.get_ticks()

# ---------------------------------
# МОНЕТЫ
# ---------------------------------
coin_radius = 12
coin_speed = 5

# Список монет
coins = []

# Таймер для добавления монет
coin_spawn_delay = 1500  # миллисекунды
last_coin_spawn = pygame.time.get_ticks()

# Сколько монет собрано
collected_coins = 0

# ---------------------------------
# ОЧКИ
# ---------------------------------
score = 0

# ---------------------------------
# ФУНКЦИИ
# ---------------------------------
def draw_road():
    """
    Рисует фон, дорогу и разметку.
    """
    global lane_line_y

    # Фон вокруг дороги
    screen.fill(GREEN)

    # Дорога
    pygame.draw.rect(screen, DARK_GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))

    # Боковые линии дороги
    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 4)

    # Прерывистая разметка по центру
    lane_x = WIDTH // 2 - 5
    for i in range(-1, 10):
        y = lane_line_y + i * 80
        pygame.draw.rect(screen, WHITE, (lane_x, y, 10, 40))

    # Двигаем разметку вниз
    lane_line_y += lane_line_speed

    # Когда разметка ушла вниз, начинаем снова
    if lane_line_y >= 80:
        lane_line_y = 0


def draw_player(x, y):
    """
    Рисует машину игрока простыми фигурами.
    """
    # Корпус
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height), border_radius=8)

    # Стекло
    pygame.draw.rect(screen, WHITE, (x + 8, y + 10, 24, 18), border_radius=4)

    # Колеса
    pygame.draw.rect(screen, BLACK, (x - 4, y + 10, 6, 15))
    pygame.draw.rect(screen, BLACK, (x - 4, y + 45, 6, 15))
    pygame.draw.rect(screen, BLACK, (x + player_width - 2, y + 10, 6, 15))
    pygame.draw.rect(screen, BLACK, (x + player_width - 2, y + 45, 6, 15))


def draw_enemy(enemy):
    """
    Рисует вражескую машину.
    enemy = [x, y]
    """
    x, y = enemy

    pygame.draw.rect(screen, RED, (x, y, enemy_width, enemy_height), border_radius=8)
    pygame.draw.rect(screen, WHITE, (x + 8, y + 10, 24, 18), border_radius=4)

    pygame.draw.rect(screen, BLACK, (x - 4, y + 10, 6, 15))
    pygame.draw.rect(screen, BLACK, (x - 4, y + 45, 6, 15))
    pygame.draw.rect(screen, BLACK, (x + enemy_width - 2, y + 10, 6, 15))
    pygame.draw.rect(screen, BLACK, (x + enemy_width - 2, y + 45, 6, 15))


def draw_coin(coin):
    """
    Рисует монету.
    coin = [x, y]
    x, y - центр монеты
    """
    x, y = coin

    pygame.draw.circle(screen, YELLOW, (x, y), coin_radius)
    pygame.draw.circle(screen, BLACK, (x, y), coin_radius, 2)

    # Небольшая буква C внутри монеты
    text = font_small.render("C", True, BLACK)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def spawn_enemy():
    """
    Создает нового врага в случайной полосе.
    """
    lanes = [110, 180, 250]  # x-координаты для 3 полос
    x = random.choice(lanes)
    y = -enemy_height
    enemies.append([x, y])


def spawn_coin():
    """
    Создает новую монету в случайной полосе.
    """
    lanes = [WIDTH // 2, 140, 210, 280]
    x = random.choice(lanes)
    y = -20
    coins.append([x, y])


def move_enemies():
    """
    Двигает врагов вниз.
    Если враг ушел за экран, удаляем и увеличиваем score.
    """
    global score, enemy_speed

    for enemy in enemies[:]:
        enemy[1] += enemy_speed

        # Если враг ушел вниз
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)
            score += 1

            # Можно постепенно ускорять игру
            if score % 5 == 0:
                enemy_speed += 0.3


def move_coins():
    """
    Двигает монеты вниз.
    Если монета ушла за экран, удаляем.
    """
    for coin in coins[:]:
        coin[1] += coin_speed

        if coin[1] - coin_radius > HEIGHT:
            coins.remove(coin)


def get_player_rect():
    """
    Возвращает прямоугольник игрока для проверки столкновений.
    """
    return pygame.Rect(player_x, player_y, player_width, player_height)


def get_enemy_rect(enemy):
    """
    Возвращает прямоугольник врага.
    """
    return pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)


def coin_touches_player(coin):
    """
    Проверка, коснулась ли монета игрока.
    Упростим:
    проверяем, находится ли центр монеты внутри прямоугольника игрока.
    """
    player_rect = get_player_rect()
    coin_x, coin_y = coin
    return player_rect.collidepoint(coin_x, coin_y)


def check_collision_with_enemy():
    """
    Проверяет столкновение игрока с любым врагом.
    """
    player_rect = get_player_rect()

    for enemy in enemies:
        enemy_rect = get_enemy_rect(enemy)
        if player_rect.colliderect(enemy_rect):
            return True

    return False


def draw_texts():
    """
    Рисует текст score и coins.
    """
    # Очки слева сверху
    score_text = font_small.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Монеты справа сверху
    coins_text = font_small.render(f"Coins: {collected_coins}", True, WHITE)
    coins_rect = coins_text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(coins_text, coins_rect)


def show_game_over():
    """
    Экран конца игры.
    """
    screen.fill(BLACK)

    text1 = font_big.render("GAME OVER", True, RED)
    text2 = font_small.render(f"Score: {score}", True, WHITE)
    text3 = font_small.render(f"Coins collected: {collected_coins}", True, WHITE)

    rect1 = text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    rect2 = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
    rect3 = text3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(text1, rect1)
    screen.blit(text2, rect2)
    screen.blit(text3, rect3)

    pygame.display.update()
    pygame.time.delay(2500)


# ---------------------------------
# ГЛАВНЫЙ ЦИКЛ ИГРЫ
# ---------------------------------
running = True

while running:
    clock.tick(FPS)

    # -----------------------------
    # СОБЫТИЯ
    # -----------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # -----------------------------
    # УПРАВЛЕНИЕ ИГРОКОМ
    # -----------------------------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Не даем машине выехать за дорогу
    if player_x < ROAD_LEFT + 5:
        player_x = ROAD_LEFT + 5

    if player_x + player_width > ROAD_RIGHT - 5:
        player_x = ROAD_RIGHT - 5 - player_width

    # -----------------------------
    # СОЗДАНИЕ ВРАГОВ
    # -----------------------------
    current_time = pygame.time.get_ticks()

    if current_time - last_enemy_spawn > enemy_spawn_delay:
        spawn_enemy()
        last_enemy_spawn = current_time

    # -----------------------------
    # СОЗДАНИЕ МОНЕТ
    # -----------------------------
    if current_time - last_coin_spawn > coin_spawn_delay:
        spawn_coin()
        last_coin_spawn = current_time

    # -----------------------------
    # ДВИЖЕНИЕ ОБЪЕКТОВ
    # -----------------------------
    move_enemies()
    move_coins()

    # -----------------------------
    # ПРОВЕРКА СБОРА МОНЕТ
    # -----------------------------
    for coin in coins[:]:
        if coin_touches_player(coin):
            coins.remove(coin)
            collected_coins += 1

    # -----------------------------
    # ПРОВЕРКА СТОЛКНОВЕНИЯ С ВРАГОМ
    # -----------------------------
    if check_collision_with_enemy():
        show_game_over()
        pygame.quit()
        sys.exit()

    # -----------------------------
    # ОТРИСОВКА
    # -----------------------------
    draw_road()
    draw_player(player_x, player_y)

    for enemy in enemies:
        draw_enemy(enemy)

    for coin in coins:
        draw_coin(coin)

    draw_texts()

    pygame.display.update()
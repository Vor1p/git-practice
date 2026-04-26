import pygame
import random
import sys

# -----------------------------
# ИНИЦИАЛИЗАЦИЯ
# -----------------------------
pygame.init()

WIDTH = 400
HEIGHT = 400
CELL = 20  # размер одной клетки

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# -----------------------------
# ЦВЕТА
# -----------------------------
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)
WHITE = (255, 255, 255)
GRAY = (70, 70, 70)

# -----------------------------
# ШРИФТЫ
# -----------------------------
font = pygame.font.SysFont("Arial", 20)
big_font = pygame.font.SysFont("Arial", 32)

# -----------------------------
# ФУНКЦИЯ СТАРТА / РЕСТАРТА ИГРЫ
# -----------------------------
def reset_game():
    """
    Возвращает все начальные значения игры.
    """
    snake = [(200, 200)]
    dx, dy = CELL, 0   # старт: движение вправо
    score = 0
    level = 1
    speed = 7
    game_over = False
    food = generate_food(snake)
    return snake, dx, dy, score, level, speed, food, game_over

# -----------------------------
# ФУНКЦИЯ ГЕНЕРАЦИИ ЕДЫ
# -----------------------------
def generate_food(snake):
    """
    Генерирует еду в случайной клетке,
    но не внутри змейки.
    """
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        if (x, y) not in snake:
            return (x, y)

# -----------------------------
# СТАРТОВЫЕ ДАННЫЕ
# -----------------------------
snake, dx, dy, score, level, speed, food, game_over = reset_game()

# -----------------------------
# ГЛАВНЫЙ ЦИКЛ
# -----------------------------
while True:
    clock.tick(speed)

    # -------------------------
    # СОБЫТИЯ
    # -------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Если игра окончена — R делает рестарт
            if game_over:
                if event.key == pygame.K_r:
                    snake, dx, dy, score, level, speed, food, game_over = reset_game()

            else:
                # Управление змейкой
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -CELL
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, CELL
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -CELL, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = CELL, 0

    # -------------------------
    # ЕСЛИ НЕ GAME OVER — ИГРАЕМ
    # -------------------------
    if not game_over:
        # Текущая голова змеи
        head_x, head_y = snake[0]

        # Новая позиция головы
        new_head = (head_x + dx, head_y + dy)

        # ---------------------
        # ПОРТАЛЫ
        # ---------------------
        # Если вышли за край — появляемся с другой стороны
        if new_head[0] < 0:
            new_head = (WIDTH - CELL, new_head[1])
        elif new_head[0] >= WIDTH:
            new_head = (0, new_head[1])

        if new_head[1] < 0:
            new_head = (new_head[0], HEIGHT - CELL)
        elif new_head[1] >= HEIGHT:
            new_head = (new_head[0], 0)

        # ---------------------
        # ПРОВЕРКА СТОЛКНОВЕНИЯ С СОБОЙ
        # ---------------------
        if new_head in snake:
            game_over = True
        else:
            # Добавляем новую голову
            snake.insert(0, new_head)

            # -----------------
            # ЕСЛИ СЪЕЛИ ЕДУ
            # -----------------
            if new_head == food:
                score += 1
                food = generate_food(snake)

                # Каждые 3 очка — новый уровень
                if score % 3 == 0:
                    level += 1
                    speed += 1
            else:
                # Если не съели еду — хвост удаляем
                snake.pop()

    # -------------------------
    # ОТРИСОВКА
    # -------------------------
    screen.fill(BLACK)

    # Сетка для наглядности
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    # Еда
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL), border_radius=4)

    # Змейка
    for i, segment in enumerate(snake):
        if i == 0:
            # Голова
            pygame.draw.rect(screen, DARK_GREEN, (segment[0], segment[1], CELL, CELL), border_radius=4)
        else:
            # Тело
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL, CELL), border_radius=4)

    # Текст score и level
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    mode_text = font.render("Mode: Portal", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 35))
    screen.blit(mode_text, (10, 60))

    # -------------------------
    # ЭКРАН GAME OVER
    # -------------------------
    if game_over:
        game_over_text = big_font.render("GAME OVER", True, RED)
        restart_text = font.render("Press R to restart", True, WHITE)
        final_score_text = font.render(f"Final score: {score}", True, WHITE)

        rect1 = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        rect2 = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
        rect3 = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

        screen.blit(game_over_text, rect1)
        screen.blit(restart_text, rect2)
        screen.blit(final_score_text, rect3)

    pygame.display.update()
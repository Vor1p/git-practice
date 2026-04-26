import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint")

clock = pygame.time.Clock()

# -----------------------------
# ЦВЕТА
# -----------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)

colors = [BLACK, RED, GREEN, BLUE]
current_color = BLACK

# -----------------------------
# РЕЖИМЫ
# -----------------------------
mode = "draw"   # draw / rect / circle / eraser

# -----------------------------
# ПЕРЕМЕННЫЕ ДЛЯ ФИГУР
# -----------------------------
drawing = False
start_pos = None

# холст (чтобы не стиралось при перерисовке)
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# -----------------------------
# ГЛАВНЫЙ ЦИКЛ
# -----------------------------
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # -------------------------
        # КЛАВИШИ (режимы и цвета)
        # -------------------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = "draw"
            elif event.key == pygame.K_2:
                mode = "rect"
            elif event.key == pygame.K_3:
                mode = "circle"
            elif event.key == pygame.K_4:
                mode = "eraser"

            # Цвета
            elif event.key == pygame.K_q:
                current_color = BLACK
            elif event.key == pygame.K_w:
                current_color = RED
            elif event.key == pygame.K_e:
                current_color = GREEN
            elif event.key == pygame.K_r:
                current_color = BLUE

        # -------------------------
        # МЫШКА НАЖАТА
        # -------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        # -------------------------
        # МЫШКА ОТПУЩЕНА
        # -------------------------
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            end_pos = event.pos

            if mode == "rect":
                rect = pygame.Rect(start_pos, 
                                   (end_pos[0] - start_pos[0],
                                    end_pos[1] - start_pos[1]))
                pygame.draw.rect(canvas, current_color, rect, 2)

            elif mode == "circle":
                radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2) ** 0.5)
                pygame.draw.circle(canvas, current_color, start_pos, radius, 2)

        # -------------------------
        # ДВИЖЕНИЕ МЫШИ (рисование)
        # -------------------------
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if mode == "draw":
                    pygame.draw.circle(canvas, current_color, event.pos, 5)

                elif mode == "eraser":
                    pygame.draw.circle(canvas, WHITE, event.pos, 10)

    # -----------------------------
    # ОТРИСОВКА
    # -----------------------------
    screen.fill(WHITE)

    # рисуем холст
    screen.blit(canvas, (0, 0))

    # -----------------------------
    # UI (подсказки)
    # -----------------------------
    font = pygame.font.SysFont("Arial", 18)

    text1 = font.render("Modes: 1-Draw  2-Rect  3-Circle  4-Eraser", True, BLACK)
    text2 = font.render("Colors: Q-Black W-Red E-Green R-Blue", True, BLACK)
    text3 = font.render(f"Current mode: {mode}", True, BLACK)

    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 30))
    screen.blit(text3, (10, 50))

    pygame.display.update()
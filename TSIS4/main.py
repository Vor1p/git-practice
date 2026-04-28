import pygame
import sys
from config import *
from game import Game
from db import Database
from settings_manager import SettingsManager

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# ---------------- STATE ----------------
state = "MENU"
username = ""
game = None

settings = SettingsManager()

# ---------------- DB ----------------
try:
    db = Database()
    use_db = True
except:
    db = None
    use_db = False


# ---------------- BUTTON ----------------
class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)

        txt = self.font.render(self.text, True, (255,255,255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


# ---------------- INPUT ----------------
class InputBox:
    def __init__(self):
        self.rect = pygame.Rect(150, 250, 300, 50)
        self.text = ""
        self.active = False
        self.font = pygame.font.Font(None, 36)

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        return False

    def draw(self):
        pygame.draw.rect(screen, (80,80,80), self.rect)
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)

        txt = self.font.render(self.text or "Enter name", True, (255,255,255))
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 10))


# ---------------- FUNCTIONS ----------------
def start_game():
    global game, state
    game = Game(username, settings)
    state = "PLAY"


def save_score(score, level):
    if use_db:
        try:
            db.save_game_result(username, score, level)
        except:
            pass


# ---------------- UI ----------------
btn_play = Button(200, 200, 200, 50, "PLAY", (0,150,0))
btn_leaderboard = Button(200, 270, 200, 50, "LEADERBOARD", (0,0,150))
btn_quit = Button(200, 340, 200, 50, "QUIT", (150,0,0))

input_box = InputBox()

# ---------------- LEADERBOARD ----------------
def get_leaderboard():
    if use_db:
        try:
            return db.get_leaderboard(10)
        except:
            return []
    return []


# ---------------- LOOP ----------------
running = True

while running:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # -------- MENU --------
        if state == "MENU":
            if not username:
                if input_box.handle(event):
                    username = input_box.text or "Player"
            else:
                if btn_play.clicked(event):
                    start_game()

                if btn_leaderboard.clicked(event):
                    state = "LEADERBOARD"

                if btn_quit.clicked(event):
                    running = False

        # -------- GAME OVER RETURN --------
        elif state == "GAMEOVER":
            if event.type == pygame.KEYDOWN:
                state = "MENU"
                username = ""
                input_box.text = ""

        # -------- LEADERBOARD EXIT --------
        elif state == "LEADERBOARD":
            if event.type == pygame.KEYDOWN:
                state = "MENU"

    # ---------------- DRAW ----------------

    # -------- MENU --------
    if state == "MENU":
        title = pygame.font.Font(None, 60).render("SNAKE GAME", True, (0,255,0))
        screen.blit(title, (170, 100))

        if not username:
            input_box.draw()
        else:
            btn_play.draw()
            btn_leaderboard.draw()
            btn_quit.draw()

    # -------- PLAY --------
    elif state == "PLAY":
        game.run()   # 👈 ВАЖНО: ВЕСЬ ЦИКЛ ВНУТРИ GAME

        # если Game закончился → переключаем экран
        if game.game_over:
            save_score(game.score, game.level)
            state = "GAMEOVER"

    # -------- LEADERBOARD --------
    elif state == "LEADERBOARD":
        screen.fill((30,30,30))

        data = get_leaderboard()

        y = 100
        for i, row in enumerate(data):
            txt = f"{i+1}. {row[0]} - {row[1]}"
            screen.blit(font.render(txt, True, (255,255,255)), (150, y))
            y += 40

        hint = font.render("Press any key to go back", True, (150,150,150))
        screen.blit(hint, (180, 500))

    # -------- GAME OVER --------
    elif state == "GAMEOVER":
        txt = font.render("GAME OVER", True, (255,0,0))
        screen.blit(txt, (220, 250))

        txt2 = font.render("Press any key", True, (255,255,255))
        screen.blit(txt2, (200, 300))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
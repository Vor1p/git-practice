import pygame
import sys
import os
import random
from persistence import load_settings, load_leaderboard, save_score
from ui import Button, TextInput
from racer import Player, Enemy, Obstacle, PowerUp

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

settings = load_settings()

# --- Sound ---
def load_sound(name):
    try:
        return pygame.mixer.Sound(os.path.join('assets', 'sounds', name))
    except:
        return None

snd_crash = load_sound('crash.wav')
snd_powerup = load_sound('powerup.wav')

# --- State ---
state = "MENU"
player_name = "Player"

score = 0
distance = 0
level = 1

# --- Groups ---
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
powerups = pygame.sprite.Group()
coins = pygame.sprite.Group()

player = None

# --- Reset ---
def reset_game():
    global player, score, distance, level
    all_sprites.empty()
    enemies.empty()
    obstacles.empty()
    powerups.empty()
    coins.empty()

    player = Player(settings["car_color"])
    all_sprites.add(player)

    score = 0
    distance = 0
    level = 1

# --- UI ---
btn_play = Button(200,150,200,50,"Play")
btn_board = Button(200,220,200,50,"Leaderboard")
btn_settings = Button(200,290,200,50,"Settings")
btn_quit = Button(200,360,200,50,"Quit")
btn_back = Button(200,500,200,50,"Back")
btn_retry = Button(200,350,200,50,"Retry")
btn_menu = Button(200,420,200,50,"Menu")
name_input = TextInput(200,250,200,40)

# --- Timers ---
SPAWN_ENEMY = pygame.USEREVENT + 1
SPAWN_OBSTACLE = pygame.USEREVENT + 2
SPAWN_POWERUP = pygame.USEREVENT + 3
SPAWN_COIN = pygame.USEREVENT + 4

pygame.time.set_timer(SPAWN_ENEMY, 1500)
pygame.time.set_timer(SPAWN_OBSTACLE, 2500)
pygame.time.set_timer(SPAWN_POWERUP, 6000)
pygame.time.set_timer(SPAWN_COIN, 1200)

# --- HUD ---
def draw_hud():
    screen.blit(font.render(f"Score: {int(score)}", True, (255,255,255)), (10,10))
    screen.blit(font.render(f"Level: {level}", True, (255,255,255)), (10,40))

# --- Loop ---
running = True
while running:
    screen.fill((50,150,50))
    pygame.draw.rect(screen, (40,40,40), (150,0,300,600))

    for y in range(0,600,40):
        pygame.draw.rect(screen,(255,255,255),(245,(y+int(distance*10))%600,10,20))
        pygame.draw.rect(screen,(255,255,255),(345,(y+int(distance*10))%600,10,20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "MENU":
            if btn_play.is_clicked(event): state = "NAME"
            if btn_board.is_clicked(event): state = "BOARD"
            if btn_settings.is_clicked(event): state = "SETTINGS"
            if btn_quit.is_clicked(event): running = False

        elif state == "NAME":
            name_input.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                player_name = name_input.text or "Player"
                reset_game()
                state = "PLAY"

        elif state == "PLAY":
            if event.type == SPAWN_ENEMY:
                e = Enemy(settings["difficulty"])
                all_sprites.add(e)
                enemies.add(e)

            if event.type == SPAWN_OBSTACLE:
                o = Obstacle()
                all_sprites.add(o)
                obstacles.add(o)

            if event.type == SPAWN_POWERUP:
                p = PowerUp()
                all_sprites.add(p)
                powerups.add(p)

            if event.type == SPAWN_COIN:
                c = PowerUp()  # можно заменить на Coin если есть
                all_sprites.add(c)
                coins.add(c)

        elif state in ["BOARD","SETTINGS"]:
            if btn_back.is_clicked(event): state = "MENU"

        elif state == "GAMEOVER":
            if btn_retry.is_clicked(event):
                reset_game()
                state = "PLAY"
            if btn_menu.is_clicked(event): state = "MENU"

    # --- DRAW STATES ---
    if state == "MENU":
        btn_play.draw(screen)
        btn_board.draw(screen)
        btn_settings.draw(screen)
        btn_quit.draw(screen)

    elif state == "NAME":
        screen.blit(font.render("Enter name:", True, (255,255,255)), (200,200))
        name_input.draw(screen)

    elif state == "PLAY":
        all_sprites.update()

        # движение
        distance += 0.1
        score += 0.2

        # уровень
        if score > level * 200:
            level += 1
            for e in enemies:
                e.speed += 1

        # коллизии
        if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player, obstacles):
            if settings["sound"] and snd_crash:
                snd_crash.play()
            save_score(player_name, int(score), int(distance))
            state = "GAMEOVER"

        # бонусы
        for p in pygame.sprite.spritecollide(player, powerups, True):
            if settings["sound"] and snd_powerup:
                snd_powerup.play()
            player.nitro_active = True
            player.powerup_timer = pygame.time.get_ticks() + 3000

        # монеты
        for c in pygame.sprite.spritecollide(player, coins, True):
            score += 10

        all_sprites.draw(screen)
        draw_hud()

    elif state == "BOARD":
        screen.fill((30,30,30))
        board = load_leaderboard()
        for i, e in enumerate(board):
            txt = f"{i+1}. {e['name']} - {e['score']}"
            screen.blit(font.render(txt, True, (255,255,255)), (150,50+i*30))
        btn_back.draw(screen)

    elif state == "SETTINGS":
        screen.blit(font.render("SETTINGS", True, (255,255,255)), (240,100))
        btn_back.draw(screen)

    elif state == "GAMEOVER":
        screen.blit(font.render("GAME OVER", True, (255,0,0)), (200,250))
        btn_retry.draw(screen)
        btn_menu.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
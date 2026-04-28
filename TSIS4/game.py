import pygame
import random
import sys
from config import *
from db import Database

class Food:
    def __init__(self, x, y, food_type="normal"):
        self.x = x
        self.y = y
        self.type = food_type
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 5000 if food_type == "timer" else None  # 5 seconds for timer food
    
    def get_color(self):
        colors = {
            "normal": GREEN,
            "bonus": YELLOW,
            "timer": ORANGE,
            "poison": DARK_RED
        }
        return colors.get(self.type, GREEN)
    
    def get_points(self):
        points = {
            "normal": 1,
            "bonus": 3,
            "timer": 2,
            "poison": 0
        }
        return points.get(self.type, 1)
    
    def is_expired(self):
        if self.duration and self.type == "timer":
            return pygame.time.get_ticks() - self.spawn_time > self.duration
        return False

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.type = power_type
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 8000  # 8 seconds on field
    
    def get_color(self):
        colors = {
            "speed_boost": CYAN,
            "slow_motion": BLUE,
            "shield": PURPLE
        }
        return colors.get(self.type, WHITE)
    
    def get_effect(self):
        effects = {
            "speed_boost": {"speed_multiplier": 1.5, "duration": 5000},
            "slow_motion": {"speed_multiplier": 0.7, "duration": 5000},
            "shield": {"shield": True, "duration": None}  # Until triggered
        }
        return effects.get(self.type)
    
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.duration

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_color(self):
        return GRAY

class Snake:
    def __init__(self):
        self.body = [(GRID_SIZE // 2, GRID_SIZE // 2)]
        self.direction = RIGHT
        self.grow = False
        self.shield = False
        self.shield_active_until = 0
        self.active_effects = {}
    
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def check_collision(self, obstacles):
        head = self.body[0]
        
        # Wall collision
        if head[0] < 0 or head[0] >= GRID_SIZE or head[1] < 0 or head[1] >= GRID_SIZE:
            if self.shield:
                return False
            return True
        
        # Self collision
        if head in self.body[1:]:
            if self.shield:
                return False
            return True
        
        # Obstacle collision
        if head in [(obs.x, obs.y) for obs in obstacles]:
            if self.shield:
                return False
            return True
        
        return False
    
    def eat_food(self, food_type):
        self.grow = True
        if food_type == "poison":
            # Remove 2 segments
            for _ in range(min(2, len(self.body) - 1)):
                if len(self.body) > 1:
                    self.body.pop()
            return len(self.body) <= 1  # Game over if too short
        return False
    
    def activate_powerup(self, powerup):
        effect = powerup.get_effect()
        if "speed_multiplier" in effect:
            self.active_effects["speed"] = {
                "multiplier": effect["speed_multiplier"],
                "end_time": pygame.time.get_ticks() + effect["duration"]
            }
        elif "shield" in effect:
            self.shield = True
        return True
    
    def update_effects(self):
        current_time = pygame.time.get_ticks()
        
        # Update speed effect
        if "speed" in self.active_effects:
            if current_time > self.active_effects["speed"]["end_time"]:
                del self.active_effects["speed"]
        
        # Update shield effect
        if self.shield:
            pass  # Shield lasts until triggered
    
    def get_speed_multiplier(self):
        if "speed" in self.active_effects:
            return self.active_effects["speed"]["multiplier"]
        return 1.0

class Game:
    def __init__(self, username, settings_manager):
        self.username = username
        self.settings_manager = settings_manager
        self.db = Database()
        self.personal_best = self.db.get_personal_best(username)
        
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        
        self.reset_game()
    
    def reset_game(self):
        self.snake = Snake()
        self.foods = []
        self.powerups = []
        self.obstacles = []
        self.score = 0
        self.level = 1
        self.food_eaten = 0
        self.game_over = False
        
        # Spawn initial food
        self.spawn_food()
        
        # Spawn obstacles for level 3+
        if self.level >= 3:
            self.spawn_obstacles()
    
    def spawn_food(self):
        available_positions = self.get_available_positions()
        if not available_positions:
            return
        
        x, y = random.choice(available_positions)
        
        # Random food type with probabilities
        rand = random.random()
        if rand < 0.6:  # 60% normal
            food_type = "normal"
        elif rand < 0.8:  # 20% bonus
            food_type = "bonus"
        elif rand < 0.9:  # 10% timer
            food_type = "timer"
        else:  # 10% poison
            food_type = "poison"
        
        self.foods.append(Food(x, y, food_type))
    
    def spawn_powerup(self):
        if self.powerups:  # Only one power-up at a time
            return
        
        available_positions = self.get_available_positions()
        if not available_positions:
            return
        
        x, y = random.choice(available_positions)
        power_type = random.choice(["speed_boost", "slow_motion", "shield"])
        self.powerups.append(PowerUp(x, y, power_type))
    
    def spawn_obstacles(self):
        num_obstacles = min(5 + self.level, 15)
        self.obstacles = []
        
        for _ in range(num_obstacles):
            available_positions = self.get_available_positions(include_snake=False)
            if available_positions:
                x, y = random.choice(available_positions)
                self.obstacles.append(Obstacle(x, y))
    
    def get_available_positions(self, include_snake=True):
        taken = set()
        
        # Add obstacles
        for obs in self.obstacles:
            taken.add((obs.x, obs.y))
        
        # Add foods
        for food in self.foods:
            taken.add((food.x, food.y))
        
        # Add powerups
        for powerup in self.powerups:
            taken.add((powerup.x, powerup.y))
        
        # Add snake body
        if include_snake:
            for segment in self.snake.body:
                taken.add(segment)
        
        available = []
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if (x, y) not in taken:
                    available.append((x, y))
        return available
    
    def update(self):
        if self.game_over:
            return
        
        # Update snake effects
        self.snake.update_effects()
        
        # Move snake
        self.snake.move()
        
        # Check collision
        if self.snake.check_collision(self.obstacles):
            self.game_over = True
            self.save_result()
            return
        
        # Check food collision
        head = self.snake.body[0]
        for food in self.foods[:]:
            if head[0] == food.x and head[1] == food.y:
                # Eat food
                game_over = self.snake.eat_food(food.type)
                self.score += food.get_points()
                self.food_eaten += 1
                self.foods.remove(food)
                
                if game_over:
                    self.game_over = True
                    self.save_result()
                    return
                
                # Check level up
                if self.food_eaten >= self.level * FOODS_PER_LEVEL:
                    self.level_up()
                
                self.spawn_food()
                break
        
        # Check powerup collision
        for powerup in self.powerups[:]:
            if head[0] == powerup.x and head[1] == powerup.y:
                self.snake.activate_powerup(powerup)
                self.powerups.remove(powerup)
                break
        
        # Remove expired foods
        self.foods = [f for f in self.foods if not f.is_expired()]
        
        # Remove expired powerups
        self.powerups = [p for p in self.powerups if not p.is_expired()]
        
        # Randomly spawn powerup (5% chance each frame)
        if len(self.powerups) == 0 and random.random() < 0.05:
            self.spawn_powerup()
    
    def level_up(self):
        self.level += 1
        self.food_eaten = 0
        
        # Spawn obstacles for level 3+
        if self.level == 3:
            self.spawn_obstacles()
        elif self.level > 3:
            self.spawn_obstacles()
    
    def save_result(self):
        self.db.save_game_result(self.username, self.score, self.level)
    
    def get_speed(self):
        base_speed = INITIAL_SPEED + (self.level - 1) * SPEED_INCREMENT
        multiplier = self.snake.get_speed_multiplier()
        return int(base_speed * multiplier)
    
    def draw_grid(self):
        if not self.settings_manager.get("grid_overlay"):
            return
        
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (50, 50, 50), (0, y), (WINDOW_WIDTH, y))
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            rect = pygame.Rect(obstacle.x * CELL_SIZE, obstacle.y * CELL_SIZE, 
                              CELL_SIZE - 1, CELL_SIZE - 1)
            pygame.draw.rect(self.screen, obstacle.get_color(), rect)
        
        # Draw foods
        for food in self.foods:
            rect = pygame.Rect(food.x * CELL_SIZE, food.y * CELL_SIZE, 
                              CELL_SIZE - 1, CELL_SIZE - 1)
            pygame.draw.rect(self.screen, food.get_color(), rect)
            
            # Add effect for timer food
            if food.type == "timer":
                remaining = max(0, (food.spawn_time + food.duration - pygame.time.get_ticks()) / 1000)
                font = pygame.font.Font(None, 20)
                text = font.render(str(int(remaining)) + "s", True, WHITE)
                self.screen.blit(text, (food.x * CELL_SIZE + 5, food.y * CELL_SIZE + 5))
        
        # Draw powerups
        for powerup in self.powerups:
            rect = pygame.Rect(powerup.x * CELL_SIZE, powerup.y * CELL_SIZE, 
                              CELL_SIZE - 1, CELL_SIZE - 1)
            pygame.draw.rect(self.screen, powerup.get_color(), rect)
        
        # Draw snake
        snake_color = tuple(self.settings_manager.get("snake_color"))
        for i, segment in enumerate(self.snake.body):
            rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, 
                              CELL_SIZE - 1, CELL_SIZE - 1)
            color = snake_color if i == 0 else (snake_color[0] // 1.5, 
                                                snake_color[1] // 1.5, 
                                                snake_color[2] // 1.5)
            pygame.draw.rect(self.screen, color, rect)
        
        # Draw grid
        self.draw_grid()
        
        # Draw UI
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        best_text = font.render(f"Best: {self.personal_best}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
        self.screen.blit(best_text, (10, 90))
        
        # Draw active effects
        y_offset = 130
        if self.snake.shield:
            shield_text = font.render("SHIELD ACTIVE", True, PURPLE)
            self.screen.blit(shield_text, (10, y_offset))
            y_offset += 40
        
        if "speed" in self.snake.active_effects:
            effect = self.snake.active_effects["speed"]
            remaining = max(0, (effect["end_time"] - pygame.time.get_ticks()) / 1000)
            if effect["multiplier"] > 1:
                text = f"SPEED BOOST: {remaining:.1f}s"
                color = CYAN
            else:
                text = f"SLOW MOTION: {remaining:.1f}s"
                color = BLUE
            speed_text = font.render(text, True, color)
            self.screen.blit(speed_text, (10, y_offset))
        
        pygame.display.flip()
    
    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.snake.direction != DOWN:
                        self.snake.direction = UP
                    elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                        self.snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                        self.snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                        self.snake.direction = RIGHT
            
            self.update()
            self.draw()
            self.clock.tick(self.get_speed())
        
        return True
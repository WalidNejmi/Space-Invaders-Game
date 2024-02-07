import pygame
import random
import time
import pygame.font

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.init()

# Play sound
sound = pygame.mixer.Sound("game_sound.mp3")
sound.play()

bullet_sound = pygame.mixer.Sound("shoot.wav")

clock = pygame.time.Clock()

# Setting up the screen
screen_width = 800
screen_lenght = 600
screen = pygame.display.set_mode((screen_width, screen_lenght))
pygame.display.set_caption("Space Invaders")
screen.fill(BLACK)
pygame.display.flip()

spaceship_image = pygame.image.load("spaceship.png")
spaceship_image.set_colorkey(BLACK)
spaceship_image = pygame.transform.scale(spaceship_image, (70, 70)).convert_alpha()

enemy_image = pygame.image.load("enemy.png")
enemy_image.set_colorkey(BLACK)
enemy_image = pygame.transform.scale(enemy_image, (50, 50)).convert_alpha()

laser_image = pygame.image.load("laser.png")
laser_image.set_colorkey(BLACK)
laser_image = pygame.transform.scale(laser_image, (10, 10)).convert_alpha()

background_image = pygame.image.load("space.png").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_lenght))

title_font = pygame.font.SysFont('Arial', 50, False, False)
title_text = title_font.render("Space Invaders Game", False, WHITE)

# Game variables
score = 0
start_time = time.time()
enemy_spawn_threshold = 10  # Initial threshold for spawning new enemies
enemy_spawn_timer = 0

# Game loop
running = True
game_over = False
game_state = "MENU"

# Define player class
class Player:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = (screen_width - self.width) // 2
        self.y = screen_lenght - self.height - 25
        self.speed = 5
        self.move_upx = False
        self.move_downx = False
        self.move_leftx = False
        self.move_rightx = False

    def move_up(self):
        if self.y > 0:
            self.y -= self.speed

    def move_down(self):
        if self.y < screen_lenght - self.height:
            self.y += self.speed

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x < screen_width - self.width:
            self.x += self.speed

    def draw(self):
        screen.blit(spaceship_image, (self.x, self.y))


# Define enemy class
class Enemy:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = random.randrange(0, screen_width - self.width)
        self.y = random.randrange(20, 300)
        self.speed = 2

    def update(self):
        self.y += self.speed
        if self.y > screen_lenght or self.check_collision():
            self.reset()

    def reset(self):
        self.x = random.randrange(0, screen_width - self.width)
        self.y = random.randrange(-300, -self.height)  # Randomize the starting y position

    def check_collision(self):
        for enemy in enemies:
            if enemy != self:
                if self.x < enemy.x + enemy.width and self.x + self.width > enemy.x and self.y < enemy.y + enemy.height and self.y + self.height > enemy.y:
                    return True
        return False

    def draw(self):
        screen.blit(enemy_image, (self.x, self.y))


# Define bullet class
class Bullet:
    def __init__(self):
        self.width = 5
        self.height = 15
        self.x = 0
        self.y = 0
        self.speed = 8
        self.state = "ready"

    def fire(self, player):
        if self.state == "ready":
            self.x = player.x + player.width // 2 - self.width // 2
            self.y = player.y
            self.state = "fire"

    def update(self):
        if self.state == "fire":
            self.y -= self.speed
            if self.y <= 0:
                self.reset()

    def reset(self):
        self.state = "ready"

    def draw(self):
        if self.state == "fire":
            screen.blit(laser_image, (self.x, self.y))

class Stars:
    def __init__(self):
        self.font = pygame.font.SysFont('Calibri', 30, False, False)
        self.rgb1 = random.randrange(0, 255)
        self.rgb2 = random.randrange(0, 255)
        self.rgb3 = random.randrange(0, 255)
        self.text = self.font.render(".", True, (self.rgb1, self.rgb2, self.rgb3))

    def update(self):
        self.x = random.randrange(0, 800)
        self.y = random.randrange(0, 600)

    def draw(self):
        screen.blit(self.text, [self.x, self.y])

# Create objects
player = Player()
enemies = [Enemy() for _ in range(5)]  # Create a list of enemy objects
bullet = Bullet()
stars = [Stars() for _ in range(50)]  # Create a list of star objects

# Menu button class
class Button:
    def __init__(self, x, y, width, height, color, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 50)
        text = font.render(self.text, False, BLACK)
        text_rect = text.get_rect(center=(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
        screen.blit(text, text_rect)

    def check_collision(self, pos):
        return self.rect.collidepoint(pos)

# Menu button action functions
def start_game():
    global game_state
    game_state = "GAME"

def quit_game():
    global running
    running = False

# Create menu buttons
play_button = Button(350, 300, 75, 30, WHITE, "Play", start_game)

def draw_on_menu():
    screen.fill(BLACK)
    screen.blit(background_image, [0, 0])
    screen.blit(title_text, (175, 150))
    pygame.display.flip()

def reset_game():
    global player, enemies, bullet, score, start_time, enemy_spawn_threshold, enemy_spawn_timer

    player = Player()
    enemies = [Enemy() for _ in range(5)]
    bullet = Bullet()
    score = 0
    start_time = time.time()
    enemy_spawn_threshold = 10
    enemy_spawn_timer = 0
    font = pygame.font.SysFont('Calibri', 50, True, False)
    reset = font.render("Starting over...", True, WHITE)
    screen.blit(reset, (245, 250))
    sound = pygame.mixer.Sound("reset_sound.wav")
    sound.play()
    pygame.display.flip()
    time.sleep(2)


while game_state == "MENU":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            game_state = "QUIT"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if play_button.check_collision(mouse_pos):
                start_game()
    # Draw menu screen
    draw_on_menu()
    play_button.draw()
    pygame.display.flip()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "GAME":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_leftx = True
                elif event.key == pygame.K_RIGHT:
                    player.move_rightx = True
                elif event.key == pygame.K_UP:
                    player.move_upx = True
                elif event.key == pygame.K_DOWN:
                    player.move_downx = True
                elif event.key == pygame.K_SPACE:
                    bullet.fire(player)
                    bullet_sound.play()
                elif event.key == pygame.K_r:
                    # Reset the game when "r" is pressed
                    reset_game()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.move_leftx = False
                elif event.key == pygame.K_RIGHT:
                    player.move_rightx = False
                elif event.key == pygame.K_UP:
                    player.move_upx = False
                elif event.key == pygame.K_DOWN:
                    player.move_downx = False

    if game_state == "GAME":
        # Update player position
        if player.move_upx:
            player.move_up()
        if player.move_downx:
            player.move_down()
        if player.move_leftx:
            player.move_left()
        if player.move_rightx:
            player.move_right()

        # Update game objects
        for enemy in enemies:
            enemy.update()
        bullet.update()

        # Check for collision with player
        for enemy in enemies:
            if player.x < enemy.x + enemy.width and player.x + player.width > enemy.x and player.y < enemy.y + enemy.height and player.y + player.height > enemy.y:
                running = False

        # Check for collision with bullet
        for enemy in enemies:
            if bullet.x >= enemy.x and bullet.x <= enemy.x + enemy.width and bullet.y <= enemy.y + enemy.height:
                enemy.reset()
                bullet.reset()
                score += 100

        # Calculate time elapsed
        elapsed_time = time.time() - start_time

        # Check if one second has passed
        if elapsed_time >= 1:
            score += 200
            start_time = time.time()

        # Spawn new enemies
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_threshold:
            enemies.append(Enemy())
            enemy_spawn_timer = 0
            enemy_spawn_threshold += 5  

        # Draw everything on the screen
        screen.fill(BLACK)
        player.draw()
        for enemy in enemies:
            enemy.draw()
        bullet.draw()

        # Update and draw stars
        for star in stars:
            star.update()
            star.draw()

        # Draw score
        font = pygame.font.SysFont('Calibri', 25, True, False)
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        clock.tick(60)
        pygame.display.flip()

# Game over
if game_state == "GAME":
    print("Game Over")
    print("Score:", score)
    font = pygame.font.SysFont('Calibri', 50, True, False)
    game_over = font.render("Game Over", True, RED)
    screen.blit(game_over, (265, 250))
    pygame.display.flip()
    # PLay the game over
    sound = pygame.mixer.Sound("gameover.wav")
    sound.play()
    time.sleep(3)

# Quit the game
pygame.quit()
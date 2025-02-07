import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.5
JUMP_STRENGTH = 10
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
ENEMY_SPEED = 2
BULLET_WIDTH = 5
BULLET_HEIGHT = 5
BULLET_SPEED = 10
PLANK_WIDTH = 100
PLANK_HEIGHT = 20

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19) 
GREEN = (0, 255, 0)  

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("help")

class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera_rect.topleft)

    def update(self, target):
        x = -target.rect.centerx + SCREEN_WIDTH // 2
        y = -target.rect.centery + SCREEN_HEIGHT // 2

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = max(-(self.height - SCREEN_HEIGHT), y)

        self.camera_rect = pygame.Rect(x, y, self.width, self.height)

class Player:
    def __init__(self, map_width):
        self.rect = pygame.Rect(100, SCREEN_HEIGHT - PLAYER_HEIGHT - 100, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.velocity_y = 0
        self.on_ground = False
        self.direction = 1
        self.planks = 0  
        self.map_width = map_width  
        self.score = 0 

    def move(self, dx):
        self.rect.x += dx
        
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > self.map_width - PLAYER_WIDTH:
            self.rect.x = self.map_width - PLAYER_WIDTH

        if dx < 0:
            self.direction = -1
        elif dx > 0:
            self.direction = 1

    def jump(self):
        if self.on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.on_ground = False

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        if self.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
            self.on_ground = True
            self.velocity_y = 0

class Enemy:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.direction = direction  # 1 for right, -1 for left

    def update(self):
        self.rect.x += ENEMY_SPEED * self.direction

class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, BULLET_WIDTH, BULLET_HEIGHT)
        self.direction = direction
        self.start_x = x
        self.max_distance = 300

    def update(self):
        self.rect.x += BULLET_SPEED * self.direction

        if abs(self.rect.x - self.start_x) > self.max_distance:
            return True
        return False

class Plank:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLANK_WIDTH, PLANK_HEIGHT)
        self.broken = False

    def draw(self, surface, camera):
        if not self.broken:
            pygame.draw.rect(surface, BROWN, camera.apply(self))

def menu():
    while True:
        screen.fill(WHITE)

        font = pygame.font.Font(None, 74)
        title_text = font.render("omegalol", True, BLACK)
        start_text = font.render("Начать", True, BLACK)
        exit_text = font.render("Выход", True, BLACK)

        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(exit_text, exit_rect)

        mouse_pos = pygame.mouse.get_pos()
        if start_rect.collidepoint(mouse_pos):
            start_text = font.render("Начать игру", True, BLACK)
            if pygame.mouse.get_pressed()[0]:
                return
        else:
            start_text = font.render("Начать игру", True, BLACK)

        if exit_rect.collidepoint(mouse_pos):
            exit_text = font.render("Выход", True, BLACK)
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                sys.exit()
        else:
            exit_text = font.render("Выход", True, BLACK)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def game_over_screen(score):
    while True:
        screen.fill(WHITE)

        font = pygame.font.Font(None, 74)
        game_over_text = font.render("Game Over", True, BLACK)
        score_text = font.render(f"Score: {score}", True, BLACK)
        retry_text = font.render("Retry", True, BLACK)
        exit_text = font.render("Exit", True, BLACK)

        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(retry_text, retry_rect)
        screen.blit(exit_text, exit_rect)

        mouse_pos = pygame.mouse.get_pos()
        if retry_rect.collidepoint(mouse_pos):
            retry_text = font.render("Retry", True, BLACK)
            if pygame.mouse.get_pressed()[0]:
                return True
        else:
            retry_text = font.render("Retry", True, BLACK)

        if exit_rect.collidepoint(mouse_pos):
            exit_text = font.render("Exit", True, BLACK)
            if pygame.mouse.get_pressed()[0]:
                return False
        else:
            exit_text = font.render("Exit", True, BLACK)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def load_map_image(filename, new_size):
    original_image = pygame.image.load(filename).convert()
    return pygame.transform.scale(original_image, new_size)

new_map_size = (1300, 600)
map_image = load_map_image("img/middle.png", new_map_size)

menu()
player = Player(new_map_size[0])
enemies = []
bullets = []


plank = Plank(300, SCREEN_HEIGHT - 100)  
camera = Camera(new_map_size[0], new_map_size[1])

clock = pygame.time.Clock()
enemy_spawn_time = 0
notification = ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-5)
    if keys[pygame.K_RIGHT]:
        player.move(5)
    if keys[pygame.K_SPACE]:
        player.jump()
    if keys[pygame.K_f]:
        if player.direction == 1:
            bullets.append(Bullet(player.rect.x + PLAYER_WIDTH,
                                  player.rect.y + PLAYER_HEIGHT // 2,
                                  player.direction))
        else:
            bullets.append(Bullet(player.rect.x - BULLET_WIDTH,
                                  player.rect.y + PLAYER_HEIGHT // 2,
                                  player.direction))
    if keys[pygame.K_t]:
        if plank.rect.colliderect(player.rect) and not plank.broken:
            player.planks += 1
            plank.broken = True
            notification = "Вы собрали доску!"

    player.update()

    enemy_spawn_time += clock.get_time()
    if enemy_spawn_time >= 1000: 
        spawn_side = random.choice(["left", "right"])
        
        if spawn_side == "left":
            spawn_x = -ENEMY_WIDTH 
            direction = 1 
        else:
            spawn_x = new_map_size[0]  
            direction = -1  
        
      
        spawn_y = player.rect.y

        enemies.append(Enemy(spawn_x, spawn_y, direction))
        enemy_spawn_time = 0  

    for enemy in enemies:
        enemy.update()

    for bullet in bullets[:]:
        if bullet.update():
            bullets.remove(bullet)
            continue
        for enemy in enemies[:]:
            if bullet.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                if bullet in bullets:
                    bullets.remove(bullet)
                    player.score += 1  
                    break

    
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            if game_over_screen(player.score):
                player = Player(new_map_size[0])
                enemies = []
                bullets = []
                plank = Plank(300, SCREEN_HEIGHT - 100)
                player.score = 0
            else:
                pygame.quit()
                sys.exit()

    
    screen.fill(WHITE)
    screen.blit(map_image, (0, 0))

    camera.update(player)

    
    screen.blit(map_image, camera.camera_rect.topleft)

    pygame.draw.rect(screen, BLUE, camera.apply(player))

    
    plank.draw(screen, camera)
    for enemy in enemies:
        pygame.draw.rect(screen, RED, camera.apply(enemy))

    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, camera.apply(bullet))


    if notification:
        font = pygame.font.Font(None, 36)
        notification_text = font.render(notification, True, BLACK)
        screen.blit(notification_text, (SCREEN_WIDTH // 2 - notification_text.get_width() // 2, SCREEN_HEIGHT // 2))
        notification = ""  


    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {player.score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
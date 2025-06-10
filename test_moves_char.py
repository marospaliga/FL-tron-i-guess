import pygame

# --- Initialization ---
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1000, 1000
FPS = 60
LINE_LENGTH = 10000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(0, 0, 255)):
        super().__init__()
        self.color = color
        self.size = 15
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(color)
        self.x = x
        self.y = y
        self.speed = 5
        self.life = 3
        self.dx = -1
        self.dy = 0
        self.line = []  # was tail, now line
        self.line_color = (color[0]//2, color[1]//2, color[2]//2)  # darker line

    def move(self):
        # Store head center as new line segment
        center = (int(self.x + self.size // 2), int(self.y + self.size // 2))
        if not self.line or self.line[-1] != center:
            self.line.append(center)
        if len(self.line) > LINE_LENGTH:
            self.line.pop(0)
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self, surf):
        if len(self.line) > 1:
            pygame.draw.lines(surf, self.line_color, False, self.line, 10) #line/s 10 = wide
        pygame.draw.rect(surf, self.color, (self.x, self.y, self.size, self.size))

    def get_head(self): #headshot
        return (int(self.x + self.size // 2), int(self.y + self.size // 2)) 

    def check_self_collision(self): #headshot checker
        head = self.get_head()
        return any(abs(head[0] - p[0]) < self.size//2 and abs(head[1] - p[1]) < self.size//2 for p in self.line[:-10]) 

    def check_collision_with(self, other): #wall collision checker
        head = self.get_head()
        other_head = other.get_head()
        return (
            any(abs(head[0] - p[0]) < self.size//2 and abs(head[1] - p[1]) < self.size//2 for p in other.line)
            or (abs(head[0] - other_head[0]) < self.size//2 and abs(head[1] - other_head[1]) < self.size//2)
        )

    def check_bounds(self):
        return not (0 <= self.x <= WIDTH - self.size and 0 <= self.y <= HEIGHT - self.size)

    def reset(self, x, y, dx, dy):
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy
        self.line.clear()
        self.life -= 1

class Player2(Player):
    def __init__(self, x, y):
        super().__init__(x, y, color=(255, 255, 0))
        self.dx = 1
        self.dy = 0

font = pygame.font.Font(None, 36)
run = True

# --- Instantiate Players ---
player = Player(700, 500, color=(0, 0, 255))
player2 = Player(300, 500, color=(255, 255, 0))

paused = False # defined pause

# --- Game Loop ---
while run:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = not paused  # pause

    if paused:
        # Draw current state, then overlay pause message
        player.draw(screen)
        player2.draw(screen)
        screen.blit(font.render(f'Player 1: {player.life}', True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f'Player 2: {player2.life}', True, (255, 255, 255)), (800, 10))
        pause_msg = font.render("PAUSED - Press P to resume", True, (255, 0, 0))
        screen.blit(pause_msg, (WIDTH//2 - pause_msg.get_width()//2, HEIGHT//2 - 50))
        pygame.display.update()
        continue


    keys = pygame.key.get_pressed()

    # Player 1 controls (arrow keys) - changes direction, but always moves
    if keys[pygame.K_LEFT] and player.dx != 1:
        player.dx, player.dy = -1, 0
    if keys[pygame.K_RIGHT] and player.dx != -1:
        player.dx, player.dy = 1, 0
    if keys[pygame.K_UP] and player.dy != 1:
        player.dx, player.dy = 0, -1
    if keys[pygame.K_DOWN] and player.dy != -1:
        player.dx, player.dy = 0, 1

    # Player 2 controls (WASD) - changes direction, but always moves
    if keys[pygame.K_a] and player2.dx != 1:
        player2.dx, player2.dy = -1, 0
    if keys[pygame.K_d] and player2.dx != -1:
        player2.dx, player2.dy = 1, 0
    if keys[pygame.K_w] and player2.dy != 1:
        player2.dx, player2.dy = 0, -1
    if keys[pygame.K_s] and player2.dy != -1:
        player2.dx, player2.dy = 0, 1

    player.move()
    player2.move()

    # --- Collision & Bounds Check ---
    if player.check_bounds() or player.check_self_collision() or player.check_collision_with(player2):
        player.reset(700, 500, -1, 0)
        player2.reset(300, 500, 1, 0)

    if player2.check_bounds() or player2.check_self_collision() or player2.check_collision_with(player):
        player.reset(700, 500, -1, 0)
        player2.reset(300, 500, 1, 0)

    if player.life == 0 or player2.life == 0:
        run = False

    # --- Draw ---
    player.draw(screen)
    player2.draw(screen)

    screen.blit(font.render(f'Player 1: {player.life}', True, (255, 255, 255)), (10, 10))
    screen.blit(font.render(f'Player 2: {player2.life}', True, (255, 255, 255)), (800, 10))

    pygame.display.update()

pygame.quit()

#nice game 
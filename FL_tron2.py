import pygame

pygame.font.init()
pygame.init()
pygame.display.set_caption("yeah")
clock = pygame.time.Clock()

GUI = pygame.display.set_mode((800, 800))

run = True

trail = []
trail2 = []
trial_color = (0,0,150)
trial2_color = (150,150,0)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(0, 0, 255)):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(color)
        self.color = color
        self.x = x
        self.y = y
        self.speed = 5
        self.life = 3
        self.dx = -1  # pohyb vlavo
        self.dy = 0
    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
    


class Player2(Player):
    def __init__(self, x, y):
        super().__init__(x, y, color=(255, 255, 0))
        self.dx = 1  # pohyb vpravo
        self.dy = 0



player = Player(600, 400)
player2 = Player2(200, 400)

while run:
    clock.tick(60)
    font = pygame.font.Font(None, 36)
    GUI.fill(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    trail.append([player.x, player.y])
    trail2.append([player2.x, player2.y])

    for pos in trail:
        pygame.draw.rect(GUI, trial_color, (*pos, 15, 15))
    for pos in trail2:
        pygame.draw.rect(GUI, trial2_color, (*pos, 15, 15))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.dx != 1:
        player.dx, player.dy = -1, 0
    if keys[pygame.K_RIGHT] and player.dx != -1:
        player.dx, player.dy = 1, 0
    if keys[pygame.K_UP] and player.dy != 1:
        player.dx, player.dy = 0, -1
    if keys[pygame.K_DOWN] and player.dy != -1:
        player.dx, player.dy = 0, 1


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

    def check_bounds(p):
        out = False
        if p.x < 0 or p.x > 800 - 15 or p.y < 0 or p.y > 800 - 15:
            p.life -= 1
            out = True
        return out

    if check_bounds(player):
        player.x, player.y = 600, 400
        player.dx, player.dy = -1, 0
    if check_bounds(player2):
        player2.x, player2.y = 200, 400
        player2.dx, player2.dy = 1, 0

    if player.life == 0 or player2.life == 0:
        run = False

    GUI.blit(player.image, (player.x, player.y))
    GUI.blit(player2.image, (player2.x, player2.y))
    life = font.render(f'Player 1: {player.life}', True, (255, 255, 255))
    life2 = font.render(f'Player 2: {player2.life}', True, (255, 255, 255))
    GUI.blit(life, (10, 10))
    GUI.blit(life2, (650, 10))

    pygame.display.update()

pygame.quit()
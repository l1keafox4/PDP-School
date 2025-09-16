"""Dodge Blocks - simple Pygame mini-game for portfolio."""
import pygame
import random
import sys

WIDTH, HEIGHT = 600, 800
FPS = 60
PLAYER_SIZE = 50
BLOCK_WIDTH = 50
BLOCK_HEIGHT = 50

pygame.init()
FONT = pygame.font.SysFont('Arial', 24)
BIGFONT = pygame.font.SysFont('Arial', 48)

def draw_text(surface, text, size, x, y, center=False, color=(255,255,255)):
    if size == 'big':
        font = BIGFONT
    else:
        font = FONT
    txt = font.render(text, True, color)
    rect = txt.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(txt, rect)

class Player:
    def __init__(self):
        self.rect = pygame.Rect((WIDTH//2 - PLAYER_SIZE//2, HEIGHT - PLAYER_SIZE - 20), (PLAYER_SIZE, PLAYER_SIZE))
        self.speed = 7

    def move(self, dx):
        self.rect.x += dx * self.speed
        self.rect.x = max(0, min(WIDTH - PLAYER_SIZE, self.rect.x))

    def draw(self, surf):
        pygame.draw.rect(surf, (66, 135, 245), self.rect, border_radius=8)
        # eyes
        eye_w = 6
        pygame.draw.rect(surf, (255,255,255), (self.rect.x+12, self.rect.y+14, eye_w, eye_w))
        pygame.draw.rect(surf, (255,255,255), (self.rect.x+PLAYER_SIZE-18, self.rect.y+14, eye_w, eye_w))

class Block:
    def __init__(self, x, y, speed, w=BLOCK_WIDTH, h=BLOCK_HEIGHT):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
        self.color = (random.randint(180,255), random.randint(50,180), random.randint(50,180))

    def update(self):
        self.rect.y += self.speed

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=6)

class Star:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.polygon(surface, (255, 223, 0), [(self.rect.centerx, self.rect.top),
                                                     (self.rect.left, self.rect.centery),
                                                     (self.rect.centerx, self.rect.bottom),
                                                     (self.rect.right, self.rect.centery)])

def main():
    global BLOCK_SPEED_BASE
    BLOCK_SPEED_BASE = 3
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dodge Blocks")
    clock = pygame.time.Clock()

    running = True
    game_started = False
    star_count = 0

    while running:
        screen.fill((30,30,40))
        draw_text(screen, "Dodge Blocks", 'big', WIDTH//2, HEIGHT//2-40, center=True, color=(240,240,240))
        draw_text(screen, "Press SPACE to start", 'small', WIDTH//2, HEIGHT//2+10, center=True, color=(200,200,200))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True
                    break

        if game_started:
            break

    player = Player()
    blocks = []
    stars = []
    spawn_timer = 0
    spawn_interval = 800  # milliseconds
    score = 0
    game_over = False
    last_tick = pygame.time.get_ticks()

    while running:
        dt = clock.tick(FPS)
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if game_over and event.key == pygame.K_r:
                    player = Player()
                    blocks = []
                    stars = []
                    spawn_timer = 0
                    star_count = 0
                    score = 0
                    game_over = False
                    last_tick = pygame.time.get_ticks()

        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if not game_over:
            player.move(dx)

        if not game_over:
            spawn_timer += dt
            if spawn_timer >= spawn_interval:
                spawn_timer = 0
                lane_x = random.choice([100, 200, 300, 400, 500])
                speed = BLOCK_SPEED_BASE + (score // 10)
                blocks.append(Block(lane_x, -BLOCK_HEIGHT, speed))

        # spawn stars
        if not game_over:
            if random.random() < 0.01:  # 1% chance every frame
                lane_x = random.choice([100, 200, 300, 400, 500])
                stars.append(Star(lane_x, -30, BLOCK_SPEED_BASE))

        if not game_over:
            for b in blocks:
                b.update()

        for b in blocks:
            if b.rect.colliderect(player.rect):
                game_over = True

        # update stars
        for star in stars:
            star.update()
            if star.rect.colliderect(player.rect):
                player.speed += 1  # Increase player speed on star collection
                stars.remove(star)
                star_count += 1

        before = len(blocks)
        blocks = [b for b in blocks if b.rect.y <= HEIGHT + 50]
        removed = before - len(blocks)
        if removed > 0 and not game_over:
            score += removed * 1

        # draw stars
        screen.fill((30,30,40))
        pygame.draw.rect(screen, (20,20,30), (0,0, WIDTH, 70))
        draw_text(screen, "Dodge Blocks", 'big', 20, 12, center=False, color=(240,240,240))
        draw_text(screen, f"Score: {score}", 'small', WIDTH-150, 22, color=(200,200,200))
        draw_text(screen, f"Stars: {star_count}", 'small', WIDTH-150, 52, color=(200,200,200))

        pygame.draw.rect(screen, (40,40,55), (10, 80, WIDTH-20, HEIGHT-100), border_radius=12)
        for b in blocks:
            b.draw(screen)
        for star in stars:
            star.draw(screen)
        player.draw(screen)

        if game_over:
            draw_text(screen, "GAME OVER", 'big', WIDTH//2, HEIGHT//2-40, center=True, color=(255,90,90))
            draw_text(screen, f"Score: {score}", 'small', WIDTH//2, HEIGHT//2+10, center=True)
            draw_text(screen, f"Stars: {star_count}", 'small', WIDTH//2, HEIGHT//2+40, center=True)
            draw_text(screen, "Press R to restart or ESC to quit", 'small', WIDTH//2, HEIGHT//2+60, center=True, color=(200,200,200))

        pygame.display.flip()

        # increase difficulty
        if score % 10 == 0 and score > 0:
            BLOCK_SPEED_BASE += 0.1

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

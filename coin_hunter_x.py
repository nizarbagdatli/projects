import pygame
import random
import sys

WIDTH, HEIGHT = 900, 520
FPS = 60

PLAYER_SPEED = 5
ENEMY_SPEED = 3
COIN_RADIUS = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Hunter X")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 56)


class Player:
    def __init__(self):
        self.rect = pygame.Rect(80, HEIGHT // 2 - 18, 36, 36)
        self.lives = 3
        self.score = 0

    def update(self, keys):
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])

        self.rect.x += dx * PLAYER_SPEED
        self.rect.y += dy * PLAYER_SPEED

        self.rect.x = max(0, min(WIDTH - self.rect.w, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.h, self.rect.y))

    def draw(self, surf):
        pygame.draw.rect(surf, (30, 180, 255), self.rect)
        pygame.draw.circle(surf, (255, 255, 255), (self.rect.centerx + 8, self.rect.centery - 6), 4)


class Enemy:
    def __init__(self, speed=ENEMY_SPEED):
        size = random.randint(28, 44)
        self.rect = pygame.Rect(WIDTH + random.randint(40, 200),
                                random.randint(20, HEIGHT - size - 20),  size, size)
        self.speed = speed 
        self.hit_cd = 0  

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = WIDTH + random.randint(40, 220)
            self.rect.y = random.randint(20, HEIGHT - self.rect.h - 20)

        if self.hit_cd > 0:
            self.hit_cd -= 1

    def draw(self, surf):
        pygame.draw.rect(surf, (255, 80, 80), self.rect)


class Coin:
    def __init__(self):
        self.pos = [random.randint(140, WIDTH - 40), random.randint(30, HEIGHT - 30)]
        self.r = COIN_RADIUS

    def respawn(self):
        self.pos[0] = random.randint(140, WIDTH - 40)
        self.pos[1] = random.randint(30, HEIGHT - 30)

    def draw(self, surf):
        pygame.draw.circle(surf, (255, 200, 20), self.pos, self.r)
        pygame.draw.circle(surf, (255, 240, 180), self.pos, max(2, self.r // 3), 2)

    def collides_with_player(self, player_rect):
        cx, cy = self.pos
        closest_x = max(player_rect.left, min(cx, player_rect.right))
        closest_y = max(player_rect.top,  min(cy, player_rect.bottom))
        dx = cx - closest_x
        dy = cy - closest_y
        return (dx * dx + dy * dy) <= (self.r * self.r)


def draw_hud(player, level):
    hud = f"Score: {player.score}   Lives: {player.lives}   Level: {level}"
    screen.blit(font.render(hud, True, (235, 235, 235)), (16, 12))


def main():
    player = Player()
    coin = Coin()

    level = 1
    enemies = [Enemy(speed=ENEMY_SPEED)]
    game_over = False

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player = Player()
                    coin = Coin()
                    level = 1
                    enemies = [Enemy(speed=ENEMY_SPEED)]
                    game_over = False

        keys = pygame.key.get_pressed()
        if not game_over:
            player.update(keys)

            for e in enemies:
                e.update()

            if coin.collides_with_player(player.rect):
                player.score += 10
                coin.respawn()

                if player.score % 50 == 0:
                    level += 1
                    enemies.append(Enemy(speed=ENEMY_SPEED + level * 0.35))

            for e in enemies:
                if player.rect.colliderect(e.rect) and e.hit_cd == 0:
                    player.lives -= 1
                    e.hit_cd = 30  
                    if player.lives <= 0:
                        game_over = True

        screen.fill((18, 18, 24))
        coin.draw(screen)
        for e in enemies:
            e.draw(screen)
        player.draw(screen)
        draw_hud(player, level)

        if game_over:
            msg1 = big_font.render("GAME OVER", True, (240, 240, 240))
            msg2 = font.render("Press R to restart", True, (240, 240, 240))
            screen.blit(msg1, msg1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
            screen.blit(msg2, msg2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

        pygame.display.flip()


if __name__ == "__main__":
    main()

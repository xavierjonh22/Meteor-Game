import pygame
import random
import sys
import os
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Meteor Evader")
WIDTH, HEIGHT = 800, 800
SPACESHIPSIZE = 40
FPS = 60


class Spaceship:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, SPACESHIPSIZE, SPACESHIPSIZE)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        self.rect.x = max(0, min(self.rect.x, WIDTH - SPACESHIPSIZE))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - SPACESHIPSIZE))
class Meteor:
    def __init__(self):
        self.size = random.randint(20, 60)
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.spawn_meteor()

    def spawn_meteor(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            self.rect.x = random.randint(0, WIDTH - self.size)
            self.rect.y = 0
            self.dy = random.randint(2, 6)
            self.dx = 0
        elif side == 'bottom':
            self.rect.x = random.randint(0, WIDTH - self.size)
            self.rect.y = HEIGHT - self.size
            self.dy = -random.randint(2, 6)
            self.dx = 0
        elif side == 'left':
            self.rect.x = 0
            self.rect.y = random.randint(0, HEIGHT - self.size)
            self.dy = 0
            self.dx = random.randint(2, 6)
        elif side == 'right':
            self.rect.x = WIDTH - self.size
            self.rect.y = random.randint(0, HEIGHT - self.size)
            self.dy = 0
            self.dx = -random.randint(2, 6)

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
def main():
    clock = pygame.time.Clock()
    spaceship = Spaceship()
    meteors = []
    spawntime = 0
    survivaltime = 0
    longesttime = 0
    running = True

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * 5
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * 5
        spaceship.move(dx, dy)


        spawntime += clock.get_time()
        if spawntime > 5000:
            meteor = Meteor()
            meteors.append(meteor)

            spawntime = 0


        for meteor in meteors[:]:
            meteor.move()
            if meteor.rect.colliderect(spaceship.rect):
                game_over = True
                while game_over:
                    screen.fill((0, 0, 0))
                    font = pygame.font.Font(None, 50)
                    game_over_text = font.render("Game Over", True, (255, 0, 0))
                    time_text = font.render(f"Survival Time: {survivaltime // 1000}s", True, (255, 255, 255))
                    best_text = font.render(f"Best Time: {longesttime // 1000}s", True, (255, 255, 255))
                    Exit_text = font.render("Press ESC to quit", True, (255, 255, 255))

                    screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 200))
                    screen.blit(time_text, (WIDTH //2 - 250, HEIGHT // 2 - 30))
                    screen.blit(best_text, (WIDTH // 2 - 130, HEIGHT // 2 + 20))
                    screen.blit(Exit_text, (WIDTH // 2 - 140, HEIGHT // 2 + 80))
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        pygame.quit()
                        sys.exit()




            if (meteor.rect.x < 0 or meteor.rect.x > WIDTH or
                    meteor.rect.y < 0 or meteor.rect.y > HEIGHT):
                meteors.remove(meteor)

            pygame.draw.rect(screen, (255, 0, 0), meteor.rect)


        pygame.draw.rect(screen, (0, 255, 0), spaceship.rect)


        survivaltime += clock.get_time()
        timer_surface = pygame.font.Font(None, 36).render(f'Time: {survivaltime // 1000}', True, (255, 255, 255))
        screen.blit(timer_surface, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
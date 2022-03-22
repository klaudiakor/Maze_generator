
import sys
import pygame
import maze_generator as mg

screen_width = 640
screen_height = 400

# 16x16 - wall size
maze_height = screen_height//16
maze_width = screen_width//16


class Player(object):
    speed = 2

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)

    def moveRight(self):
        self.rect.x += self.speed
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.right = wall.rect.left

    def moveLeft(self):
        self.rect.x -= self.speed
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.left = wall.rect.right

    def moveDown(self):
        self.rect.y += self.speed
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.bottom = wall.rect.top

    def moveUp(self):
        if self.rect.y < 0:
            self.rect.y += self.speed
        self.rect.y -= self.speed
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.top = wall.rect.bottom


class Wall(object):

    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)


pygame.init()


pygame.display.set_caption("Get to the red square!")
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
walls = []

maze = mg.generateMaze(maze_height, maze_width).splitlines()

x = 1
y = 1
for row in maze:
    for col in row:
        if col == '0':
            Wall((x, y))
        if col == 'I':  # Entrance
            player = Player(x+3, 0)
        if col == 'O':  # Exit
            end_rect = pygame.Rect(x+3, y, 10, 10)
        x += 8
    y += 16
    x = 1

running = True
while running:

    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.moveLeft()
    if key[pygame.K_RIGHT]:
        player.moveRight()
    if key[pygame.K_UP]:
        player.moveUp()
    if key[pygame.K_DOWN]:
        player.moveDown()

    if player.rect.colliderect(end_rect):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("YOU WON", 1, (255, 255, 255))
        text_rec = text.get_rect(center=(screen_width/2, screen_height/2))
        screen.blit(text, text_rec)
        pygame.display.flip()
        pygame.time.delay(1000)
        pygame.quit()
        sys.exit()

    # Draw the scene
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (0, 128, 64), wall.rect)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.ellipse(screen, (255, 200, 0), player.rect)
    pygame.display.flip()
    clock.tick(360)

pygame.quit()

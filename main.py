from game import Game
import pygame, sys

# general setup
pygame.init()
clock = pygame.time.Clock()
icon = pygame.image.load('assets/icon.png')

# colors
BG_COLOR = (21, 21, 21)
BG_PATTER_COLOR = (20, 20, 20)

# screen
screen_width = 500
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Catch them Eggs, Fool!')
pygame.display.set_icon(icon)
rect_size = 50

game = Game(screen, screen_width, screen_height)

def bg():
    for x in range(0, screen_width, rect_size):
        for y in range(0, screen_height, rect_size):
            rect = pygame.Rect(x, y, rect_size, rect_size)
            pygame.draw.rect(screen, BG_PATTER_COLOR, rect, 2)

# loop
while True:
    # bg
    screen.fill(BG_COLOR)
    bg()
    # events
    if game.close_window:
        pygame.quit()
        sys.exit()

    game.run()

    pygame.display.update()
    clock.tick(60)

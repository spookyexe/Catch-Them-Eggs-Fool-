import pygame

class Egg(pygame.sprite.Sprite):
    def __init__(self, surface, surface_w, surface_h, size, pos, color) -> None:
        super().__init__()
        self.screen = surface
        self.screen_width = surface_w
        self.screen_height = surface_h

        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)

        self.speed = 6

        self.lose = False

    def boundaries(self):
        # lose
        if self.rect.bottom >= self.screen_height-self.screen_height/16:
            self.lose = True
            print('LOSE')
        # kills the sprite
        if self.rect.bottom >= self.screen_height-self.screen_height/16+self.rect.h/2:
            self.kill()

    def update(self):
        # egg movement
        self.rect.y += self.speed
        # egg boundaries
        self.boundaries()
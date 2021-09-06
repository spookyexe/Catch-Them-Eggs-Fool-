import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, surface, surface_w, surface_h, size, pos, color) -> None:
        super().__init__()
        self.screen = surface
        self.screen_width = surface_w
        self.screen_height = surface_h

        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)

        self.speed = 7
        self.velocity = 0

    def boundaries(self):
        # teleports the player if the player hits the side of the screen to the other side of the screen
        if self.rect.left <= 0-self.rect.w-1:
            self.rect.right = self.screen_width+self.rect.w
        if self.rect.right >= self.screen_width+self.rect.w+1:
            self.rect.left = 0-self.rect.w

    def update(self):
        # player movement
        self.rect.x += self.velocity
        # player boundaries
        self.boundaries()
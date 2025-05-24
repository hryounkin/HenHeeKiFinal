from settings import *

class Sprite(pygame.sprite.Sprite):
    """
    General sprite class for game objects (e.g., ground tiles).
    It scales the provided surface to maintain consistent sizing.
    """
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        # Convert image for faster blitting with per-pixel alpha transparency
        self.image = surf.convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (int(TILE_SIZE * SCALE_FACTOR), int(TILE_SIZE * SCALE_FACTOR))
        )
        # Set the top-left position of the sprite
        self.rect = self.image.get_rect(topleft=pos)

class CollisionSprite(pygame.sprite.Sprite):
    """
    Sprite for collision detection.
    Typically uses plain surfaces to delineate areas where the player cannot move.
    """
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        # The image is used to create the collision rect, no need to scale here
        self.image = surf
        # Set the sprite's position based on the top-left corner
        self.rect = self.image.get_rect(topleft=pos)

class TransitionSprite(CollisionSprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
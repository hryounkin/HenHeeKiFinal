from settings import *

class Sprite(pygame.sprite.Sprite):
    """
    General sprite class for game objects.
    """
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        # Convert image for faster blitting with per-pixel alpha transparency
        self.image = surf.convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (int(TILE_SIZE * SCALE_FACTOR), int(TILE_SIZE * SCALE_FACTOR))
        )
        self.rect = self.image.get_rect(topleft=pos)

class CollisionSprite(pygame.sprite.Sprite):
    """
    Sprite for collision detection.
    """
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class TransitionSprite(CollisionSprite):
    """
    Special case for detecting when the player enters a transition zone.
    """
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)


class RelicSprite(CollisionSprite):
    """
    Used for detecting relics.
    """
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
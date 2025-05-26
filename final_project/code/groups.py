import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT


class AllSprites(pygame.sprite.Group):
    """
    Custom sprite group that handles drawing all sprites with a camera offset.
    It centers the view on a specified target, usually the player's position.
    """
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        # Initialize the camera offset (Vector2 for x and y coordinates)
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        """
        Draws all sprites in the group relative to the target_pos.

        :param target_pos: Tuple (x, y) representing the central point (e.g., player's center)
        """
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        # Draw each sprite with the computed offset
        for sprite in self:
            adjusted_position = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, adjusted_position)
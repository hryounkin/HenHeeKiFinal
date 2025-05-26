import pygame
from os.path import join
from os import walk
from settings import *


class Player(pygame.sprite.Sprite):
    """
    The Player class handles rendering, input, movement, animation,
    and collision detection for the main character.
    """

    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)

        # Dimensions of the player sprite before scaling
        self.width = 16
        self.height = 32

        # Path for the initial player image
        self.object_image = PLAYER_IMAGE_FOLDER + 'sprite_000.png'

        # Load all animation frames for movement
        self.load_images()

        # Set initial animation state
        self.state = 'down'
        self.frame_index = 0

        # Load and scale the default image for initial display
        self.image = pygame.image.load(self.object_image).convert_alpha()
        self.image = pygame.transform.smoothscale(
            self.image, (int(self.width * SCALE_FACTOR), int(self.height * SCALE_FACTOR))
        )
        # Set the initial rect centered at the given position
        self.rect = self.image.get_rect(center=pos)

        # Define the hitbox for collision detection (slightly smaller than the sprite)
        self.hitbox_rect = self.rect.inflate(0, -30)

        # Movement settings
        self.direction = pygame.Vector2()
        self.speed = 400
        self.collision_sprites = collision_sprites


    def load_images(self):
        """
        Loads animation frames from subdirectories for each movement state.
        Images are located in directories named after the state ('up', 'down', etc.)
        """
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}
        for state in self.frames.keys():
            # Walk through the image directory for the given state
            for folder_path, sub_folders, filenames in walk(join('..', 'images', 'player', state)):
                if filenames:
                    for file in filenames:
                        full_path = join(folder_path, file)
                        surf = pygame.image.load(full_path).convert_alpha()
                        surf = pygame.transform.smoothscale(
                            surf, (int(self.width * SCALE_FACTOR), int(self.height * SCALE_FACTOR))
                        )
                        self.frames[state].append(surf)


    def input(self):
        """
        Processes keyboard input to update the movement direction of the player.
        Arrow keys control movement along the x and y axes.
        """
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        # Normalize the vector to ensure consistent speed in diagonal movement
        if self.direction.length() != 0:
            self.direction = self.direction.normalize()


    def move(self, dt):
        """
        Moves the player and handles collision detection.

        :param dt: Delta time in seconds from the last frame (ensures smooth movement).
        """
        # Move horizontally, then resolve horizontal collisions
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # Move vertically, then resolve vertical collisions
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')

        # Align the visible sprite's rect with the hitbox
        self.rect.center = self.hitbox_rect.center


    def collision(self, direction):
        """
        Checks for collisions in a specific direction and adjusts the hitbox accordingly.

        :param direction: String indicator ("horizontal" or "vertical")
        """
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # Moving right
                        self.hitbox_rect.right = sprite.rect.left
                    elif self.direction.x < 0:  # Moving left
                        self.hitbox_rect.left = sprite.rect.right
                elif direction == 'vertical':
                    if self.direction.y < 0:  # Moving up
                        self.hitbox_rect.top = sprite.rect.bottom
                    elif self.direction.y > 0:  # Moving down
                        self.hitbox_rect.bottom = sprite.rect.top


    def animate(self, dt):
        """
        Updates the player's animation frame based on movement and elapsed time.

        :param dt: Delta time in seconds.
        """
        # Change animation state based on the movement direction
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        # Update the frame index when moving; reset if there's no movement
        if self.direction.length() != 0:
            self.frame_index += 5 * dt
        else:
            self.frame_index = 0

        # Update the image based on the current frame in the animation cycle
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]


    def get_position(self):
        return self.rect.center


    def update(self, dt):
        """
        Update function called each frame to process input, move the player, animation, and i_frames.

        :param dt: Delta time in seconds.
        """
        self.input()
        self.move(dt)
        self.animate(dt)
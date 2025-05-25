import pygame
from os.path import join
from os import walk
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, player):
        super().__init__(groups)

        # Dimensions of the player sprite before scaling
        self.width = 16
        self.height = 32

        # Path for the initial enemy image
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
        self.pos = pygame.Vector2(self.rect.center)

        self.hitbox_rect = self.rect.inflate(0, -30)

        # Movement settings
        self.player_to_chase = player
        self.detect_radius = 200
        self.chase_radius = 700
        self.current_radius = self.detect_radius
        self.speed = 100  # Movement speed (pixels per second)
        self.direction = pygame.Vector2()
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


    def chasePlayer(self, player_xy, chase_radius):
        #tracking direction and distance to player
        player_x, player_y = player_xy

        player_distance = pygame.Vector2(player_x, player_y).distance_to(pygame.Vector2(self.rect.center))

        if player_distance < self.chase_radius:
            self.current_radius = self.chase_radius

        #if the player is too far away, the enemy will idle
        if player_distance > chase_radius:
            self.direction=pygame.Vector2(0,0)
            self.current_radius = self.detect_radius

        #if within the chase radius, follow the player
        else:
            self.direction = pygame.Vector2(player_x, player_y) - pygame.Vector2(self.rect.center)
            if self.direction.length() > 0:
                self.direction = self.direction.normalize()


    def move(self, dt):
        """
        Moves the player and handles collision detection.

        :param dt: Delta time in seconds from the last frame (ensures smooth movement).
        """
        self.pos += self.direction * self.speed * dt

        # Move horizontally, then resolve horizontal collisions
        self.hitbox_rect.center = (round(self.pos.x), round(self.pos.y))
        self.collision('horizontal')
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                elif direction == 'vertical':
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                    elif self.direction.y > 0:
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


    def update(self, dt):
        self.chasePlayer(self.player_to_chase.rect.center, self.current_radius)

        self.move(dt)
        self.animate(dt)

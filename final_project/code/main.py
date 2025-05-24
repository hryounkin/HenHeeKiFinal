import pygame.key

from settings import *
from player import Player
from enemy import Enemy
from sprites import Sprite, CollisionSprite, TransitionSprite
from pytmx.util_pygame import load_pygame
from groups import AllSprites


class Game:
    """
    Main game class responsible for initializing the game, loading map data,
    and running the main game loop.
    """


    def __init__(self):
        # Initialize Pygame modules
        pygame.init()

        # Set up the display window
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Final Project COMP1020')

        # Clock for managing frame rates
        self.clock = pygame.time.Clock()
        self.running = True

        # Load background music and set volume
        # self.music = pygame.mixer.Sound(r'..\audio\10. Overworld.mp3')
        # self.music.set_volume(0.3)
        # self.music.play()

        # Set up sprite groups
        self.all_sprites = AllSprites()  # For all renderable sprites
        self.collision_sprites = pygame.sprite.Group()  # For objects that the player collides with
        self.enemy_sprites = pygame.sprite.Group() # For enemies
        self.transition_sprites = pygame.sprite.Group() # For transition zones

        # Player Setup
        self.player_exists = False
        self.player_health = 5

        # Load the map and initialize objects
        self.setup(FINALMAP_FILE)

    def setup(self, MAP_FILE):
        """
        Loads the TMX map and sets up game objects based on specific map layers.
        """
        #Empty collision objects
        self.collision_sprites.empty()
        self.all_sprites.empty()
        self.enemy_sprites.empty()
        self.transition_sprites.empty()

        # Load the map data using PyTMX
        map_data = load_pygame(MAP_FILE)
        self.display_surface.fill('black')
        pygame.time.delay(100)
        # Process collision objects from the 'Collisions' layer
        for obj in map_data.get_layer_by_name('Collision'):
            # Collision objects are scaled using a factor of 2
            CollisionSprite(
                (obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR),
                pygame.Surface((obj.width * SCALE_FACTOR, obj.height * SCALE_FACTOR)),
                self.collision_sprites
            )

        # Process the 'Ground' layer and add each tile as a sprite
        for x, y, image in map_data.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE * SCALE_FACTOR, y * TILE_SIZE * SCALE_FACTOR), image, self.all_sprites)

        # Process the 'Ground_2' layer similarly for additional visual tiles
        for x, y, image in map_data.get_layer_by_name('Objects').tiles():
            Sprite((x * TILE_SIZE * SCALE_FACTOR, y * TILE_SIZE * SCALE_FACTOR), image, self.all_sprites)

        # Locate the starting position for the player via the "Places" layer.
        for obj in map_data.get_layer_by_name("Places"):
            if obj.name == 'Hero':
                if self.player_exists:
                    self.player.kill()
                    self.player = None
                    self.player_exists=False

                self.player = Player(
                    (obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR),
                    self.all_sprites,
                    self.collision_sprites
                )
                self.player_exists=True

            if obj.name == 'Transition':
                TransitionSprite(
                    (obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR),
                    pygame.Surface((obj.width * SCALE_FACTOR, obj.height * SCALE_FACTOR)),
                    self.collision_sprites
                )
            if obj.name == 'Enemy':
                self.enemy = Enemy(
                    (obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR),
                    self.all_sprites,
                    self.enemy_sprites,
                    self.player
                )

    def run(self):
        """
        The main game loop that handles events, updates game objects,
        renders frames, and maintains the frame rate.
        """
        while self.running:
            # Calculate the time delta (in seconds) for smooth movement updates.
            dt = self.clock.tick() / 1000

            main_keys = pygame.key.get_pressed()
            # Event handling loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if main_keys[pygame.K_ESCAPE]:
                self.running = False
            if main_keys[pygame.K_l]:
                self.setup(FIRSTMAP_FILE)
            if main_keys[pygame.K_o]:
                self.setup(BLANKMAP_FILE)
            if main_keys[pygame.K_p]:
                self.setup(FINALMAP_FILE)
            # Update all sprites (calls update on every sprite in the group)
            self.all_sprites.update(dt)

            # Clear the screen with a black background
            self.display_surface.fill('black')
            # Draw all sprites, centering the camera on the player
            self.all_sprites.draw(self.player.rect.center)


            # Update the full display surface to the screen
            pygame.display.update()

        # Clean up and exit when the game loop is terminated
        pygame.quit()


if __name__ == '__main__':
    # Instantiate and run the game
    game = Game()
    game.run()
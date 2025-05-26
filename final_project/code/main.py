import pygame.key

from settings import *
from player import Player
from enemy import Enemy
from sprites import Sprite, CollisionSprite, TransitionSprite, RelicSprite
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from random import randint


class Game:
    """
    Main game class responsible for initializing the game, loading map data,
    tracking player health, and running the main game loop.
    """
    def __init__(self):
        pygame.init()

        #display window setup
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Final Project COMP1020')

        # Clock for managing frame rates
        self.clock = pygame.time.Clock()
        self.running = True

        # Set up sprite groups
        self.all_sprites = AllSprites()  # For all renderable sprites
        self.collision_sprites = pygame.sprite.Group()  # For objects that the player collides with
        self.transition_sprites = pygame.sprite.Group() # For transition zones
        self.relic_sprites = pygame.sprite.Group() #For relics

        #font for UI
        self.font = pygame.font.SysFont('monospace', 24)
        self.font2 = pygame.font.SysFont('monospace', 60)

        # Player Setup
        self.player_exists = False
        self.game_health = 3
        self.invincible = False
        self.invincible_timer = 0

        # Relic setup
        self.relics_collected = 0
        self.snow_relic_collected = False
        self.forest_relic_collected = False


        # Load the map to start
        self.current_map= "Forest"
        self.setup(FOREST_MAP_FILE)


    def setup(self, map_file):
        """
        Loads map layers, clearing out old data.
        """
        #Empty collision and sprite objects
        self.collision_sprites.empty()
        self.all_sprites.empty()
        self.transition_sprites.empty()
        self.relic_sprites.empty()

        # Load the map data using PyTMX
        map_data = load_pygame(map_file)
        self.display_surface.fill('black')
        pygame.time.delay(100)

        # Collision layer setup
        for obj in map_data.get_layer_by_name('collision'):
            CollisionSprite(
                (obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR),
                pygame.Surface((obj.width * SCALE_FACTOR, obj.height * SCALE_FACTOR)),
                self.collision_sprites
            )

        # Base ground layer
        for x, y, image in map_data.get_layer_by_name('ground').tiles():
            Sprite((x * TILE_SIZE * SCALE_FACTOR, y * TILE_SIZE * SCALE_FACTOR), image, self.all_sprites)

        # Objects that exist over the ground layer
        for x, y, image in map_data.get_layer_by_name('objects').tiles():
            Sprite((x * TILE_SIZE * SCALE_FACTOR, y * TILE_SIZE * SCALE_FACTOR), image, self.all_sprites)


        for x, y, image in map_data.get_layer_by_name('relics').tiles():
            if map_file == SNOW_MAP_FILE and self.snow_relic_collected == False:
                Sprite((x * TILE_SIZE * SCALE_FACTOR, y * TILE_SIZE * SCALE_FACTOR), image, self.all_sprites)
            if map_file == FOREST_MAP_FILE and self.forest_relic_collected == False:
                Sprite((x * TILE_SIZE * SCALE_FACTOR, y * TILE_SIZE * SCALE_FACTOR), image, self.all_sprites)


        for obj in map_data.get_layer_by_name('relic_detect'):
            if map_file == SNOW_MAP_FILE and self.snow_relic_collected == False:
                self.relic = RelicSprite(
                    (obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR),
                    pygame.Surface((obj.width * SCALE_FACTOR, obj.height * SCALE_FACTOR)),
                    self.relic_sprites
                )
                self.relic_sprites.add(self.relic)
            if map_file == FOREST_MAP_FILE and self.forest_relic_collected == False:
                self.relic = RelicSprite(
                    (obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR),
                    pygame.Surface((obj.width * SCALE_FACTOR, obj.height * SCALE_FACTOR)),
                    self.relic_sprites
                )
                self.relic_sprites.add(self.relic)



        for obj in map_data.get_layer_by_name("places"):
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
                    self.transition_sprites
                )

            if obj.name == 'Enemy':
                self.enemy = Enemy(
                    (obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR),
                    self.all_sprites,
                    self.collision_sprites,
                    self.player,
                    self,
                    randint(200, 280)
                )

            if obj.name == 'Boss':
                self.enemy = Enemy(
                    (obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR),
                    self.all_sprites,
                    self.collision_sprites,
                    self.player,
                    self,
                    randint(300, 380)
                )


    def map_transition(self, map):
        self.setup(map)

    def game_over(self):
        #ends the game
        game_end_text =  "GAME OVER"
        relic_banner = self.font.render(game_end_text, True, (255, 0, 0))
        self.display_surface.blit(relic_banner, (450 ,350))
        pygame.display.update()
        pygame.time.delay(2800)
        self.running = False

    def game_win(self):
        game_end_text = "YOU WIN"
        relic_banner = self.font.render(game_end_text, True, (255, 0, 0))
        self.display_surface.blit(relic_banner, (450, 350))
        pygame.display.update()
        pygame.time.delay(2800)
        self.running = False

    def take_damage(self, amount):
        if not self.invincible:
            self.game_health -= amount
            if self.game_health <= 0:
                self.game_over()
            self.invincible = True
            self.invincible_timer = pygame.time.get_ticks()


    def run(self):
        """
        The main game loop that handles events, updates game objects,
        renders frames, and maintains the frame rate.
        """
        while self.running:
            dt = self.clock.tick() / 1000
            main_keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #emergency quit button
            if main_keys[pygame.K_ESCAPE]:
                self.game_over()

            #check for transitions between maps
            for transition in self.transition_sprites:
                if self.player.rect.colliderect(transition.rect):
                    if self.current_map == "Snow":
                        self.map_transition(FOREST_MAP_FILE)
                        self.current_map = "Forest"
                    else:
                        self.map_transition(SNOW_MAP_FILE)
                        self.current_map = "Snow"

            #checks for relic pick up
            for relic in self.relic_sprites:
                if self.player.rect.colliderect(relic.rect):
                    if (self.current_map == "Forest") and (self.forest_relic_collected == False):
                        self.forest_relic_collected = True
                        self.relics_collected += 1
                    if (self.current_map == "Snow") and (self.snow_relic_collected == False):
                        self.snow_relic_collected = True
                        self.relics_collected += 1
                if self.relics_collected == 2:
                    self.game_win()

            # Update all sprites
            self.all_sprites.update(dt)

            # Clears and redraws the screen
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)

            # updates i frames
            if self.invincible and ((pygame.time.get_ticks() - self.invincible_timer) >1000):
                self.invincible = False

            # HP UI
            text = "Life: " + str(self.game_health)
            life_banner = self.font.render(text, True, (255, 0, 0))
            self.display_surface.blit(life_banner, (20, 20))
            text2 = "Relics Collected: " + str(self.relics_collected)
            relic_banner = self.font.render(text2, True, (255, 255, 0))
            self.display_surface.blit(relic_banner, (20, 50))

            # screen update
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
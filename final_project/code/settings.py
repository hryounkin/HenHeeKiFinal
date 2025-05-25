import pygame
from os.path import join
from os import walk  # Used for traversing directories to load images

# ------------------------------------------------------------------
# Global game settings and file paths.
# ------------------------------------------------------------------

# Dimensions of the game window
WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 780

# Base tile size of the map (to be scaled by the game)
TILE_SIZE = 32

# Scale Factor
SCALE_FACTOR = 2

# Path to the TMX file containing the tile map configuration.
SNOWMAP_FILE = "../maps/TMX/MAP_SNOW.tmx"

# Directory path for the player's sprite images (specifically for the 'down' state).
PLAYER_IMAGE_FOLDER = '../images/player/down/'
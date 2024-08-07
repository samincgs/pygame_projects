import pygame
from random import randint, choice
from pytmx.util_pygame import load_pygame
from os.path import join
from os import walk

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
FRAMERATE = 60
BG_COLOR = '#fcdfcd'
import pygame
from os.path import join
from pytmx.util_pygame import load_pygame
from os import walk
from random import choice

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
FRAMERATE = 60
BG_COLOR = '#fcdfcd'
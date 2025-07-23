import pygame
import json

from constants import *

# loads an animation by loading a sequence of images from the given folder path
def load_animation(path, frame_count=8):
    frames = []

    # load each frame image based on frame_count
    for i in range(1, frame_count + 1):
        filename = "assets/" + path + "/" + str(i) + ".png"
        image = pygame.image.load(filename).convert_alpha()

        frames.append(image)
    
    return frames

# loads a single image with alpha transparency
def load_img(path):
    filename = "assets/" + path + ".png"
    image = pygame.image.load(filename).convert_alpha()

    return image

# loads and parses JSON file from assets folder
def load_json(path):
    with open("assets/" + path + ".json", 'r') as data:
        return json.load(data)

# calculates a bounding rectangle around a list of tile positions (each tile is a tuple/list)
def get_bounds(tiles):
    xs = [t[0] for t in tiles]
    ys = [t[1] for t in tiles]

    left = min(xs) * VIRTUAL_TILE
    top = min(ys) * VIRTUAL_TILE

    width = (max(xs) - min(xs) + 1) * VIRTUAL_TILE
    height = (max(ys) - min(ys) + 1) * VIRTUAL_TILE

    return pygame.Rect(left, top, width, height)
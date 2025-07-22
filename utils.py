import pygame
import json

from constants import *

def load_animation(path, frame_count=8):
    frames = []

    for i in range(1, frame_count + 1):
        filename = "assets/" + path + "/" + str(i) + ".png"
        image = pygame.image.load(filename).convert_alpha()

        frames.append(image)
    
    return frames

def load_img(path):
    filename = "assets/" + path + ".png"
    image = pygame.image.load(filename).convert_alpha()

    return image

def load_json(path):
    with open("assets/" + path + ".json", 'r') as data:
        return json.load(data)

def get_bounds(tiles):
    xs = [t[0] for t in tiles]
    ys = [t[1] for t in tiles]

    left = min(xs) * VIRTUAL_TILE
    top = min(ys) * VIRTUAL_TILE
    width = (max(xs) - min(xs) + 1) * VIRTUAL_TILE
    height = (max(ys) - min(ys) + 1) * VIRTUAL_TILE

    return pygame.Rect(left, top, width, height)
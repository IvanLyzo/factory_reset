import pygame

def load_animation(path, frame_count=8):
    frames = []

    for i in range(1, frame_count + 1):
        filename = "assets/" + path + "/" + str(i) + ".png"
        image = pygame.image.load(filename).convert_alpha()

        frames.append(image)
    
    return frames
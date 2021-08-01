from random import randint
import pygame

class Food():

    def __init__(self, screen_width : int, screen_height : int, grid_size : int) -> None:
        
        # Appereance
        self.color = (255,0,0) # Red

        # Position
        self.x = randint(1, grid_size - 2) * grid_size
        self.y = randint(1, grid_size - 2) * grid_size
        self.width = grid_size
        self.height = grid_size

        # Misc
        self.grid_size = grid_size


    def draw(self, screen) -> None:
        apple = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, apple)

    def eaten(self) -> None:
        self.x = randint(1, self.grid_size - 2) * self.grid_size
        self.y = randint(1, self.grid_size - 2) * self.grid_size
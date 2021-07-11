import pygame

class Button():

    def __init__(self, pos_x : int, pos_y : int, image_path : str) -> None:
        
        # Appearance
        self.image = pygame.image.load(image_path)

        # Position
        self.x = pos_x
        self.y = pos_y


    def draw(self, screen) -> None:
        screen.blit(self.image, (self.x, self.y))

    def click(self, pos) -> bool:
        square = self.image.get_rect()
        square = square.move(self.x, self.y)
        return square.collidepoint(pos) == 1
        
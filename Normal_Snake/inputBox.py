import pygame

class InputBox():

    def __init__(self, pos_x : int, pos_y : int, width : int, height : int, color) -> None:

        self.x = pos_x
        self.y = pos_y

        self.width = width
        self.height = height

        self.color = color

        self.text = ""
        self.font = pygame.font.SysFont(None, 30)


    def draw(self, screen) -> None:
        text_surface = self.font.render(f'Name: {self.text}', True, (255,255,255))
        screen.blit(text_surface, (self.x, self.y))

    def write(self, events):

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(self.text) >= 1:
                    return True, self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

        return False, self.text
        

    def click(self, pos) -> bool:
        square = pygame.Rect(self.x, self.y, self.width, self.height)
        # square = square.move(self.x, self.y)
        return square.collidepoint(pos) == 1

        


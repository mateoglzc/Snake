import pygame

class Snake():

    def __init__(self, width : int, height : int, grid_size : int) -> None:
        # Appearance
        self.height = grid_size - 2
        self.width = grid_size - 2
        self.color = (255,255,255) # White

        # Movement  
        self.x = width//2
        self.y = height//2
        self.x_speed = 1
        self.y_speed = 0
        self.length = 0
        self.positions = []
        self.direction = 'right'

        # Misc
        self.grid_size = grid_size
        self.screen_width = width
        self.screen_height = height

    def draw(self, screen) -> None:

        for i in self.positions[::-1]:
            square = pygame.Rect(i[0],i[1],self.width, self.height)
            pygame.draw.rect(screen, self.color, square)

    def move(self, screen_width, screen_height) -> bool:

        done = False

        if self.length + 1 == len(self.positions):
            for i in range(self.length):
                self.positions[i] = self.positions[i+1]
            self.positions[self.length] = (self.x, self.y)
        else:
            for i in range(self.length - 1):
                self.positions[i] = self.positions[i+1]
            self.positions.append((self.x, self.y))


        if self.x == screen_width or self.x == -self.grid_size:
            done = True
            self.reset();
        elif self.y == screen_height or self.y == -self.grid_size:
            done = True
            self.reset()

        if self.length > 3 and self.positions[-1] in self.positions[:-1]:
            done = True
            self.reset()
        
        self.x += self.x_speed * 20
        self.y += self.y_speed * 20

        return done

    def turn(self, action : list) -> None:

        # Clock wise directions
        d = ['up', 'right', 'down', 'left']
        idx = d.index(self.direction)

        if max(action) == action[1]:
            idx += 1
            if idx == len(d):
                idx = 0
            self.direction = d[idx]
        elif max(action) == action[2]:
            idx -= 1
            if idx < 0:
                idx = len(d) - 1
            self.direction = d[idx]

        directions = {'left' : (-1, 0), 'right' : (1, 0), 'up' : (0, -1), 'down' : (0,1)}
        self.x_speed = directions[self.direction][0]
        self.y_speed = directions[self.direction][1]

    def reset(self):
        self.positions = []
        self.x = self.screen_width//2
        self.y = self.screen_height//2
        self.length = 0
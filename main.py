from apple import Food
from snake import Snake
import pygame
import sys


def eat(snake : Snake,  food : Food) -> None:
    if (snake.x, snake.y) == (food.x, food.y):
        food.eaten()
        snake.length += 1;    

def main():

    pygame.init()

    # Clock
    clock = pygame.time.Clock()

    # Game Screen
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Snake")

    
    # Grid
    grid_size = 20
    grid_w = (width/grid_size)
    grid_h = (height/grid_size)

    def drawGrid(screen=screen):
        for y in range(int(grid_h)):
            for x in range(int(grid_w)):
                if (x + y) % 2 == 0:
                    square = pygame.Rect((x*grid_size, y*grid_size), (grid_size, grid_size))
                    pygame.draw.rect(screen, (0,0,0), square)
                else:
                    square = pygame.Rect((x*grid_size, y*grid_size), (grid_size, grid_size))
                    pygame.draw.rect(screen, (0,0,0), square)

    snake = Snake(width, height, grid_size)
    food = Food(width, height, grid_size)

    # Game Loop
    while True:

        # Check which keys are pressed
        keys = pygame.key.get_pressed()

        # Check for events 
        for event in pygame.event.get():

            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                
                # Quick exit
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Snake Movement
                if event.key == pygame.K_DOWN:
                    snake.turn('down')
                if event.key == pygame.K_UP:
                    snake.turn('up')
                if event.key == pygame.K_LEFT:
                    snake.turn('left')
                if event.key == pygame.K_RIGHT:
                    snake.turn('right')

        drawGrid()

        snake.draw(screen)
        food.draw(screen)

        snake.move(width, height)

        eat(snake, food)    

        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()
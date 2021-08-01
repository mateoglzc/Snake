from apple import Food
from snake import Snake
from button import Button
from inputBox import InputBox
import pygame
import pandas as pd
import sys

def saveRecord(name : str, score : int):
    records = pd.read_csv("./records.csv")
    new_score = [name,score]
    records.loc[len(records)] = new_score
    records.to_csv("./records.csv", index=False)

def getRecords():
    records = pd.read_csv("./records.csv")
    records = records.sort_values(by=["Score"], ascending=False)
    return records.to_dict(orient="list")


def drawGrid(screen, grid_w, grid_h, grid_size):
    for y in range(int(grid_h)):
        for x in range(int(grid_w)):
            if (x + y) % 2 == 0:
                square = pygame.Rect((x*grid_size, y*grid_size), (grid_size, grid_size))
                pygame.draw.rect(screen, (104,159,56), square)
            else:
                square = pygame.Rect((x*grid_size, y*grid_size), (grid_size, grid_size))
                pygame.draw.rect(screen, (124,179,66), square)

    for y in range(int(grid_h)):
        square = pygame.Rect((0, y*grid_size), (grid_size, grid_size))
        pygame.draw.rect(screen, (51,105,30), square)
        
    for y in range(int(grid_h)):
        square = pygame.Rect((380, y*grid_size), (grid_size, grid_size))
        pygame.draw.rect(screen, (51,105,30), square)

    for x in range(int(grid_w)):
        square = pygame.Rect((x*grid_size, 0), (grid_size, grid_size))
        pygame.draw.rect(screen, (51,105,30), square)

    for x in range(int(grid_w)):
        square = pygame.Rect((x*grid_size, 380), (grid_size, grid_size))
        pygame.draw.rect(screen, (51,105,30), square)

def snakeGame(screen, width, height, grid_h, grid_w, grid_size, font, score, snake, food) -> str:

    def eat(snake : Snake,  food : Food) -> bool:
        if (snake.x, snake.y) == (food.x, food.y):
            food.eaten()
            snake.length += 1;
            return True
        return False

    scene = "Snake"


    keys = pygame.key.get_pressed()

    # Snake Movement
    if keys[pygame.K_DOWN]:
        snake.turn('down')
    if keys[pygame.K_UP]:
        snake.turn('up')
    if keys[pygame.K_LEFT]:
        snake.turn('left')
    if keys[pygame.K_RIGHT]:
        snake.turn('right')

    # Draw Grid
    drawGrid(screen, grid_w, grid_h, grid_size)
            

    snake.draw(screen)
    food.draw(screen)

    done = snake.move(width, height)

    if eat(snake, food):
        score += 1
    
    if done:
        scene = "RegRecord"

    return scene, score

def startMenu(screen, start_button, exit_button) -> str:

    scene = "Start"

    # Title
    title = pygame.image.load("./Images/snake_title.png")
    
    # Draw Buttons
    start_button.draw(screen)
    exit_button.draw(screen)
    
    rigth_click, left_click, _ = pygame.mouse.get_pressed()

    if rigth_click and start_button.click(pygame.mouse.get_pos()):
        scene = 'Snake'
    elif rigth_click and exit_button.click(pygame.mouse.get_pos()):
        pygame.quit()
        sys.exit()
        
    screen.blit(title, (25, 50))

    return scene

def registerRecord(screen, input_box, events, title, font, sc) -> str:
        scene = "RegRecord"

        input_box.draw(screen)        
        ready, record_name = input_box.write(events)

        # Render records
        records = getRecords()
        names = records["Name"]
        scores = records["Score"]

        screen.blit(title, (50,50))

        x = 105
        y = 145

        for i in range(15):

            if i < len(names):
                name = font.render(f'{names[i]}', True, (255,255,255))
                score = font.render(f'{scores[i]}', True, (255,255,255))

                screen.blit(name, (x, y))
                screen.blit(score, (x+160, y))

                y += 20

        if ready:
            saveRecord(record_name, sc)
            scene = "Start"
            input_box.text = ''
            sc = 0

        return scene, sc

def main():

    pygame.init()

    # Clock
    clock = pygame.time.Clock()

    # Game Screen
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Snake")

    # Menu Buttons
    start_button = Button(80, 220, "./Images/start.png")
    exit_button = Button(220, 220, "./Images/exit.png")
    
    # Input text box
    record_input = InputBox(105, 110, 100, 50, (255, 134, 192))
    
    # Grid
    grid_size = 20
    grid_w = (width/grid_size)
    grid_h = (height/grid_size)
    
    snake = Snake(width, height, grid_size)
    food = Food(width, height, grid_size)
    
    # Score
    score = 0
    font = pygame.font.SysFont(None, 24)

    scene = "Start"

    # Record Title
    record_title = pygame.image.load("./Images/NewRecord.png")

    # Game Loop
    while True:

        # Draw Grid
        drawGrid(screen, grid_w, grid_h, grid_size)

        events = pygame.event.get()

        # Check which keys are pressed
        keys = pygame.key.get_pressed()

        # Check for events 
        for event in events:

            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:

                pygame.quit()
                sys.exit()


        if scene == "Start":

            scene = startMenu(screen, start_button, exit_button)

        elif scene == "Snake":

            scene, score = snakeGame(
                screen,
                width, height,
                grid_h, grid_w, grid_size,
                font,
                score,
                snake, food
                )

            score_text = font.render(f'Score: {score}', True, (255,255,255))
            screen.blit(score_text, (20,4))
        
        elif scene == "RegRecord":
            scene, score = registerRecord(
                screen, 
                record_input, 
                events,
                record_title,
                font,
                score
                )
    


        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()
from apple import Food
from snake import Snake
from agent import Agent
import pygame
import sys

def eat(snake : Snake,  food : Food) -> bool:
    if (snake.x, snake.y) == (food.x, food.y):
        food.eaten()
        snake.length += 1;
        return True
    return False    

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
    
    # Score
    score = 0
    record = 0
    font = pygame.font.SysFont(None, 24)

    # Reward
    reward = 0

    # Agent
    agent = Agent()

    itr = 0

    # Game Loop
    while True:

        score_text = font.render(f'Score: {score}', True, (255,255,255))

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
    
        # Play step

        # State of the game
        current_state = agent.get_state(snake, food)

        # Snake Movement
        action = agent.get_action(current_state)

        snake.turn(action)

        drawGrid()

        snake.draw(screen)
        food.draw(screen)

        done = snake.move(width, height)

        if eat(snake, food):
            score += 1
            reward += 20 # If our AI eats a piece of fruit then we give it a reward of +10

        screen.blit(score_text, (20,20))
        pygame.display.flip()
        clock.tick(40)

        new_state = agent.get_state(snake, food)

        # Train short memory
        agent.train_short_memory(current_state, action, reward, new_state, done)

        # Remember
        agent.remember(current_state, action, reward, new_state, done)

        if itr > 500:
            done = True

        itr += 1
        
        if done:
            # Train long memory
            # This is very important to our agent because it allows it to train on all of the past games and gain 'experience'

            reward -= 10

            # Reset Game
            agent.num_games += 1
            agent.train_long_memory()
            snake.reset()

            if score > record:
                record = score

                agent.model.saveModel()

            print(f'Game: {agent.num_games} Score: {score} Record: {record}, Reward: {reward}')

            score = 0
            reward = 0
            itr = 0



if __name__ == "__main__":
    main()
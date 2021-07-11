# Agent for the "Deep Q" model

import torch
import random
import numpy as np
from collections import deque

from model import SnakeLinearQ, SnakeTrainer

# Constant Parameters 
MAX_MEMORY = 100000
BATCH_SIZE = 1000
LEARN_RATE = 0.001

class Agent():

    def __init__(self) -> None:
        self.num_games = 0 
        self.epsilon = 0 # Control the randomness
        self.gamma = 0.9 # Discount rate

        # If we exceed this memory it will remove elements from the left of the array by calling the function 'popleft()'
        self.memory = deque(maxlen=MAX_MEMORY)

        # - Model
        self.model = SnakeLinearQ(8, 256, 3)
        # - Training algorithm
        self.trainer = SnakeTrainer(self.model, self.gamma, self.epsilon, LEARN_RATE)

    def get_state(self, snake, fruit) -> np.array:

        # Position of the snake's head
        snake_pos = (snake.x, snake.y)
        snake_dir = (snake.x_speed, snake.y_speed)

        # Food position
        food_pos = (fruit.x, fruit.y)

        # Directions
        directions = {(-1, 0) : 'left', (1, 0) : 'right', (0, -1) : 'up', (0, 1) : 'down'}
   

        # Danger
        danger_straight = False
        danger_right = False
        danger_left = False

        if directions[snake_dir] == 'left':
            
            if snake_pos[0] >= 340:
                danger_straight = True
            if snake_pos[1] >= 340:
                danger_right = True
            elif snake_pos[1] <= 40:
                danger_right = True

        elif directions[snake_dir] == 'right':

            if snake_pos[0] <= 40:
                danger_straight = True
            if snake_pos[1] >= 340:
                danger_right = True
            elif snake_pos[1] <= 40:
                danger_right = True

        elif directions[snake_dir] == 'up':
            
            if snake_pos[1] <= 40:
                danger_straight = True
            if snake_pos[0] >= 340:
                danger_right = True
            elif snake_pos[0] <= 40:
                danger_left = True

        elif directions[snake_dir] == 'down':
            
            if snake_pos[1] >= 340:
                danger_straight = True
            if snake_pos[0] >= 340:
                danger_right = True
            elif snake_pos[0] <= 40:
                danger_left = True

        state = [

            # Danger
            # danger_straight, danger_right, danger_left,
            
            # Direction
            directions[snake_dir] == 'left',
            directions[snake_dir] == 'right',
            directions[snake_dir] == 'up',
            directions[snake_dir] == 'down',

            # Food location
            food_pos[0] < snake_pos[0],
            food_pos[0] > snake_pos[0],
            food_pos[1] < snake_pos[1],
            food_pos[1] > snake_pos[1]
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done) -> None:
        
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        
        if len(self.memory) > BATCH_SIZE:
            sample = random.sample(self.memory, BATCH_SIZE)
        else:
            sample = self.memory

        states, actions, rewards, next_states, dones = zip(*sample)
        self.trainer.trainStep(states, actions, rewards, next_states, dones)


    def train_short_memory(self, state, action, reward, next_state, done) -> None:

        self.trainer.trainStep(state, action, reward, next_state, done)

    def get_action(self, state) -> list:

        # Random moves (Tradeoff between exploration and explotation)
        self.epsilon = 80 - self.num_games
        final_move = [0,0,0]

        if random.randint(0,200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float32)
            # Forward pass
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = move
        return final_move
